"""Marginale transverse fermée du puff sur la grille EDP.

La marginale Q(y, z, t) est l'intégrale longitudinale de la concentration
du puff (kg m⁻²) — « marginale » par analogie avec les lois marginales :
la concentration vue depuis la direction intégrée. La solution fermée du
package la donne en gaussienne produit,
évaluée à la distance parcourue d = u·t. Elle sert de condition d'entrée
au schéma transitoire (note 54) et de référence des écarts de masse sur
la même grille — jamais de la masse totale : le noyau du puff est pair en
z, la moitié de la masse du noyau fermé est formellement sous le sol et
la grille porte la demi-colonne miroir.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real

import numpy as np

from jdriftx.experiences.evaluation_puff import SourceImpulsionnelle
from jdriftx.experiences.reference_independante import EchantillonneurBilineaire, GrilleEdp
from jdriftx.similitude import sigma_y, sigma_z


@dataclass(frozen=True)
class MarginaleFermee:
    """Marginale transverse fermée du puff, liée à une source et une grille.

    Porte les deux lectures fermées du transverse : le champ Q(y, z) à un
    instant donné et la masse d'un champ sur la grille. C'est la condition
    d'entrée du schéma transitoire et la référence des écarts de masse.

    Attributs :
        source : source impulsionnelle évaluée (masse, vent, classe, x0).
        grille : grille EDP des nœuds transverses et verticaux.
    """

    source: SourceImpulsionnelle
    grille: GrilleEdp

    def champ(self, t: float) -> np.ndarray:
        """Champ de la marginale fermée sur la grille, à l'instant t (s).

        L'instant doit être un réel float64 fini strictement positif : à t=0,
        les écarts-types transverses sont nuls et la marginale n'est pas une
        fonction gaussienne régulière sur la grille.
        """
        if isinstance(t, (bool, np.bool_)) or not isinstance(t, Real):
            raise ValueError("t must be a finite real scalar (booleans excluded).")
        try:
            instant = float(t)
        except (OverflowError, TypeError, ValueError) as err:
            raise ValueError("t must be representable as finite float64.") from err
        if not np.isfinite(instant):
            raise ValueError("t must be finite.")
        if instant <= 0.0:
            raise ValueError("t must be strictly positive.")
        distance = self.source.u * instant
        if not np.isfinite(distance) or distance <= 0.0:
            raise ValueError("The puff travel distance u*t must be finite and strictly positive.")
        sy = sigma_y(distance, self.source.classe)
        sz = sigma_z(distance, self.source.classe)
        mailles_y, mailles_z = self.grille.mailles()
        champ = (
            self.source.masse
            / (2.0 * np.pi * sy * sz)
            * np.exp(-(mailles_y**2) / (2.0 * sy**2))
            * np.exp(-(mailles_z**2) / (2.0 * sz**2))
        )
        return np.asarray(champ, dtype=float)

    def masse(self, champ: np.ndarray) -> float:
        """Masse d'un champ de marginale sur la grille (trapèzes doubles)."""
        return EchantillonneurBilineaire(champ, self.grille).integrale()
