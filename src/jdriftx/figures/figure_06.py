"""Génère la figure 6 : identification de source, sensibilité du coût.

Le schéma est une reconstruction conceptuelle (niveau R1), figure 6 du
plan de figures du chapitre de 2008 (p. 255) : une pollution est détectée
dans le coin inférieur gauche du domaine ; la carte de sensibilité du
coût d'ajustement (débit optimal en forme fermée pour chaque position
candidate) montre une vallée le long de l'axe du vent, signature de la
non-identifiabilité position-débit. Ce n'est pas une reproduction de la
figure du chapitre Springer ni une validation quantitative des données
historiques.

Toutes les valeurs affichées proviennent du résultat typé
``jdriftx.experiences.identification_source`` (scénario -> observations ->
coûts -> vallée -> manifeste) : la figure rend des résultats calculés et
ne peut pas diverger silencieusement de l'implémentation testée. La carte
de sensibilité est explicitement étiquetée comme un coût d'ajustement,
jamais comme une probabilité de source. La sortie est déterministe ; la
copie versionnée du SVG doit rester strictement synchronisée (test
d'égalité octet par octet).
"""

from __future__ import annotations

import math
from html import escape

from jdriftx.experiences.identification_source import (
    SCENARIO_DEFAUT,
    ResultatIdentification,
    ScenarioIdentification,
    concentration,
    resoudre_scenario,
)

SVG_WIDTH = 1100
SVG_HEIGHT = 780

ECHELLE = 0.125
PAS_CELLULE = 100.0
PANEL_A_X = 35.0
PANEL_B_X = 330.0
PANEL_Y = 103.0
SEUILS_CHAMP = (2e-4, 6e-4, 1.5e-3, 3e-3, 6e-3)
COULEURS_CHAMP = ("#dbe9f7", "#b3d0ea", "#86b4db", "#5b93c8", "#2f6fae")
SEUILS_COUT = (1e-6, 1e-2, 1e-1, 5e-1)
COULEURS_COUT = ("#d56a30", "#e68d50", "#f2b078", "#f9d3ab", "#fdecd6")
ETIQUETTES_CHAMP = ("2e-4", "6e-4", "1.5e-3", "3e-3", "6e-3")
ETIQUETTES_COUT = ("0", "<=1e-2", "<=1e-1", "<=0.5", ">0.5")
_COUPE_X0 = 45.0
_COUPE_LARG = 525.0
_COUPE_Y0 = 450.0
_COUPE_ECHELLE = 28.0
_COUPE_PORTEE = 400.0


def _text(x: float, y: float, value: str, *, size: int = 17, weight: str = "normal") -> str:
    """Renvoie un élément text SVG échappé."""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" fill="#202833">{escape(value)}</text>'
    )


def _px(x0: float, x: float) -> float:
    """Convertit une abscisse monde (m) en pixels dans un panneau."""
    return x0 + x * ECHELLE


def _py(y: float) -> float:
    """Convertit une ordonnée monde (m) en pixels (axe y vers le haut)."""
    return PANEL_Y + (2000.0 - y) * ECHELLE


def _fleche(x0: float, depart: tuple[float, float], arrivee: tuple[float, float]) -> list[str]:
    """Dessine une flèche entre deux points monde, avec pointe triangulaire."""
    px1, py1 = _px(x0, depart[0]), _py(depart[1])
    px2, py2 = _px(x0, arrivee[0]), _py(arrivee[1])
    dx = px2 - px1
    dy = py2 - py1
    norme = math.sqrt(dx * dx + dy * dy)
    ux, uy = dx / norme, dy / norme
    bx, by = px2 - 10.0 * ux, py2 - 10.0 * uy
    return [
        (
            f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" '
            'stroke="#2864a5" stroke-width="2"/>'
        ),
        (
            f'<polygon points="{px2:.1f},{py2:.1f} {bx - 4.0 * uy:.1f},{by + 4.0 * ux:.1f} '
            f'{bx + 4.0 * uy:.1f},{by - 4.0 * ux:.1f}" fill="#2864a5"/>'
        ),
    ]


