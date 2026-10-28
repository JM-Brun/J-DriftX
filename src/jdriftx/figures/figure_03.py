"""Génère la figure 3 : modèle réduit contre EDP, deux résolutions indépendantes.

Le schéma est une reconstruction conceptuelle (niveau R1), figure 3 du
plan de figures du chapitre de 2008 (p. 254) : sous les mêmes entrées
(vent uniforme, diffusivité transversale constante, colonne d'entrée du
panache de similitude, fenêtre latérale avec Dirichlet nul), la forme
fermée du modèle réduit et une résolution directe de l'équation de
transport-diffusion par schéma explicite sont comparées sur les nœuds
des mêmes tranches. Ce n'est pas une reproduction de la figure du
chapitre Springer ni une validation quantitative des données
historiques.

Toutes les valeurs affichées proviennent de la tranche typée
``jdriftx.experiences.modele_reduit_edp`` (configuration -> tranches ->
normes -> manifeste) : la figure rend des résultats calculés et ne
peut pas diverger silencieusement de l'implémentation testée. La sortie
est déterministe ; la copie versionnée du SVG doit rester strictement
synchronisée (test d'égalité octet par octet).
"""

from __future__ import annotations

import math
from html import escape

from jdriftx.experiences.modele_reduit_edp import (
    SCENARIO_DEFAUT,
    ResultatComparaison,
    TrancheComparaison,
    comparer_scenario,
)

SVG_WIDTH = 1100
SVG_HEIGHT = 780

ECHELLE = 0.25
PAS_CELLULE_X = 100.0
PAS_CELLULE_Y = 20.0
_X_ORIGINE = 300.0
_Y_MAXIMUM = 300.0
PANEL_X = 35.0
LIGNE1_Y = 100.0
LIGNE2_Y = 290.0
LIGNE3_Y = 480.0
SEUILS_CHAMP = (1e-4, 3e-4, 8e-4, 2e-3, 5e-3)
COULEURS_CHAMP = ("#dbe9f7", "#b3d0ea", "#86b4db", "#5b93c8", "#2f6fae")
SEUILS_ECART = (5e-7, 1.5e-6, 4e-6, 1e-5, 2e-5)
COULEURS_ECART = ("#fdecd6", "#f9d3ab", "#f2b078", "#e68d50", "#d56a30")
_ORDONNEE_HAUT = 130.0
_LOG_SEUIL_HAUT = -1.8
_ECHELLE_LOG = 93.75
_ABSCISSES_CONVERGENCE = ((20.0, 620.0), (10.0, 830.0), (5.0, 1040.0))


def _text(x: float, y: float, value: str, *, size: int = 17, weight: str = "normal") -> str:
    """Renvoie un élément text SVG échappé."""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" fill="#202833">{escape(value)}</text>'
    )


def _px(x0: float, x: float) -> float:
    """Convertit une abscisse monde (m) en pixels dans un panneau."""
    return x0 + (x - _X_ORIGINE) * ECHELLE


def _py(y0: float, y: float) -> float:
    """Convertit une ordonnée monde (m) en pixels (axe y vers le haut)."""
    return y0 + (_Y_MAXIMUM - y) * ECHELLE


def _marquages(x0: float, y0: float) -> list[str]:
    """Dessine l'axe du panache et le marqueur d'entrée d'un panneau."""
    elements: list[str] = []
    py_axe = _py(y0, 0.0)
    elements.append(
        f'<line x1="{_px(x0, _X_ORIGINE):.1f}" y1="{py_axe:.1f}" '
        f'x2="{_px(x0, 2000.0):.1f}" y2="{py_axe:.1f}" '
        'stroke="#7c8894" stroke-width="1.5" stroke-dasharray="4 3"/>'
    )
    px_e = _px(x0, _X_ORIGINE)
    elements.append(f'<circle cx="{px_e:.1f}" cy="{py_axe:.1f}" r="5" fill="#2864a5"/>')
    elements.append(_text(px_e + 8.0, py_axe - 8.0, "E", size=13, weight="bold"))
    return elements


def _panneau_champ(
    x0: float,
    y0: float,
    tranches: tuple[TrancheComparaison, ...],
    demi_largeur: float,
    *,
    numerique: bool,
) -> tuple[list[str], int]:
    """Dessine un champ de concentration en bandes, aux nœuds des tranches."""
    elements: list[str] = []
    cellules = 0
    nombre_y = int(2.0 * demi_largeur / PAS_CELLULE_Y)
    for tranche in tranches:
        for j in range(nombre_y):
            y = -demi_largeur + j * PAS_CELLULE_Y
            k = 2 * j
            valeur = tranche.numerique[k] if numerique else tranche.reduite[k]
            if valeur < SEUILS_CHAMP[0]:
                continue
            bande = sum(1 for seuil in SEUILS_CHAMP if valeur >= seuil) - 1
            elements.append(
                f'<rect x="{_px(x0, tranche.x):.1f}" y="{_py(y0, y + PAS_CELLULE_Y):.1f}" '
                f'width="{PAS_CELLULE_X * ECHELLE:.1f}" height="{PAS_CELLULE_Y * ECHELLE:.1f}" '
                f'fill="{COULEURS_CHAMP[bande]}" stroke="#8fb3d9" stroke-width="1"/>'
            )
            cellules += 1
    return elements, cellules


