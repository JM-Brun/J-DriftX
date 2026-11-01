"""Implémentations de relief et lecture de modèles numériques de terrain."""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from pathlib import Path
from typing import Self

import numpy as np
from numpy.typing import ArrayLike, NDArray

from jdriftx.terrain import TerrainKind, terrain_surface


def _reel_fini(valeur: object, nom: str) -> float:
    """Valide un scalaire reel fini et representable en float."""
    if isinstance(valeur, bool) or not isinstance(valeur, Real):
        raise ValueError(f"{nom} doit etre un nombre reel (booleen exclu).")
    try:
        resultat = float(valeur)
    except (OverflowError, TypeError, ValueError) as err:
        raise ValueError(f"{nom} doit etre representable comme float fini.") from err
    if not np.isfinite(resultat):
        raise ValueError(f"{nom} doit etre fini.")
    return resultat


def _tableau_reel_fini(valeur: ArrayLike, nom: str) -> NDArray[np.float64]:
    """Convertit en float64 sans coercition textuelle ni booléens masqués par promotion."""
    try:
        brut = np.asarray(valeur)
        # NumPy peut promouvoir [0.0, True] en int64 et perdre la trace du booléen.
        # N'inspecter en objet que les entrées séquentielles, pas les grands ndarray typés.
        valeurs_brutes = (
            np.asarray(valeur, dtype=object) if not isinstance(valeur, np.ndarray) else None
        )
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} doit etre un tableau numerique reel.") from err
    if valeurs_brutes is not None and any(
        isinstance(element, (bool, np.bool_)) for element in valeurs_brutes.flat
    ):
        raise ValueError(f"{nom} doit etre un tableau numerique reel (booleens exclus).")
    if brut.dtype.kind not in "iuf":
        msg = f"{nom} doit etre un tableau numerique reel (booleens et complexes exclus)."
        raise ValueError(msg)
    try:
        resultat = np.asarray(brut, dtype=np.float64)
    except (TypeError, ValueError, OverflowError) as err:
        raise ValueError(f"{nom} doit etre representable en float64.") from err
    if not np.all(np.isfinite(resultat)):
        raise ValueError(f"{nom} doit contenir uniquement des valeurs finies.")
    return resultat


def _verifie_coordonnees(x_arr: NDArray[np.floating], y_arr: NDArray[np.floating]) -> None:
    """Valide la forme et la finitude des coordonnées spatiales."""
    if x_arr.shape != y_arr.shape:
        msg = "x et y doivent avoir des formes identiques."
        raise ValueError(msg)
    if not np.all(np.isfinite(x_arr)) or not np.all(np.isfinite(y_arr)):
        msg = "Les coordonnees doivent etre finies."
        raise ValueError(msg)


def _coordonnees_normalisees(
    coordonnees: NDArray[np.float64],
    origine: float,
    pas: float,
) -> NDArray[np.float64]:
    """Calcule (coordonnees - origine) / pas sans débordement intermédiaire."""
    meme_signe = np.signbit(coordonnees) == np.signbit(origine)
    with np.errstate(over="ignore"):
        difference = coordonnees - origine
    with np.errstate(over="ignore", divide="ignore", under="ignore", invalid="ignore"):
        indices_directs = difference / pas
        echelle = np.maximum(np.maximum(np.abs(coordonnees), abs(origine)), pas)
        difference_normalisee = coordonnees / echelle - origine / echelle
        indices_normalises = difference_normalisee / (pas / echelle)
    return np.asarray(np.where(meme_signe, indices_directs, indices_normalises), dtype=float)


def _interpole_lineairement_stable(
    a: ArrayLike,
    b: ArrayLike,
    poids: ArrayLike,
) -> NDArray[np.float64]:
    """Sélectionne une forme dont la branche retenue évite le débordement."""
    a_arr = np.asarray(a, dtype=np.float64)
    b_arr = np.asarray(b, dtype=np.float64)
    poids_arr = np.asarray(poids, dtype=np.float64)
    meme_signe = np.signbit(a_arr) == np.signbit(b_arr)
    with np.errstate(over="ignore", invalid="ignore"):
        interpolation_meme_signe = a_arr + poids_arr * (b_arr - a_arr)
        interpolation_signes_opposes = (1.0 - poids_arr) * a_arr + poids_arr * b_arr
    return np.asarray(
        np.where(meme_signe, interpolation_meme_signe, interpolation_signes_opposes),
        dtype=float,
    )


