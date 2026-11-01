"""Oracle analytique isolé du problème de navigation gaussien GZ-1.

Problème idéal : noyau fondamental isotrope 3D à diffusivité constante,
vent uniforme et commande isotrope bornée par la vitesse d'expansion du
seuil gaussien. Ce module ne réutilise pas les lois de Briggs de
jdriftx.similitude.concentration_puff et ne constitue pas un modèle
atmosphérique opérationnel.

Unités SI : positions m, temps s, masse kg, concentration kg m⁻³,
diffusivité m² s⁻¹ et vitesse m s⁻¹. La navigation est limitée à
0 < t <= t_etoile.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, pi, sqrt
from numbers import Real

import numpy as np
from numpy.typing import NDArray

__all__ = ["ModeleGZ1"]


def _scalaire_positif(valeur: float, nom: str) -> float:
    """Valide un scalaire réel, fini et strictement positif."""
    if isinstance(valeur, (bool, np.bool_)) or not isinstance(valeur, Real):
        raise ValueError(f"{nom} doit être un réel strictement positif.")
    try:
        resultat = float(valeur)
    except (OverflowError, TypeError, ValueError) as err:
        raise ValueError(f"{nom} doit être représentable en float64.") from err
    if not isfinite(resultat) or resultat <= 0.0:
        raise ValueError(f"{nom} doit être fini et strictement positif.")
    return resultat


def _vecteur3(
    valeur: tuple[float, float, float] | NDArray[np.float64], nom: str
) -> tuple[float, float, float]:
    """Convertit une coordonnée 3D en tuple réel fini et immuable."""
    brut = np.asarray(valeur)
    elements = np.asarray(valeur, dtype=object)
    contient_non_reel = any(
        isinstance(element, (bool, np.bool_, complex, np.complexfloating))
        for element in elements.flat
    )
    if (
        brut.shape != (3,)
        or brut.dtype.kind not in "iuf"
        or contient_non_reel
        or not np.all(np.isfinite(brut))
    ):
        raise ValueError(f"{nom} doit être un vecteur réel fini de dimension 3.")
    return (float(brut[0]), float(brut[1]), float(brut[2]))


@dataclass(frozen=True)
class ModeleGZ1:
    """Paramètres et fonctions fermées du problème gaussien GZ-1.

    Args:
        masse: masse impulsionnelle M (kg), strictement positive.
        seuil: concentration seuil C₀ (kg m⁻³), strictement positive.
        diffusivite: diffusivité isotrope K (m² s⁻¹), strictement positive.
        vent: vecteur uniforme u (m s⁻¹).
        origine: position initiale x₀ (m).

    Le modèle exclut dépôt, réaction, frontières et coefficients variables.
    """

    masse: float
    seuil: float
    diffusivite: float
    vent: tuple[float, float, float] = (0.0, 0.0, 0.0)
    origine: tuple[float, float, float] = (0.0, 0.0, 0.0)

    def __post_init__(self) -> None:
        """Valide les paramètres et fige les vecteurs."""
        object.__setattr__(self, "masse", _scalaire_positif(self.masse, "La masse"))
        object.__setattr__(self, "seuil", _scalaire_positif(self.seuil, "Le seuil"))
        object.__setattr__(
            self, "diffusivite", _scalaire_positif(self.diffusivite, "La diffusivité")
        )
        object.__setattr__(self, "vent", _vecteur3(self.vent, "Le vent"))
        object.__setattr__(self, "origine", _vecteur3(self.origine, "L'origine"))

    @property
    def t_etoile(self) -> float:
        """Temps du rayon maximal t* (s)."""
        return float(
            (self.masse / (self.seuil * exp(1.5))) ** (2.0 / 3.0)
            / (4.0 * pi * self.diffusivite)
        )

    @property
    def t_extinction(self) -> float:
        """Temps d'extinction du niveau C=C₀, e·t* (s)."""
        return exp(1.0) * self.t_etoile

    @property
    def rayon_maximal(self) -> float:
        """Rayon maximal R(t*) (m)."""
        return sqrt(6.0 * self.diffusivite * self.t_etoile)

    @property
    def _vent_array(self) -> NDArray[np.float64]:
        """Vent sous forme de tableau NumPy."""
        return np.asarray(self.vent, dtype=float)

    @property
    def _origine_array(self) -> NDArray[np.float64]:
        """Origine sous forme de tableau NumPy."""
        return np.asarray(self.origine, dtype=float)

    def rayon(self, temps: float) -> float:
        """Rayon R(t) (m), pour 0 < t <= e·t*."""
        t = _scalaire_positif(temps, "Le temps")
        if t > self.t_extinction:
            raise ValueError("Le rayon réel du seuil n'existe plus après e·t*.")
        facteur = 1.0 + log(self.t_etoile / t)
        carre = 6.0 * self.diffusivite * t * facteur
        return sqrt(max(0.0, carre))

    def vitesse_expansion(self, temps: float) -> float:
        """Dérivée R'(t) (m s⁻¹) sur 0 < t <= t*.

        La singularité en t→0⁺ est intégrable ; t=0 n'est jamais évalué.
        """
        t = _scalaire_positif(temps, "Le temps")
        if t > self.t_etoile:
            raise ValueError("La borne GZ-1 n'est définie que pendant l'expansion.")
        rayon = self.rayon(t)
        if rayon == 0.0:
            return 0.0
        return 3.0 * self.diffusivite * log(self.t_etoile / t) / rayon

    def concentration(
        self, position: tuple[float, float, float] | NDArray[np.float64], temps: float
    ) -> float:
        """Noyau fondamental 3D C(x,t) (kg m⁻³), pour t>0."""
        t = _scalaire_positif(temps, "Le temps")
        x = np.asarray(_vecteur3(position, "La position"), dtype=float)
        centre = self._origine_array + self._vent_array * t
        ecart = x - centre
        exposant = -float(ecart @ ecart) / (4.0 * self.diffusivite * t)
        amplitude = self.masse / (4.0 * pi * self.diffusivite * t) ** 1.5
        resultat = amplitude * exp(exposant)
        if not isfinite(resultat):
            raise ValueError("La concentration n'est pas représentable en float64.")
        return float(resultat)

    def ensemble_atteignable(
        self, position: tuple[float, float, float] | NDArray[np.float64], temps: float
    ) -> bool:
        """Teste x ∈ B̄(x₀+ut,R(t)), pour 0<t<=t*."""
        t = _scalaire_positif(temps, "Le temps")
        if t > self.t_etoile:
            raise ValueError("L'ensemble atteignable GZ-1 est limité à t <= t*.")
        x = np.asarray(_vecteur3(position, "La position"), dtype=float)
        centre = self._origine_array + self._vent_array * t
        return bool(np.linalg.norm(x - centre) <= self.rayon(t))

    def fonction_contact(
        self, cible: tuple[float, float, float] | NDArray[np.float64], temps: float
    ) -> float:
        """g_B(t)=|x_B-x_0-u*t|^2-R(t)^2 (m²), pour 0<t<=t*."""
        t = _scalaire_positif(temps, "Le temps")
        if t > self.t_etoile:
            raise ValueError("Le contact GZ-1 est recherché sur 0 < t <= t*.")
        b = np.asarray(_vecteur3(cible, "La cible"), dtype=float)
        relatif = b - self._origine_array - self._vent_array * t
        return float(relatif @ relatif - self.rayon(t) ** 2)

    def valeur_hj(
        self, position: tuple[float, float, float] | NDArray[np.float64], temps: float
    ) -> float:
        """Valeur Hopf-Lax max(|x-x_0-u*t|-R(t),0), en mètres."""
        t = _scalaire_positif(temps, "Le temps")
        if t > self.t_etoile:
            raise ValueError("La valeur HJ GZ-1 est définie ici pour t <= t*.")
        x = np.asarray(_vecteur3(position, "La position"), dtype=float)
        centre = self._origine_array + self._vent_array * t
        return max(float(np.linalg.norm(x - centre)) - self.rayon(t), 0.0)

    def commande_radiale(
        self,
        deplacement: tuple[float, float, float] | NDArray[np.float64],
        temps_final: float,
        temps: float,
    ) -> tuple[float, float, float]:
        """Commande s(τ)=z R'(τ)/R(T), avec |z|<=R(T).

        temps est le temps courant τ ; temps_final est l'instant T visé.
        """
        final = _scalaire_positif(temps_final, "Le temps final")
        courant = _scalaire_positif(temps, "Le temps courant")
        if final > self.t_etoile or courant > final:
            raise ValueError("Il faut 0 < temps <= temps_final <= t*.")
        z = np.asarray(_vecteur3(deplacement, "Le déplacement"), dtype=float)
        rayon_final = self.rayon(final)
        norme = float(np.linalg.norm(z))
        if norme > rayon_final:
            raise ValueError("Le déplacement demandé est hors de la boule atteignable.")
        if norme == 0.0:
            return (0.0, 0.0, 0.0)
        commande = z / rayon_final * self.vitesse_expansion(courant)
        return (float(commande[0]), float(commande[1]), float(commande[2]))

    def jauge_randers(
        self, deplacement: tuple[float, float, float] | NDArray[np.float64], temps: float
    ) -> float:
        """Norme F(v) en secondes pour un déplacement tangent v (m).

        Définie uniquement si R'(t)>||u||. Cette jauge instantanée n'est
        pas une formule de portée cumulée pour le système GZ-1.
        """
        t = _scalaire_positif(temps, "Le temps")
        if t >= self.t_etoile:
            raise ValueError("Randers est défini uniquement pour t < t*.")
        c = self.vitesse_expansion(t)
        u = self._vent_array
        norme_vent = float(np.linalg.norm(u))
        if c <= norme_vent:
            raise ValueError("Randers régulier exige strictement R'(t) > ||u||.")
        v = np.asarray(_vecteur3(deplacement, "Le déplacement"), dtype=float)
        a = c * c - norme_vent * norme_vent
        produit = float(u @ v)
        return (sqrt(produit * produit + a * float(v @ v)) - produit) / a

    def premier_contact(
        self, cible: tuple[float, float, float] | NDArray[np.float64]
    ) -> float | None:
        """Premier zéro de g_B sur (0,t*], ou None si la cible est hors portée.

        Pour un vent constant, g_B''(t)=2|u|²+6K/t>0 : g_B est strictement
        convexe. Son minimum unique est trouvé par dichotomie sur g'_B,
        puis le premier zéro par dichotomie sur l'intervalle croissant.
        Cette méthode détecte aussi le contact tangent sans balayage discret.
        Un résidu positif inférieur à 1e-12 de l'échelle géométrique est
        classé comme tangence à la précision float64 ; un minimum négatif,
        même très proche de zéro, conserve la dichotomie du premier zéro.
        """
        b = np.asarray(_vecteur3(cible, "La cible"), dtype=float)
        delta = b - self._origine_array
        u = self._vent_array
        if float(np.linalg.norm(delta)) == 0.0:
            return 0.0
        t_max = self.t_etoile

        def derivee(t: float) -> float:
            relatif = delta - u * t
            return -2.0 * float(u @ relatif) - 6.0 * self.diffusivite * log(t_max / t)

        if derivee(t_max) <= 0.0:
            t_min = t_max
        else:
            bas, haut = 0.0, t_max
            for _ in range(100):
                milieu = 0.5 * (bas + haut)
                if milieu == 0.0 or derivee(milieu) < 0.0:
                    bas = milieu
                else:
                    haut = milieu
            t_min = 0.5 * (bas + haut)

        g_min = self.fonction_contact(b, t_min)
        tolerance = 1e-12 * max(1.0, float(delta @ delta), self.rayon_maximal**2)
        if g_min > tolerance:
            return None
        if g_min >= 0.0:
            return t_min

        bas, haut = 0.0, t_min
        for _ in range(100):
            milieu = 0.5 * (bas + haut)
            if milieu == 0.0 or self.fonction_contact(b, milieu) > 0.0:
                bas = milieu
            else:
                haut = milieu
        return 0.5 * (bas + haut)
