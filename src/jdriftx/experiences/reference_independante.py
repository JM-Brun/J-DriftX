"""Comparaison à référence indépendante : résolution EDP du cas S0 (étape 5).

Cette étape reconstruit une route de calcul indépendante de la solution de
similitude : une équation aux dérivées partielles de diffusion 2D (transverse
et verticale) marchée en longitude sous l'hypothèse de vent uniforme, et
compare ses résultats ponctuels à la solution fermée du package sur le cas S0
figé (docs/48 §2.2). La méthodologie suit la note 35 (cost model étape par
étape : les coûts des deux routes sont mesurés séparément ; le facteur
historique 10³-10⁴ de l'ouvrage de 2008 n'est ni reconstruit ni revendiqué).

Étiquetage explicite, conformément à l'ordre confirmé de l'issue #232 :

- Héritage documentaire : la comparaison à référence indépendante est
  « annoncée seulement » dans le chapitre « Reduced-Order Modelling of
  Dispersion » (Brun & Mohammadi, 2008, DOI 10.1007/978-1-4020-8758-5_14) ;
  aucun chiffre de l'ouvrage n'est utilisé comme cible.
- Reconstruction : schéma explicite FTCS (forward en longitude, centré en
  transverse et vertical) marchant en x sur l'équation de diffusion
  K = (U/2)·d(sigma²)/dx, avec nombre de Fourier borné à 1/3, condition au sol de
  type miroir (Neumann), Dirichlet aux bords de fenêtre, entrée partagée
  (solution fermée du package à x d'entrée) et tranches prélevées aux arcs.
- Extension : aucune.

Garde-fous : la comparaison est un contrôle de cohérence entre deux routes de
calcul du même package sur un cas synthétique ; ce n'est pas une validation
physique. Les ``dict`` restent confinés à la frontière d'export JSON
(``model_dump`` de Pydantic), conformément à la charte du projet.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from importlib import metadata

import numpy as np
from pydantic import BaseModel, ConfigDict

from jdriftx.benchmarks.cas import CasS0
from jdriftx.benchmarks.metriques import fac2, nmse
from jdriftx.contrats import PanacheGaussien
from jdriftx.similitude import sigma_y, sigma_z
from jdriftx.stabilite import ClasseStabilite, FormeSigmaZ

__all__ = [
    "PARAMETRES_EDP_DEFAUT",
    "SEUIL_FOURIER",
    "ComparaisonReference",
    "ManifesteReference",
    "ParametresEdp",
    "PointComparaison",
    "SolutionEdp",
    "TrancheEdp",
    "comparer_reference",
    "construire_manifeste",
    "derivee_sigma_carre",
    "resoudre_edp",
]

SEUIL_FOURIER: float = 1.0 / 3.0
"""Nombre de Fourier maximal (somme des directions transverse et verticale).

