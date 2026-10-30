"""Comparaison à référence indépendante : résolution EDP du cas S0 (étape 5).

Cette étape reconstruit une route de calcul indépendante de la solution de
similitude : une équation aux dérivées partielles de diffusion 2D (transverse
et verticale) marchée en longitude sous l'hypothèse de vent uniforme, et
compare ses résultats ponctuels à la solution fermée du package sur le cas S0
figé (docs/48 §2.2). La méthodologie suit la note 35 (cost model étape par
étape : les coûts des deux routes sont mesurés séparément ; le facteur
historique 10³-10⁴ de l'ouvrage de 2008 n'est ni reconstruit ni revendiqué).

Architecture (séparation des considérations, révision interne) :

- ``ModeleDiffusion`` (protocole) : physique de diffusion transverse et
  verticale, implémentée par ``DiffusionBriggs`` (jdriftx.stabilite) ;
  point d'extension de S0-b (cisaillement) et de la paramétrisation R3.
- ``GrilleEdp`` : géométrie seule (nœuds, mailles, couverture quatre
  écarts-types) ; point d'extension de la colonne multi-niveaux de R3.
- ``SolveurEdp`` : schéma FTCS (pas stable, miroir au sol, Dirichlet aux
  bords, tranches aux arcs) ; point d'extension de l'EDP transitoire du puff.
- ``EchantillonneurBilineaire`` : lecture ponctuelle et bilan d'un champ
  sur la grille (interpolation, intégrale, flux) ; réutilisée par l'EDP
  transitoire du puff (note 54).
- ``RouteFermee``/``RouteEdp`` : les deux routes mesurées séparément
  (note 35), assemblées par ``comparer_reference`` avec les métriques
  partagées.

Le comportement numérique de cette révision est inchangé : mêmes formules,
même ordre d'opérations, résultats identiques à l'implémentation d'origine
(vérifié par les tests existants, conservés tels quels).

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
from itertools import pairwise
from typing import Protocol

import numpy as np
from pydantic import BaseModel, ConfigDict

from jdriftx._protocoles import ModeleConcentration
from jdriftx.benchmarks.cas import CasS0, PointMesure
from jdriftx.benchmarks.metriques import fac2, nmse
from jdriftx.concentrations import PanacheGaussien
from jdriftx.similitude import sigma_y, sigma_z
from jdriftx.stabilite import ClasseStabilite, FormeSigmaZ

__all__ = [
    "DIFFUSION_BRIGGS",
    "PARAMETRES_EDP_DEFAUT",
    "SEUIL_FOURIER",
    "CoefficientsDiffusion",
    "ComparaisonReference",
    "DiffusionBriggs",
    "EchantillonneurBilineaire",
    "GrilleEdp",
    "ManifesteReference",
    "MesureEdp",
    "ModeleDiffusion",
    "ParametresEdp",
    "PointComparaison",
    "RouteEdp",
    "RouteFermee",
    "SolutionEdp",
    "SolveurDeReference",
    "SolveurEdp",
    "TrancheEdp",
    "comparer_reference",
    "construire_manifeste",
    "derivee_sigma_carre",
    "resoudre_edp",
]


def _tableau_immuable(
    valeur: np.ndarray,
    nom: str,
    *,
    dimension: int,
    taille_minimale: int = 1,
    strictement_croissant: bool = False,
) -> np.ndarray:
    """Valide puis détache un tableau dans un tampon réellement non modifiable."""
    if isinstance(valeur, np.ndarray):
        valeur_non_reelle = valeur.dtype.kind in {"b", "c"} or (
            valeur.dtype.kind == "O"
            and any(
                isinstance(element, (bool, np.bool_, complex, np.complexfloating))
                for element in valeur.flat
            )
        )
    else:
        brut = np.asarray(valeur, dtype=object)
        valeur_non_reelle = any(
            isinstance(element, (bool, np.bool_, complex, np.complexfloating))
            for element in brut.flat
        )
    if valeur_non_reelle:
        msg = f"{nom} doit contenir des valeurs reelles "
        raise ValueError(msg + "(booleens exclus; complexes exclus).")
    tableau = np.asarray(valeur, dtype=float)
    if tableau.ndim != dimension or tableau.size < taille_minimale:
        raise ValueError(f"{nom} doit avoir {dimension} dimension(s) et être non vide.")
    if not np.all(np.isfinite(tableau)):
        raise ValueError(f"{nom} doit contenir uniquement des valeurs finies.")
    if strictement_croissant:
        ecarts = np.diff(tableau)
        if not np.all(np.isfinite(ecarts)) or np.any(ecarts <= 0.0):
            raise ValueError(f"{nom} doit être strictement croissant avec des écarts finis.")

    base: object = tableau
    while isinstance(base, np.ndarray) and base.base is not None:
        base = base.base
    if not tableau.flags.writeable and isinstance(base, bytes):
        return tableau

    copie = np.array(tableau, dtype=float, copy=True)
    return np.frombuffer(copie.tobytes(), dtype=copie.dtype).reshape(copie.shape)


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
        valeurs = (
            self.pas_transverse_y,
            self.pas_transverse_z,
            self.demi_largeur_y,
            self.hauteur_max,
        )
        if any(
            isinstance(valeur, (bool, np.bool_, complex, np.complexfloating)) for valeur in valeurs
        ):
            msg = "Les paramètres EDP doivent être réels (booléens exclus ; complexes exclus)."
            raise ValueError(msg)
        if not all(np.isfinite(valeur) for valeur in valeurs):
            msg = "Les paramètres EDP doivent être finis."
            raise ValueError(msg)
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
        with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
            rapport_y = (
                np.float64(self.demi_largeur_y)
                / np.float64(self.pas_transverse_y)
                * np.float64(2.0)
            )
            rapport_z = np.float64(self.hauteur_max) / np.float64(self.pas_transverse_z)
        if not np.isfinite(rapport_y) or rapport_y <= 0.0:
            msg = "Le rapport de discrétisation latérale doit être représentable en float64."
            raise ValueError(msg)
        if not np.isfinite(rapport_z) or rapport_z <= 0.0:
            msg = "Le rapport de discrétisation verticale doit être représentable en float64."
            raise ValueError(msg)
        if abs(rapport_y - np.rint(rapport_y)) > 1e-9:
            msg = "La fenêtre doit être un multiple entier du pas transverse."
            raise ValueError(msg)
        if abs(rapport_z - np.rint(rapport_z)) > 1e-9:
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
    if any(
        isinstance(value, (bool, np.bool_, complex, np.complexfloating))
        for value in (x, coefficient, d)
    ):
        msg = "Les paramètres de dérivée doivent être réels (booléens exclus ; complexes exclus)."
        raise ValueError(msg)
    try:
        with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
            x_reel = np.float64(x)
            coefficient_reel = np.float64(coefficient)
            d_reel = np.float64(d)
    except (OverflowError, TypeError, ValueError) as err:
        msg = "Les paramètres de dérivée doivent être représentables en float64."
        raise ValueError(msg) from err
    if not all(np.isfinite(value) for value in (x_reel, coefficient_reel, d_reel)):
        msg = "Les paramètres de dérivée doivent être finis et représentables en float64."
        raise ValueError(msg)
    if x_reel <= 0.0:
        msg = "La distance sous le vent doit être strictement positive."
        raise ValueError(msg)
    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        produit = coefficient_reel * x_reel
        carre = produit * produit
        denominateur = 1.0 + d_reel * x_reel
        variance = carre / denominateur
        facteur_derivee = 2.0 / x_reel - d_reel / denominateur
        resultat = variance * facteur_derivee
    sous_debordement = (
        (coefficient_reel != 0.0 and produit == 0.0)
        or (produit != 0.0 and carre == 0.0)
        or (carre != 0.0 and variance == 0.0)
        or (variance != 0.0 and facteur_derivee != 0.0 and resultat == 0.0)
    )
    if sous_debordement or not all(
        np.isfinite(value)
        for value in (produit, carre, denominateur, variance, facteur_derivee, resultat)
    ):
        msg = "La dérivée de sigma² n'est pas représentable en float64."
        raise ValueError(msg)
    return float(resultat)


@dataclass(frozen=True)
class CoefficientsDiffusion:
    """Coefficients (a_y, d_y, b_z, d_z) des sigma de Briggs d'une classe.

    Porte la dérivée exacte de sigma², seule quantitative pour le schéma ;
    les deux directions (transverse, verticale) partagent la même forme.

    Attributs :
        a_y, d_y : coefficients de sigma_y (m, sans unité).
        b_z, d_z : coefficients de sigma_z (m, sans unité).
    """

    a_y: float
    d_y: float
    b_z: float
    d_z: float

    def __post_init__(self) -> None:
        """Refuse les coefficients booléens avant tout calcul de diffusion."""
        valeurs = (self.a_y, self.d_y, self.b_z, self.d_z)
        if any(
            isinstance(value, (bool, np.bool_, complex, np.complexfloating)) for value in valeurs
        ):
            msg = (
                "Les coefficients de diffusion doivent être réels "
                "(booléens exclus ; complexes exclus)."
            )
            raise ValueError(msg)

    def derivee_sigma_y_carre(self, x: float) -> float:
        """Dérivée exacte de sigma_y² en x (m), strictement positive."""
        return derivee_sigma_carre(x, self.a_y, self.d_y)

    def derivee_sigma_z_carre(self, x: float) -> float:
        """Dérivée exacte de sigma_z² en x (m), strictement positive."""
        return derivee_sigma_carre(x, self.b_z, self.d_z)

    def pas_longitudinal(self, x_debut: float, x_fin: float, parametres: ParametresEdp) -> float:
        """Plus grand pas en base/2^k stable au dernier arc (nombre de Fourier).

        Le nombre de Fourier est évalué au dernier arc, là où sigma² croît le
        plus ; le pas de base est la distance d'entrée (100 m pour le cas S0
        figé) et il est divisé par deux jusqu'à ce que la somme des
        contributions transverse et verticale passe sous SEUIL_FOURIER.
        """
        if isinstance(x_debut, (bool, np.bool_, complex, np.complexfloating)):
            msg = "La distance de début doit être réelle (booléen exclu ; complexe exclu)."
            raise ValueError(msg)
        dy = parametres.pas_transverse_y
        dz = parametres.pas_transverse_z
        for exposant in range(0, 41):
            candidat = x_debut / 2.0**exposant
            fourier = (
                0.5 * self.derivee_sigma_y_carre(x_fin) * candidat / dy**2
                + 0.5 * self.derivee_sigma_z_carre(x_fin) * candidat / dz**2
            )
            if fourier <= SEUIL_FOURIER:
                return float(candidat)
        msg = "Aucun pas longitudinal stable trouvé (exposant > 40)."
        raise ValueError(msg)


class ModeleDiffusion(Protocol):
    """Interface des modèles de diffusion (point d'extension du schéma).

    Un modèle fournit les coefficients des sigma d'une classe de stabilité :
    c'est la seule porte d'entrée de la physique dans la marche numérique.
    S0-b (cisaillement du vent) s'y branchera sans toucher au schéma ni à
    la grille ; R3 réutilisera la même interface pour sa paramétrisation.
    """

    def coefficients(self, classe: str, x: float) -> CoefficientsDiffusion:
        """Coefficients de diffusion de la classe au point x (m).

        Lève une ValueError si la classe ou sa forme est hors périmètre.
        """
        ...


@dataclass(frozen=True)
class DiffusionBriggs:
    """Modèle de référence : lois de Briggs rurales via jdriftx.stabilite.

    Formes couvertes : LINEAIRE (d = 0) et RACINE (d > 0). La forme INVERSE
    (sigma_z = b·x/(1 + d·x), classes E et F) n'est pas dérivable en sigma²
    au sens du schéma et est rejetée sans ambiguïté.
    """

    def coefficients(self, classe: str, x: float) -> CoefficientsDiffusion:
        """Coefficients de la classe, forme INVERSE rejetée (ValueError)."""
        if isinstance(x, (bool, np.bool_, complex, np.complexfloating)):
            msg = "La distance d'évaluation doit être réelle (booléen exclu ; complexe exclu)."
            raise ValueError(msg)
        if not np.isfinite(x):
            msg = "La distance d'évaluation doit être finie."
            raise ValueError(msg)
        stable = ClasseStabilite(classe)
        a_y, d_y = stable.coeff_sigma_y
        forme, b_z, d_z = stable.coeff_sigma_z
        if forme is FormeSigmaZ.INVERSE:
            msg = (
                "La forme INVERSE de sigma_z (classes E et F) est hors périmètre "
                "de la résolution EDP marchée."
            )
            raise ValueError(msg)
        return CoefficientsDiffusion(a_y=a_y, d_y=d_y, b_z=b_z, d_z=d_z)


DIFFUSION_BRIGGS: ModeleDiffusion = DiffusionBriggs()
"""Modèle de diffusion par défaut : lois de Briggs rurales du package."""


@dataclass(frozen=True)
class TrancheEdp:
    """Tranche du champ EDP prélevée à un arc de mesure.

    Attributs :
        x : distance sous le vent de la tranche (m).
        champ : concentrations (kg m^-3) sur la grille transverse/verticale.
    """

    x: float
    champ: np.ndarray

    def __post_init__(self) -> None:
        """Valide et fige le champ porté par la tranche."""
        if isinstance(self.x, (bool, np.bool_, complex, np.complexfloating)):
            msg = "L'abscisse de la tranche doit être réelle (booléen exclu ; complexe exclu)."
            raise ValueError(msg)
        if not np.isfinite(self.x):
            msg = "L'abscisse de la tranche doit être finie."
            raise ValueError(msg)
        object.__setattr__(
            self, "champ", _tableau_immuable(self.champ, "Le champ de la tranche", dimension=2)
        )


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

    def __post_init__(self) -> None:
        """Valide la cohérence de la solution et fige ses axes et sa séquence."""
        if isinstance(self.x_entree, (bool, np.bool_, complex, np.complexfloating)) or isinstance(
            self.pas_longitudinal, (bool, np.bool_, complex, np.complexfloating)
        ):
            msg = (
                "L'abscisse d'entrée et le pas longitudinal doivent être numériques "
                "(booléens exclus ; complexes exclus)."
            )
            raise ValueError(msg)
        if not np.isfinite(self.x_entree):
            msg = "L'abscisse d'entrée de la solution doit être finie."
            raise ValueError(msg)
        if not np.isfinite(self.pas_longitudinal) or self.pas_longitudinal <= 0.0:
            msg = "Le pas longitudinal doit être fini et strictement positif."
            raise ValueError(msg)
        abscisses_y = _tableau_immuable(
            self.abscisses_y,
            "Les abscisses y",
            dimension=1,
            taille_minimale=2,
            strictement_croissant=True,
        )
        abscisses_z = _tableau_immuable(
            self.abscisses_z,
            "Les abscisses z",
            dimension=1,
            taille_minimale=2,
            strictement_croissant=True,
        )
        tranches = tuple(self.tranches)
        if not tranches:
            msg = "La solution doit contenir au moins une tranche."
            raise ValueError(msg)
        if not all(isinstance(tranche, TrancheEdp) for tranche in tranches):
            msg = "Les tranches de la solution doivent être des objets TrancheEdp."
            raise ValueError(msg)
        forme_attendue = (abscisses_y.size, abscisses_z.size)
        if any(tranche.champ.shape != forme_attendue for tranche in tranches):
            msg = "Chaque tranche doit avoir la forme de la grille de la solution."
            raise ValueError(msg)
        positions = tuple(tranche.x for tranche in tranches)
        if any(not np.isfinite(position) for position in positions) or any(
            suivant <= precedent for precedent, suivant in pairwise(positions)
        ):
            msg = "Les abscisses des tranches doivent être finies et croissantes."
            raise ValueError(msg)
        object.__setattr__(self, "abscisses_y", abscisses_y)
        object.__setattr__(self, "abscisses_z", abscisses_z)
        object.__setattr__(self, "tranches", tranches)


class SolveurDeReference(Protocol):
    """Contrat d'un solveur produisant une solution échantillonnable.

    Une route de comparaison dépend de la structure de sortie, pas du schéma
    numérique. Un solveur alternatif peut donc remplacer FTCS s'il fournit
    les mêmes coordonnées et tranches, sans hériter de SolveurEdp.
    """

    def resoudre(self) -> SolutionEdp:
        """Retourne la solution sur la grille et aux arcs du cas configuré."""
        ...


@dataclass(frozen=True)
class GrilleEdp:
    """Géométrie de la grille EDP : nœuds latéraux symétriques, colonne du sol.

    La grille ne porte aucune considération numérique ni physique : elle
    construit les nœuds, les mailles d'évaluation du contrat d'entrée et la
    couverture quatre écarts-types exigée au dernier arc. C'est le point
    d'extension de R3 (colonne multi-niveaux : nœuds verticaux enrichis).

    Attributs :
        abscisses_y : nœuds latéraux (m), symétriques autour de zéro.
        abscisses_z : nœuds verticaux (m), du sol au sommet de fenêtre.
    """

    abscisses_y: np.ndarray
    abscisses_z: np.ndarray

    def __post_init__(self) -> None:
        """Valide la géométrie et fige les deux axes de la grille."""
        object.__setattr__(
            self,
            "abscisses_y",
            _tableau_immuable(
                self.abscisses_y,
                "Les abscisses y",
                dimension=1,
                taille_minimale=2,
                strictement_croissant=True,
            ),
        )
        object.__setattr__(
            self,
            "abscisses_z",
            _tableau_immuable(
                self.abscisses_z,
                "Les abscisses z",
                dimension=1,
                taille_minimale=2,
                strictement_croissant=True,
            ),
        )

    @classmethod
    def depuis_parametres(cls, parametres: ParametresEdp) -> GrilleEdp:
        """Construit les nœuds depuis les paramètres (fenêtre symétrique)."""
        abscisses_y = np.arange(
            -parametres.demi_largeur_y,
            parametres.demi_largeur_y + 0.5 * parametres.pas_transverse_y,
            parametres.pas_transverse_y,
        )
        abscisses_z = np.arange(
            0.0,
            parametres.hauteur_max + 0.5 * parametres.pas_transverse_z,
            parametres.pas_transverse_z,
        )
        return cls(abscisses_y=abscisses_y, abscisses_z=abscisses_z)

    def mailles(self) -> tuple[np.ndarray, np.ndarray]:
        """Mailles 2D (meshgrid, indexation ij) pour l'évaluation d'entrée."""
        mailles_y, mailles_z = np.meshgrid(self.abscisses_y, self.abscisses_z, indexing="ij")
        return mailles_y, mailles_z

    @classmethod
    def pour_le_cas(cls, cas: CasS0, parametres: ParametresEdp) -> GrilleEdp:
        """Construit la grille du cas en validant la couverture quatre sigma.

        La troncature à quatre écarts-types est documentée (note 51) : la
        fenêtre latérale couvre 4·sigma_y et la colonne verticale la hauteur
        source augmentée de 4·sigma_z, tous deux au dernier arc du cas.
        """
        x_fin = float(cas.arcs[-1])
        classe = cas.source.classe
        if parametres.demi_largeur_y < 4.0 * float(sigma_y(x_fin, classe)):
            msg = (
                "La fenêtre latérale doit couvrir quatre écarts-types au dernier "
                "arc (troncature documentée)."
            )
            raise ValueError(msg)
        seuil_z = cas.source.hauteur + 4.0 * float(sigma_z(x_fin, classe))
        if parametres.hauteur_max < seuil_z:
            msg = (
                "La colonne verticale doit couvrir la hauteur source plus quatre "
                "écarts-types verticaux au dernier arc."
            )
            raise ValueError(msg)
        return cls.depuis_parametres(parametres)


class SolveurEdp:
    """Schéma explicite FTCS marché en longitude, tranches prélevées aux arcs.

    Le solveur porte les seules considérations numériques : pas longitudinal
    stable (SEUIL_FOURIER), condition au sol de type miroir (Neumann),
    Dirichlet nul aux bords latéraux et au sommet de fenêtre, prélèvement des
    tranches aux arcs de mesure. La physique de diffusion vient du modèle
    injecté (ModeleDiffusion), la géométrie de la grille (GrilleEdp) : une
    EDP transitoire du puff réutilisera la même grille et le même modèle en
    changeant la marche.

    Attributs :
        cas : cas S0 figé portant la source et les arcs de mesure.
        parametres : paramètres numériques de la grille transverse/verticale.
        modele : modèle de diffusion (Briggs par défaut).
        condition_entree : champ initial (panache gaussien partagé par défaut).
    """

    def __init__(
        self,
        cas: CasS0,
        parametres: ParametresEdp,
        modele: ModeleDiffusion = DIFFUSION_BRIGGS,
        condition_entree: ModeleConcentration | None = None,
    ) -> None:
        """Injecte le cas, la géométrie, la diffusion et le champ d'entrée."""
        self.cas = cas
        self.parametres = parametres
        self.modele = modele
        self.condition_entree = (
            condition_entree if condition_entree is not None else PanacheGaussien(source=cas.source)
        )

    def resoudre(self) -> SolutionEdp:
        """Résout du premier au dernier arc : modèle, grille, pas, arcs, marche.

        L'ordre de validation est celui de l'implémentation d'origine :
        coefficients (forme INVERSE rejetée), couverture de fenêtre, pas
        longitudinal stable, divisibilité des arcs, puis marche FTCS.
        """
        classe = self.cas.source.classe
        x_entree = float(self.cas.arcs[0])
        x_fin = float(self.cas.arcs[-1])
        coefficients = self.modele.coefficients(classe, x_fin)
        grille = GrilleEdp.pour_le_cas(self.cas, self.parametres)
        dx = coefficients.pas_longitudinal(x_entree, x_fin, self.parametres)
        self._verifier_arcs(dx)
        return self._marcher(grille, coefficients, x_entree, dx)

    def _verifier_arcs(self, dx: float) -> None:
        """Exige des arcs multiples entiers du pas longitudinal (écart strict)."""
        for precedent, arc in zip(self.cas.arcs[:-1], self.cas.arcs[1:], strict=True):
            if abs((arc - precedent) / dx - round((arc - precedent) / dx)) > 1e-9:
                msg = (
                    "Les arcs doivent être des multiples entiers du pas "
                    "longitudinal depuis l'entrée."
                )
                raise ValueError(msg)

    def _marcher(
        self,
        grille: GrilleEdp,
        coefficients: CoefficientsDiffusion,
        x_entree: float,
        dx: float,
    ) -> SolutionEdp:
        """Marche le schéma FTCS de l'entrée au dernier arc, tranches aux arcs.

        Méthodologie (note 35, étape 5 de l'issue #232) : schéma explicite
        marché en longitude sur K = (U/2)·d(sigma²)/dx (U disparaît du champ),
        entrée partagée à x du premier arc (solution fermée du package sur la
        grille), condition au sol de type miroir (Neumann : ∂C/∂z = 0 au sol),
        Dirichlet nul aux bords latéraux et au sommet de fenêtre.
        """
        pas_y = self.parametres.pas_transverse_y
        pas_z = self.parametres.pas_transverse_z
        mailles_y, mailles_z = grille.mailles()
        champ = np.asarray(
            self.condition_entree.concentration(x_entree, mailles_y, mailles_z),
            dtype=float,
        )
        if champ.shape != mailles_y.shape:
            msg = "La condition d'entrée doit retourner un champ de même forme que la grille."
            raise ValueError(msg)
        if not np.all(np.isfinite(champ)):
            msg = "La condition d'entrée doit retourner des concentrations finies."
            raise ValueError(msg)
        champ = champ.copy()
        champ[0, :] = 0.0
        champ[-1, :] = 0.0
        champ[:, -1] = 0.0

        cibles = {round((arc - x_entree) / dx): float(arc) for arc in self.cas.arcs[1:]}
        tranches: list[TrancheEdp] = [TrancheEdp(x=x_entree, champ=champ.copy())]
        total = round((float(self.cas.arcs[-1]) - x_entree) / dx)
        suivant = np.empty_like(champ)

        x = x_entree
        for pas in range(1, total + 1):
            x_milieu = x + 0.5 * dx
            c_y = 0.5 * coefficients.derivee_sigma_y_carre(x_milieu) * dx / pas_y**2
            c_z = 0.5 * coefficients.derivee_sigma_z_carre(x_milieu) * dx / pas_z**2
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
            arc_vise = cibles.get(pas)
            if arc_vise is not None:
                tranches.append(TrancheEdp(x=arc_vise, champ=champ.copy()))

        return SolutionEdp(
            x_entree=x_entree,
            pas_longitudinal=dx,
            abscisses_y=grille.abscisses_y,
            abscisses_z=grille.abscisses_z,
            tranches=tuple(tranches),
        )


def resoudre_edp(
    cas: CasS0,
    parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
    modele: ModeleDiffusion = DIFFUSION_BRIGGS,
    condition_entree: ModeleConcentration | None = None,
) -> SolutionEdp:
    """Résout l'EDP de diffusion marchée en x, du premier au dernier arc.

    Le solveur FTCS et le panache gaussien restent les défauts. Le modèle de
    diffusion et la condition initiale sont injectables ; cette dernière
    doit respecter le contrat ModeleConcentration et retourner un champ
    fini de la forme de la grille.
    """
    return SolveurEdp(cas, parametres, modele, condition_entree).resoudre()


def _pas_longitudinal(
    classe: str, x_debut: float, x_fin: float, parametres: ParametresEdp
) -> float:
    """Plus grand pas stable pour la diffusion Briggs de la classe (compat)."""
    return DIFFUSION_BRIGGS.coefficients(classe, x_fin).pas_longitudinal(x_debut, x_fin, parametres)


class EchantillonneurBilineaire:
    """Lecture ponctuelle et bilan d'un champ sur la grille EDP.

    Regroupe les opérations de lecture d'un champ résolu : interpolation
    bilinéaire aux points de mesure (après résolution), intégrale sur la
    grille et flux massique transverse. Réutilisée par l'EDP transitoire
    du puff (note 54) ; c'est le point d'extension d'un échantillonnage
    enrichi (profils verticaux multi-niveaux de R3).

    Attributs :
        champ : champ lu (tranche à un arc ou marginale à un instant).
        grille : grille de nœuds associée (même solution).
    """

    def __init__(self, champ: np.ndarray, grille: GrilleEdp) -> None:
        """Lie le champ à sa grille (les deux viennent de la même solution)."""
        self.champ = _tableau_immuable(
            champ,
            "Le champ à échantillonner",
            dimension=2,
        )
        forme_attendue = (grille.abscisses_y.size, grille.abscisses_z.size)
        if self.champ.shape != forme_attendue:
            msg = "Le champ doit avoir la forme de la grille EDP."
            raise ValueError(msg)
        self.grille = grille

    def concentration(self, y: float, z: float) -> float:
        """Interpole bilinéairement la concentration au point (y, z) (m).

        Lève une ValueError si le point sort de la fenêtre couverte par la
        grille : les points de comparaison doivent rester dans le domaine.
        """
        coordonnees: list[float] = []
        msg_coordonnees = "Les coordonnées y et z doivent être réelles et finies (booléens exclus)."
        for nom, valeur in (("y", y), ("z", z)):
            if isinstance(valeur, (bool, np.bool_)) or not isinstance(
                valeur, (int, float, np.integer, np.floating)
            ):
                raise ValueError(msg_coordonnees)
            try:
                coordonnee = float(valeur)
            except (OverflowError, TypeError, ValueError) as err:
                msg = f"La coordonnée {nom} doit être représentable en float64."
                raise ValueError(msg) from err
            if not np.isfinite(coordonnee):
                raise ValueError(msg_coordonnees)
            coordonnees.append(coordonnee)
        y_reel, z_reel = coordonnees

        abscisses_y = self.grille.abscisses_y
        abscisses_z = self.grille.abscisses_z
        pas_y = float(abscisses_y[1] - abscisses_y[0])
        pas_z = float(abscisses_z[1] - abscisses_z[0])
        f_y = (y_reel - float(abscisses_y[0])) / pas_y
        f_z = (z_reel - float(abscisses_z[0])) / pas_z
        if f_y < 0.0 or f_y > abscisses_y.size - 1 or f_z < 0.0 or f_z > abscisses_z.size - 1:
            msg = "Le point de comparaison sort de la fenêtre de la grille EDP."
            raise ValueError(msg)
        i_y = min(int(f_y), abscisses_y.size - 2)
        i_z = min(int(f_z), abscisses_z.size - 2)
        t_y = f_y - i_y
        t_z = f_z - i_z
        c00 = float(self.champ[i_y, i_z])
        c10 = float(self.champ[i_y + 1, i_z])
        c01 = float(self.champ[i_y, i_z + 1])
        c11 = float(self.champ[i_y + 1, i_z + 1])
        return float(
            c00 * (1.0 - t_y) * (1.0 - t_z)
            + c10 * t_y * (1.0 - t_z)
            + c01 * (1.0 - t_y) * t_z
            + c11 * t_y * t_z
        )

    def integrale(self) -> float:
        """Intégrale du champ sur la fenêtre de la grille (trapèzes doubles)."""
        integrale = np.trapezoid(
            np.trapezoid(self.champ, x=self.grille.abscisses_z, axis=1),
            x=self.grille.abscisses_y,
        )
        return float(integrale)

    def flux(self, u: float) -> float:
        """Flux massique transverse (kg/s) d'une tranche : U·∫∫ C dy dz."""
        return float(u * self.integrale())


@dataclass(frozen=True)
class MesureEdp:
    """Mesure de la route EDP : valeurs ponctuelles, flux, solution, coût.

    Attributs :
        valeurs : concentrations EDP interpolées aux points (kg m^-3).
        ecarts_flux : écarts relatifs de flux aux arcs, entrée exclue.
        solution : solution EDP complète (tranches, grille, pas).
        cout_s : coût mesuré de la route : résolution, échantillonnage, flux.
    """

    valeurs: tuple[float, ...]
    ecarts_flux: tuple[float, ...]
    solution: SolutionEdp
    cout_s: float


class RouteFermee:
    """Route de référence : solution fermée du package, coût mesuré (note 35).

    Attributs :
        cas : cas S0 figé évalué par le contrat de concentration partagé.
    """

    def __init__(self, cas: CasS0) -> None:
        """Porte le cas figé dont la vérité exacte sert de référence."""
        self.cas = cas

    def mesurer(self, points: tuple[PointMesure, ...]) -> tuple[tuple[float, ...], float]:
        """Évalue la solution fermée aux points et mesure le coût de la route."""
        debut = time.perf_counter()
        verite = np.asarray(self.cas.verite(points), dtype=float)
        cout_s = time.perf_counter() - debut
        return tuple(float(v) for v in verite), float(cout_s)


class RouteEdp:
    """Route candidate : résolution EDP, échantillonnage et flux, coût mesuré.

    Le coût couvre exactement la résolution, l'échantillonnage bilinéaire et
    le bilan de flux (note 35 : les deux routes sont mesurées séparément,
    sans facteur historique).

    Attributs :
        cas : cas S0 figé auquel le solveur injecté est appliqué.
        parametres : paramètres numériques de la grille transverse/verticale.
        modele : modèle de diffusion (Briggs par défaut).
        solveur : implémentation du protocole SolveurDeReference, optionnelle.
    """

    def __init__(
        self,
        cas: CasS0,
        parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
        modele: ModeleDiffusion = DIFFUSION_BRIGGS,
        solveur: SolveurDeReference | None = None,
    ) -> None:
        """Injecte le solveur ; FTCS reste l'implémentation par défaut."""
        self.cas = cas
        self.parametres = parametres
        self.modele = modele
        self.solveur = solveur if solveur is not None else SolveurEdp(cas, parametres, modele)

    def mesurer(self, points: tuple[PointMesure, ...]) -> MesureEdp:
        """Résout, échantillonne et intègre la route EDP ; coût mesuré ensemble."""
        debut = time.perf_counter()
        solution = self.solveur.resoudre()
        grille = GrilleEdp(abscisses_y=solution.abscisses_y, abscisses_z=solution.abscisses_z)
        tranches = {tranche.x: tranche for tranche in solution.tranches}
        valeurs: list[float] = []
        for point in points:
            echantillonneur = EchantillonneurBilineaire(tranches[point.x].champ, grille)
            valeurs.append(echantillonneur.concentration(point.y, point.z))
        u = self.cas.source.u
        flux_entree = EchantillonneurBilineaire(solution.tranches[0].champ, grille).flux(u)
        ecarts_flux: list[float] = []
        for tranche in solution.tranches[1:]:
            echantillonneur = EchantillonneurBilineaire(tranche.champ, grille)
            ecarts_flux.append(abs(echantillonneur.flux(u) - flux_entree) / flux_entree)
        cout_s = time.perf_counter() - debut
        return MesureEdp(
            valeurs=tuple(valeurs),
            ecarts_flux=tuple(ecarts_flux),
            solution=solution,
            cout_s=float(cout_s),
        )


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
    cas: CasS0,
    parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
    modele: ModeleDiffusion = DIFFUSION_BRIGGS,
) -> ComparaisonReference:
    """Compare la route EDP à la solution fermée sur la grille du cas.

    Orchestration seulement : les deux routes partagent la paramétrisation
    (Briggs via jdriftx.stabilite) et l'entrée (la route fermée évalue
    ``cas.verite(points)``, la route EDP part de la même solution fermée à
    l'arc d'entrée puis diffuse) ; les métriques FAC2 et NMSE sont celles du
    registre partagé (jdriftx.benchmarks.metriques, issue #43) ; les coûts
    des deux routes sont mesurés séparément (note 35), sans facteur
    historique.
    """
    points = cas.points()
    fermee, cout_ferme = RouteFermee(cas).mesurer(points)
    mesure = RouteEdp(cas, parametres, modele).mesurer(points)
    comparaisons = tuple(
        PointComparaison(
            x=float(point.x),
            y=float(point.y),
            z=float(point.z),
            fermee=valeur_fermee,
            edp=valeur_edp,
            ratio=float(valeur_edp / valeur_fermee),
        )
        for point, valeur_fermee, valeur_edp in zip(points, fermee, mesure.valeurs, strict=True)
    )
    ecarts_relatifs = [abs(point.edp - point.fermee) / point.fermee for point in comparaisons]
    return ComparaisonReference(
        cas_source=(
            f"debit={cas.source.debit} kg/s, u={cas.source.u} m/s, "
            f"classe={cas.source.classe}, hauteur={cas.source.hauteur} m"
        ),
        parametres=parametres,
        points=comparaisons,
        fac2=fac2(list(fermee), list(mesure.valeurs)),
        nmse=nmse(list(fermee), list(mesure.valeurs)),
        ecart_relatif_max=float(max(ecarts_relatifs)),
        ecart_flux_max=float(max(mesure.ecarts_flux)),
        cout_ferme_s=cout_ferme,
        cout_edp_s=mesure.cout_s,
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
