"""Modèle réduit contre EDP : deux résolutions indépendantes, mêmes entrées.

Cette expérience porte la figure 3 du plan de figures du chapitre de 2008
(p. 254) : comparer, sous les mêmes entrées, la solution de similitude
(forme fermée, « modèle réduit ») et une résolution directe de l'équation
de transport-diffusion (schéma numérique, « EDP »). Le problème de
référence est bien posé : transport longue distance 2D horizontal,
U dC/dx = K d2C/dy2, vent uniforme U le long de x, diffusivité
transversale constante K, domaine x >= x_entree avec Dirichlet nul aux
bords latéraux. L'entrée à x_entree est la colonne intégrée en z du
panache de similitude : le niveau proche fournit la quantité d'entrée,
et les deux routes partagent exactement ce champ, ce vent, ce domaine
et les mêmes tranches de comparaison.

La forme fermée est la solution exacte de ce problème de référence à
diffusivité constante ; l'écart mesuré aux nœuds est donc l'erreur de
discrétisation du schéma. Le schéma explicite FTCS avance en x avec un
pas longitudinal dx = U dy^2 / (3 K) : le nombre de Fourier
K dx / (U dy^2) vaut exactement 1/3 sur les trois maillages (2 dy, dy,
dy/2) et l'erreur décroît comme le carré du pas transversal. Le bilan
de masse est contrôlé à chaque tranche : le flux transversal, la
vitesse multipliée par l'intégrale de C dy, doit rester égal au flux
émis ; l'écart résiduel est la queue tronquée par la fenêtre (au moins
quatre écarts-types au terme).

Le livrable est conceptuel (niveau R1) : ni la géométrie, ni les
coefficients, ni les conditions du chapitre ne sont disponibles ; ce
cas synthétique établit la cohérence des deux résolutions, pas une
reproduction. Tous les objets sont immuables et validés à la
construction ; les ``dict`` restent confinés à la frontière d'export
JSON, conformément à la charte qualité du dépôt.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib import metadata
from typing import Literal

NiveauFidelite = Literal["R0", "R1", "R2"]


def _valide_positif(nom: str, valeur: float) -> None:
    """Lève ValueError si le paramètre n'est pas fini et strictement positif."""
    if not math.isfinite(valeur) or valeur <= 0.0:
        msg = f"Le paramètre {nom} doit être fini et strictement positif."
        raise ValueError(msg)


def _est_multiple_exact(valeur: float, pas: float) -> bool:
    """Vrai si valeur est un multiple entier exact de pas en flottant."""
    quotient = valeur / pas
    return quotient == math.floor(quotient)


