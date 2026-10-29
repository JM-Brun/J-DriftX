"""EDP transitoire du puff : marche en temps de la marginale transverse.

Cette étape reconstruit une seconde route de calcul pour la source
impulsionnelle de l'étape 6 : la marginale transverse Q(y, z, t) du puff
(intégrale longitudinale de la concentration) vérifie ∂Q/∂t =
Ky(t)·∂²Q/∂y² + Kz(t)·∂²Q/∂z², avec K = (u/2)·d(sigma²)/dx évalué à la
distance parcourue d = u·t (Briggs via le modèle injecté). La condition
d'entrée est la marginale fermée du package posée au premier instant de
passage ; la marche est explicite en temps (FTCS), le sol est de type
miroir (Neumann : ∂Q/∂z = 0 au sol, exact ici car le noyau du puff est
pair en z), les bords latéraux et le sommet de fenêtre sont de Dirichlet
nul. La structure longitudinale reste analytique (carte travel-time de la
note 37, isotropie sigma_x = sigma_y du noyau fermé) : C(x, y, z, t) est
la marginale échantillonnée multipliée par le facteur gaussien
longitudinal évalué à d = u·t.

Étiquetage explicite, conformément à l'ordre confirmé de l'issue #232 :

- Héritage documentaire : aucune source historique ; cette étape est la
  suite directe de l'évaluation dirigée du puff (note 53) et n'utilise
  aucun chiffre de l'ouvrage de 2008 comme cible.
- Reconstruction : marche explicite FTCS en temps (nombre de Fourier
  borné à 1/3 au dernier passage), entrée fermée au premier instant de
  passage, miroir au sol, Dirichlet aux bords de fenêtre, structure
  longitudinale analytique.
- Extension : seconde extension conditionnelle du contrat minimal
  (docs/47 §5) : la source impulsionnelle de la note 53 reçoit sa route
  EDP transitoire, sur la grille du cas S0 figé (docs/48 §2.2).

Garde-fous : la comparaison est un contrôle d'auto-cohérence entre deux
routes du même package sur un cas synthétique ; ce n'est pas une
validation physique. Le noyau du puff est symétrique en z autour du sol
(sans hauteur de source) : la moitié de la masse du noyau fermé est
formellement sous le sol, la grille porte la demi-colonne miroir, et les
écarts de masse sont comparés à la marginale analytique sur la même
grille, pas à la masse totale. Les ``dict`` restent confinés à la
frontière d'export JSON (``model_dump`` de Pydantic), conformément à la
charte du projet.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from importlib import metadata

import numpy as np
from pydantic import BaseModel, ConfigDict

from jdriftx.benchmarks.cas import PointMesure
from jdriftx.benchmarks.metriques import fac2, nmse
from jdriftx.experiences.evaluation_puff import SourceImpulsionnelle
from jdriftx.experiences.reference_independante import (
    DIFFUSION_BRIGGS,
    PARAMETRES_EDP_DEFAUT,
    SEUIL_FOURIER,
    CoefficientsDiffusion,
    GrilleEdp,
    ModeleDiffusion,
    ParametresEdp,
)
from jdriftx.similitude import concentration_puff, sigma_y, sigma_z

__all__ = [
    "ComparaisonTransitoire",
    "InstantPuff",
    "ManifesteTransitoire",
    "MesureTransitoire",
    "PointComparaisonPuff",
    "RouteEdpPuff",
    "RouteFermeePuff",
    "SolutionTransitoire",
    "SolveurTransitoire",
    "comparer_transitoire",
    "construire_manifeste",
    "resoudre_transitoire",
]


@dataclass(frozen=True)
class InstantPuff:
    """Instantané de la marginale transverse à un instant de passage.

    Attributs :
        t : instant de l'instantané (s), strictement positif.
        champ : marginale transverse Q (kg m⁻²) sur la grille.
    """

    t: float
    champ: np.ndarray


@dataclass(frozen=True)
class SolutionTransitoire:
    """Solution de l'EDP transitoire, de l'entrée au dernier passage.

    Attributs :
        t_entree : instant de la condition d'entrée (s).
        pas_temps : pas de temps de la marche (s), fraction inverse d'une
            puissance de deux de l'espacement des passages.
        abscisses_y : nœuds latéraux (m), symétriques autour de zéro.
        abscisses_z : nœuds verticaux (m), du sol au sommet de fenêtre.
        instants : instantanés prélevés à l'entrée puis à chaque passage.
    """

    t_entree: float
    pas_temps: float
    abscisses_y: np.ndarray
    abscisses_z: np.ndarray
    instants: tuple[InstantPuff, ...]


def _verifier_points_aux_arcs(arcs: tuple[float, ...], points: tuple[PointMesure, ...]) -> None:
    """Exige des points situés aux arcs de passage, sinon ValueError."""
    for point in points:
        if point.x not in arcs:
            msg = "Le point doit se trouver à un arc de passage."
            raise ValueError(msg)


def _marginale_analytique(
    source: SourceImpulsionnelle,
    grille: GrilleEdp,
    t: float,
) -> np.ndarray:
    """Marginale transverse fermée du puff sur la grille, à l'instant t (s)."""
    distance = source.u * t
    sy = sigma_y(distance, source.classe)
    sz = sigma_z(distance, source.classe)
    mailles_y, mailles_z = grille.mailles()
    champ = (
        source.masse / (2.0 * np.pi * sy * sz)
        * np.exp(-(mailles_y**2) / (2.0 * sy**2))
        * np.exp(-(mailles_z**2) / (2.0 * sz**2))
    )
    return np.asarray(champ, dtype=float)


