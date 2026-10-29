"""Tests de la comparaison à référence indépendante (étape 5 de l'issue #232)."""

import json
import math

import numpy as np
import pytest
from pydantic import ValidationError

import jdriftx.experiences.reference_independante as module_reference
from jdriftx.benchmarks.cas import CAS_S0_DEFAUT, CasS0
from jdriftx.contrats import PanacheGaussien
from jdriftx.experiences.reference_independante import (
    PARAMETRES_EDP_DEFAUT,
    ComparaisonReference,
    ParametresEdp,
    PointComparaison,
    SolutionEdp,
    _pas_longitudinal,
    comparer_reference,
    construire_manifeste,
    derivee_sigma_carre,
    resoudre_edp,
)
from jdriftx.similitude import sigma_y, sigma_z
from jdriftx.source import SourcePanache


@pytest.fixture(scope="module")
def comparaison() -> ComparaisonReference:
    """Comparaison de la grille fine, calculée une seule fois."""
    return comparer_reference(CAS_S0_DEFAUT)


@pytest.fixture(scope="module")
def solution() -> SolutionEdp:
    """Solution EDP de la grille fine, calculée une seule fois."""
    return resoudre_edp(CAS_S0_DEFAUT)


@pytest.fixture(scope="module")
def grossier() -> ComparaisonReference:
    """Comparaison de la grille grossière (contrôle de convergence)."""
    return comparer_reference(CAS_S0_DEFAUT, ParametresEdp(5.0, 4.0, 340.0, 240.0))


def test_les_parametres_defaut_couvrent_quatre_ecarts_types() -> None:
    """La grille fine couvre quatre écarts-types au dernier arc (classe C)."""
    # Given — les paramètres par défaut et le dernier arc du cas S0 figé.
    dernier_arc = CAS_S0_DEFAUT.arcs[-1]
    # Then — la fenêtre latérale couvre 4 sigma_y au dernier arc.
    assert PARAMETRES_EDP_DEFAUT.demi_largeur_y >= 4.0 * float(sigma_y(dernier_arc, "C"))
    # Then — la colonne couvre la hauteur source plus 4 sigma_z.
    seuil_z = CAS_S0_DEFAUT.source.hauteur + 4.0 * float(sigma_z(dernier_arc, "C"))
    assert PARAMETRES_EDP_DEFAUT.hauteur_max >= seuil_z


def test_la_grille_fine_est_calibree(solution: SolutionEdp) -> None:
    """Pas longitudinal 100/1024 m, 7168 pas, tranches aux arcs, grille paire."""
    # Given — la solution EDP de la grille fine.
    # Then — le pas longitudinal est réduit en puissances de deux (Fourier).
    assert solution.pas_longitudinal == 100.0 / 1024.0
    # Then — 7168 pas de marche entre l'entrée et le dernier arc.
    nb_pas = (solution.tranches[-1].x - solution.x_entree) / solution.pas_longitudinal
    assert nb_pas == pytest.approx(7168.0)
    # Then — tranches prélevées à l'entrée puis à chaque arc de mesure.
    attendus = [100.0, 200.0, 400.0, 800.0]
    assert [tranche.x for tranche in solution.tranches] == attendus
    # Then — grille symétrique latéralement, du sol au sommet de fenêtre.
    assert solution.abscisses_y.size == 273
    assert solution.abscisses_z.size == 121
    assert np.array_equal(solution.abscisses_y, -solution.abscisses_y[::-1])
    assert solution.abscisses_z[0] == pytest.approx(0.0)


def test_l_entree_est_partagee_avec_la_forme_fermee(solution: SolutionEdp) -> None:
    """La condition d'entrée est exactement la solution fermée du contrat."""
    # Given — le contrat de concentration partagé, sur la grille de la solution.
    mailles_y, mailles_z = np.meshgrid(solution.abscisses_y, solution.abscisses_z, indexing="ij")
    attendu = np.asarray(
        PanacheGaussien(source=CAS_S0_DEFAUT.source).concentration(
            solution.x_entree, mailles_y, mailles_z
        ),
        dtype=float,
    )
    attendu[0, :] = 0.0
    attendu[-1, :] = 0.0
    attendu[:, -1] = 0.0
    # Then — la tranche d'entrée coïncide exactement avec le contrat partagé.
    assert np.array_equal(solution.tranches[0].champ, attendu)


def test_la_comparaison_couvre_la_grille_du_cas(
    comparaison: ComparaisonReference,
) -> None:
    """Les 12 points du cas S0 figé sont comparés, tous positifs et finis."""
    # Given — la grille de prélèvements du cas S0 figé (docs/48 §2.2).
    attendus = {
        (arc, y, CAS_S0_DEFAUT.z_mesure)
        for arc in CAS_S0_DEFAUT.arcs
        for y in CAS_S0_DEFAUT.positions_laterales
    }
    observes = {(p.x, p.y, p.z) for p in comparaison.points}
    # Then — les 12 points attendus sont couverts, exactement.
    assert observes == attendus
    # Then — concentrations strictement positives et ratios finis.
    for point in comparaison.points:
        assert point.fermee > 0.0
        assert point.edp > 0.0
        assert math.isfinite(point.edp)
        assert point.ratio > 0.0