def _marques_vent(scenario: ScenarioIdentification, x0: float) -> list[str]:
    """Dessine les mesures de vent concordantes et leurs flèches de vent."""
    vitesse = math.sqrt(scenario.vent[0] * scenario.vent[0] + scenario.vent[1] * scenario.vent[1])
    ex = (scenario.vent[0] / vitesse, scenario.vent[1] / vitesse)
    elements: list[str] = []
    for mesure in scenario.mesures_vent:
        px, py = _px(x0, mesure[0]), _py(mesure[1])
        elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#2864a5"/>')
        arrivee = (mesure[0] + 280.0 * ex[0], mesure[1] + 280.0 * ex[1])
        elements.extend(_fleche(x0, mesure, arrivee))
    return elements


def _marques_capteurs(scenario: ScenarioIdentification, x0: float) -> list[str]:
    """Dessine les cinq capteurs et l'anneau du capteur de détection."""
    elements: list[str] = []
    for capteur in scenario.capteurs:
        px, py = _px(x0, capteur[0]), _py(capteur[1])
        elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#202833"/>')
    capteur = scenario.capteurs[scenario.indice_detection]
    px, py = _px(x0, capteur[0]), _py(capteur[1])
    elements.append(
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="none" '
        'stroke="#c0392b" stroke-width="2"/>'
    )
    elements.append(_text(px + 12.0, py - 8.0, "détection", size=12))
    return elements


def _legende(
    x0: float,
    etiquettes: tuple[str, ...],
    couleurs: tuple[str, ...],
    contour: str,
) -> list[str]:
    """Dessine une rangée de cinq pastilles de légende avec leurs étiquettes."""
    elements: list[str] = []
    for indice in range(5):
        px = x0 + indice * 50.0
        elements.append(
            f'<rect x="{px:.1f}" y="372" width="12" height="12" '
            f'fill="{couleurs[indice]}" stroke="{contour}" stroke-width="1"/>'
        )
        elements.append(_text(px + 16.0, 382.0, etiquettes[indice], size=12))
    return elements


def _panneau_champ(
    scenario: ScenarioIdentification,
    x0: float,
) -> tuple[list[str], int]:
    """Dessine le champ de concentration en bandes, aux centres des cellules."""
    elements: list[str] = []
    cellules = 0
    cote = scenario.fenetre.largeur
    nombre = int(cote / PAS_CELLULE)
    for j in range(nombre):
        for i in range(nombre):
            centre = (i * PAS_CELLULE + 0.5 * PAS_CELLULE, j * PAS_CELLULE + 0.5 * PAS_CELLULE)
            valeur = concentration(scenario, centre, scenario.source_vrai, scenario.debit_vrai)
            if valeur < SEUILS_CHAMP[0]:
                continue
            bande = sum(1 for seuil in SEUILS_CHAMP if valeur >= seuil) - 1
            elements.append(
                f'<rect x="{_px(x0, i * PAS_CELLULE):.1f}" '
                f'y="{_py(j * PAS_CELLULE + PAS_CELLULE):.1f}" '
                f'width="{PAS_CELLULE * ECHELLE:.1f}" height="{PAS_CELLULE * ECHELLE:.1f}" '
                f'fill="{COULEURS_CHAMP[bande]}" stroke="#8fb3d9" stroke-width="1"/>'
            )
            cellules += 1
    return elements, cellules


