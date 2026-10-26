"""Classes de stabilite atmospherique de Pasquill et lois de Briggs associees.

Ce module definit le vocabulaire des six classes de stabilite (A a F) comme des
objets a part entiere : chaque classe porte son regime, ses conditions
meteorologiques typiques d'usage et les coefficients des lois de Briggs qui
gouvernent la croissance des ecarts-types de dispersion sigma_y et sigma_z
avec la distance sous le vent.

Les caracteristiques documentees decrivent la classification d'origine
(Pasquill, 1961 ; courbes de Gifford ; formules de Briggs, 1973, pour un site
rural) : ce sont des reperes d'usage, pas un diagnostic automatique de la
stabilite a partir de mesures. Aucun module ne determine la classe a partir
de donnees meteorologiques.

Les lois sont evaluees par `jdriftx.similitude`, qui lit ses coefficients
ici : source unique de verite.

References : chapitre "Reduced-Order Modelling of Dispersion" (Brun &
Mohammadi, 2008) ; formules de Briggs reprises par Martin (1976).
"""

from __future__ import annotations

from enum import StrEnum


class FormeSigmaZ(StrEnum):
    """Forme de la loi de croissance de l'ecart-type vertical sigma_z(x).

    Trois familles de lois de Briggs (site rural) : lineaire pour les classes
    instables A et B, en racine carree pour C et D, inverse pour les classes
    stables E et F. Les lois completes sont evaluees dans
    `jdriftx.similitude.sigma_z`.
    """

    LINEAIRE = "lin"
    RACINE = "sqrt"
    INVERSE = "inv"


class ClasseStabilite(StrEnum):
    """Classe de stabilite atmospherique de Pasquill, de A (tres instable) a F (stable).

    Chaque membre porte les caracteristiques documentees de sa classe :
    regime, conditions typiques d'usage (classification d'origine, Pasquill
    1961) et coefficients des lois de Briggs rurales pour sigma_y et sigma_z.
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

    @property
    def regime(self) -> str:
        """Regime de stabilite, de tres instable (A) a stable (F)."""
        if self is ClasseStabilite.A:
            return "tres instable"
        if self is ClasseStabilite.B:
            return "moderement instable"
        if self is ClasseStabilite.C:
            return "faiblement instable"
        if self is ClasseStabilite.D:
            return "neutre"
        if self is ClasseStabilite.E:
            return "faiblement stable"
        return "stable"

    @property
    def conditions_typiques(self) -> str:
        """Conditions meteorologiques typiques d'usage de la classe (Pasquill, 1961).

        Ce sont des reperes issus de la classification d'origine, pas un
        diagnostic automatique a partir de mesures.
        """
        if self is ClasseStabilite.A:
            return (
                "jour, insolation forte et vent faible (moins de 2 m/s) ; convection vigoureuse"
            )
        if self is ClasseStabilite.B:
            return "jour, insolation moderee ou vent de 2 a 3 m/s"
        if self is ClasseStabilite.C:
            return "jour nuageux ou insolation faible, vent de 3 a 5 m/s"
        if self is ClasseStabilite.D:
            return "couvert dense jour et nuit, ou vent de plus de 6 m/s ; classe de reference"
        if self is ClasseStabilite.E:
            return "nuit, vent de 3 a 5 m/s ou ciel partiellement couvert"
        return "nuit claire et vent faible (moins de 3 m/s) ; inversion nocturne"

    @property
    def coeff_sigma_y(self) -> tuple[float, float]:
        """Coefficients (a, d) de la loi de Briggs rurale pour sigma_y.

        La loi est sigma_y(x) = a * x / sqrt(1 + d * x), avec x la distance
        sous le vent en metres.
        """
        if self is ClasseStabilite.A:
            return (0.22, 0.0001)
        if self is ClasseStabilite.B:
            return (0.16, 0.0001)
        if self is ClasseStabilite.C:
            return (0.11, 0.0001)
        if self is ClasseStabilite.D:
            return (0.08, 0.0001)
        if self is ClasseStabilite.E:
            return (0.06, 0.0001)
        return (0.04, 0.0001)

    @property
    def coeff_sigma_z(self) -> tuple[FormeSigmaZ, float, float]:
        """Forme et coefficients (b, d) de la loi de Briggs rurale pour sigma_z.

        Les formes sont documentees dans `FormeSigmaZ` ; les lois completes
        sont evaluees dans `jdriftx.similitude.sigma_z`.
        """
        if self is ClasseStabilite.A:
            return (FormeSigmaZ.LINEAIRE, 0.20, 0.0)
        if self is ClasseStabilite.B:
            return (FormeSigmaZ.LINEAIRE, 0.12, 0.0)
        if self is ClasseStabilite.C:
            return (FormeSigmaZ.RACINE, 0.08, 0.0002)
        if self is ClasseStabilite.D:
            return (FormeSigmaZ.RACINE, 0.06, 0.0015)
        if self is ClasseStabilite.E:
            return (FormeSigmaZ.INVERSE, 0.03, 0.0003)
        return (FormeSigmaZ.INVERSE, 0.016, 0.0003)