@dataclass(frozen=True)
class ScenarioComparaisonEDP:
    """Configuration immuable de la comparaison modèle réduit / EDP.

    Attributes:
        vent: vitesse longitudinale uniforme U (m s^-1), strictement positive.
        diffusivite: diffusivité transversale constante K (m^2 s^-1), positive.
        debit: flux de masse total Q (kg s^-1) passé à la colonne d'entrée.
        x_entree: distance sous le vent de l'entrée (m), multiple du pas de tranche.
        x_fin: distance sous le vent de fin de comparaison (m), multiple du pas.
        demi_largeur: demi-largeur transversale W (m), multiple du pas grossier.
        pas_transverse: pas transversal du maillage de référence (m), divise W.
        pas_tranche: espacement des tranches de comparaison (m), divise le domaine.
    """

    vent: float
    diffusivite: float
    debit: float
    x_entree: float
    x_fin: float
    demi_largeur: float
    pas_transverse: float
    pas_tranche: float

    def __post_init__(self) -> None:
        """Valide les paramètres et la compatibilité des trois maillages."""
        _valide_positif("vent", self.vent)
        _valide_positif("diffusivite", self.diffusivite)
        _valide_positif("debit", self.debit)
        _valide_positif("x_entree", self.x_entree)
        _valide_positif("x_fin", self.x_fin)
        _valide_positif("demi_largeur", self.demi_largeur)
        _valide_positif("pas_transverse", self.pas_transverse)
        _valide_positif("pas_tranche", self.pas_tranche)
        if self.x_fin <= self.x_entree:
            msg = "x_fin doit être strictement au-delà de x_entree."
            raise ValueError(msg)
        if not _est_multiple_exact(self.x_entree, self.pas_tranche):
            msg = "x_entree doit être un multiple exact du pas de tranche."
            raise ValueError(msg)
        if not _est_multiple_exact(self.x_fin, self.pas_tranche):
            msg = "x_fin doit être un multiple exact du pas de tranche."
            raise ValueError(msg)
        if not _est_multiple_exact(self.demi_largeur, 2.0 * self.pas_transverse):
            msg = "La demi-largeur doit être un multiple exact du pas grossier."
            raise ValueError(msg)
        if self.demi_largeur < 4.0 * self.ecart_type(self.x_fin):
            msg = "La fenêtre doit couvrir au moins quatre écarts-types au terme."
            raise ValueError(msg)
        for pas in self.maillages():
            if not _est_multiple_exact(self.pas_tranche, self.pas_longitudinal(pas)):
                msg = f"Le pas de tranche doit être un multiple exact du pas longitudinal {pas}."
                raise ValueError(msg)

    def ecart_type(self, x: float) -> float:
        """Écart-type transversal de similitude à la distance sous le vent x (m)."""
        return math.sqrt(2.0 * self.diffusivite * x / self.vent)

    def maillages(self) -> tuple[float, float, float]:
        """Renvoie les pas transversaux des trois maillages, du grossier au fin."""
        return (
            2.0 * self.pas_transverse,
            self.pas_transverse,
            self.pas_transverse / 2.0,
        )

    def pas_longitudinal(self, pas_transverse: float) -> float:
        """Pas longitudinal du schéma explicite (nombre de Fourier 1/3)."""
        return self.vent * pas_transverse * pas_transverse / (3.0 * self.diffusivite)

    def nombre_tranches(self) -> int:
        """Nombre de tranches de comparaison, entrée incluse."""
        intervalles = int(round((self.x_fin - self.x_entree) / self.pas_tranche))
        return intervalles + 1

    def concentration_reduite(self, x: float, y: float) -> float:
        """Colonne intégrée en z du panache de similitude (kg m^-2), forme fermée.

        Args:
            x: distance sous le vent de la source (m) ; nulle en amont.
            y: coordonnée transversale (m).

        Returns:
            La concentration colonne en (x, y) : solution exacte du
            problème de référence à diffusivité constante.
        """
        if x <= 0.0:
            return 0.0
        sigma = self.ecart_type(x)
        lateral = y / sigma
        return (
            self.debit
            / (math.sqrt(2.0 * math.pi) * self.vent * sigma)
            * math.exp(-0.5 * lateral * lateral)
        )


@dataclass(frozen=True)
class TrancheComparaison:
    """Tranche de comparaison : champs numérique et réduit aux mêmes nœuds.

    Attributes:
        x: distance sous le vent de la tranche (m).
        numerique: champ de l'EDP directe aux nœuds transversaux (kg m^-2).
        reduite: champ de la forme fermée aux mêmes nœuds (kg m^-2).
    """

    x: float
    numerique: tuple[float, ...]
    reduite: tuple[float, ...]


@dataclass(frozen=True)
class ResultatMaillage:
    """Normes d'erreur et bilan de masse pour un maillage donné.

    Attributes:
        pas_transverse: pas transversal du maillage (m).
        pas_longitudinal: pas longitudinal du schéma (m).
        nombre_noeuds: nombre de nœuds transversaux.
        l2_relative: norme L2 relative de l'écart aux nœuds des tranches.
        linf_relative: norme L infinie relative de l'écart.
        ecart_flux_numerique: écart relatif maximal du flux de l'EDP.
        ecart_flux_reduit: écart relatif maximal du flux de la forme fermée.
    """

    pas_transverse: float
    pas_longitudinal: float
    nombre_noeuds: int
    l2_relative: float
    linf_relative: float
    ecart_flux_numerique: float
    ecart_flux_reduit: float