Le schéma explicite marché en x est stable si la somme des contributions
de diffusion des deux directions reste sous 1/3 (démonstration classique
du schéma FTCS, à pondération égale entre directions) ; le pas
longitudinal est réduit en puissances de deux jusqu'à satisfaire ce seuil
au dernier arc, là où la diffusion cumulée est maximale.
"""


@dataclass(frozen=True)
class ParametresEdp:
    """Paramètres numériques de la grille EDP, validés à la construction.

    Attributs :
        pas_transverse_y : espacement des nœuds latéraux (m), positif.
        pas_transverse_z : espacement des nœuds verticaux (m), positif.
        demi_largeur_y : demi-largeur de la fenêtre latérale (m), positive,
            multiple entier du pas transverse (la fenêtre est symétrique).
        hauteur_max : sommet de la colonne verticale (m), positif, multiple
            entier du pas vertical.
    """

    pas_transverse_y: float
    pas_transverse_z: float
    demi_largeur_y: float
    hauteur_max: float

    def __post_init__(self) -> None:
        """Valide positivité, largeur et multiplicité des pas, sinon ValueError."""
        if self.pas_transverse_y <= 0.0:
            msg = "Le pas transverse doit être strictement positif."
            raise ValueError(msg)
        if self.pas_transverse_z <= 0.0:
            msg = "Le pas vertical doit être strictement positif."
            raise ValueError(msg)
        if self.demi_largeur_y <= 0.0:
            msg = "La demi-largeur doit être strictement positive."
            raise ValueError(msg)
        if self.hauteur_max <= 0.0:
            msg = "La hauteur maximale doit être strictement positive."
            raise ValueError(msg)
        rapport_y = 2.0 * self.demi_largeur_y / self.pas_transverse_y
        if abs(rapport_y - round(rapport_y)) > 1e-9:
            msg = "La fenêtre doit être un multiple entier du pas transverse."
            raise ValueError(msg)
        rapport_z = self.hauteur_max / self.pas_transverse_z
        if abs(rapport_z - round(rapport_z)) > 1e-9:
            msg = "La hauteur doit être un multiple entier du pas vertical."
            raise ValueError(msg)


PARAMETRES_EDP_DEFAUT: ParametresEdp = ParametresEdp(
    pas_transverse_y=2.5,
    pas_transverse_z=2.0,
    demi_largeur_y=340.0,
    hauteur_max=240.0,
)
"""Paramètres calibrés de la grille fine : fenêtre couvrant quatre écarts-types
au dernier arc (800 m) pour la classe C, pas transverse 2,5 m, pas vertical
2,0 m, pas longitudinal 100/1024 m (nombre de Fourier 0,225 au dernier arc)."""


def derivee_sigma_carre(x: float, coefficient: float, d: float) -> float:
    """Dérivée exacte de sigma² = (coefficient·x)²/(1 + d·x) en x (m), positive.

    Formes couvertes : LINEAIRE (d = 0) et RACINE (d > 0) des lois de Briggs
    rurales (jdriftx.stabilite) ; la forme INVERSE (sigma = b·x/(1 + d·x)) n'est
    pas celle évaluée ici et est rejetée en amont.

    Lever une ValueError si x n'est pas strictement positif.
    """
    if x <= 0.0:
        msg = "La distance sous le vent doit être strictement positive."
        raise ValueError(msg)
    variance = (coefficient * x) ** 2 / (1.0 + d * x)
    return float(variance * (2.0 / x - d / (1.0 + d * x)))


@dataclass(frozen=True)
class TrancheEdp:
    """Tranche du champ EDP prélevée à un arc de mesure.

    Attributs :
        x : distance sous le vent de la tranche (m).
        champ : concentrations (kg m^-3) sur la grille transverse/verticale.
    """

    x: float
    champ: np.ndarray


@dataclass(frozen=True)
class SolutionEdp:
    """Solution EDP marchée en longitude, du premier au dernier arc.

    Attributs :
        x_entree : distance sous le vent de la condition d'entrée (m).
        pas_longitudinal : pas de marche en x (m), multiple inverse d'une
            puissance de deux de l'espacement des arcs.
        abscisses_y : nœuds latéraux (m), symétriques autour de zéro.
        abscisses_z : nœuds verticaux (m), du sol au sommet de fenêtre.
        tranches : champ prélevé à l'entrée puis à chaque arc (m).
    """

    x_entree: float
    pas_longitudinal: float
    abscisses_y: np.ndarray
    abscisses_z: np.ndarray
    tranches: tuple[TrancheEdp, ...]


def _coefficients_diffusion(classe: str, x: float) -> tuple[float, float, float, float]:
    """Coefficients (a_y, d_y, b_z, d_z) de la classe, forme INVERSE rejetée.

    La dérivée de sigma² est porteuse de la diffusion effective : seules les
    formes LINEAIRE et RACINE des lois de Briggs (jdriftx.stabilite) sont
    couvertes ; la forme INVERSE (classes E et F) est explicitement hors
    périmètre et lève une ValueError pour rester sans ambiguïté.
    """
    stable = ClasseStabilite(classe)
    a_y, d_y = stable.coeff_sigma_y
    forme, b_z, d_z = stable.coeff_sigma_z
    if forme is FormeSigmaZ.INVERSE:
        msg = (
            "La forme INVERSE de sigma_z (classes E et F) est hors périmètre "
            "de la résolution EDP marchée."
        )
        raise ValueError(msg)
    return a_y, d_y, b_z, d_z


def _pas_longitudinal(
    classe: str, x_debut: float, x_fin: float, parametres: ParametresEdp
) -> float:
    """Plus grand pas en base/2^k stable au dernier arc (nombre de Fourier).

    Le nombre de Fourier est évalué au dernier arc, là où sigma² croît le plus ;
    le pas de base est la distance d'entrée (100 m pour le cas S0 figé) et
    il est divisé par deux jusqu'à ce que la somme des contributions
    transverse et verticale passe sous SEUIL_FOURIER.
    """
    a_y, d_y, b_z, d_z = _coefficients_diffusion(classe, x_fin)
    dy = parametres.pas_transverse_y
    dz = parametres.pas_transverse_z
    for exposant in range(0, 41):
        candidat = x_debut / 2.0**exposant
        fourier = (
            0.5 * derivee_sigma_carre(x_fin, a_y, d_y) * candidat / dy**2
            + 0.5 * derivee_sigma_carre(x_fin, b_z, d_z) * candidat / dz**2
        )
        if fourier <= SEUIL_FOURIER:
            return float(candidat)
    msg = "Aucun pas longitudinal stable trouvé (exposant > 40)."
    raise ValueError(msg)


def resoudre_edp(cas: CasS0, parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT) -> SolutionEdp:
    """Résout l'EDP de diffusion marchée en x, du premier au dernier arc.

    Méthodologie (note 35, étape 5 de l'issue #232) : schéma explicite FTCS
    marché en longitude sur K = (U/2)·d(sigma²)/dx (U disparaît du champ), entrée
    partagée à x du premier arc (solution fermée du package sur la grille),
    condition au sol de type miroir (Neumann : ∂C/∂z = 0 au sol), Dirichlet
    nul aux bords latéraux et au sommet de fenêtre, tranches prélevées aux
    arcs de mesure.
    """
    classe = cas.source.classe
    x_entree = float(cas.arcs[0])
    x_fin = float(cas.arcs[-1])
    a_y, d_y, b_z, d_z = _coefficients_diffusion(classe, x_fin)

    demi_largeur = parametres.demi_largeur_y
    if demi_largeur < 4.0 * float(sigma_y(x_fin, classe)):
        msg = (
            "La fenêtre latérale doit couvrir quatre écarts-types au dernier "
            "arc (troncature documentée)."
        )
        raise ValueError(msg)
    if parametres.hauteur_max < cas.source.hauteur + 4.0 * float(sigma_z(x_fin, classe)):
        msg = (
            "La colonne verticale doit couvrir la hauteur source plus quatre "
            "écarts-types verticaux au dernier arc."
        )
        raise ValueError(msg)

    dx = _pas_longitudinal(classe, x_entree, x_fin, parametres)
    for precedent, arc in zip((x_entree, *cas.arcs[1:]), cas.arcs[1:], strict=True):
        if abs((arc - precedent) / dx - round((arc - precedent) / dx)) > 1e-9:
            msg = "Les arcs doivent être des multiples entiers du pas longitudinal depuis l'entrée."
            raise ValueError(msg)

    pas_y = parametres.pas_transverse_y
    pas_z = parametres.pas_transverse_z
    abscisses_y = np.arange(-demi_largeur, demi_largeur + 0.5 * pas_y, pas_y)
    abscisses_z = np.arange(0.0, parametres.hauteur_max + 0.5 * pas_z, pas_z)

    mailles_y, mailles_z = np.meshgrid(abscisses_y, abscisses_z, indexing="ij")
    panache = PanacheGaussien(source=cas.source)
    champ = np.asarray(panache.concentration(x_entree, mailles_y, mailles_z), dtype=float)
    champ[0, :] = 0.0
    champ[-1, :] = 0.0
    champ[:, -1] = 0.0

    cibles = {round((arc - x_entree) / dx): float(arc) for arc in cas.arcs[1:]}
    tranches: list[TrancheEdp] = [TrancheEdp(x=x_entree, champ=champ.copy())]
    total = round((x_fin - x_entree) / dx)
    suivant = np.empty_like(champ)

    x = x_entree
    for pas in range(1, total + 1):
        x_milieu = x + 0.5 * dx
        c_y = 0.5 * derivee_sigma_carre(x_milieu, a_y, d_y) * dx / pas_y**2
        c_z = 0.5 * derivee_sigma_carre(x_milieu, b_z, d_z) * dx / pas_z**2
        interieur = champ[1:-1, 1:-1]
        suivant[1:-1, 1:-1] = (
            interieur
            + c_y * (champ[2:, 1:-1] - 2.0 * interieur + champ[:-2, 1:-1])
            + c_z * (champ[1:-1, 2:] - 2.0 * interieur + champ[1:-1, :-2])
        )
        sol = champ[1:-1, 0]
        suivant[1:-1, 0] = (
            sol
            + c_y * (champ[2:, 0] - 2.0 * sol + champ[:-2, 0])
            + c_z * 2.0 * (champ[1:-1, 1] - sol)
        )
        suivant[0, :] = 0.0
        suivant[-1, :] = 0.0
        suivant[:, -1] = 0.0
        champ, suivant = suivant, champ
        x += dx
        arc = cibles.get(pas)
        if arc is not None:
            tranches.append(TrancheEdp(x=arc, champ=champ.copy()))

    return SolutionEdp(
        x_entree=x_entree,
        pas_longitudinal=dx,
        abscisses_y=abscisses_y,
        abscisses_z=abscisses_z,
        tranches=tuple(tranches),
    )


def _interp_bilineaire(
    tranche: TrancheEdp, abscisses_y: np.ndarray, abscisses_z: np.ndarray, y: float, z: float
) -> float:
    """Interpole bilinéairement la concentration au point (y, z) (m).

    Lève une ValueError si le point sort de la fenêtre couverte par la
    grille : les points de comparaison doivent rester dans le domaine.
    """
    pas_y = float(abscisses_y[1] - abscisses_y[0])
    pas_z = float(abscisses_z[1] - abscisses_z[0])
    f_y = (y - float(abscisses_y[0])) / pas_y
    f_z = (z - float(abscisses_z[0])) / pas_z
    if f_y < 0.0 or f_y > abscisses_y.size - 1 or f_z < 0.0 or f_z > abscisses_z.size - 1:
        msg = "Le point de comparaison sort de la fenêtre de la grille EDP."
        raise ValueError(msg)
    i_y = min(int(f_y), abscisses_y.size - 2)
    i_z = min(int(f_z), abscisses_z.size - 2)
    t_y = f_y - i_y
    t_z = f_z - i_z
    c00 = float(tranche.champ[i_y, i_z])
    c10 = float(tranche.champ[i_y + 1, i_z])
    c01 = float(tranche.champ[i_y, i_z + 1])
    c11 = float(tranche.champ[i_y + 1, i_z + 1])
    return float(
        c00 * (1.0 - t_y) * (1.0 - t_z)
        + c10 * t_y * (1.0 - t_z)
        + c01 * (1.0 - t_y) * t_z
        + c11 * t_y * t_z
    )


def _flux_tranche(
    tranche: TrancheEdp, abscisses_y: np.ndarray, abscisses_z: np.ndarray, u: float
) -> float:
    """Flux massique transverse (kg/s) d'une tranche : U·∫∫ C dy dz."""
    integrale = np.trapezoid(np.trapezoid(tranche.champ, x=abscisses_z, axis=1), x=abscisses_y)
    return float(u * integrale)


class PointComparaison(BaseModel):
    """Comparaison ponctuelle fermée/EDP en un point de mesure."""

    model_config = ConfigDict(frozen=True)

    x: float
    y: float
    z: float
    fermee: float
    edp: float
    ratio: float


class ComparaisonReference(BaseModel):
    """Comparaison complète de la route EDP à la solution fermée.

    Attributs :
        cas_source : identification du cas comparé (débit, vent, classe).
        parametres : paramètres numériques de la grille EDP.
        points : comparaisons ponctuelles, une par point de mesure.
        fac2 : fraction des points dans un facteur 2 (métrique partagée).
        nmse : erreur quadratique normalisée (métrique partagée).
        ecart_relatif_max : écart relatif maximal fermée/EDP (sans unité).
        ecart_flux_max : écart relatif maximal de flux aux arcs (sans unité).
        cout_ferme_s : coût de la route fermée, mesuré (s).
        cout_edp_s : coût de la route EDP, mesuré séparément (s).
    """

    model_config = ConfigDict(frozen=True)

    cas_source: str
    parametres: ParametresEdp
    points: tuple[PointComparaison, ...]
    fac2: float
    nmse: float
    ecart_relatif_max: float
    ecart_flux_max: float
    cout_ferme_s: float
    cout_edp_s: float

    def vers_dict(self) -> dict[str, object]:
        """Exporte la comparaison en dictionnaire JSON-natif (frontière)."""
        return self.model_dump(mode="json")


class ManifesteReference(BaseModel):
    """Manifeste de la comparaison à référence indépendante (étape 5)."""

    model_config = ConfigDict(frozen=True)

    identifiant: str
    niveau_fidelite: str
    source: str
    heritage_documentaire: str
    reconstruction: str
    extension: str
    limites: tuple[str, ...]
    cas: CasS0
    comparaison: ComparaisonReference
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire JSON-natif (frontière)."""
        return self.model_dump(mode="json")


def comparer_reference(
    cas: CasS0, parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT
) -> ComparaisonReference:
    """Compare la route EDP à la solution fermée sur la grille du cas.

    Les deux routes partagent la paramétrisation (Briggs via
    jdriftx.stabilite) et l'entrée : la route fermée évalue
    ``cas.verite(points)``, la route EDP part de la même solution fermée à
    l'arc d'entrée puis diffuse. Les métriques FAC2 et NMSE sont celles du
    registre partagé (jdriftx.benchmarks.metriques, issue #43) ; les coûts
    des deux routes sont mesurés séparément (note 35), sans facteur
    historique.
    """
    points = cas.points()
    debut_ferme = time.perf_counter()
    verite = np.asarray(cas.verite(points), dtype=float)
    cout_ferme = time.perf_counter() - debut_ferme

    debut_edp = time.perf_counter()
    solution = resoudre_edp(cas, parametres)
    tranches = {tranche.x: tranche for tranche in solution.tranches}
    edp = [
        _interp_bilineaire(
            tranches[point.x], solution.abscisses_y, solution.abscisses_z, point.y, point.z
        )
        for point in points
    ]
    flux_entree = _flux_tranche(
        solution.tranches[0], solution.abscisses_y, solution.abscisses_z, cas.source.u
    )
    ecarts_flux: list[float] = []
    for tranche in solution.tranches[1:]:
        flux = _flux_tranche(tranche, solution.abscisses_y, solution.abscisses_z, cas.source.u)
        ecarts_flux.append(abs(flux - flux_entree) / flux_entree)
    cout_edp = time.perf_counter() - debut_edp

    fermee = [float(v) for v in verite]
    comparaisons = tuple(
        PointComparaison(
            x=float(point.x),
            y=float(point.y),
            z=float(point.z),
            fermee=float(v),
            edp=float(e),
            ratio=float(e / v),
        )
        for point, v, e in zip(points, fermee, edp, strict=True)
    )
    ecarts_relatifs = [abs(point.edp - point.fermee) / point.fermee for point in comparaisons]
    return ComparaisonReference(
        cas_source=(
            f"debit={cas.source.debit} kg/s, u={cas.source.u} m/s, "
            f"classe={cas.source.classe}, hauteur={cas.source.hauteur} m"
        ),
        parametres=parametres,
        points=comparaisons,
        fac2=fac2(fermee, edp),
        nmse=nmse(fermee, edp),
        ecart_relatif_max=float(max(ecarts_relatifs)),
        ecart_flux_max=float(max(ecarts_flux)),
        cout_ferme_s=float(cout_ferme),
        cout_edp_s=float(cout_edp),
    )


def construire_manifeste(cas: CasS0, comparaison: ComparaisonReference) -> ManifesteReference:
    """Construit le manifeste étiqueté de la comparaison (statuts figés).

    Le manifeste porte l'étiquetage héritage/reconstruction/extension et
    les limites explicites ; la version du code est lue dans les
    métadonnées d'installation si disponible, « non-installe » sinon.
    """
    try:
        version = metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        version = "non-installe"
    return ManifesteReference(
        identifiant="jdriftx-reference-independante-001",
        niveau_fidelite="R1",
        source="Chapitre « Reduced-Order Modelling of Dispersion » (Brun & "
        "Mohammadi, 2008), DOI 10.1007/978-1-4020-8758-5_14",
        heritage_documentaire=(
            "Comparaison à référence indépendante « annoncée seulement » dans "
            "le chapitre de 2008 (figure 3) : aucun chiffre de l'ouvrage n'est "
            "utilisé comme cible."
        ),
        reconstruction=(
            "Schéma explicite FTCS marché en longitude (nombre de Fourier "
            "≤ 1/3, miroir au sol, Dirichlet aux bords, fenêtre 4 sigma, tranches "
            "aux arcs, entrée partagée avec la solution fermée)."
        ),
        extension="Aucune (l'évaluation du puff et le multi-niveaux restent hors périmètre).",
        limites=(
            "Contrôle d'auto-cohérence entre deux routes du même package sur "
            "un cas synthétique : pas une validation physique.",
            "Le facteur historique 10³-10⁴ n'est pas revendiqué : les coûts "
            "sont mesurés séparément, sans facteur.",
            "Fenêtre tronquée à quatre écarts-types et grille calibrée pour "
            "la classe C du cas S0 figé (docs/48 §2.2).",
        ),
        cas=cas,
        comparaison=comparaison,
        version_code=version,
        commande=(
            "uv run python -c 'from jdriftx.benchmarks.cas import CAS_S0_DEFAUT; "
            "from jdriftx.experiences.reference_independante import comparer_reference; "
            "print(comparer_reference(CAS_S0_DEFAUT))'"
        ),
    )