def _masse(champ: np.ndarray, grille: GrilleEdp) -> float:
    """Masse de la marginale sur la grille (trapèzes doubles)."""
    integrale = np.trapezoid(
        np.trapezoid(champ, x=grille.abscisses_z, axis=1),
        x=grille.abscisses_y,
    )
    return float(integrale)


def _bilineaire(champ: np.ndarray, grille: GrilleEdp, y: float, z: float) -> float:
    """Interpole bilinéairement la marginale au point (y, z) (m)."""
    abscisses_y = grille.abscisses_y
    abscisses_z = grille.abscisses_z
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
    c00 = float(champ[i_y, i_z])
    c10 = float(champ[i_y + 1, i_z])
    c01 = float(champ[i_y, i_z + 1])
    c11 = float(champ[i_y + 1, i_z + 1])
    return float(
        c00 * (1.0 - t_y) * (1.0 - t_z)
        + c10 * t_y * (1.0 - t_z)
        + c01 * (1.0 - t_y) * t_z
        + c11 * t_y * t_z
    )


class SolveurTransitoire:
    """Schéma explicite FTCS marché en temps, instantanés aux passages.

    Le solveur porte les seules considérations numériques : pas de temps
    stable (SEUIL_FOURIER au dernier passage), condition au sol de type
    miroir (Neumann), Dirichlet nul aux bords latéraux et au sommet de
    fenêtre, instantanés prélevés aux instants de passage. La physique de
    diffusion vient du modèle injecté (ModeleDiffusion), la géométrie de
    la grille (GrilleEdp) ; il étend le solveur en longitude de l'étape 5
    (reference_independante) au cas transitoire du puff.

    Attributs :
        source : source impulsionnelle évaluée (masse, vent, classe, x0).
        arcs : distances sous le vent des arcs de passage (m).
        parametres : paramètres numériques de la grille transverse/verticale.
        modele : modèle de diffusion (Briggs par défaut).
    """

    def __init__(
        self,
        source: SourceImpulsionnelle,
        arcs: tuple[float, ...],
        parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
        modele: ModeleDiffusion = DIFFUSION_BRIGGS,
    ) -> None:
        """Injecte les quatre considérations : source, arcs, géométrie, physique."""
        self.source = source
        self.arcs = arcs
        self.parametres = parametres
        self.modele = modele

    def resoudre(self) -> SolutionTransitoire:
        """Résout de l'entrée au dernier passage : modèle, fenêtre, pas, arcs.

        L'ordre de validation est celui de l'étape 5 : coefficients (forme
        INVERSE rejetée), couverture de fenêtre, pas de temps stable,
        divisibilité des passages depuis l'entrée, puis marche FTCS.
        """
        u = self.source.u
        t_entree = float(self.arcs[0]) / u
        x_fin = float(self.arcs[-1])
        coefficients = self.modele.coefficients(self.source.classe, x_fin)
        self._verifier_fenetre(x_fin)
        grille = GrilleEdp.depuis_parametres(self.parametres)
        pas_temps = self._pas_temps_stable(coefficients, u, t_entree, x_fin)
        self._verifier_passages(pas_temps, t_entree)
        return self._marcher(grille, coefficients, t_entree, pas_temps)

    def _verifier_fenetre(self, x_fin: float) -> None:
        """Exige la couverture de quatre écarts-types au dernier passage."""
        classe = self.source.classe
        if self.parametres.demi_largeur_y < 4.0 * float(sigma_y(x_fin, classe)):
            msg = (
                "La fenêtre latérale doit couvrir quatre écarts-types du puff "
                "au dernier instant de passage."
            )
            raise ValueError(msg)
        if self.parametres.hauteur_max < 4.0 * float(sigma_z(x_fin, classe)):
            msg = (
                "La colonne verticale doit couvrir quatre écarts-types "
                "verticaux du puff au dernier instant de passage."
            )
            raise ValueError(msg)

    def _pas_temps_stable(
        self,
        coefficients: CoefficientsDiffusion,
        u: float,
        t_entree: float,
        x_fin: float,
    ) -> float:
        """Plus grand pas en t_entree/2^k stable au dernier passage (Fourier)."""
        dy = self.parametres.pas_transverse_y
        dz = self.parametres.pas_transverse_z
        for exposant in range(0, 41):
            candidat = t_entree / 2.0**exposant
            fourier = (
                0.5 * u * coefficients.derivee_sigma_y_carre(x_fin) * candidat / dy**2
                + 0.5 * u * coefficients.derivee_sigma_z_carre(x_fin) * candidat / dz**2
            )
            if fourier <= SEUIL_FOURIER:
                return float(candidat)
        msg = "Aucun pas de temps stable trouvé (exposant > 40)."
        raise ValueError(msg)

    def _verifier_passages(self, pas_temps: float, t_entree: float) -> None:
        """Exige des passages multiples entiers du pas depuis l'entrée."""
        for arc in self.arcs[1:]:
            ecart_pas = (float(arc) / self.source.u - t_entree) / pas_temps
            if abs(ecart_pas - round(ecart_pas)) > 1e-9:
                msg = (
                    "Les instants de passage doivent être des multiples entiers "
                    "du pas de temps depuis l'entrée."
                )
                raise ValueError(msg)

    def _marcher(
        self,
        grille: GrilleEdp,
        coefficients: CoefficientsDiffusion,
        t_entree: float,
        pas_temps: float,
    ) -> SolutionTransitoire:
        """Marche le schéma FTCS en temps, instantanés à l'entrée et aux passages.

        Méthodologie (note 35) : K = (u/2)·d(sigma²)/dx évalué à la distance
        parcourue du milieu du pas ; schéma explicite en temps, centré en
        transverse et vertical ; miroir au sol (Neumann : ∂Q/∂z = 0 au sol,
        exact car le noyau du puff est pair en z), Dirichlet nul aux bords.
        """
        u = self.source.u
        pas_y = self.parametres.pas_transverse_y
        pas_z = self.parametres.pas_transverse_z
        champ = _marginale_analytique(self.source, grille, t_entree)
        champ[0, :] = 0.0
        champ[-1, :] = 0.0
        champ[:, -1] = 0.0

        cibles = {
            round((float(arc) / u - t_entree) / pas_temps): float(arc) / u
            for arc in self.arcs[1:]
        }
        instants: list[InstantPuff] = [InstantPuff(t=t_entree, champ=champ.copy())]
        total = round((float(self.arcs[-1]) / u - t_entree) / pas_temps)
        suivant = np.empty_like(champ)

        t = t_entree
        for pas in range(1, total + 1):
            t_milieu = t + 0.5 * pas_temps
            distance_milieu = u * t_milieu
            diffusion_y = coefficients.derivee_sigma_y_carre(distance_milieu)
            diffusion_z = coefficients.derivee_sigma_z_carre(distance_milieu)
            c_y = 0.5 * u * diffusion_y * pas_temps / pas_y**2
            c_z = 0.5 * u * diffusion_z * pas_temps / pas_z**2
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
            t += pas_temps
            instant_vise = cibles.get(pas)
            if instant_vise is not None:
                instants.append(InstantPuff(t=instant_vise, champ=champ.copy()))

        return SolutionTransitoire(
            t_entree=t_entree,
            pas_temps=pas_temps,
            abscisses_y=grille.abscisses_y,
            abscisses_z=grille.abscisses_z,
            instants=tuple(instants),
        )