def _panneau_cout(
    scenario: ScenarioIdentification,
    resultat: ResultatIdentification,
    x0: float,
) -> tuple[list[str], int]:
    """Dessine la carte des coûts minimaux, valeur au nœud, cellule à droite."""
    elements: list[str] = []
    cellules = 0
    pas = scenario.pas_candidats
    nombre = int(scenario.fenetre.largeur / pas) + 1
    for j in range(nombre - 1):
        for i in range(nombre - 1):
            cout = resultat.couts_grille[j * nombre + i]
            relatif = cout / resultat.cout_nul
            if relatif <= SEUILS_COUT[0]:
                bande = 0
            elif relatif <= SEUILS_COUT[1]:
                bande = 1
            elif relatif <= SEUILS_COUT[2]:
                bande = 2
            elif relatif <= SEUILS_COUT[3]:
                bande = 3
            else:
                bande = 4
            elements.append(
                f'<rect x="{_px(x0, i * pas):.1f}" y="{_py(j * pas + pas):.1f}" '
                f'width="{pas * ECHELLE:.1f}" height="{pas * ECHELLE:.1f}" '
                f'fill="{COULEURS_COUT[bande]}" stroke="#d9a76a" stroke-width="1"/>'
            )
            cellules += 1
    return elements, cellules


def _panneau_coupe(
    scenario: ScenarioIdentification,
    resultat: ResultatIdentification,
) -> list[str]:
    """Dessine la coupe du coût le long de l'axe du vent, en échelle log."""
    elements: list[str] = []
    vitesse = math.sqrt(scenario.vent[0] * scenario.vent[0] + scenario.vent[1] * scenario.vent[1])
    ex = (scenario.vent[0] / vitesse, scenario.vent[1] / vitesse)
    pas = scenario.pas_candidats
    nombre = int(scenario.fenetre.largeur / pas) + 1
    portee = -_COUPE_PORTEE * (ex[0] + ex[1])
    marqueurs: list[tuple[float, float]] = []
    for k in reversed(range(9)):
        x = scenario.source_vrai[0] - _COUPE_PORTEE + k * pas
        indice = int(x / pas)
        cout = resultat.couts_grille[indice * nombre + indice]
        relatif = cout / resultat.cout_nul
        proj = (x - scenario.source_vrai[0]) * (ex[0] + ex[1])
        px = _COUPE_X0 + (proj + portee) / (2.0 * portee) * _COUPE_LARG
        log = -6.0 if relatif <= 1e-6 else math.log10(relatif)
        py = _COUPE_Y0 - log * _COUPE_ECHELLE
        marqueurs.append((px, py))
    points = " ".join(f"{px:.1f},{py:.1f}" for px, py in marqueurs)
    elements.append(
        f'<polyline points="{points}" fill="none" stroke="#2f6fae" '
        'stroke-width="2" stroke-dasharray="6 4"/>'
    )
    for px, py in marqueurs:
        elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#2864a5"/>')
    py_seuil = _COUPE_Y0 + 2.0 * _COUPE_ECHELLE
    elements.append(
        f'<line x1="{_COUPE_X0:.1f}" y1="{py_seuil:.1f}" '
        f'x2="{_COUPE_X0 + _COUPE_LARG:.1f}" y2="{py_seuil:.1f}" '
        'stroke="#7c8894" stroke-width="1.5" stroke-dasharray="4 3"/>'
    )
    px_source, py_source = marqueurs[4]
    elements.append(
        f'<line x1="{px_source:.1f}" y1="{_COUPE_Y0:.1f}" '
        f'x2="{px_source:.1f}" y2="{_COUPE_Y0 + 190.0:.1f}" '
        'stroke="#7c8894" stroke-width="1.5" stroke-dasharray="4 3"/>'
    )
    elements.append(f'<circle cx="{px_source:.1f}" cy="{py_source:.1f}" r="6" fill="#c0392b"/>')
    px_decale, py_decale = marqueurs[1]
    elements.append(
        f'<circle cx="{px_decale:.1f}" cy="{py_decale:.1f}" r="9" '
        'fill="none" stroke="#c0392b" stroke-width="2"/>'
    )
    elements.append(_text(px_source + 10.0, py_source + 18.0, "J = 0 (exact)", size=13))
    ligne_decale = f"candidat décalé : {resultat.cout_relatif_decale:.1e}"
    elements.append(_text(px_decale + 12.0, py_decale - 6.0, ligne_decale, size=13))
    elements.append(_text(250.0, 520.0, "J/J0 = 1e-2 : seuil de la vallée", size=13))
    elements.append(_text(_COUPE_X0, _COUPE_Y0 + 210.0, "amont", size=13))
    elements.append(_text(px_source - 22.0, _COUPE_Y0 + 210.0, "source", size=13))
    elements.append(_text(_COUPE_X0 + _COUPE_LARG - 26.0, _COUPE_Y0 + 210.0, "aval", size=13))
    for exposant in (0, 2, 4, 6):
        py = _COUPE_Y0 + exposant * _COUPE_ECHELLE - 4.0
        valeur = f"1e-{exposant:d}" if exposant else "1e0"
        elements.append(_text(56.0, py, valeur, size=12))
    return elements


