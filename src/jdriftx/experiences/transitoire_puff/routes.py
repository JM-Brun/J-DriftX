"""Routes de mesure du puff transitoire : fermée, EDP, structure longitudinale.

Les deux routes de la comparaison partagent la même géométrie de passages
(arcs sous le vent, instants dirigés t = arc/u) et seules leurs lectures
diffèrent : la route fermée évalue le noyau du package aux points de
mesure ; la route EDP résout la marginale transverse puis l'échantillonne
et lui applique la structure longitudinale. La structure est une
interface injectable (StructureLongitudinale) : le facteur gaussien
analytique (carte travel-time de la note 37, isotropie sigma_x = sigma_y
du noyau fermé) est l'implémentation par défaut, et le point d'extension
de S0-b (cisaillement) s'y branchera sans toucher aux routes.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

import numpy as np

from jdriftx.benchmarks.cas import PointMesure
from jdriftx.experiences.evaluation_puff import SourceImpulsionnelle
from jdriftx.experiences.reference_independante import (
    DIFFUSION_BRIGGS,
    PARAMETRES_EDP_DEFAUT,
    EchantillonneurBilineaire,
    GrilleEdp,
    ModeleDiffusion,
    ParametresEdp,
)
from jdriftx.experiences.transitoire_puff.marginale import MarginaleFermee
from jdriftx.experiences.transitoire_puff.solveur import (
    InstantPuff,
    PassagesPuff,
    SolutionTransitoire,
    SolveurTransitoire,
)
from jdriftx.similitude import concentration_puff, sigma_y


class StructureLongitudinale(Protocol):
    """Interface des structures longitudinales de la concentration dirigée.

    La structure porte la seule dépendance longitudinale de la lecture
    dirigée C(x, y, z, t) = Q(y, z, t)·facteur(x, t). L'implémentation
    nominale est analytique (carte travel-time de la note 37) ; le point
    d'extension de S0-b (cisaillement) s'y branche sans toucher aux
    routes ni au solveur.
    """

    def facteur(self, x: float, t: float) -> float:
        """Facteur longitudinal (m⁻¹) du noyau dirigé au point x, instant t."""
        ...


@dataclass(frozen=True)
class FacteurLongitudinalAnalytique:
    """Structure longitudinale gaussienne analytique (carte travel-time).

    Isotropie du noyau fermé : sigma_x = sigma_y (note 37), évalué à la
    distance parcourue d = u·t. Porte la source dont dépend la classe de
    stabilité et le point d'émission x0.

    Attributs :
        source : source impulsionnelle évaluée (vent, classe, x0).
    """

    source: SourceImpulsionnelle

    def facteur(self, x: float, t: float) -> float:
        """Facteur gaussien longitudinal à la distance parcourue d = u·t."""
        distance = self.source.u * t
        sigma_x = sigma_y(distance, self.source.classe)
        return float(
            np.exp(-((x - self.source.x0 - distance) ** 2) / (2.0 * sigma_x**2))
            / (np.sqrt(2.0 * np.pi) * float(sigma_x))
        )


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
        PassagesPuff(source=self.source, arcs=self.arcs).exiger_points_aux_arcs(points)
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
    le facteur longitudinal et les écarts de masse (note 35 : les deux
    routes sont mesurées séparément, sans facteur historique).

    Attributs :
        source : source impulsionnelle résolue par le schéma FTCS en temps.
        arcs : distances sous le vent des arcs de passage (m).
        parametres : paramètres numériques de la grille transverse/verticale.
        modele : modèle de diffusion (Briggs par défaut).
        structure : structure longitudinale injectable, analytique par défaut.
    """

    def __init__(
        self,
        source: SourceImpulsionnelle,
        arcs: tuple[float, ...],
        parametres: ParametresEdp = PARAMETRES_EDP_DEFAUT,
        modele: ModeleDiffusion = DIFFUSION_BRIGGS,
        structure: StructureLongitudinale | None = None,
    ) -> None:
        """Injecte les considérations du solveur, plus la structure dirigée."""
        self.source = source
        self.arcs = arcs
        self.parametres = parametres
        self.modele = modele
        self.structure: StructureLongitudinale = (
            structure if structure is not None else FacteurLongitudinalAnalytique(source=source)
        )

    def mesurer(self, points: tuple[PointMesure, ...]) -> MesureTransitoire:
        """Résout, échantillonne et pèse la route EDP ; coût mesuré ensemble."""
        PassagesPuff(source=self.source, arcs=self.arcs).exiger_points_aux_arcs(points)
        debut = time.perf_counter()
        solution = SolveurTransitoire(
            self.source, self.arcs, self.parametres, self.modele
        ).resoudre()
        grille = GrilleEdp(abscisses_y=solution.abscisses_y, abscisses_z=solution.abscisses_z)
        marginale = MarginaleFermee(source=self.source, grille=grille)
        par_instant = {instant.t: instant for instant in solution.instants}
        valeurs: list[float] = []
        for point in points:
            instant = par_instant[point.x / self.source.u]
            valeurs.append(self._dirigee(instant, grille, point))
        ecarts_masse: list[float] = []
        for instant in solution.instants:
            masse_edp = marginale.masse(instant.champ)
            masse_fermee = marginale.masse(marginale.champ(instant.t))
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
        t = point.x / self.source.u
        echantillon = EchantillonneurBilineaire(instant.champ, grille).concentration(
            point.y, point.z
        )
        return echantillon * self.structure.facteur(point.x, t)