@dataclass(frozen=True)
class ReliefPlat:
    """Terrain plat d altitude nulle, cas de reference des solutions gaussiennes."""

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Retourne une altitude nulle (m) aux points (x, y)."""
        x_arr = _tableau_reel_fini(x, "Les coordonnees x")
        y_arr = _tableau_reel_fini(y, "Les coordonnees y")
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
        height = _reel_fini(self.height, "La hauteur du relief")
        width = _reel_fini(self.width, "La largeur du relief")
        center_x = _reel_fini(self.center_x, "Le centre x du relief")
        center_y = _reel_fini(self.center_y, "Le centre y du relief")
        if width <= 0.0:
            msg = "La largeur du relief doit être strictement positive."
            raise ValueError(msg)
        if not isinstance(self.kind, str) or self.kind not in ("flat", "hill", "valley", "ridge"):
            msg = f"Type de relief inconnu : {self.kind!r}."
            raise ValueError(msg)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "center_x", center_x)
        object.__setattr__(self, "center_y", center_y)

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Evalue l altitude du relief (m) aux points (x, y) : delegation pure."""
        x_arr = _tableau_reel_fini(x, "Les coordonnees x")
        y_arr = _tableau_reel_fini(y, "Les coordonnees y")
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
    reguliere : entetes ncols, nrows, cellsize et nodata_value optionnel,
    puis les altitudes ligne par ligne depuis la ligne la plus au nord.
    Chaque axe d origine admet les deux enregistrements du format Esri :
    xllcorner/yllcorner (angle de la cellule sud-ouest) ou
    xllcenter/yllcenter (centre de cette cellule), mutuellement exclusifs
    par axe. Les valeurs decrivent des cellules ; x0 et y0 designent
    toujours le centre de la cellule sud-ouest.

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
        altitudes = _tableau_reel_fini(self.altitudes, "Les altitudes").copy()
        if altitudes.ndim != 2 or altitudes.size == 0:
            msg = "La grille d altitudes doit etre bidimensionnelle non vide."
            raise ValueError(msg)
        pas = _reel_fini(self.pas, "Le pas de grille")
        x0 = _reel_fini(self.x0, "L origine x de la grille")
        y0 = _reel_fini(self.y0, "L origine y de la grille")
        sans_donnee = (
            None
            if self.sans_donnee is None
            else _reel_fini(self.sans_donnee, "La valeur sans donnee")
        )
        if pas <= 0.0:
            msg = "Le pas de grille doit etre strictement positif."
            raise ValueError(msg)
        # A read-only flag on an owning ndarray can be re-enabled by its caller.
        # A bytes-backed array makes the validated storage immutable at NumPy level.
        altitudes_immutable = np.frombuffer(altitudes.tobytes(), dtype=altitudes.dtype).reshape(
            altitudes.shape
        )
        object.__setattr__(self, "altitudes", altitudes_immutable)
        object.__setattr__(self, "pas", pas)
        object.__setattr__(self, "x0", x0)
        object.__setattr__(self, "y0", y0)
        object.__setattr__(self, "sans_donnee", sans_donnee)

    @classmethod
    def depuis_texte(cls, texte: str) -> Self:
        """Construit le relief depuis le texte d un fichier .asc standard.

        Le format Esri ASCII raster documente deux enregistrements par axe :
        xllcorner (angle de la cellule sud-ouest) ou xllcenter (centre de
        cette cellule). Chaque axe declare independemment son enregistrement ;
        les deux cles d un meme axe sont mutuellement exclusives.
        """
        jetons = texte.split()
        reconnues = {
            "ncols",
            "nrows",
            "cellsize",
            "nodata_value",
            "xllcorner",
            "yllcorner",
            "xllcenter",
            "yllcenter",
        }
        entete: dict[str, float] = {}
        position = 0
        while position + 1 < len(jetons):
            cle = jetons[position].lower()
            if cle not in reconnues:
                break
            if cle in entete:
                msg = f"Cle d entete .asc dupliquee : {cle}."
                raise ValueError(msg)
            try:
                entete[cle] = float(jetons[position + 1])
            except ValueError as err:
                msg = f"Valeur invalide pour {cle} : {jetons[position + 1]}."
                raise ValueError(msg) from err
            position += 2
        manquantes = {"ncols", "nrows", "cellsize"} - set(entete)
        for paire in (("xllcorner", "xllcenter"), ("yllcorner", "yllcenter")):
            presentes = [cle for cle in paire if cle in entete]
            if len(presentes) == 2:
                msg = f"Entete .asc incoherente : {' et '.join(paire)} sont exclusifs."
                raise ValueError(msg)
            if not presentes:
                manquantes.add("/".join(paire))
        if manquantes:
            msg = f"Entete .asc incomplete : {', '.join(sorted(manquantes))}."
            raise ValueError(msg)
        ncols = entete["ncols"]
        nrows = entete["nrows"]
        if not np.isfinite(ncols) or not np.isfinite(nrows):
            msg = "ncols et nrows doivent etre finis."
            raise ValueError(msg)
        if ncols != int(ncols) or nrows != int(nrows) or ncols < 1 or nrows < 1:
            msg = "ncols et nrows doivent etre des entiers au moins 1."
            raise ValueError(msg)
        pas = entete["cellsize"]
        if pas <= 0.0:
            msg = "cellsize doit etre strictement positif."
            raise ValueError(msg)
        try:
            valeurs = np.asarray(jetons[position:], dtype=float)
        except ValueError as err:
            msg = "La grille contient une valeur d altitude non numerique."
            raise ValueError(msg) from err
        if valeurs.size != int(ncols) * int(nrows):
            msg = "La grille ne contient pas ncols x nrows valeurs."
            raise ValueError(msg)
        altitudes = valeurs.reshape(int(nrows), int(ncols))
        origine_x = (
            entete["xllcenter"] if "xllcenter" in entete else entete["xllcorner"] + 0.5 * pas
        )
        origine_y = (
            entete["yllcenter"] if "yllcenter" in entete else entete["yllcorner"] + 0.5 * pas
        )
        return cls(
            altitudes=altitudes,
            x0=origine_x,
            y0=origine_y,
            pas=pas,
            sans_donnee=entete.get("nodata_value"),
        )

    @classmethod
    def depuis_fichier(cls, chemin: Path) -> Self:
        """Construit le relief depuis un fichier .asc du disque."""
        return cls.depuis_texte(chemin.read_text(encoding="utf-8"))

    def altitude(self, x: ArrayLike, y: ArrayLike) -> NDArray[np.float64]:
        """Interpole lineairement l altitude (m) aux points (x, y).

        Le domaine d interpolation est l enveloppe des centres des cellules,
        de (x0, y0) a (x0 + (ncols - 1) * pas, y0 + (nrows - 1) * pas) :
        la demi-cellule exterieure du raster est refusee, aucune
        extrapolation au-dela du dernier centre n est faite (decision de
        domaine explicite ; l acceptation des enregistrements coin ou
        centre du format ne l etend pas).

        Raises:
            ValueError: formes differentes, point hors emprise ou cellule
                sans donnee a poids non nul dans l interpolation.
        """
        x_arr = _tableau_reel_fini(x, "Les coordonnees x")
        y_arr = _tableau_reel_fini(y, "Les coordonnees y")
        _verifie_coordonnees(x_arr, y_arr)
        nrows, ncols = self.altitudes.shape
        colonne = _coordonnees_normalisees(x_arr, self.x0, self.pas)
        ligne = _coordonnees_normalisees(y_arr, self.y0, self.pas)
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
        # L'interpolation bilinéaire est une interpolation linéaire successive.
        # La forme a + t*(b-a) est sûre pour deux valeurs de même signe ;
        # la forme pondérée est sûre pour deux valeurs de signes opposés.
        z_bas = _interpole_lineairement_stable(z00, z10, tx)
        z_haut = _interpole_lineairement_stable(z01, z11, tx)
        z = _interpole_lineairement_stable(z_bas, z_haut, ty)
        return np.asarray(z, dtype=float)


__all__ = [
    "ReliefMntAscii",
    "ReliefPlat",
    "ReliefSynthetique",
]