def _verifier_resultat(
    scenario: ScenarioIdentification,
    resultat: ResultatIdentification,
) -> None:
    """Vérifie les invariants scientifiques avant tout rendu."""
    if resultat.cout_minimum != 0.0:
        msg = "Le minimum du coût doit être exactement nul à la source vraie."
        raise ValueError(msg)
    if resultat.position_estimee != scenario.source_vrai:
        msg = "La position estimée doit coïncider avec la source vraie."
        raise ValueError(msg)
    if abs(resultat.debit_etoile - scenario.debit_vrai) > 1e-12:
        msg = "Le débit ajusté au minimum doit retrouver le débit vrai."
        raise ValueError(msg)
    if resultat.concentration_detection < scenario.seuil_detection:
        msg = "Le capteur de détection doit dépasser le seuil de détection."
        raise ValueError(msg)
    if not 30 <= resultat.cellules_detectees <= 50:
        msg = "Le nombre de cellules détectées doit rester lisible."
        raise ValueError(msg)
    if resultat.concentration_maximale <= scenario.seuil_detection:
        msg = "Le champ doit dépasser le seuil de détection quelque part."
        raise ValueError(msg)
    if not 5 <= resultat.nombre_cellules_vallee <= 9:
        msg = "La vallée du coût doit compter de cinq à neuf cellules."
        raise ValueError(msg)
    if resultat.etendue_vallee < 6.0 * resultat.largeur_vallee:
        msg = "La vallée doit être nettement plus longue que large."
        raise ValueError(msg)
    if not 1e-4 <= resultat.cout_relatif_decale <= 1e-2:
        msg = "Le candidat décalé doit montrer une ambiguïté réelle."
        raise ValueError(msg)


def _lignes_parametres(
    scenario: ScenarioIdentification,
    resultat: ResultatIdentification,
) -> tuple[str, str, str, str, str, str, str]:
    """Renvoie les lignes de texte du bloc paramètres."""
    vitesse = math.sqrt(scenario.vent[0] * scenario.vent[0] + scenario.vent[1] * scenario.vent[1])
    ligne_vent = f"Vent uniforme U = {vitesse:.1f} m/s vers le sud-ouest."
    ligne_diffusivite = f"Diffusivité transversale K = {scenario.diffusivite:.0f} m²/s."
    ligne_debit = f"Débit vrai Q = {scenario.debit_vrai:.1f} kg/s, source dans le vignoble."
    ligne_capteurs = f"Cinq capteurs au sol ; seuil de détection {scenario.seuil_detection:.1e}."
    nombre = int(scenario.fenetre.largeur / scenario.pas_candidats) + 1
    ligne_candidats = (
        f"Candidats : grille {nombre} fois {nombre}, pas {scenario.pas_candidats:.0f} m."
    )
    ligne_mesures = "Trois mesures de vent concordantes : champ uniforme reconstruit."
    ligne_cout = f"Coût nul J0 = {resultat.cout_nul:.1e} (absence de source)."
    return (
        ligne_vent,
        ligne_diffusivite,
        ligne_debit,
        ligne_capteurs,
        ligne_candidats,
        ligne_mesures,
        ligne_cout,
    )