def _panneau_ecart(
    x0: float,
    y0: float,
    tranches: tuple[TrancheComparaison, ...],
    demi_largeur: float,
) -> tuple[list[str], int]:
    """Dessine l'écart entre les deux champs en bandes, aux mêmes nœuds."""
    elements: list[str] = []
    cellules = 0
    nombre_y = int(2.0 * demi_largeur / PAS_CELLULE_Y)
    for tranche in tranches:
        for j in range(nombre_y):
            y = -demi_largeur + j * PAS_CELLULE_Y
            k = 2 * j
            valeur = abs(tranche.numerique[k] - tranche.reduite[k])
            if valeur < SEUILS_ECART[0]:
                continue
            bande = sum(1 for seuil in SEUILS_ECART if valeur >= seuil) - 1
            elements.append(
                f'<rect x="{_px(x0, tranche.x):.1f}" y="{_py(y0, y + PAS_CELLULE_Y):.1f}" '
                f'width="{PAS_CELLULE_X * ECHELLE:.1f}" height="{PAS_CELLULE_Y * ECHELLE:.1f}" '
                f'fill="{COULEURS_ECART[bande]}" stroke="#d9a76a" stroke-width="1"/>'
            )
            cellules += 1
    return elements, cellules


def _panneau_convergence(resultat: ResultatComparaison) -> list[str]:
    """Dessine la décroissance de l'erreur L2 aux trois maillages."""
    elements: list[str] = []
    marqueurs: list[tuple[float, float, float, float]] = []
    for (pas, px), maillage in zip(_ABSCISSES_CONVERGENCE, resultat.maillages, strict=True):
        erreur = maillage.l2_relative
        py = _ORDONNEE_HAUT + (_LOG_SEUIL_HAUT - math.log10(erreur)) * _ECHELLE_LOG
        marqueurs.append((pas, px, py, erreur))
    points = " ".join(f"{px:.1f},{py:.1f}" for _pas, px, py, _erreur in marqueurs)
    elements.append(
        f'<polyline points="{points}" fill="none" stroke="#2f6fae" '
        'stroke-width="2" stroke-dasharray="6 4"/>'
    )
    elements.append('<line x1="560" y1="280" x2="1060" y2="280" stroke="#7c8894" '
                    'stroke-width="1.5"/>')
    for pas, px, py, erreur in marqueurs:
        elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#2864a5"/>')
        elements.append(_text(px - 24.0, py - 14.0, f"{erreur:.1e}", size=15))
        elements.append(_text(px - 24.0, 296.0, f"dy = {pas:.0f} m", size=14))
    return elements


