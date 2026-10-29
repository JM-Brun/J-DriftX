"""Tests de l'EDP transitoire du puff (marginale transverse).

Couverture (issue #232) : calibration fine et grossière de la marche en
temps, entrée partagée avec la marginale fermée, comparaison dirigée sous
les seuils calibrés, convergence fine/grossier, rejets explicites (classe
INVERSE, fenêtres quatre écarts-types, passages non multiples, points
hors arcs), cohérence des instants avec le temps dirigé de l'étape 6,
coûts mesurés séparément, immuabilité, manifeste étiqueté, export
JSON-natif, modèle de diffusion injectable.
"""

from __future__ import annotations

import dataclasses
import json
import math

import numpy as np
import pytest
from pydantic import ValidationError

import jdriftx.experiences.transitoire_puff as module_transitoire
from jdriftx.benchmarks.cas import CAS_S0_DEFAUT, PointMesure
from jdriftx.experiences.evaluation_puff import PUFF_DEFAUT, SourceImpulsionnelle, temps_dirige
from jdriftx.experiences.reference_independante import (
    DIFFUSION_BRIGGS,
    PARAMETRES_EDP_DEFAUT,
    CoefficientsDiffusion,
    ParametresEdp,
)
from jdriftx.experiences.transitoire_puff import (
    ComparaisonTransitoire,
    ManifesteTransitoire,
    SolutionTransitoire,
    comparer_transitoire,
    construire_manifeste,
    resoudre_transitoire,
)
from jdriftx.similitude import sigma_y, sigma_z


@pytest.fixture(scope="module")
def arcs() -> tuple[float, ...]:
    """Arcs de passage du cas S0 figé (docs/48 §2.2)."""
    return CAS_S0_DEFAUT.arcs


@pytest.fixture(scope="module")
def grille() -> tuple[PointMesure, ...]:
    """Grille de prélèvements du cas S0 figé (12 points)."""
    return CAS_S0_DEFAUT.points()


@pytest.fixture(scope="module")
def solution(arcs: tuple[float, ...]) -> SolutionTransitoire:
    """Solution transitoire de la grille fine, calculée une seule fois."""
    return resoudre_transitoire(PUFF_DEFAUT, arcs)


@pytest.fixture(scope="module")
def comparaison(arcs: tuple[float, ...], grille: tuple[PointMesure, ...]) -> ComparaisonTransitoire:
    """Comparaison de la grille fine, calculée une seule fois."""
    return comparer_transitoire(PUFF_DEFAUT, arcs, grille)


@pytest.fixture(scope="module")
def grossier(arcs: tuple[float, ...], grille: tuple[PointMesure, ...]) -> ComparaisonTransitoire:
    """Comparaison de la grille grossière (contrôle de convergence)."""
    parametres = ParametresEdp(5.0, 4.0, 340.0, 240.0)
    return comparer_transitoire(PUFF_DEFAUT, arcs, grille, parametres)


@pytest.fixture(scope="module")
def manifeste(comparaison: ComparaisonTransitoire) -> ManifesteTransitoire:
    """Manifeste étiqueté de l'EDP transitoire, construit une seule fois."""
    return construire_manifeste(comparaison)


def test_les_parametres_defaut_couvrent_quatre_ecarts_types(arcs: tuple[float, ...]) -> None:
    """La grille fine couvre quatre écarts-types du puff au dernier passage."""
    # Given — les paramètres par défaut et le dernier arc du cas S0 figé.
    dernier_arc = arcs[-1]
    # Then — la fenêtre latérale couvre 4 sigma_y au dernier passage.
    assert PARAMETRES_EDP_DEFAUT.demi_largeur_y >= 4.0 * float(sigma_y(dernier_arc, "C"))
    # Then — la colonne couvre 4 sigma_z, sans hauteur de source (puff pair en z).
    assert PARAMETRES_EDP_DEFAUT.hauteur_max >= 4.0 * float(sigma_z(dernier_arc, "C"))