def resoudre_transitoire(
    source: SourceImpulsionnelle,
    arcs: tuple[float, ...],
    parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
    modele: ModeleDiffusion = DIFFUSION_BRIGGS,
) -> SolutionTransitoire:
    """Résout l'EDP transitoire du puff, de l'entrée au dernier passage.

    Point d'entrée public de la route EDP : délègue au solveur. Le modèle
    de diffusion est injectable — c'est le point d'extension de S0-b
    (cisaillement) ; le schéma et la grille restent ceux de l'étape 5.
    """
    return SolveurTransitoire(source, arcs, parametres, modele).resoudre()


@dataclass(frozen=True)
class MesureTransitoire:
    """Mesure de la route EDP transitoire : valeurs, masse, solution, coût.

    Attributs :
        valeurs : concentrations dirigées EDP aux points (kg m⁻³).
        ecarts_masse : écarts relatifs de masse vs marginale fermée, un par
            instantané de la solution, entrée incluse.
        solution : solution transitoire complète (instants, grille, pas).
        cout_s : coût mesuré de la route : résolution, échantillonnage, masse.
    """

    valeurs: tuple[float, ...]
    ecarts_masse: tuple[float, ...]
    solution: SolutionTransitoire
    cout_s: float


class RouteFermeePuff:
    """Route de référence : solution fermée du puff, coût mesuré (note 35).

    Attributs :
        source : source impulsionnelle évaluée aux instants de passage.
        arcs : distances sous le vent des arcs de passage (m).
    """

    def __init__(self, source: SourceImpulsionnelle, arcs: tuple[float, ...]) -> None:
        """Porte la source et les arcs de passage de la comparaison."""
        self.source = source
        self.arcs = arcs

    def mesurer(self, points: tuple[PointMesure, ...]) -> tuple[tuple[float, ...], float]:
        """Évalue la solution fermée aux points (t = x/u), coût mesuré."""
        _verifier_points_aux_arcs(self.arcs, points)
        debut = time.perf_counter()
        valeurs = np.asarray(
            [
                concentration_puff(
                    x=point.x,
                    y=point.y,
                    z=point.z,
                    t=point.x / self.source.u,
                    masse=self.source.masse,
                    u=self.source.u,
                    classe=self.source.classe,
                    x0=self.source.x0,
                )
                for point in points
            ],
            dtype=float,
        )
        cout_s = time.perf_counter() - debut
        return tuple(float(valeur) for valeur in valeurs), float(cout_s)


