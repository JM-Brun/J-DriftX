"""Contrats d interface entre les elements du modele (docs/42).

Le package separe deja des valeurs bien identifiables : la source du
panache (source.SourcePanache), le champ plan a fonction de courant
(champ_analytique), les terrains synthetiques (terrain) et les solutions
de similitude (similitude). Le risque documente en docs/41 est
l accouplement : changer un element (relief, vent 2D ou 3D, modele de
concentration) oblige a reecrire chaque site d appel. Ce module definit
les frontieres stables : des protocoles PEP 544 (typage structurel) et
des adaptateurs qui branchent les elements existants derriere un contrat
commun. Un element peut alors changer sans impact sur les autres.

Limites : le relief du contrat est une geometrie (altitude du sol), pas
un effet sur l ecoulement ; les puits (depot au sol) ne sont pas
modelises avant la porte G1 ; le vent du contrat est stationnaire.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Self, runtime_checkable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from jdriftx.champ_analytique import ChampPlan
from jdriftx.similitude import concentration_panache
from jdriftx.source import SourcePanache
from jdriftx.terrain import TerrainKind, terrain_surface

__all__ = [
    "ModeleConcentration",
    "PanacheGaussien",
    "Relief",
    "ReliefMntAscii",
    "ReliefPlat",
    "ReliefSynthetique",
    "SuperpositionPanaches",
    "Vent",
    "VentDeChampPlan",
    "VentProfilPuissance",
    "VentUniforme",
]


def _verifie_formes(x_arr: NDArray[np.floating], y_arr: NDArray[np.floating]) -> None:
    """Rejette les grilles x et y de formes differentes."""
    if x_arr.shape != y_arr.shape:
        msg = "x et y doivent avoir des formes identiques."
        raise ValueError(msg)


@runtime_checkable
class Relief(Protocol):
    """Contrat d un relief : altitude du sol evaluee sur des grilles.

    Le contrat est vectorise (grilles de points, comme le rendu) : tout
    objet fournissant altitude avec cette signature satisfait le
    protocole, sans heritage.
    """

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Altitude du sol (m) aux points (x, y), formes identiques."""
        ...


@runtime_checkable
class Vent(Protocol):
    """Contrat d un champ de vent stationnaire, plan ou tridimensionnel.

    Le contrat est ponctuel (un point a la fois, comme l integration des
    trajectoires) : un champ plan renvoie w = 0, un champ 3D renseigne la
    composante verticale. Changer de modele de vent ne change pas les
    appelants.
    """

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Composantes (u, v, w) du vent (m s^-1) au point (x, y, z) (m)."""
        ...


@runtime_checkable
class ModeleConcentration(Protocol):
    """Contrat d un modele de concentration evaluable sur une grille."""

    def concentration(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> np.ndarray:
        """Concentrations (kg m^-3) aux points (x, y, z)."""
        ...


@dataclass(frozen=True)
class ReliefPlat:
    """Terrain plat d altitude nulle, cas de reference des solutions gaussiennes."""

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Retourne une altitude nulle (m) aux points (x, y)."""
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        _verifie_formes(x_arr, y_arr)
        return np.zeros_like(x_arr)