def render_figure_03_svg() -> str:
    """Renvoie le SVG déterministe de la figure 3 (modèle réduit vs EDP)."""
    scenario = SCENARIO_DEFAUT
    resultat = comparer_scenario(scenario)
    grossier, reference, fin = resultat.maillages
    if resultat.ratio_grossier < 3.0 or resultat.ratio_grossier > 5.0:
        msg = "La convergence du maillage grossier doit rester d'ordre deux."
        raise ValueError(msg)
    if resultat.ratio_fin < 3.0 or resultat.ratio_fin > 5.0:
        msg = "La convergence du maillage fin doit rester d'ordre deux."
        raise ValueError(msg)
    if grossier.l2_relative <= reference.l2_relative or reference.l2_relative <= fin.l2_relative:
        msg = "L'erreur doit décroître quand le maillage se raffine."
        raise ValueError(msg)
    if resultat.ecart_flux_max >= 1e-4 or resultat.ecart_flux_reduit >= 1e-4:
        msg = "Le bilan de masse doit rester sous 1e-4 aux tranches."
        raise ValueError(msg)
    if resultat.nombre_tranches < 8:
        msg = "Le nombre de tranches doit rester lisible."
        raise ValueError(msg)
    panneau_a, cellules_a = _panneau_champ(
        PANEL_X, LIGNE1_Y, resultat.tranches, scenario.demi_largeur, numerique=False
    )
    panneau_b, cellules_b = _panneau_champ(
        PANEL_X, LIGNE2_Y, resultat.tranches, scenario.demi_largeur, numerique=True
    )
    if cellules_a < 150 or cellules_b < 150:
        msg = "Les cartes de concentration ne doivent pas être vides."
        raise ValueError(msg)
    if cellules_a != cellules_b:
        msg = "Les deux cartes doivent compter les mêmes cellules affichées."
        raise ValueError(msg)
    panneau_c, cellules_c = _panneau_ecart(
        PANEL_X, LIGNE3_Y, resultat.tranches, scenario.demi_largeur
    )
    if cellules_c < 100:
        msg = "La carte d'écart ne doit pas être vide."
        raise ValueError(msg)
    vent_txt = f"{scenario.vent:.1f}"
    ligne_vent = f"Vent uniforme U = {vent_txt} m/s le long de x."
    diffusivite_txt = f"{scenario.diffusivite:.0f}"
    ligne_diffusivite = f"Diffusivité transversale K = {diffusivite_txt} m²/s, constante."
    debit_txt = f"{scenario.debit:.1f}"
    ligne_debit = f"Flux de masse Q = {debit_txt} kg/s dans la colonne d'entrée."
    entree_txt = f"{scenario.x_entree:.0f}"
    ligne_entree = f"Entrée à {entree_txt} m : colonne du panache de similitude."
    fenetre_txt = f"{scenario.demi_largeur:.0f}"
    ligne_fenetre = f"Fenêtre ±{fenetre_txt} m : au moins 4 écarts-types, Dirichlet nul."
    pas_txt = f"{scenario.pas_transverse:.0f}"
    ligne_maillage = f"Maillage de référence dy = {pas_txt} m ; r = 1/3 (schéma explicite)."
    tranches_txt = f"{resultat.nombre_tranches}"
    tranche_txt = f"{scenario.pas_tranche:.0f}"
    ligne_tranches = f"{tranches_txt} tranches de comparaison tous les {tranche_txt} m."
    l2_txt = f"{resultat.l2_reference:.1e}"
    linf_txt = f"{resultat.linf_reference:.1e}"
    ligne_normes = f"L2 relative : {l2_txt} ; L infinie relative : {linf_txt}."
    flux_num_txt = f"{resultat.ecart_flux_max:.1e}"
    flux_red_txt = f"{resultat.ecart_flux_reduit:.1e}"
    ligne_flux_1 = "Bilan de masse, écart de flux maximal aux tranches :"
    ligne_flux_2 = f"EDP {flux_num_txt} ; forme fermée {flux_red_txt} (rapporté à Q)."
    r1_txt = f"{resultat.ratio_grossier:.1f}"
    r2_txt = f"{resultat.ratio_fin:.1f}"
    ligne_convergence = f"Convergence : \u00d7{r1_txt} puis \u00d7{r2_txt} en divisant dy par deux."
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
        f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Figure 3 : modèle réduit contre EDP, deux résolutions</title>',
        '<desc id="desc">Transport-diffusion 2D : comparaison de la forme fermée et du '
        "schéma explicite aux mêmes nœuds.</desc>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        _text(
            32.0,
            38.0,
            "Figure 3 — Modèle réduit vs EDP : deux résolutions, mêmes entrées",
            size=22,
            weight="bold",
        ),
        _text(
            32.0,
            66.0,
            "Transport-diffusion 2D, vent uniforme : forme fermée contre schéma "
            "explicite, mêmes tranches.",
            size=16,
        ),
        _text(35.0, 92.0, "A. Modèle réduit (forme fermée, maillage 10 m)", size=16, weight="bold"),
        '<rect x="30" y="95" width="435" height="160" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_a,
        *_marquages(PANEL_X, LIGNE1_Y),
        _text(
            35.0,
            282.0,
            "B. EDP directe (schéma explicite, maillage 10 m)",
            size=16,
            weight="bold",
        ),
        '<rect x="30" y="285" width="435" height="160" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_b,
        *_marquages(PANEL_X, LIGNE2_Y),
        _text(35.0, 472.0, "C. Écart aux nœuds : |numérique - réduit|", size=16, weight="bold"),
        '<rect x="30" y="475" width="435" height="160" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_c,
        *_marquages(PANEL_X, LIGNE3_Y),
        _text(530.0, 92.0, "D. Convergence de maillage (L2 relative)", size=16, weight="bold"),
        '<rect x="525" y="95" width="545" height="210" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *_panneau_convergence(resultat),
        _text(530.0, 340.0, "Paramètres", size=17, weight="bold"),
        _text(530.0, 368.0, ligne_vent, size=15),
        _text(530.0, 392.0, ligne_diffusivite, size=15),
        _text(530.0, 416.0, ligne_debit, size=15),
        _text(530.0, 440.0, ligne_entree, size=15),
        _text(530.0, 464.0, ligne_fenetre, size=15),
        _text(530.0, 488.0, ligne_maillage, size=15),
        _text(530.0, 512.0, ligne_tranches, size=15),
        _text(530.0, 544.0, "Écarts aux nœuds (maillage de référence)", size=17, weight="bold"),
        _text(530.0, 572.0, ligne_normes, size=15),
        _text(530.0, 596.0, ligne_flux_1, size=15),
        _text(530.0, 620.0, ligne_flux_2, size=15),
        _text(530.0, 644.0, ligne_convergence, size=15),
        _text(530.0, 676.0, "Lecture", size=17, weight="bold"),
        _text(
            530.0,
            704.0,
            "La forme fermée est exacte : l'écart aux nœuds est l'erreur",
            size=15,
        ),
        _text(
            530.0,
            728.0,
            "de discrétisation du schéma : elle décroît comme le carré du pas.",
            size=15,
        ),
        _text(
            30.0,
            765.0,
            "Reconstruction conceptuelle (R1) ; cas synthétique ; pas une "
            "reproduction quantitative du chapitre de 2008 (p. 254).",
            size=13,
        ),
        "</svg>",
    ]
    return "\n".join(elements) + "\n"