class RouteEdpPuff:
    """Route candidate : EDP transitoire, échantillonnage, coût mesuré.

    Le coût couvre exactement la résolution, l'échantillonnage bilinéaire,
    le facteur longitudinal analytique et les écarts de masse (note 35 :
    les deux routes sont mesurées séparément, sans facteur historique).

    Attributs :
        source : source impulsionnelle résolue par le schéma FTCS en temps.
        arcs : distances sous le vent des arcs de passage (m).
        parametres : paramètres numériques de la grille transverse/verticale.
        modele : modèle de diffusion (Briggs par défaut).
    """

    def __init__(
        self,
        source: SourceImpulsionnelle,
        arcs: tuple[float, ...],
        parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
        modele: ModeleDiffusion = DIFFUSION_BRIGGS,
    ) -> None:
        """Injecte les mêmes considérations que le solveur (points d'extension)."""
        self.source = source
        self.arcs = arcs
        self.parametres = parametres
        self.modele = modele

    def mesurer(self, points: tuple[PointMesure, ...]) -> MesureTransitoire:
        """Résout, échantillonne et pèse la route EDP ; coût mesuré ensemble."""
        _verifier_points_aux_arcs(self.arcs, points)
        debut = time.perf_counter()
        solution = SolveurTransitoire(
            self.source, self.arcs, self.parametres, self.modele
        ).resoudre()
        grille = GrilleEdp(abscisses_y=solution.abscisses_y, abscisses_z=solution.abscisses_z)
        par_instant = {instant.t: instant for instant in solution.instants}
        valeurs: list[float] = []
        for point in points:
            instant = par_instant[point.x / self.source.u]
            valeurs.append(self._dirigee(instant, grille, point))
        ecarts_masse: list[float] = []
        for instant in solution.instants:
            masse_edp = _masse(instant.champ, grille)
            attendue = _marginale_analytique(self.source, grille, instant.t)
            masse_fermee = _masse(attendue, grille)
            ecarts_masse.append(abs(masse_edp - masse_fermee) / masse_fermee)
        cout_s = time.perf_counter() - debut
        return MesureTransitoire(
            valeurs=tuple(valeurs),
            ecarts_masse=tuple(ecarts_masse),
            solution=solution,
            cout_s=float(cout_s),
        )

    def _dirigee(self, instant: InstantPuff, grille: GrilleEdp, point: PointMesure) -> float:
        """Concentration dirigée : marginale échantillonnée, facteur longitudinal."""
        u = self.source.u
        t = point.x / u
        distance = u * t
        sigma_x = sigma_y(distance, self.source.classe)
        facteur = float(
            np.exp(-((point.x - self.source.x0 - distance) ** 2) / (2.0 * sigma_x**2))
            / (np.sqrt(2.0 * np.pi) * float(sigma_x))
        )
        return _bilineaire(instant.champ, grille, point.y, point.z) * facteur