@dataclass(frozen=True)
class ReliefSynthetique:
    """Relief synthetique d enseignement, delegue au module terrain.

    Attributes:
        kind: forme du relief (flat, hill, valley, ridge).
        height: hauteur du relief, sans unite (module d enseignement).
        width: demi-largeur caracteristique, strictement positive.
        center_x: abscisse du centre du relief.
        center_y: ordonnee du centre du relief.
    """

    kind: TerrainKind
    height: float = 1.0
    width: float = 1.5
    center_x: float = 0.0
    center_y: float = 0.0

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Evalue l altitude du relief (m) aux points (x, y) : delegation pure."""
        return terrain_surface(
            x,
            y,
            self.kind,
            height=self.height,
            width=self.width,
            center_x=self.center_x,
            center_y=self.center_y,
        )


@dataclass(frozen=True)
class ReliefMntAscii:
    """Relief lu d un MNT au format ESRI ASCII Grid (.asc), standard d echange.

    Le format .asc (QGIS, GDAL, exports altimetriques) decrit une grille
    reguliere : entetes ncols, nrows, xllcorner, yllcorner, cellsize et
    nodata_value optionnel, puis les altitudes ligne par ligne depuis la
    ligne la plus au nord. Les valeurs decrivent des cellules ; x0 et y0
    designent le centre de la cellule sud-ouest.

    Attributes:
        altitudes: grille (nrows, ncols), finie, ligne 0 au nord.
        x0: abscisse du centre de la cellule sud-ouest (m).
        y0: ordonnee du centre de la cellule sud-ouest (m).
        pas: taille de cellule (m), strictement positive.
        sans_donnee: valeur marquant les cellules sans donnee, ou None.
    """

    altitudes: NDArray[np.float64]
    x0: float
    y0: float
    pas: float
    sans_donnee: float | None = None

    def __post_init__(self) -> None:
        """Valide la grille et la geometrie, sinon leve une ValueError."""
        if self.altitudes.ndim != 2 or self.altitudes.size == 0:
            msg = "La grille d altitudes doit etre bidimensionnelle non vide."
            raise ValueError(msg)
        if not np.all(np.isfinite(self.altitudes)):
            msg = "Les altitudes doivent etre finies."
            raise ValueError(msg)
        if not np.isfinite(self.pas) or self.pas <= 0.0:
            msg = "Le pas de grille doit etre strictement positif."
            raise ValueError(msg)
        if not np.isfinite(self.x0) or not np.isfinite(self.y0):
            msg = "L origine de la grille doit etre finie."
            raise ValueError(msg)

    @classmethod
    def depuis_texte(cls, texte: str) -> Self:
        """Construit le relief depuis le texte d un fichier .asc standard."""
        jetons = texte.split()
        attendus = {"ncols", "nrows", "xllcorner", "yllcorner", "cellsize"}
        entete: dict[str, float] = {}
        position = 0
        while position + 1 < len(jetons):
            cle = jetons[position].lower()
            if cle not in attendus and cle != "nodata_value":
                break
            try:
                entete[cle] = float(jetons[position + 1])
            except ValueError as err:
                msg = f"Valeur invalide pour {cle} : {jetons[position + 1]}."
                raise ValueError(msg) from err
            position += 2
        manquantes = attendus - set(entete)
        if manquantes:
            msg = f"Entete .asc incomplete : {', '.join(sorted(manquantes))}."
            raise ValueError(msg)
        ncols = entete["ncols"]
        nrows = entete["nrows"]
        if ncols != int(ncols) or nrows != int(nrows) or ncols < 1 or nrows < 1:
            msg = "ncols et nrows doivent etre des entiers au moins 1."
            raise ValueError(msg)
        pas = entete["cellsize"]
        if pas <= 0.0:
            msg = "cellsize doit etre strictement positif."
            raise ValueError(msg)
        valeurs = np.asarray(jetons[position:], dtype=float)
        if valeurs.size != int(ncols) * int(nrows):
            msg = "La grille ne contient pas ncols x nrows valeurs."
            raise ValueError(msg)
        altitudes = valeurs.reshape(int(nrows), int(ncols))
        return cls(
            altitudes=altitudes,
            x0=entete["xllcorner"] + 0.5 * pas,
            y0=entete["yllcorner"] + 0.5 * pas,
            pas=pas,
            sans_donnee=entete.get("nodata_value"),
        )

    @classmethod
    def depuis_fichier(cls, chemin: Path) -> Self:
        """Construit le relief depuis un fichier .asc du disque."""
        return cls.depuis_texte(chemin.read_text(encoding="utf-8"))

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Interpole lineairement l altitude (m) aux points (x, y).

        Raises:
            ValueError: formes differentes, point hors emprise ou cellule
                sans donnee touchee par l interpolation.
        """
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        _verifie_formes(x_arr, y_arr)
        nrows, ncols = self.altitudes.shape
        colonne = (x_arr - self.x0) / self.pas
        ligne = (y_arr - self.y0) / self.pas
        if np.any(colonne < 0.0) or np.any(colonne > ncols - 1):
            msg = "Point hors de l emprise horizontale du MNT."
            raise ValueError(msg)
        if np.any(ligne < 0.0) or np.any(ligne > nrows - 1):
            msg = "Point hors de l emprise verticale du MNT."
            raise ValueError(msg)
        colonne = np.clip(colonne, 0.0, ncols - 1)
        ligne = np.clip(ligne, 0.0, nrows - 1)
        i0 = np.floor(colonne).astype(int)
        j0 = np.floor(ligne).astype(int)
        i1 = np.minimum(i0 + 1, ncols - 1)
        j1 = np.minimum(j0 + 1, nrows - 1)
        r0 = nrows - 1 - j0
        r1 = nrows - 1 - j1
        z00 = self.altitudes[r0, i0]
        z10 = self.altitudes[r0, i1]
        z01 = self.altitudes[r1, i0]
        z11 = self.altitudes[r1, i1]
        if self.sans_donnee is not None:
            proches = (z00, z10, z01, z11)
            if any(np.any(coin == self.sans_donnee) for coin in proches):
                msg = "Interpolation sur une cellule sans donnee."
                raise ValueError(msg)
        tx = colonne - i0
        ty = ligne - j0
        z = (
            z00 * (1.0 - tx) * (1.0 - ty)
            + z10 * tx * (1.0 - ty)
            + z01 * (1.0 - tx) * ty
            + z11 * tx * ty
        )
        return np.asarray(z, dtype=float)