def test_la_marche_fine_est_calibree(solution: SolutionTransitoire) -> None:
    """Pas de temps (100/3)/1024 s, 7168 pas, instants aux passages, grille paire."""
    # Given — la solution transitoire de la grille fine.
    # Then — le pas de temps est réduit en puissances de deux (Fourier).
    assert solution.pas_temps == (100.0 / 3.0) / 1024.0
    # Then — 7168 pas de marche entre l'entrée et le dernier passage.
    nb_pas = (solution.instants[-1].t - solution.t_entree) / solution.pas_temps
    assert nb_pas == pytest.approx(7168.0)
    # Then — instantanés prélevés à l'entrée puis à chaque arc de passage.
    attendus = [100.0 / 3.0, 200.0 / 3.0, 400.0 / 3.0, 800.0 / 3.0]
    assert [instant.t for instant in solution.instants] == attendus
    # Then — grille symétrique latéralement, du sol au sommet de fenêtre.
    assert solution.abscisses_y.size == 273
    assert solution.abscisses_z.size == 121
    assert np.array_equal(solution.abscisses_y, -solution.abscisses_y[::-1])


def test_l_entree_est_partagee_avec_la_marginale_fermee(
    solution: SolutionTransitoire,
) -> None:
    """La condition d'entrée est exactement la marginale fermée, bords nuls."""
    # Given — la solution et la marginale fermée évaluée à l'instant d'entrée.
    mailles_y, mailles_z = np.meshgrid(solution.abscisses_y, solution.abscisses_z, indexing="ij")
    distance = PUFF_DEFAUT.u * solution.t_entree
    sy = sigma_y(distance, PUFF_DEFAUT.classe)
    sz = sigma_z(distance, PUFF_DEFAUT.classe)
    attendu_brut = (
        PUFF_DEFAUT.masse
        / (2.0 * np.pi * sy * sz)
        * np.exp(-(mailles_y**2) / (2.0 * sy**2))
        * np.exp(-(mailles_z**2) / (2.0 * sz**2))
    )
    attendu = np.asarray(attendu_brut, dtype=float)
    attendu[0, :] = 0.0
    attendu[-1, :] = 0.0
    attendu[:, -1] = 0.0
    # Then — l'instantané d'entrée coïncide exactement avec la marginale fermée.
    assert np.array_equal(solution.instants[0].champ, attendu)


def test_la_comparaison_fine_est_calibree(comparaison: ComparaisonTransitoire) -> None:
    """FAC2 parfait, NMSE sous 1e-4, écarts et masse bornés (grille fine)."""
    # Then — toutes les prédictions EDP sont dans un facteur 2.
    assert comparaison.fac2 == 1.0
    # Then — l'erreur quadratique normalisée reste sous 1e-4.
    assert 0.0 < comparaison.nmse < 1e-4
    # Then — l'écart relatif maximal reste sous 1,2 % (interpolation bilinéaire).
    assert 0.0 < comparaison.ecart_relatif_max < 1.2e-2
    # Then — la masse de la marginale est conservée à 5e-4 (troncature 4 sigma).
    assert 0.0 <= comparaison.ecart_masse_max < 5e-4
    # Then — les 12 points du cas S0 figé sont couverts, aux instants exacts.
    assert len(comparaison.points) == 12
    attendus = (100.0 / 3.0, 200.0 / 3.0, 400.0 / 3.0, 800.0 / 3.0)
    assert comparaison.instants == attendus


def test_la_grille_grossiere_reste_dans_les_seuils(grossier: ComparaisonTransitoire) -> None:
    """La grille grossière reste dans les seuils : FAC2, NMSE et écarts bornés."""
    # Given — la comparaison grossière (pas doublés en transverse et vertical).
    # Then — toutes les prédictions EDP restent dans un facteur 2.
    assert grossier.fac2 == 1.0
    # Then — l'erreur quadratique normalisée reste sous 2e-3.
    assert 0.0 < grossier.nmse < 2e-3
    # Then — l'écart relatif maximal reste sous 6 %.
    assert 0.0 < grossier.ecart_relatif_max < 6e-2


def test_affiner_la_grille_reduit_l_erreur(
    comparaison: ComparaisonTransitoire, grossier: ComparaisonTransitoire
) -> None:
    """Affiner la grille divise l'erreur quadratique d'un facteur supérieur à 20."""
    # Given — les comparaisons fine et grossière de la même grille de points.
    # When — les erreurs quadratiques normalisées sont confrontées.
    # Then — la grille fine divise l'erreur d'un facteur supérieur à 20.
    assert grossier.nmse > 20.0 * comparaison.nmse