class PointComparaisonPuff(BaseModel):
    """Comparaison ponctuelle fermée/EDP transitoire en un point de mesure."""

    model_config = ConfigDict(frozen=True)

    x: float
    y: float
    z: float
    fermee: float
    edp: float
    ratio: float


class ComparaisonTransitoire(BaseModel):
    """Comparaison complète de la route EDP transitoire à la solution fermée.

    Attributs :
        source_puff : identification de la source comparée (masse, vent, classe).
        parametres : paramètres numériques de la grille EDP transverse.
        instants : instants de passage couverts par la solution (s).
        points : comparaisons ponctuelles, une par point de mesure.
        fac2 : fraction des points dans un facteur 2 (métrique partagée).
        nmse : erreur quadratique normalisée (métrique partagée).
        ecart_relatif_max : écart relatif maximal fermée/EDP (sans unité).
        ecart_masse_max : écart relatif maximal de masse aux instantanés.
        cout_ferme_s : coût de la route fermée, mesuré (s).
        cout_edp_s : coût de la route EDP, mesuré séparément (s).
    """

    model_config = ConfigDict(frozen=True)

    source_puff: str
    parametres: ParametresEdp
    instants: tuple[float, ...]
    points: tuple[PointComparaisonPuff, ...]
    fac2: float
    nmse: float
    ecart_relatif_max: float
    ecart_masse_max: float
    cout_ferme_s: float
    cout_edp_s: float

    def vers_dict(self) -> dict[str, object]:
        """Exporte la comparaison en dictionnaire JSON-natif (frontière)."""
        return self.model_dump(mode="json")