@dataclass(frozen=True)
class ResultatComparaison:
    """Résultats immuables de la comparaison modèle réduit / EDP.

    Attributes:
        tranches: tranches du maillage de référence (champs pour la figure).
        maillages: normes par maillage, du grossier au fin.
        l2_reference: norme L2 relative au maillage de référence.
        linf_reference: norme L infinie relative au maillage de référence.
        ratio_grossier: l2 du maillage grossier sur l2 du maillage de référence.
        ratio_fin: l2 du maillage de référence sur l2 du maillage fin.
        ecart_flux_max: écart de flux maximal de l'EDP au maillage de référence.
        ecart_flux_reduit: écart de flux maximal de la forme fermée.
        concentration_max: maximum de la forme fermée aux nœuds (kg m^-2).
        nombre_tranches: nombre de tranches de comparaison.
    """

    tranches: tuple[TrancheComparaison, ...]
    maillages: tuple[ResultatMaillage, ...]
    l2_reference: float
    linf_reference: float
    ratio_grossier: float
    ratio_fin: float
    ecart_flux_max: float
    ecart_flux_reduit: float
    concentration_max: float
    nombre_tranches: int


def _noeuds_transversaux(
    scenario: ScenarioComparaisonEDP,
    pas: float,
) -> list[float]:
    """Renvoie les abscisses transversales des nœuds d'un maillage."""
    nombre = int(round(2.0 * scenario.demi_largeur / pas)) + 1
    return [-scenario.demi_largeur + i * pas for i in range(nombre)]


def _flux_transversal(
    scenario: ScenarioComparaisonEDP,
    valeurs: tuple[float, ...],
    pas: float,
) -> float:
    """Flux massique transversal, vitesse fois l'intégrale de C dy (kg s^-1)."""
    total = 0.0
    for i in range(len(valeurs) - 1):
        total += 0.5 * (valeurs[i] + valeurs[i + 1]) * pas
    return scenario.vent * total


def _pas_explicite(champ: list[float], coefficient: float) -> list[float]:
    """Avance le champ d'un pas longitudinal du schéma FTCS (Dirichlet nul)."""
    suivant: list[float] = [0.0] * len(champ)
    for i in range(1, len(champ) - 1):
        suivant[i] = champ[i] + coefficient * (champ[i + 1] - 2.0 * champ[i] + champ[i - 1])
    return suivant


def resoudre_edp(
    scenario: ScenarioComparaisonEDP,
    pas_transverse: float,
) -> tuple[TrancheComparaison, ...]:
    """Résout l'EDP directe par le schéma explicite, aux tranches de comparaison.

    Args:
        scenario: configuration immuable de la comparaison.
        pas_transverse: pas transversal du maillage (m).

    Returns:
        Les tranches de comparaison : le champ numérique et la forme
        fermée aux mêmes nœuds, de l'entrée au terme.
    """
    noeuds = _noeuds_transversaux(scenario, pas_transverse)
    dx = scenario.pas_longitudinal(pas_transverse)
    coefficient = scenario.diffusivite * dx / (scenario.vent * pas_transverse * pas_transverse)
    pas_par_tranche = int(round(scenario.pas_tranche / dx))
    champ = [scenario.concentration_reduite(scenario.x_entree, y) for y in noeuds]
    tranches: list[TrancheComparaison] = []
    tranches.append(
        TrancheComparaison(
            x=scenario.x_entree,
            numerique=tuple(champ),
            reduite=tuple(scenario.concentration_reduite(scenario.x_entree, y) for y in noeuds),
        )
    )
    for i in range(scenario.nombre_tranches() - 1):
        for _ in range(pas_par_tranche):
            champ = _pas_explicite(champ, coefficient)
        x = scenario.x_entree + (i + 1) * scenario.pas_tranche
        tranches.append(
            TrancheComparaison(
                x=x,
                numerique=tuple(champ),
                reduite=tuple(scenario.concentration_reduite(x, y) for y in noeuds),
            )
        )
    return tuple(tranches)