def test_la_forme_inverse_de_sigma_z_est_rejetee(arcs: tuple[float, ...]) -> None:
    """Les classes E et F (sigma_z INVERSE) sont refusées sans ambiguïté."""
    # Given — un puff de classe E (forme INVERSE de sigma_z), arcs du cas S0.
    source = SourceImpulsionnelle(masse=1.0, u=3.0, classe="E")
    # Then — la résolution lève une ValueError explicite.
    with pytest.raises(ValueError, match="INVERSE"):
        resoudre_transitoire(source, arcs)


def test_une_fenetre_insuffisante_est_rejetee(arcs: tuple[float, ...]) -> None:
    """La fenêtre doit couvrir quatre écarts-types du puff, sans hauteur source."""
    # Given — des fenêtres trop étroites pour le dernier passage.
    etroite = ParametresEdp(2.5, 2.0, 300.0, 240.0)
    basse = ParametresEdp(2.5, 2.0, 340.0, 200.0)
    # Then — la couverture latérale est exigée au dernier passage.
    with pytest.raises(ValueError, match="écarts-types du puff"):
        resoudre_transitoire(PUFF_DEFAUT, arcs, etroite)
    # Then — la couverture verticale est exigée au dernier passage.
    with pytest.raises(ValueError, match="écarts-types verticaux"):
        resoudre_transitoire(PUFF_DEFAUT, arcs, basse)


def test_les_passages_non_multiples_sont_rejetes() -> None:
    """Les passages doivent être multiples entiers du pas de temps."""
    # Given — un arc de passage hors grille de pas (210 m entre 100 et 200).
    # When — la résolution est demandée sur ces arcs.
    # Then — la divisibilité depuis l'entrée est exigée.
    with pytest.raises(ValueError, match="multiples entiers du pas de temps"):
        resoudre_transitoire(PUFF_DEFAUT, (100.0, 210.0))


def test_un_point_hors_des_arcs_est_rejete(arcs: tuple[float, ...]) -> None:
    """Un point de comparaison hors arc de passage est rejeté."""
    # Given — un point de mesure entre deux arcs de passage.
    hors_arc = PointMesure(x=150.0, y=0.0, z=1.5)
    # Then — la comparaison refuse le point.
    with pytest.raises(ValueError, match="arc de passage"):
        comparer_transitoire(PUFF_DEFAUT, arcs, (hors_arc,))


def test_les_instants_rejoignent_le_temps_dirige(
    arcs: tuple[float, ...],
    comparaison: ComparaisonTransitoire,
) -> None:
    """Les instants de passage coïncident avec le temps dirigé de l'étape 6."""
    # Given — l'axe du puff aux arcs de passage (temps dirigé de la note 53).
    # When — les temps dirigés sont confrontés aux instants de la solution.
    # Then — chaque instant de passage vaut tau = x/u (pseudo-distance uniforme).
    for arc in arcs:
        tau = temps_dirige(PUFF_DEFAUT, PointMesure(x=arc, y=0.0, z=1.5))
        assert math.isclose(tau, arc / PUFF_DEFAUT.u, rel_tol=1e-12)
        assert any(math.isclose(tau, t, rel_tol=1e-12) for t in comparaison.instants)


def test_les_couts_sont_mesures_separement(comparaison: ComparaisonTransitoire) -> None:
    """Coûts finis et positifs ; la route EDP coûte plus que la fermée."""
    # Then — le coût de la route fermée est fini et positif.
    assert math.isfinite(comparaison.cout_ferme_s)
    assert comparaison.cout_ferme_s > 0.0
    # Then — le coût de la route EDP est fini et positif.
    assert math.isfinite(comparaison.cout_edp_s)
    assert comparaison.cout_edp_s > 0.0
    # Then — la marche FTCS (7168 pas) coûte plus que 12 évaluations fermées.
    assert comparaison.cout_edp_s > comparaison.cout_ferme_s