def test_les_deux_routes_coincident_sur_la_grille(
    comparaison: ComparaisonReference,
) -> None:
    """FAC2 parfait, NMSE sous 1e-3, écarts bornés sur les 12 points."""
    # Given — la comparaison calibrée de la grille fine.
    # Then — toutes les prédictions EDP sont dans un facteur 2.
    assert comparaison.fac2 == 1.0
    # Then — l'erreur quadratique normalisée reste sous 1e-3.
    assert 0.0 < comparaison.nmse < 1e-3
    # Then — l'écart relatif maximal reste sous 2 % (arc d'entrée).
    assert 0.0 < comparaison.ecart_relatif_max < 0.02
    # Then — le flux est conservé à 1e-3 près aux arcs (troncature 4 sigma).
    assert 0.0 < comparaison.ecart_flux_max < 1e-3


def test_le_premier_arc_restitue_l_entree_partagee(
    comparaison: ComparaisonReference,
) -> None:
    """Au premier arc, l'écart ne vient que de l'interpolation verticale."""
    # Given — les trois points du premier arc (100 m).
    ratios = [p.ratio for p in comparaison.points if p.x == 100.0]
    # Then — trois points, tous dans un facteur de 1 % de la fermée.
    assert len(ratios) == 3
    for ratio in ratios:
        assert 0.99 <= ratio <= 1.01


def test_la_symetrie_laterale_est_exacte(
    comparaison: ComparaisonReference,
) -> None:
    """La symétrie en y du panache est préservée à l'identique par le schéma."""
    # Given — les comparaisons groupées par arc, puis par position latérale.
    par_arc: dict[float, dict[float, PointComparaison]] = {}
    for point in comparaison.points:
        par_arc.setdefault(point.x, {})[point.y] = point
    # Then — à chaque arc, y = -50 m et y = +50 m coïncident exactement.
    for par_y in par_arc.values():
        assert -50.0 in par_y
        assert 50.0 in par_y
        assert par_y[-50.0].edp == pytest.approx(par_y[50.0].edp, rel=1e-14)
        assert par_y[-50.0].fermee == par_y[50.0].fermee


def test_affiner_la_grille_reduit_l_erreur(
    comparaison: ComparaisonReference, grossier: ComparaisonReference
) -> None:
    """La grille grossière reste dans les seuils et converge vers la fine."""
    # Given — la comparaison grossière (pas doublés en transverse et vertical).
    # Then — son pas longitudinal est 100/256 m (Fourier inchangé).
    assert _pas_longitudinal("C", 100.0, 800.0, grossier.parametres) == 100.0 / 256.0
    # Then — elle reste dans les seuils de reprise des métriques.
    assert grossier.fac2 == 1.0
    assert 0.0 < grossier.ecart_relatif_max < 0.05
    # Then — affiner la grille divise l'erreur quadratique (convergence).
    assert grossier.nmse > comparaison.nmse


def test_la_derivee_rejoint_la_parametrisation_partagee() -> None:
    """La dérivée exacte de sigma² coïncide avec la paramétrisation partagée."""
    # Given — un pas de différenciation centrale et la classe C (Briggs rural).
    h = 0.01
    for x in (50.0, 100.0, 200.0, 400.0, 800.0):
        # When — la dérivée exacte est confrontée aux différences finies.
        dfy = (float(sigma_y(x + h, "C")) ** 2 - float(sigma_y(x - h, "C")) ** 2) / (2.0 * h)
        assert derivee_sigma_carre(x, 0.11, 0.0001) == pytest.approx(dfy, rel=1e-6)
        dfz = (float(sigma_z(x + h, "C")) ** 2 - float(sigma_z(x - h, "C")) ** 2) / (2.0 * h)
        assert derivee_sigma_carre(x, 0.08, 0.0002) == pytest.approx(dfz, rel=1e-6)


def test_la_forme_inverse_de_sigma_z_est_rejetee() -> None:
    """Les classes E et F (sigma_z INVERSE) sont refusées sans ambiguïté."""
    # Given — un cas de classe E (forme INVERSE de sigma_z), grille minimale.
    cas = CasS0(
        source=SourcePanache(debit=2.0, u=3.0, classe="E", hauteur=1.0),
        arcs=(100.0, 200.0),
        positions_laterales=(0.0,),
        z_mesure=1.5,
    )
    # Then — la résolution lève une ValueError explicite.
    with pytest.raises(ValueError, match="INVERSE"):
        resoudre_edp(cas)


def test_une_fenetre_insuffisante_est_rejetee() -> None:
    """La fenêtre doit couvrir quatre écarts-types, en largeur et en hauteur."""
    # Given — des fenêtres trop étroites pour le dernier arc du cas figé.
    etroite = ParametresEdp(2.5, 2.0, 50.0, 240.0)
    basse = ParametresEdp(2.5, 2.0, 340.0, 50.0)
    # Then — la résolution refuse les deux configurations.
    with pytest.raises(ValueError, match="écarts-types"):
        resoudre_edp(CAS_S0_DEFAUT, etroite)
    with pytest.raises(ValueError, match="écarts-types"):
        resoudre_edp(CAS_S0_DEFAUT, basse)