def _normes_maillage(
    scenario: ScenarioComparaisonEDP,
    tranches: tuple[TrancheComparaison, ...],
    pas_transverse: float,
) -> ResultatMaillage:
    """Calcule les normes d'erreur et le bilan de masse d'un maillage."""
    somme_ecarts = 0.0
    somme_reduit = 0.0
    ecart_max = 0.0
    reduit_max = 0.0
    ecart_flux_numerique = 0.0
    ecart_flux_reduit = 0.0
    for tranche in tranches:
        for i in range(len(tranche.numerique)):
            ecart = tranche.numerique[i] - tranche.reduite[i]
            somme_ecarts += ecart * ecart
            somme_reduit += tranche.reduite[i] * tranche.reduite[i]
            ecart_max = max(ecart_max, abs(ecart))
            reduit_max = max(reduit_max, tranche.reduite[i])
        flux_numerique = _flux_transversal(scenario, tranche.numerique, pas_transverse)
        flux_reduit = _flux_transversal(scenario, tranche.reduite, pas_transverse)
        ecart_flux_numerique = max(
            ecart_flux_numerique,
            abs(flux_numerique - scenario.debit) / scenario.debit,
        )
        ecart_flux_reduit = max(
            ecart_flux_reduit,
            abs(flux_reduit - scenario.debit) / scenario.debit,
        )
    l2 = math.sqrt(somme_ecarts) / math.sqrt(somme_reduit)
    linf = ecart_max / reduit_max
    return ResultatMaillage(
        pas_transverse=pas_transverse,
        pas_longitudinal=scenario.pas_longitudinal(pas_transverse),
        nombre_noeuds=len(tranches[0].numerique),
        l2_relative=l2,
        linf_relative=linf,
        ecart_flux_numerique=ecart_flux_numerique,
        ecart_flux_reduit=ecart_flux_reduit,
    )


def comparer_scenario(scenario: ScenarioComparaisonEDP) -> ResultatComparaison:
    """Compare le modèle réduit et l'EDP directe aux nœuds de trois maillages.

    Args:
        scenario: configuration immuable de la comparaison.

    Returns:
        Les tranches du maillage de référence, les normes des trois
        maillages (grossier, référence, fin), les rapports de
        convergence et le bilan de masse du maillage de référence.
    """
    resultats: list[ResultatMaillage] = []
    tranches_reference: tuple[TrancheComparaison, ...] | None = None
    for pas in scenario.maillages():
        tranches = resoudre_edp(scenario, pas)
        resultats.append(_normes_maillage(scenario, tranches, pas))
        if pas == scenario.pas_transverse:
            tranches_reference = tranches
    if tranches_reference is None:
        msg = "Le maillage de référence est absent de la liste des maillages."
        raise ValueError(msg)
    grossier, reference, fin = resultats
    concentration_max = 0.0
    for tranche in tranches_reference:
        for valeur in tranche.reduite:
            concentration_max = max(concentration_max, valeur)
    return ResultatComparaison(
        tranches=tranches_reference,
        maillages=tuple(resultats),
        l2_reference=reference.l2_relative,
        linf_reference=reference.linf_relative,
        ratio_grossier=grossier.l2_relative / reference.l2_relative,
        ratio_fin=reference.l2_relative / fin.l2_relative,
        ecart_flux_max=reference.ecart_flux_numerique,
        ecart_flux_reduit=reference.ecart_flux_reduit,
        concentration_max=concentration_max,
        nombre_tranches=len(tranches_reference),
    )


SCENARIO_DEFAUT = ScenarioComparaisonEDP(
    vent=3.0,
    diffusivite=4.0,
    debit=2.0,
    x_entree=300.0,
    x_fin=2000.0,
    demi_largeur=300.0,
    pas_transverse=10.0,
    pas_tranche=100.0,
)