def test_les_resultats_sont_immuables(
    solution: SolutionTransitoire, comparaison: ComparaisonTransitoire
) -> None:
    """La solution et la comparaison sont gelées après construction."""
    # Then — les instantanés (dataclasses gelées) refusent la mutation.
    with pytest.raises(dataclasses.FrozenInstanceError):
        solution.instants[0].t = 0.0
    # Then — les modèles Pydantic gelés refusent la mutation.
    with pytest.raises(ValidationError):
        comparaison.fac2 = 0.5


def test_le_manifeste_est_etiquete(manifeste: ManifesteTransitoire) -> None:
    """Le manifeste porte l'identifiant, le niveau et l'étiquetage figés."""
    # Then — l'identifiant et le niveau de fidélité sont explicites.
    assert manifeste.identifiant == "jdriftx-transitoire-puff-001"
    assert manifeste.niveau_fidelite == "R1"
    # Then — la source et l'héritage sont étiquetés (aucune source historique).
    assert "DOI 10.1007/978-1-4020-8758-5_14" in manifeste.source
    assert "note 53" in manifeste.heritage_documentaire
    # Then — l'extension est la seconde extension conditionnelle (docs/47 §5).
    assert manifeste.extension.startswith("EDP transitoire du puff")
    # Then — les limites portent les garde-fous : validation, longitudinal, noyau.
    limites = " ".join(manifeste.limites)
    assert "pas une validation physique" in limites
    assert "structure longitudinale" in limites
    assert "symétrique en z" in limites


def test_l_export_frontiere_est_json_natif(manifeste: ManifesteTransitoire) -> None:
    """L'export frontière est JSON-natif : listes, pas de tuples ni de tableaux."""
    # Given — le manifeste étiqueté de la comparaison fine.
    # When — le manifeste est exporté à la frontière JSON.
    export = manifeste.vers_dict()
    # Then — l'export est sérialisable en JSON standard.
    assert json.dumps(export)
    # Then — les tuples deviennent des listes JSON-natives.
    assert isinstance(export["limites"], list)
    comparaison = export["comparaison"]
    assert isinstance(comparaison["instants"], list)
    assert len(comparaison["instants"]) == 4
    # Then — les 12 points du cas S0 figé sont exportés avec leur ratio.
    assert isinstance(comparaison["points"], list)
    assert len(comparaison["points"]) == 12
    assert comparaison["points"][0]["ratio"] > 0.0


def test_la_version_non_installee_est_supportee(
    comparaison: ComparaisonTransitoire,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sans package installé, le manifeste porte « non-installe » sans échouer."""
    # Given — un environnement où les métadonnées d'installation sont absentes.
    monkeypatch.setattr(
        module_transitoire.metadata,
        "version",
        lambda nom: (_ for _ in ()).throw(module_transitoire.metadata.PackageNotFoundError(nom)),
    )
    # When — le manifeste est construit.
    manifeste = construire_manifeste(comparaison)
    # Then — la version est explicitement « non-installe ».
    assert manifeste.version_code == "non-installe"


def test_le_modele_de_diffusion_est_injectable() -> None:
    """Un modèle alternatif change la marche, pas l'entrée partagée."""
    # Given — un puff réduit à deux arcs et un modèle transverse doublé (jouet).

    class ModeleTransverseDouble:
        """Modèle jouet : diffusion transverse doublée, verticale inchangée."""

        def coefficients(self, classe: str, x: float) -> CoefficientsDiffusion:
            base = DIFFUSION_BRIGGS.coefficients(classe, x)
            return CoefficientsDiffusion(base.a_y * 2.0, base.d_y, base.b_z, base.d_z)

    parametres = ParametresEdp(5.0, 4.0, 340.0, 240.0)
    # When — la même géométrie est résolue avec le modèle doublé et Briggs.
    double = resoudre_transitoire(PUFF_DEFAUT, (100.0, 200.0), parametres, ModeleTransverseDouble())
    reference = resoudre_transitoire(PUFF_DEFAUT, (100.0, 200.0), parametres)
    # Then — le pas de temps est réduit (Fourier transverse doublé).
    assert double.pas_temps < reference.pas_temps
    # Then — l'entrée partagée ne dépend pas du modèle de diffusion.
    assert np.array_equal(double.instants[0].champ, reference.instants[0].champ)
    # Then — le dernier instantané diffère : le point d'extension est effectif.
    assert not np.array_equal(double.instants[-1].champ, reference.instants[-1].champ)