def _lignes_valeurs(
    scenario: ScenarioIdentification,
    resultat: ResultatIdentification,
) -> tuple[str, str, str, str, str, str, str]:
    """Renvoie les lignes de texte du bloc valeurs clés."""
    detection = f"{resultat.concentration_detection:.1e}"
    cellules = f"{resultat.cellules_detectees}"
    ligne_detection_1 = f"Concentration au coin détecté : {detection} kg/m² ;"
    ligne_detection_2 = f"{cellules} cellules au-dessus du seuil (carte A)."
    ligne_minimum = f"Minimum exact J = 0 à la source vraie, Q* = {resultat.debit_etoile:.2f} kg/s."
    ligne_vallee_1 = (
        f"Vallée (J/J0 sous 1e-2) : {resultat.nombre_cellules_vallee} cellules, "
        f"{resultat.etendue_vallee:.0f} m le long"
    )
    facteur = resultat.etendue_vallee / resultat.largeur_vallee
    ligne_vallee_2 = f"du vent, {resultat.largeur_vallee:.0f} m en travers (facteur {facteur:.1f})."
    ligne_decale_1 = (
        f"Candidat décalé de {resultat.decalage_vent:.0f} m au vent : "
        f"Q* = {resultat.debit_etoile_decale:.2f} kg/s,"
    )
    ligne_decale_2 = (
        f"coût {resultat.cout_relatif_decale:.1e} de J0 : "
        "position et débit restent couplés."
    )
    return (
        ligne_detection_1,
        ligne_detection_2,
        ligne_minimum,
        ligne_vallee_1,
        ligne_vallee_2,
        ligne_decale_1,
        ligne_decale_2,
    )


def _lignes_lecture() -> tuple[str, str, str, str, str, str, str, str]:
    """Renvoie les lignes de texte du bloc lecture."""
    return (
        "La carte B est une carte de sensibilité du coût d'ajustement :",
        "ce n'est pas une probabilité de source (aucun prior, aucun",
        "postériori, aucune normalisation bayésienne).",
        "La vallée le long de l'axe du vent traduit la dégénérescence",
        "position-débit : déplacer la source au vent et augmenter le",
        "débit change peu les concentrations prédites aux capteurs.",
        "Aucun candidat aval des capteurs ne fait mieux que l'absence",
        "de source : coût constant égal à J0.",
    )