@pytest.mark.parametrize(
    ("pas_y", "pas_z", "demi_largeur", "hauteur"),
    [
        (0.0, 2.0, 340.0, 240.0),
        (2.5, -1.0, 340.0, 240.0),
        (2.5, 2.0, 0.0, 240.0),
        (2.5, 2.0, 340.0, -5.0),
        (2.5, 2.0, 341.0, 240.0),
        (2.5, 2.0, 340.0, 241.0),
    ],
)
def test_les_parametres_invalides_sont_rejetes(
    pas_y: float, pas_z: float, demi_largeur: float, hauteur: float
) -> None:
    """Positivité et multiplicité des pas sont exigées à la construction."""
    # Given — des paramètres numériques invalides.
    # Then — la construction lève une ValueError.
    with pytest.raises(ValueError, match="doit être"):
        ParametresEdp(pas_y, pas_z, demi_largeur, hauteur)


def test_la_derivee_rejette_les_distances_non_posives() -> None:
    """La dérivée de sigma² n'est définie que pour des distances positives."""
    # Given — des distances sous le vent nulles ou négatives.
    # Then — la dérivée lève une ValueError dans les deux cas.
    with pytest.raises(ValueError, match="strictement positive"):
        derivee_sigma_carre(0.0, 0.11, 0.0001)
    with pytest.raises(ValueError, match="strictement positive"):
        derivee_sigma_carre(-100.0, 0.08, 0.0002)


def test_les_couts_sont_mesures_separement(
    comparaison: ComparaisonReference,
) -> None:
    """Les coûts des deux routes sont mesurés, finis et strictement positifs."""
    # Given — la comparaison calibrée (note 35 : coûts séparés, sans facteur).
    # Then — les deux coûts sont mesurés, finis, strictement positifs.
    assert math.isfinite(comparaison.cout_ferme_s)
    assert comparaison.cout_ferme_s > 0.0
    assert math.isfinite(comparaison.cout_edp_s)
    assert comparaison.cout_edp_s > 0.0


def test_la_comparaison_est_immuable(comparaison: ComparaisonReference) -> None:
    """Le modèle de comparaison est gelé : aucune mutation après construction."""
    # Given — la comparaison calibrée.
    # When / Then — toute affectation lève une ValidationError Pydantic.
    with pytest.raises(ValidationError):
        comparaison.fac2 = 0.5


def test_le_manifeste_est_etiquete(comparaison: ComparaisonReference) -> None:
    """Le manifeste lie la comparaison à ses sources, statuts et limites."""
    # Given — le manifeste construit sur le cas S0 figé.
    manifeste = construire_manifeste(CAS_S0_DEFAUT, comparaison)
    # Then — identification stable et niveau de fidélité R1.
    assert manifeste.identifiant == "jdriftx-reference-independante-001"
    assert manifeste.niveau_fidelite == "R1"
    # Then — source documentaire citée avec DOI.
    assert "DOI 10.1007/978-1-4020-8758-5_14" in manifeste.source
    # Then — héritage : « annoncée seulement », aucun chiffre de l'ouvrage.
    assert "annoncée seulement" in manifeste.heritage_documentaire
    # Then — extension : aucune.
    assert manifeste.extension.startswith("Aucune")
    # Then — limites : facteur historique non revendiqué, pas une validation.
    limites = " ".join(manifeste.limites)
    assert "10³-10⁴" in limites
    assert "n'est pas revendiqué" in limites
    assert "pas une validation physique" in limites


def test_l_export_frontiere_est_json_natif(
    comparaison: ComparaisonReference,
) -> None:
    """L'export du manifeste est JSON-natif : listes, pas de tuples."""
    # Given — le manifeste et son export frontière.
    manifeste = construire_manifeste(CAS_S0_DEFAUT, comparaison)
    export = manifeste.vers_dict()
    # Then — l'export est directement sérialisable, sans conversion manuelle.
    assert json.dumps(export)
    # Then — les tuples deviennent des listes à la frontière JSON.
    assert export["cas"]["arcs"] == [100.0, 200.0, 400.0, 800.0]
    assert isinstance(export["limites"], list)
    # Then — les 12 comparaisons ponctuelles sont exportées.
    assert len(export["comparaison"]["points"]) == 12
    assert export["comparaison"]["points"][0]["ratio"] > 0.0


def test_la_version_non_installee_est_supportee(
    comparaison: ComparaisonReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sans paquet installé, le manifeste porte « non-installe » sans échouer."""
    # Given — une lecture de version qui échoue (paquet non installé).

    def version_inconnue(nom: str) -> str:
        raise module_reference.metadata.PackageNotFoundError(nom)

    monkeypatch.setattr(module_reference.metadata, "version", version_inconnue)
    # When — le manifeste est construit malgré l'absence de version.
    manifeste = construire_manifeste(CAS_S0_DEFAUT, comparaison)
    # Then — la version de repli est explicite.
    assert manifeste.version_code == "non-installe"