class ManifesteTransitoire(BaseModel):
    """Manifeste de l'EDP transitoire du puff (suite de l'étape 6)."""

    model_config = ConfigDict(frozen=True)

    identifiant: str
    niveau_fidelite: str
    source: str
    heritage_documentaire: str
    reconstruction: str
    extension: str
    limites: tuple[str, ...]
    comparaison: ComparaisonTransitoire
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire JSON-natif (frontière)."""
        return self.model_dump(mode="json")


def comparer_transitoire(
    source: SourceImpulsionnelle,
    arcs: tuple[float, ...],
    points: tuple[PointMesure, ...],
    parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
    modele: ModeleDiffusion = DIFFUSION_BRIGGS,
) -> ComparaisonTransitoire:
    """Compare la route EDP transitoire à la solution fermée aux passages.

    Orchestration seulement : la route fermée évalue la solution fermée du
    puff aux instants de passage, la route EDP résout la marginale
    transverse puis lui applique la structure longitudinale analytique ;
    les métriques FAC2 et NMSE sont celles du registre partagé
    (jdriftx.benchmarks.metriques, issue #43) ; les coûts des deux routes
    sont mesurés séparément (note 35), sans facteur historique.
    """
    fermee, cout_ferme = RouteFermeePuff(source, arcs).mesurer(points)
    mesure = RouteEdpPuff(source, arcs, parametres, modele).mesurer(points)
    comparaisons = tuple(
        PointComparaisonPuff(
            x=float(point.x),
            y=float(point.y),
            z=float(point.z),
            fermee=valeur_fermee,
            edp=valeur_edp,
            ratio=float(valeur_edp / valeur_fermee),
        )
        for point, valeur_fermee, valeur_edp in zip(
            points, fermee, mesure.valeurs, strict=True
        )
    )
    ecarts_relatifs = [abs(point.edp - point.fermee) / point.fermee for point in comparaisons]
    return ComparaisonTransitoire(
        source_puff=(
            f"masse={source.masse} kg, u={source.u} m/s, "
            f"classe={source.classe}, x0={source.x0} m"
        ),
        parametres=parametres,
        instants=tuple(float(instant.t) for instant in mesure.solution.instants),
        points=comparaisons,
        fac2=fac2(list(fermee), list(mesure.valeurs)),
        nmse=nmse(list(fermee), list(mesure.valeurs)),
        ecart_relatif_max=float(max(ecarts_relatifs)),
        ecart_masse_max=float(max(mesure.ecarts_masse)),
        cout_ferme_s=cout_ferme,
        cout_edp_s=mesure.cout_s,
    )


def construire_manifeste(comparaison: ComparaisonTransitoire) -> ManifesteTransitoire:
    """Construit le manifeste étiqueté de l'EDP transitoire (statuts figés).

    Le manifeste porte l'étiquetage héritage/reconstruction/extension et
    les limites explicites ; la version du code est lue dans les
    métadonnées d'installation si disponible, « non-installe » sinon.
    """
    try:
        version = metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        version = "non-installe"
    return ManifesteTransitoire(
        identifiant="jdriftx-transitoire-puff-001",
        niveau_fidelite="R1",
        source="Chapitre « Reduced-Order Modelling of Dispersion » (Brun & "
        "Mohammadi, 2008), DOI 10.1007/978-1-4020-8758-5_14",
        heritage_documentaire=(
            "Aucune source historique : l'EDP transitoire du puff est la "
            "suite directe de l'évaluation dirigée du puff (note 53) ; aucun "
            "chiffre de l'ouvrage de 2008 n'est utilisé comme cible."
        ),
        reconstruction=(
            "Marche explicite FTCS en temps de la marginale transverse du puff "
            "(nombre de Fourier ≤ 1/3 au dernier passage, entrée fermée au "
            "premier instant de passage, miroir au sol, Dirichlet aux bords) ; "
            "structure longitudinale analytique (carte travel-time de la note "
            "37, isotropie sigma_x = sigma_y du noyau fermé)."
        ),
        extension=(
            "EDP transitoire du puff : seconde extension conditionnelle du "
            "contrat minimal (docs/47 §5) ; la source impulsionnelle de la "
            "note 53 reçoit sa route EDP transitoire, hors périmètre de la "
            "baseline continue."
        ),
        limites=(
            "Contrôle d'auto-cohérence entre deux routes du même package sur "
            "un cas synthétique : pas une validation physique.",
            "La structure longitudinale reste analytique (carte travel-time, "
            "isotropie du noyau fermé) : seule la marginale transverse est "
            "marchée numériquement.",
            "Le noyau du puff est symétrique en z autour du sol : la moitié "
            "de la masse du noyau fermé est formellement sous le sol ; la "
            "grille porte la demi-colonne miroir et les écarts de masse sont "
            "comparés à la marginale analytique sur la même grille.",
            "Fenêtre tronquée à quatre écarts-types au dernier passage, "
            "grille calibrée pour la classe C du cas S0 figé (docs/48 §2.2).",
        ),
        comparaison=comparaison,
        version_code=version,
        commande=(
            "uv run python -c 'from jdriftx.benchmarks.cas import "
            "CAS_S0_DEFAUT; from jdriftx.experiences.evaluation_puff import "
            "PUFF_DEFAUT; from jdriftx.experiences.transitoire_puff import "
            "comparer_transitoire, construire_manifeste; "
            "print(construire_manifeste(comparer_transitoire(PUFF_DEFAUT, "
            "CAS_S0_DEFAUT.arcs, CAS_S0_DEFAUT.points())))'"
        ),
    )
