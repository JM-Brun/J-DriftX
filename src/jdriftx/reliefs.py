"""Implémentations de relief et lecture de modèles numériques de terrain."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import ArrayLike, NDArray

from jdriftx.terrain import TerrainKind, terrain_surface


def _verifie_coordonnees(x_arr: NDArray[np.floating], y_arr: NDArray[np.floating]) -> None:
    """Valide la forme et la finitude des coordonnées spatiales."""
    if x_arr.shape != y_arr.shape:
        msg = "x et y doivent avoir des formes identiques."
        raise ValueError(msg)
    if not np.all(np.isfinite(x_arr)) or not np.all(np.isfinite(y_arr)):
        msg = "Les coordonnees doivent etre finies."
        raise ValueError(msg)


@dataclass(frozen=True)
class ReliefPlat:
    """Terrain plat d altitude nulle, cas de reference des solutions gaussiennes."""

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Retourne une altitude nulle (m) aux points (x, y)."""
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        _verifie_coordonnees(x_arr, y_arr)
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

    def __post_init__(self) -> None:
        """Valide les paramètres avant qu'un relief soit utilisable."""
        parametres = (self.height, self.width, self.center_x, self.center_y)
        if not all(np.isfinite(value) for value in parametres):
            msg = "Les paramètres du relief doivent être finis."
            raise ValueError(msg)
        if self.width <= 0.0:
            msg = "La largeur du relief doit être strictement positive."
            raise ValueError(msg)
        if self.kind not in ("flat", "hill", "valley", "ridge"):
            msg = f"Type de relief inconnu : {self.kind!r}."
            raise ValueError(msg)

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Evalue l altitude du relief (m) aux points (x, y) : delegation pure."""
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        _verifie_coordonnees(x_arr, y_arr)
        return terrain_surface(
            x_arr,
            y_arr,
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
        """Valide et fige la grille et sa geometrie."""
        altitudes = np.array(self.altitudes, dtype=float, copy=True)
        if altitudes.ndim != 2 or altitudes.size == 0:
            msg = "La grille d altitudes doit etre bidimensionnelle non vide."
            raise ValueError(msg)
        if not np.all(np.isfinite(altitudes)):
            msg = "Les altitudes doivent etre finies."
            raise ValueError(msg)
        if not np.isfinite(self.pas) or self.pas <= 0.0:
            msg = "Le pas de grille doit etre strictement positif."
            raise ValueError(msg)
        if not np.isfinite(self.x0) or not np.isfinite(self.y0):
            msg = "L origine de la grille doit etre finie."
            raise ValueError(msg)
        if self.sans_donnee is not None and not np.isfinite(self.sans_donnee):
            msg = "La valeur sans donnee doit etre finie."
            raise ValueError(msg)
        # A read-only flag on an owning ndarray can be re-enabled by its caller.
        # A bytes-backed array makes the validated storage immutable at NumPy level.
        altitudes_immutable = np.frombuffer(altitudes.tobytes(), dtype=altitudes.dtype).reshape(
            altitudes.shape
        )
        object.__setattr__(self, "altitudes", altitudes_immutable)

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
                sans donnee a poids non nul dans l interpolation.
        """
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        _verifie_coordonnees(x_arr, y_arr)
        if not np.all(np.isfinite(x_arr)) or not np.all(np.isfinite(y_arr)):
            msg = "Les coordonnees doivent etre finies."
            raise ValueError(msg)
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
        tx = colonne - i0
        ty = ligne - j0
        p00 = (1.0 - tx) * (1.0 - ty)
        p10 = tx * (1.0 - ty)
        p01 = (1.0 - tx) * ty
        p11 = tx * ty
        coins = ((z00, p00), (z10, p10), (z01, p01), (z11, p11))
        if self.sans_donnee is not None and any(
            np.any((coin == self.sans_donnee) & (poids > 0.0)) for coin, poids in coins
        ):
            msg = "Interpolation sur une cellule sans donnee."
            raise ValueError(msg)
        z = z00 * p00 + z10 * p10 + z01 * p01 + z11 * p11
        return np.asarray(z, dtype=float)

__all__ = [
    "ReliefMntAscii",
    "ReliefPlat",
    "ReliefSynthetique",
]
