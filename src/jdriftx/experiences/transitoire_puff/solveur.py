"""Passages du puff et schéma FTCS marché en temps de la marginale."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from jdriftx.benchmarks.cas import PointMesure
from jdriftx.experiences.evaluation_puff import SourceImpulsionnelle
from jdriftx.experiences.reference_independante import (
    DIFFUSION_BRIGGS,
    PARAMETRES_EDP_DEFAUT,
    CoefficientsDiffusion,
    GrilleEdp,
    ModeleDiffusion,
    ParametresEdp,
)
from jdriftx.experiences.transitoire_puff.marginale import MarginaleFermee
from jdriftx.similitude import sigma_y, sigma_z


@dataclass(frozen=True)
class PassagesPuff:
    """Arcs de passage du puff et leurs instants dirigés (vent uniforme).

    Porte la géométrie de l'expérience : les arcs sous le vent et les
    instants dirigés t = arc/u qui en découlent. Les points de mesure
    doivent se trouver aux arcs ; les instants de passage doivent être
    des multiples entiers du pas de temps depuis l'entrée.

    Attributs :
        source : source impulsionnelle évaluée (vent u).
        arcs : distances sous le vent des arcs de passage (m).
    """

    source: SourceImpulsionnelle
    arcs: tuple[float, ...]

    @property
    def t_entree(self) -> float:
        """Instant dirigé du premier arc : condition d'entrée (s)."""
        return float(self.arcs[0]) / self.source.u

    def exiger_points_aux_arcs(self, points: tuple[PointMesure, ...]) -> None:
        """Exige des points situés aux arcs de passage, sinon ValueError."""
        for point in points:
            if point.x not in self.arcs:
                msg = "Le point doit se trouver à un arc de passage."
                raise ValueError(msg)

    def exiger_multiples_du_pas(self, pas_temps: float) -> None:
        """Exige des passages multiples entiers du pas depuis l'entrée."""
        for arc in self.arcs[1:]:
            ecart_pas = (float(arc) / self.source.u - self.t_entree) / pas_temps
            if abs(ecart_pas - round(ecart_pas)) > 1e-9:
                msg = (
                    "Les instants de passage doivent être des multiples entiers "
                    "du pas de temps depuis l'entrée."
                )
                raise ValueError(msg)


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


class SolveurTransitoire:
    """Schéma explicite FTCS marché en temps, instantanés aux passages.

    Le solveur porte les seules considérations numériques : pas de temps
    stable (celui de l'étape 5 divisé par la vitesse — la condition de
    Fourier est la même), condition au sol de type miroir (Neumann),
    Dirichlet nul aux bords latéraux et au sommet de fenêtre, instantanés
    prélevés aux instants de passage. La physique de diffusion vient du
    modèle injecté (ModeleDiffusion), la géométrie de la grille (GrilleEdp)
    et la condition d'entrée de la marginale fermée (MarginaleFermee) : il
    étend le solveur en longitude de l'étape 5 (reference_independante)
    au cas transitoire du puff.

    Attributs :
        passages : arcs de passage et instants dirigés (source incluse).
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
        self.passages = PassagesPuff(source=source, arcs=arcs)
        self.parametres = parametres
        self.modele = modele

    def resoudre(self) -> SolutionTransitoire:
        """Résout de l'entrée au dernier passage : modèle, fenêtre, pas, arcs.

        L'ordre de validation est celui de l'étape 5 : coefficients (forme
        INVERSE rejetée), couverture de fenêtre, pas de temps stable,
        divisibilité des passages depuis l'entrée, puis marche FTCS.
        """
        source = self.passages.source
        u = source.u
        t_entree = self.passages.t_entree
        x_entree = float(self.passages.arcs[0])
        x_fin = float(self.passages.arcs[-1])
        coefficients = self.modele.coefficients(source.classe, x_fin)
        self._verifier_fenetre(x_fin)
        grille = GrilleEdp.depuis_parametres(self.parametres)
        pas_temps = coefficients.pas_longitudinal(x_entree, x_fin, self.parametres) / u
        self.passages.exiger_multiples_du_pas(pas_temps)
        return self._marcher(grille, coefficients, t_entree, pas_temps)

    def _verifier_fenetre(self, x_fin: float) -> None:
        """Exige la couverture de quatre écarts-types au dernier passage."""
        classe = self.passages.source.classe
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
        source = self.passages.source
        arcs = self.passages.arcs
        u = source.u
        pas_y = self.parametres.pas_transverse_y
        pas_z = self.parametres.pas_transverse_z
        champ = MarginaleFermee(source=source, grille=grille).champ(t_entree)
        champ[0, :] = 0.0
        champ[-1, :] = 0.0
        champ[:, -1] = 0.0

        cibles = {
            round((float(arc) / u - t_entree) / pas_temps): float(arc) / u for arc in arcs[1:]
        }
        instants: list[InstantPuff] = [InstantPuff(t=t_entree, champ=champ.copy())]
        total = round((float(arcs[-1]) / u - t_entree) / pas_temps)
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