@dataclass(frozen=True)
class ManifesteComparaisonEDP:
    """Manifeste immuable reliant l'expérience à sa spécification et ses limites.

    Attributes:
        identifiant: identifiant stable de l'expérience.
        niveau_fidelite: niveau de fidélité (R0 schéma, R1 reconstruction, R2 reproduction).
        source: référence documentée de la définition (DOI, pages).
        description: objet de l'expérience en une phrase.
        hypothese: hypothèses explicites de l'expérience.
        limites: limites explicites du livrable.
        scenario: configuration typée de l'expérience.
        resultat: résultats numériques typés de l'expérience.
        version_code: version du package au moment de la construction.
        commande: commande de reproduction.
    """

    identifiant: str
    niveau_fidelite: NiveauFidelite
    source: str
    description: str
    hypothese: tuple[str, ...]
    limites: tuple[str, ...]
    scenario: ScenarioComparaisonEDP
    resultat: ResultatComparaison
    version_code: str
    commande: str

    def vers_dict(self) -> dict[str, object]:
        """Exporte le manifeste en dictionnaire (frontière JSON uniquement)."""
        scenario = self.scenario
        return {
            "identifiant": self.identifiant,
            "niveau_fidelite": self.niveau_fidelite,
            "source": self.source,
            "description": self.description,
            "hypothese": list(self.hypothese),
            "limites": list(self.limites),
            "version_code": self.version_code,
            "commande": self.commande,
            "parametres": {
                "vent": scenario.vent,
                "diffusivite": scenario.diffusivite,
                "debit": scenario.debit,
                "x_entree": scenario.x_entree,
                "x_fin": scenario.x_fin,
                "demi_largeur": scenario.demi_largeur,
                "pas_transverse": scenario.pas_transverse,
                "pas_tranche": scenario.pas_tranche,
            },
            "resultats": {
                "l2_reference": self.resultat.l2_reference,
                "linf_reference": self.resultat.linf_reference,
                "ratio_grossier": self.resultat.ratio_grossier,
                "ratio_fin": self.resultat.ratio_fin,
                "ecart_flux_max": self.resultat.ecart_flux_max,
                "ecart_flux_reduit": self.resultat.ecart_flux_reduit,
                "concentration_max": self.resultat.concentration_max,
                "nombre_tranches": self.resultat.nombre_tranches,
            },
        }


def construire_manifeste(
    scenario: ScenarioComparaisonEDP,
    resultat: ResultatComparaison,
) -> ManifesteComparaisonEDP:
    """Assemble le manifeste de la comparaison modèle réduit / EDP.

    Args:
        scenario: configuration validée de l'expérience.
        resultat: résultats calculés par ``comparer_scenario``.

    Returns:
        Le manifeste immuable, prêt pour la figure, l'export ou l'archivage.
    """
    try:
        version_code = metadata.version("jdriftx")
    except metadata.PackageNotFoundError:
        version_code = "non-installe"
    description_manifeste = (
        "Modèle réduit contre EDP : deux résolutions indépendantes, mêmes entrées."
    )
    return ManifesteComparaisonEDP(
        identifiant="jdriftx-modele-reduit-edp-001",
        niveau_fidelite="R1",
        source=(
            "Brun, J.-M. & Mohammadi, B. (2008), « Reduced-Order Modelling of "
            "Dispersion », chapitre 14, p. 254, DOI 10.1007/978-1-4020-8758-5_14."
        ),
        description=description_manifeste,
        hypothese=(
            "Vent uniforme U le long de x, diffusivité transversale constante K.",
            "L'entrée à x_entree est la colonne intégrée en z du panache de "
            "similitude : le niveau proche fournit la quantité d'entrée.",
            "Dirichlet nul aux bords latéraux : la queue tronquée par la fenêtre "
            "est documentée (au moins quatre écarts-types au terme).",
            "Les deux routes partagent exactement l'entrée, le vent, le domaine "
            "et les tranches de comparaison.",
        ),
        limites=(
            "Cas synthétique : ni géométrie, ni coefficients, ni conditions du chapitre de 2008.",
            "La forme fermée est exacte pour ce problème à diffusivité constante ; "
            "l'écart mesuré est l'erreur de discrétisation du schéma.",
            "Le transport longue distance est 2D horizontal ; la dimension "
            "verticale est résumée par la colonne d'entrée.",
            "Ne constitue ni une validation de la calibration de Briggs, ni une "
            "reproduction quantitative du chapitre.",
        ),
        scenario=scenario,
        resultat=resultat,
        version_code=version_code,
        commande=(
            "uv run python -c 'from jdriftx.experiences.modele_reduit_edp import "
            "SCENARIO_DEFAUT, comparer_scenario; print(comparer_scenario(SCENARIO_DEFAUT))'"
        ),
    )