def render_figure_06_svg() -> str:
    """Renvoie le SVG déterministe de la figure 6 (identification de source)."""
    scenario = SCENARIO_DEFAUT
    resultat = resoudre_scenario(scenario)
    _verifier_resultat(scenario, resultat)
    panneau_a, cellules_a = _panneau_champ(scenario, PANEL_A_X)
    panneau_b, cellules_b = _panneau_cout(scenario, resultat, PANEL_B_X)
    if cellules_a < 50:
        msg = "La carte de concentration ne doit pas être vide."
        raise ValueError(msg)
    if cellules_b < 5:
        msg = "La carte de coût ne doit pas être vide."
        raise ValueError(msg)
    panneau_c = _panneau_coupe(scenario, resultat)
    (
        ligne_vent,
        ligne_diffusivite,
        ligne_debit,
        ligne_capteurs,
        ligne_candidats,
        ligne_mesures,
        ligne_cout,
    ) = _lignes_parametres(scenario, resultat)
    (
        ligne_detection_1,
        ligne_detection_2,
        ligne_minimum,
        ligne_vallee_1,
        ligne_vallee_2,
        ligne_decale_1,
        ligne_decale_2,
    ) = _lignes_valeurs(scenario, resultat)
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
        f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Figure 6 : identification de source, sensibilité du coût</title>',
        '<desc id="desc">Dispersion depuis un vignoble et carte de sensibilité '
        "du coût d'ajustement, distincte d'une probabilité de source.</desc>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        _text(
            32.0,
            38.0,
            "Figure 6 — Identification de source : carte de sensibilité du coût",
            size=22,
            weight="bold",
        ),
        _text(
            32.0,
            66.0,
            "Pollution détectée au coin inférieur gauche : fonctionnelle, débit optimal, "
            "vallée du coût.",
            size=16,
        ),
        _text(35.0, 92.0, "A. Dispersion depuis le vignoble", size=16, weight="bold"),
        '<rect x="30" y="98" width="260" height="260" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_a,
        '<rect x="210" y="153" width="25" height="25" fill="none" '
        'stroke="#2e7d32" stroke-width="2"/>',
        *_marques_vent(scenario, PANEL_A_X),
        *_marques_capteurs(scenario, PANEL_A_X),
        *_legende(PANEL_A_X, ETIQUETTES_CHAMP, COULEURS_CHAMP, "#8fb3d9"),
        _text(35.0, 396.0, "kg/m²", size=12),
        _text(330.0, 92.0, "B. Sensibilité du coût, débit ajusté", size=16, weight="bold"),
        '<rect x="325" y="98" width="260" height="260" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_b,
        '<rect x="505" y="153" width="25" height="25" fill="none" '
        'stroke="#2e7d32" stroke-width="2"/>',
        f'<line x1="{_px(PANEL_B_X, 1452.0):.1f}" y1="{_py(1548.0):.1f}" '
        f'x2="{_px(PANEL_B_X, 1548.0):.1f}" y2="{_py(1452.0):.1f}" '
        'stroke="#c0392b" stroke-width="2"/>',
        f'<line x1="{_px(PANEL_B_X, 1452.0):.1f}" y1="{_py(1452.0):.1f}" '
        f'x2="{_px(PANEL_B_X, 1548.0):.1f}" y2="{_py(1548.0):.1f}" '
        'stroke="#c0392b" stroke-width="2"/>',
        _text(_px(PANEL_B_X, 1700.0) - 20.0, _py(1700.0) - 12.0, "vallée", size=12),
        *_legende(PANEL_B_X, ETIQUETTES_COUT, COULEURS_COUT, "#d9a76a"),
        _text(330.0, 396.0, "J/J0", size=12),
        _text(35.0, 428.0, "C. Coupe du coût le long de l'axe du vent", size=16, weight="bold"),
        '<rect x="30" y="437" width="550" height="318" fill="#f6f8f6" '
        'stroke="#d5dbe3" stroke-width="2"/>',
        *panneau_c,
        _text(610.0, 92.0, "Paramètres", size=17, weight="bold"),
        _text(610.0, 120.0, ligne_vent, size=15),
        _text(610.0, 144.0, ligne_diffusivite, size=15),
        _text(610.0, 168.0, ligne_debit, size=15),
        _text(610.0, 192.0, ligne_capteurs, size=15),
        _text(610.0, 216.0, ligne_candidats, size=15),
        _text(610.0, 240.0, ligne_mesures, size=15),
        _text(610.0, 264.0, ligne_cout, size=15),
        _text(610.0, 300.0, "Valeurs clés", size=17, weight="bold"),
        _text(610.0, 328.0, ligne_detection_1, size=15),
        _text(610.0, 352.0, ligne_detection_2, size=15),
        _text(610.0, 376.0, ligne_minimum, size=15),
        _text(610.0, 400.0, ligne_vallee_1, size=15),
        _text(610.0, 424.0, ligne_vallee_2, size=15),
        _text(610.0, 448.0, ligne_decale_1, size=15),
        _text(610.0, 472.0, ligne_decale_2, size=15),
        _text(610.0, 508.0, "Lecture", size=17, weight="bold"),
        *[
            _text(610.0, y, ligne, size=15)
            for y, ligne in zip(
                (536.0, 560.0, 584.0, 608.0, 632.0, 656.0, 680.0, 704.0),
                _lignes_lecture(),
                strict=True,
            )
        ],
        _text(
            30.0,
            766.0,
            "Reconstruction conceptuelle (R1) ; cas synthétique ; pas une "
            "reproduction quantitative du chapitre de 2008 (p. 255).",
            size=13,
        ),
        "</svg>",
    ]
    return "\n".join(elements) + "\n"