@dataclass(frozen=True)
class VentUniforme:
    """Vent plan uniforme : composantes constantes, w nul.

    Attributes:
        u: composante sous le vent (m s^-1), finie.
        v: composante laterale (m s^-1), finie.
    """

    u: float
    v: float

    def __post_init__(self) -> None:
        """Valide la finitude des composantes, sinon leve une ValueError."""
        if not np.isfinite(self.u) or not np.isfinite(self.v):
            msg = "Les composantes du vent doivent etre finies."
            raise ValueError(msg)

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Retourne le vent uniforme (u, v, 0) au point (x, y, z)."""
        return self.u, self.v, 0.0


@dataclass(frozen=True)
class VentDeChampPlan:
    """Adaptateur : un champ plan existant devient un vent du contrat.

    Tout objet satisfaisant le protocole ChampPlan (fonction_courant,
    vitesse) est adapte sans modification : la composante verticale est
    nulle. Les champs 2D et 3D s echangent derriere le meme contrat.

    Attributes:
        champ: champ plan stationnaire a adapter.
    """

    champ: ChampPlan

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Evalue le vent (u, v, 0) du champ plan au point (x, y)."""
        u, v = self.champ.vitesse(x, y)
        return u, v, 0.0


@dataclass(frozen=True)
class VentProfilPuissance:
    """Vent unidirectionnel en loi de puissance, standard de couche de surface.

    u(z) = u_reference * (z / z_reference) ** exposant : profil de vent
    standard des modeles de dispersion pour la couche de surface. La
    composante verticale est nulle ; le profil est defini pour z
    strictement positif.

    Attributes:
        u_reference: vitesse (m s^-1) a la hauteur de reference, positive.
        z_reference: hauteur de reference (m), strictement positive.
        exposant: exposant de la loi de puissance, entre 0 et 1.
    """

    u_reference: float
    z_reference: float
    exposant: float

    def __post_init__(self) -> None:
        """Valide les invariants du profil, sinon leve une ValueError."""
        if not np.isfinite(self.u_reference) or self.u_reference <= 0.0:
            msg = "La vitesse de reference doit etre finie strictement positive."
            raise ValueError(msg)
        if not np.isfinite(self.z_reference) or self.z_reference <= 0.0:
            msg = "La hauteur de reference doit etre finie strictement positive."
            raise ValueError(msg)
        if not 0.0 <= self.exposant <= 1.0:
            msg = "L exposant de la loi de puissance doit etre entre 0 et 1."
            raise ValueError(msg)

    def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """Evalue le vent (u(z), 0, 0) au point (x, y, z)."""
        if z <= 0.0:
            msg = "Le profil de puissance est defini pour z strictement positif."
            raise ValueError(msg)
        u = self.u_reference * (z / self.z_reference) ** self.exposant
        return u, 0.0, 0.0


@dataclass(frozen=True)
class PanacheGaussien:
    """Panache gaussien compose : la source porte les parametres (docs/41).

    Attributes:
        source: valeur source du panache (debit, vent, classe, hauteur).
    """

    source: SourcePanache

    def concentration(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> np.ndarray:
        """Evalue les concentrations (kg m^-3) par delegation a la similitude."""
        return concentration_panache(
            x,
            y,
            z,
            debit=self.source.debit,
            u=self.source.u,
            classe=self.source.classe,
            hauteur=self.source.hauteur,
        )


@dataclass(frozen=True)
class SuperpositionPanaches:
    """Superposition lineaire (hypothese H8) de modeles de concentration.

    La concentration totale est la somme des concentrations : tout objet
    satisfaisant le contrat ModeleConcentration se combine, sans que les
    modeles se connaissent entre eux.

    Attributes:
        panaches: tuple non vide de modeles de concentration.
    """

    panaches: tuple[ModeleConcentration, ...]

    def __post_init__(self) -> None:
        """Valide l invariant : au moins un panache, sinon ValueError."""
        if not self.panaches:
            msg = "La superposition exige au moins un panache."
            raise ValueError(msg)

    def concentration(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> np.ndarray:
        """Somme les concentrations (kg m^-3) des panaches superposes."""
        total = self.panaches[0].concentration(x, y, z)
        for panache in self.panaches[1:]:
            total = total + panache.concentration(x, y, z)
        return total
