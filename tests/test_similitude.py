"""Tests physiques et numeriques des solutions de similitude."""

from itertools import pairwise
from math import erf, exp, pi, sqrt

import numpy as np
import pytest

from jdriftx.similitude import (
    concentration_panache,
    concentration_puff,
    sigma_y,
    sigma_z,
)
from jdriftx.stabilite import ClasseStabilite


@pytest.fixture
def grille() -> tuple[np.ndarray, np.ndarray]:
    """Grille laterale/verticale a x = 500 m."""
    y = np.linspace(-500.0, 500.0, 401)
    z = np.linspace(0.0, 400.0, 201)
    return y, z


def test_classe_invalide() -> None:
    """Une classe de stabilité inconnue est refusée."""
    # Given — une classe hors nomenclature de Pasquill.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="Classe de stabilite inconnue"):
        sigma_y(100.0, "Z")


def test_distance_negative() -> None:
    """Une distance sous le vent négative est refusée."""
    # Given — une distance strictement négative.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="positive ou nulle"):
        sigma_z(-1.0, "D")


def test_sigmas_croissants() -> None:
    """La dispersion ne peut que croitre avec la distance sous le vent."""
    # Given — une grille de distances sous le vent et les six classes.
    x = np.linspace(1.0, 10_000.0, 200)
    # When — les sigma_y et sigma_z sont évalués pour chaque classe.
    # Then — ils croissent strictement avec la distance pour chaque classe.
    for classe in ("A", "B", "C", "D", "E", "F"):
        assert np.all(np.diff(sigma_y(x, classe)) > 0.0)
        assert np.all(np.diff(sigma_z(x, classe)) > 0.0)


def test_positivite_panache(grille: tuple[np.ndarray, np.ndarray]) -> None:
    """Le panache gaussien est partout strictement positif."""
    # Given — une grille latérale/verticale à x = 500 m.
    y, z = grille
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le panache est évalué.
    c = concentration_panache(500.0, yy, zz, debit=1.0, u=3.0, classe="D")
    # Then — toutes les concentrations sont strictement positives.
    assert np.all(c > 0.0)


def test_symetrie_laterale(grille: tuple[np.ndarray, np.ndarray]) -> None:
    """Le panache est symétrique par rapport à l'axe y = 0."""
    # Given — une grille latérale et son image miroir.
    y, _ = grille
    # When — le panache est évalué en y et en -y.
    gauche = concentration_panache(300.0, y, 2.0, 1.0, 3.0, "D")
    droite = concentration_panache(300.0, -y, 2.0, 1.0, 3.0, "D")
    # Then — les deux évaluations coïncident.
    assert np.allclose(gauche, droite)


def test_conservation_masse_panache(grille: tuple[np.ndarray, np.ndarray]) -> None:
    """Le flux integre u*C sur (y, z) doit restituer le debit emis (a 2 %)."""
    # Given — un panache de débit 1,5 dans un vent de 4 m/s.
    y, z = grille
    debit, u = 1.5, 4.0
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le flux intégré u*C est évalué sur la section (y, z).
    c = concentration_panache(1000.0, yy, zz, debit=debit, u=u, classe="D")
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — le flux restitue le débit émis à 2 % relatif.
    assert flux == pytest.approx(debit, rel=0.02)


@pytest.mark.parametrize(
    ("classe", "x"),
    [
        ("A", 1000.0),
        ("B", 1000.0),
        ("C", 1000.0),
        ("D", 1000.0),
        ("E", 1000.0),
        ("F", 1000.0),
        ("D", 200.0),
        ("D", 5000.0),
    ],
)
def test_conservation_masse_panache_toutes_classes(classe: str, x: float) -> None:
    """Le flux integre restitue le debit emis pour six classes et plusieurs distances."""
    # Given — un panache de debit 1,5 kg/s dans un vent de 4 m/s, grille adaptee a 4 sigma.
    debit, u = 1.5, 4.0
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    y = np.linspace(-4.0 * sy, 4.0 * sy, 241)
    z = np.linspace(0.0, 4.0 * sz, 121)
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le flux u*C est integre sur la section transversale.
    c = concentration_panache(x, yy, zz, debit=debit, u=u, classe=classe)
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — le debit emis est restitue a 0,1 % relatif.
    assert flux == pytest.approx(debit, rel=1e-3)


def test_conservation_masse_panache_hauteur_non_nulle() -> None:
    """Une source en hauteur avec reflexion au sol conserve le debit emis."""
    # Given — un panache de classe D emis a 30 m de hauteur, x = 1000 m.
    debit, u, h = 2.0, 4.0, 30.0
    x, classe = 1000.0, "D"
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    y = np.linspace(-4.0 * sy, 4.0 * sy, 241)
    z = np.linspace(0.0, h + 4.0 * sz, 161)
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — le flux est integre sur la section avec le terme de reflexion.
    c = concentration_panache(x, yy, zz, debit=debit, u=u, classe=classe, hauteur=h)
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — le debit emis est restitue a 0,1 % relatif.
    assert flux == pytest.approx(debit, rel=1e-3)


def test_conservation_masse_puff() -> None:
    """L'integrale volumique du puff restitue la masse emise."""
    # Given — un puff de 10 kg apres 500 s de transport (classe C, vent 3 m/s).
    masse, u, t, classe = 10.0, 3.0, 500.0, "C"
    distance = u * t
    s = float(sigma_y(distance, classe))
    sz = float(sigma_z(distance, classe))
    n = 81
    x = np.linspace(distance - 4.0 * s, distance + 4.0 * s, n)
    y = np.linspace(-4.0 * s, 4.0 * s, n)
    z = np.linspace(-4.0 * sz, 4.0 * sz, n)
    xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")
    # When — la concentration est integree sur le volume.
    c = concentration_puff(xx, yy, zz, t=t, masse=masse, u=u, classe=classe)
    integrale = np.trapezoid(np.trapezoid(np.trapezoid(c, x, axis=0), y, axis=0), z)
    # Then — la masse emise est restituee a 0,1 % relatif.
    assert integrale == pytest.approx(masse, rel=1e-3)


def test_conservation_masse_superposition_deux_panaches() -> None:
    """Le flux d'une superposition de deux panaches est la somme des debits."""
    # Given — deux panaches de classe D, debits et hauteurs differents.
    debit1, debit2, u, x, classe = 1.2, 0.8, 4.0, 1000.0, "D"
    h1, h2 = 0.0, 30.0
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    y = np.linspace(-4.0 * sy, 4.0 * sy, 241)
    z = np.linspace(0.0, h2 + 4.0 * sz, 161)
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — la superposition des deux panaches est integree sur la section.
    c = concentration_panache(x, yy, zz, debit=debit1, u=u, classe=classe, hauteur=h1)
    c += concentration_panache(x, yy, zz, debit=debit2, u=u, classe=classe, hauteur=h2)
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — la somme des debits emis est restituee a 0,1 % relatif.
    assert flux == pytest.approx(debit1 + debit2, rel=1e-3)


@pytest.mark.parametrize(
    ("classe1", "classe2", "h1", "h2"),
    [
        ("C", "F", 0.0, 40.0),
        ("A", "E", 0.0, 50.0),
        ("B", "D", 0.0, 25.0),
    ],
)
def test_conservation_masse_superposition_classes_differentes(
    classe1: str, classe2: str, h1: float, h2: float
) -> None:
    """Le flux d'une superposition de panaches de classes differentes est la somme des debits."""
    # Given — deux panaches de classes de stabilite et de hauteurs differentes.
    debit1, debit2, u, x = 1.0, 0.5, 4.0, 1000.0
    sy_max = max(float(sigma_y(x, classe1)), float(sigma_y(x, classe2)))
    sz_max = max(float(sigma_z(x, classe1)), float(sigma_z(x, classe2)))
    y = np.linspace(-4.0 * sy_max, 4.0 * sy_max, 241)
    z = np.linspace(0.0, max(h1, h2) + 4.0 * sz_max, 161)
    yy, zz = np.meshgrid(y, z, indexing="ij")
    # When — la superposition des deux panaches est integree sur la section commune.
    c = concentration_panache(x, yy, zz, debit=debit1, u=u, classe=classe1, hauteur=h1)
    c += concentration_panache(x, yy, zz, debit=debit2, u=u, classe=classe2, hauteur=h2)
    flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
    # Then — la somme des debits emis est restituee a 0,1 % relatif.
    assert flux == pytest.approx(debit1 + debit2, rel=1e-3)


def test_conservation_masse_superposition_deux_puffs() -> None:
    """L'integrale d'une superposition de deux puffs restitue la somme des masses."""
    # Given — deux puffs de masses et classes differentes apres 500 s de transport.
    masse1, masse2, u, t = 10.0, 4.0, 3.0, 500.0
    classe1, classe2 = "C", "F"
    distance = u * t
    s_max = max(float(sigma_y(distance, classe1)), float(sigma_y(distance, classe2)))
    sz_max = max(float(sigma_z(distance, classe1)), float(sigma_z(distance, classe2)))
    n = 81
    x = np.linspace(distance - 4.0 * s_max, distance + 4.0 * s_max, n)
    y = np.linspace(-4.0 * s_max, 4.0 * s_max, n)
    z = np.linspace(-4.0 * sz_max, 4.0 * sz_max, n)
    xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")
    # When — la superposition des deux puffs est integree sur le volume commun.
    c = concentration_puff(xx, yy, zz, t=t, masse=masse1, u=u, classe=classe1)
    c += concentration_puff(xx, yy, zz, t=t, masse=masse2, u=u, classe=classe2)
    integrale = np.trapezoid(np.trapezoid(np.trapezoid(c, x, axis=0), y, axis=0), z)
    # Then — la somme des masses emises est restituee a 0,1 % relatif.
    assert integrale == pytest.approx(masse1 + masse2, rel=1e-3)


def test_erreur_de_troncature_domaine_a_resolution_controlee() -> None:
    """La fraction analytique omise diminue avec l'étendue du domaine."""
    # Given — un panache au sol : le flux exact dans [-k sy, k sy] x [0, k sz]
    # est Q * erf(k / sqrt(2))**2. Cette référence isole la troncature du domaine.
    debit, u, x, classe = 1.5, 4.0, 1000.0, "D"
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    erreurs_troncature = []
    for k in (2.0, 3.0, 4.0):
        # Pas spatial fixé en unités de sigma : le nombre de points augmente
        # avec l'étendue, au lieu de faire varier simultanément pas et domaine.
        y = np.linspace(-k * sy, k * sy, round(2.0 * k * 40.0) + 1)
        z = np.linspace(0.0, k * sz, round(k * 40.0) + 1)
        yy, zz = np.meshgrid(y, z, indexing="ij")
        c = concentration_panache(x, yy, zz, debit=debit, u=u, classe=classe)
        flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
        flux_tronque_exact = debit * erf(k / sqrt(2.0)) ** 2
        assert flux == pytest.approx(flux_tronque_exact, rel=2e-4)
        erreurs_troncature.append(abs(flux_tronque_exact - debit) / debit)

    # Then — seule l'erreur de troncature analytique est comparée entre domaines.
    assert erreurs_troncature[0] > erreurs_troncature[1] > erreurs_troncature[2]
    assert erreurs_troncature[2] < 1e-3


def test_erreur_discretisation_domaine_fixe() -> None:
    """À domaine fixé, raffiner la grille réduit l'erreur de quadrature."""
    # Given — même domaine à quatre sigma et flux exact tronqué connu.
    debit, u, x, classe, k = 1.5, 4.0, 1000.0, "D", 4.0
    sy = float(sigma_y(x, classe))
    sz = float(sigma_z(x, classe))
    flux_tronque_exact = debit * erf(k / sqrt(2.0)) ** 2
    erreurs_quadrature = []
    for n in (21, 41, 81, 161):
        y = np.linspace(-k * sy, k * sy, 2 * n - 1)
        z = np.linspace(0.0, k * sz, n)
        yy, zz = np.meshgrid(y, z, indexing="ij")
        c = concentration_panache(x, yy, zz, debit=debit, u=u, classe=classe)
        flux = u * np.trapezoid(np.trapezoid(c, y, axis=0), z)
        erreurs_quadrature.append(abs(flux - flux_tronque_exact) / debit)

    # Then — l'étendue reste identique ; seule la résolution change.
    assert all(precedente > suivante for precedente, suivante in pairwise(erreurs_quadrature))


def test_positivite_puff() -> None:
    """Le puff gaussien est strictement positif au point évalué."""
    # Given / When — un puff est évalué en un point du domaine.
    c = concentration_puff(1500.0, 10.0, 5.0, t=500.0, masse=10.0, u=3.0, classe="C")
    # Then — la concentration est strictement positive.
    assert c > 0.0


def test_puff_temps_invalide() -> None:
    """Un instant nul ou négatif est refusé pour le puff."""
    # Given — un instant t = 0.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="strictement positif"):
        concentration_puff(100.0, 0.0, 0.0, t=0.0, masse=1.0, u=2.0, classe="D")


def test_panache_against_closed_form_oracle_independent_of_package() -> None:
    """La formule scalaire indépendante recoupe l'implémentation vectorisée.

    Les coefficients viennent de l'objet canonique ClasseStabilite.C ; la
    formule scalaire reste distincte du chemin d'execution vectorise.
    Ce test est un oracle d'implémentation, pas une validation terrain ni
    une comparaison à un solveur EDP indépendant.
    """
    # Given — paramètres et points fixés, avec réflexion au sol.
    x = 500.0
    ys = (-20.0, 0.0, 35.0)
    zs = (0.0, 1.5, 12.0)
    debit, u, hauteur = 2.0, 3.0, 1.0

    # When — les coefficients sont lus depuis la source de vérité du projet.
    a, d_y = ClasseStabilite.C.coeff_sigma_y
    forme_z, b, d_z = ClasseStabilite.C.coeff_sigma_z
    assert forme_z.value == "sqrt"
    sy = a * x / sqrt(1.0 + d_y * x)
    sz = b * x / sqrt(1.0 + d_z * x)
    reference = np.array(
        [
            debit
            / (2.0 * pi * u * sy * sz)
            * exp(-(y**2) / (2.0 * sy**2))
            * (
                exp(-((z - hauteur) ** 2) / (2.0 * sz**2))
                + exp(-((z + hauteur) ** 2) / (2.0 * sz**2))
            )
            for y, z in zip(ys, zs, strict=True)
        ]
    )
    obtenu = concentration_panache(
        x=x,
        y=np.asarray(ys),
        z=np.asarray(zs),
        debit=debit,
        u=u,
        classe="C",
        hauteur=hauteur,
    )

    # Then — accord au niveau de l'arrondi flottant, sans auto-comparaison.
    np.testing.assert_allclose(obtenu, reference, rtol=1e-13, atol=0.0)


@pytest.mark.parametrize("classe", list(ClasseStabilite))
def test_enum_classe_equivalente_a_la_lettre(classe: ClasseStabilite) -> None:
    """Un membre ClasseStabilite est accepté au même titre que sa lettre.

    Les deux formes étaient déjà acceptées à l'exécution ; les annotations
    publiques le documentent désormais (audit docs/25, recommandation 6).
    """
    # Given — une classe de stabilité passée comme objet et sa lettre.
    x, y, z = 500.0, 25.0, 2.0
    # When — les sigma, le panache et le puff sont évalués avec l'enum.
    sy_enum = sigma_y(x, classe)
    sz_enum = sigma_z(x, classe)
    c_enum = concentration_panache(x, y, z, debit=1.5, u=3.0, classe=classe)
    p_enum = concentration_puff(x, y, z, t=300.0, masse=5.0, u=3.0, classe=classe)
    # Then — les évaluations coïncident exactement avec celles de la lettre.
    assert float(sy_enum) == pytest.approx(float(sigma_y(x, classe.value)))
    assert float(sz_enum) == pytest.approx(float(sigma_z(x, classe.value)))
    assert float(c_enum) == pytest.approx(
        float(concentration_panache(x, y, z, debit=1.5, u=3.0, classe=classe.value))
    )
    assert float(p_enum) == pytest.approx(
        float(concentration_puff(x, y, z, t=300.0, masse=5.0, u=3.0, classe=classe.value))
    )


@pytest.mark.parametrize("valeur", [float("nan"), float("inf"), -float("inf")])
def test_sigmas_rejettent_distance_non_finie(valeur: float) -> None:
    """Une distance sous le vent non finie est refusée par les deux écarts-types."""
    # Given — une distance NaN ou infinie, classe Pasquill objet D.
    # When / Then — les deux appels sont refusés avant tout calcul.
    with pytest.raises(ValueError, match="valeurs finies"):
        sigma_y(valeur, ClasseStabilite.D)
    with pytest.raises(ValueError, match="valeurs finies"):
        sigma_z(valeur, ClasseStabilite.D)


def test_sigmas_rejettent_tableau_contenant_nan() -> None:
    """Un tableau de distances contenant une valeur non finie est refusé."""
    # Given — une distance valide suivie d'un NaN.
    x = np.array([100.0, float("nan")])
    # When / Then — l'appel est refusé même si une seule valeur est invalide.
    with pytest.raises(ValueError, match="valeurs finies"):
        sigma_y(x, ClasseStabilite.D)


@pytest.mark.parametrize(
    "parametre",
    [
        {"debit": float("nan")},
        {"u": float("inf")},
        {"hauteur": -float("inf")},
    ],
)
def test_panache_rejette_scalaire_non_fini(parametre: dict[str, float]) -> None:
    """Un paramètre scalaire non fini du panache est refusé."""
    # Given — un NaN ou un infini parmi debit, u et hauteur, les autres valides.
    fixes = {"debit": 1.0, "u": 3.0, "hauteur": 0.0}
    fixes.update(parametre)
    # When / Then — l'appel est refusé avant tout calcul.
    with pytest.raises(ValueError, match="fini"):
        concentration_panache(500.0, 0.0, 1.0, classe=ClasseStabilite.D, **fixes)


def test_panache_rejette_distance_infinie() -> None:
    """Une distance sous le vent infinie est refusée."""
    # Given — x = +inf : le contrôle de signe passe, les sigmas débordent.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="valeurs finies"):
        concentration_panache(float("inf"), 0.0, 1.0, debit=1.0, u=3.0, classe=ClasseStabilite.D)


@pytest.mark.parametrize(
    ("y", "z"),
    [
        (np.array([float("nan")]), np.zeros(1)),
        (np.zeros(1), np.array([float("inf")])),
    ],
)
def test_panache_rejette_grille_non_finie(y: np.ndarray, z: np.ndarray) -> None:
    """Une coordonnée latérale ou verticale non finie est refusée."""
    # Given — un NaN ou un infini dans la grille y ou z.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="valeurs finies"):
        concentration_panache(500.0, y, z, debit=1.0, u=3.0, classe=ClasseStabilite.D)


def test_panache_diffuse_les_formes_selon_numpy() -> None:
    """Le panache combine x, y et z selon la diffusion NumPy."""
    # Given — x et y scalaires, z vectorisé sur quatre altitudes.
    z = np.array([0.0, 5.0, 10.0, 15.0])
    # When — le panache est évalué.
    c = concentration_panache(500.0, 25.0, z, debit=1.0, u=3.0, classe=ClasseStabilite.D)
    # Then — la forme du résultat suit la forme diffusée commune (4,).
    assert c.shape == (4,)
    assert np.all(c > 0.0)


@pytest.mark.parametrize(
    "parametre",
    [
        {"t": float("nan")},
        {"masse": float("inf")},
        {"u": -float("inf")},
        {"x0": float("nan")},
    ],
)
def test_puff_rejette_scalaire_non_fini(parametre: dict[str, float]) -> None:
    """Un paramètre scalaire non fini du puff est refusé."""
    # Given — un NaN ou un infini parmi t, masse, u et x0, les autres valides.
    fixes = {"t": 300.0, "masse": 5.0, "u": 3.0, "x0": 0.0}
    fixes.update(parametre)
    # When / Then — l'appel est refusé avant tout calcul.
    with pytest.raises(ValueError, match="fini"):
        concentration_puff(1500.0, 0.0, 1.0, classe=ClasseStabilite.C, **fixes)


@pytest.mark.parametrize(
    ("x", "y", "z"),
    [
        (np.array([float("nan")]), np.zeros(1), np.zeros(1)),
        (np.zeros(1), np.array([float("inf")]), np.zeros(1)),
        (np.zeros(1), np.zeros(1), np.array([-float("inf")])),
    ],
)
def test_puff_rejette_grille_non_finie(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> None:
    """Une coordonnée du point de calcul non finie est refusée."""
    # Given — un NaN ou un infini dans la grille x, y ou z.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="valeurs finies"):
        concentration_puff(x, y, z, t=300.0, masse=5.0, u=3.0, classe=ClasseStabilite.C)


def test_puff_rejette_distance_parcourue_infinie() -> None:
    """Un produit u*t qui déborde le float64 est refusé."""
    # Given — un vent et un temps finis dont le produit n'est pas représentable.
    # When / Then — l'appel est refusé.
    with pytest.raises(ValueError, match="distance parcourue doit rester finie"):
        concentration_puff(
            1500.0, 0.0, 1.0, t=1.0e200, masse=5.0, u=1.0e200, classe=ClasseStabilite.C
        )


def test_puff_diffuse_les_formes_selon_numpy() -> None:
    """Le puff combine x, y et z selon la diffusion NumPy."""
    # Given — x et y scalaires, z vectorisé sur trois altitudes.
    z = np.array([0.0, 2.0, 4.0])
    # When — le puff est évalué.
    c = concentration_puff(900.0, 0.0, z, t=300.0, masse=5.0, u=3.0, classe=ClasseStabilite.C)
    # Then — la forme du résultat suit la forme diffusée commune (3,).
    assert c.shape == (3,)
    assert np.all(c > 0.0)


@pytest.mark.parametrize("classe", list(ClasseStabilite))
def test_panache_pres_de_la_source_refuse_la_singularite(classe: ClasseStabilite) -> None:
    """La singularite pres de la source est refusee pour les six classes.

    Avec x = 1e-200, les ecarts-types restent positifs mais leurs carres
    sous-debordent : la concentration theorique depasse le plus grand
    float64. Le contrat leve ValueError au lieu de retourner un NaN ou
    un inf silencieux (issue #307, cas 1).
    """
    # Given — une distance extreme petite, finie, sur l axe du panache.
    # When / Then — la singularite gaussienne est refusee explicitement.
    with pytest.raises(ValueError, match="representable"):
        concentration_panache(1e-200, 0.0, 0.0, debit=1.0, u=1.0, classe=classe)


def test_panache_extreme_representable_restitue_une_valeur_finie() -> None:
    """Pres de la source, un point representable reste fini (cas 1).

    A x = 1e-200 (classe A) et environ 30 ecarts-types lateraux, chaque
    facteur intermediaire (amplitude, exponentielle) sort du domaine
    float64 alors que la solution mathematique reste representable : le
    chemin logarithmique restitue une valeur finie et positive.
    """
    # Given — un point lateral a environ 30 sigma de l axe d un panache extreme.
    y = 6.6e-200
    # When — la concentration est evaluee.
    c = concentration_panache(1e-200, y, 0.0, debit=1.0, u=1.0, classe=ClasseStabilite.A)
    # Then — la valeur restituee est finie et strictement positive.
    assert np.isfinite(c)
    assert c > 0.0


def test_panache_extreme_hors_axe_restitue_la_limite_nulle() -> None:
    """Une coordonnee extreme, finie, donne la limite nulle exacte (cas 2).

    Le rapport normalise y/sigma_y deborde vers l infini : l exponentielle
    tend vers zero et la limite mathematique, nulle, est representable.
    """
    # Given — un point lateral extreme devant un panache extreme.
    # When — la concentration est evaluee.
    c = concentration_panache(1e-200, 1e100, 0.0, debit=1.0, u=1.0, classe=ClasseStabilite.A)
    # Then — la limite nulle est restituee, sans NaN.
    assert c == 0.0


def test_panache_double_debordement_des_carres_restitue_zero() -> None:
    """Le NaN du double debordement des carres est elimine (cas 2).

    A x = 1e307 (classe A), le produit sigma_y*sigma_z deborde et
    y = 1e200 fait deborder y**2 : l ancien quotient inf/inf produisait
    NaN. Les rapports normalises restituent la limite nulle.
    """
    # Given — distance et coordonnee laterale dont les carres debordent.
    # When — la concentration est evaluee.
    c = concentration_panache(1e307, 1e200, 0.0, debit=1.0, u=1.0, classe=ClasseStabilite.A)
    # Then — la limite nulle est restituee.
    assert c == 0.0


def test_panache_melange_ordinaire_extreme_conserve_le_broadcasting() -> None:
    """Un tableau melangeant point ordinaire et extreme diffuse sa forme.

    Le point ordinaire suit le chemin direct, le point extreme le chemin
    logarithmique : la forme diffusee commune est conservee.
    """
    # Given — un tableau de distances ordinaire et extreme, coordonnees associees.
    x = np.array([100.0, 1e-200])
    y = np.array([0.0, 6.6e-200])
    # When — le panache est evalue sur la forme diffusee (2,).
    c = concentration_panache(x, y, 0.0, debit=1.0, u=1.0, classe=ClasseStabilite.A)
    # Then — la forme diffusee commune est conservee, toutes valeurs finies.
    assert c.shape == (2,)
    assert np.all(np.isfinite(c))
    assert np.all(c > 0.0)


@pytest.mark.parametrize("classe", list(ClasseStabilite))
def test_puff_pres_du_centre_refuse_la_singularite(classe: ClasseStabilite) -> None:
    """La singularite d un puff compact est refusee pour les six classes (cas 3).

    Avec u*t = 1e-200, le produit des trois ecarts-types sous-deborde au
    centre du puff : la concentration theorique depasse le plus grand
    float64, le contrat leve ValueError.
    """
    # Given — un puff extreme compact, evalue en son centre.
    # When / Then — la singularite est refusee explicitement.
    with pytest.raises(ValueError, match="representable"):
        concentration_puff(1e-200, 0.0, 0.0, t=1e-200, masse=1.0, u=1.0, classe=classe)


def test_puff_extreme_hors_centre_restitue_la_limite_nulle() -> None:
    """Un point extreme loin du centre d un puff compact donne zero (cas 3).

    Le rapport normalise (x - x0 - u*t)/sigma_x deborde vers l infini : la
    limite mathematique est nulle et representable, sans NaN.
    """
    # Given — un puff compact et un point a 1e200 m de son centre.
    # When — la concentration est evaluee.
    c = concentration_puff(1e200, 0.0, 0.0, t=1e-200, masse=1.0, u=1.0, classe=ClasseStabilite.A)
    # Then — la limite nulle est restituee, sans NaN.
    assert c == 0.0


def test_puff_extreme_representable_restitue_une_valeur_finie() -> None:
    """Un point a 50 ecarts-types d un puff compact reste representable (cas 3).

    Chaque facteur intermediaire sort du domaine float64, mais la solution
    mathematique reste finie : le chemin logarithmique la restitue.
    """
    # Given — un puff compact et un point a environ 50 sigma du centre.
    x = 50.0 * 2.2e-201 + 1e-200
    # When — la concentration est evaluee.
    c = concentration_puff(x, 0.0, 0.0, t=1e-200, masse=1.0, u=1.0, classe=ClasseStabilite.A)
    # Then — la valeur restituee est finie et strictement positive.
    assert np.isfinite(c)
    assert c > 0.0


@pytest.mark.parametrize("classe", list(ClasseStabilite))
def test_sigmas_representables_aux_tres_grandes_distances(classe: ClasseStabilite) -> None:
    """Les lois de Briggs restent évaluables pour x = 1e308."""
    # Given — une distance finie dont les produits d*x deborderaient.
    # When — les deux ecarts-types sont calcules pour chaque classe.
    sy = sigma_y(1.0e308, classe)
    sz = sigma_z(1.0e308, classe)
    # Then — les valeurs restent positives et finies.
    assert np.isfinite(sy)
    assert float(sy) > 0.0
    assert np.isfinite(sz)
    assert float(sz) > 0.0


def test_panache_distance_extreme_ne_produit_pas_de_valeur_non_finie() -> None:
    """Une concentration sous-representable a grande distance s'arrondit a zero."""
    # Given / When — le panache est evalue a une distance finie extreme.
    resultat = concentration_panache(1.0e308, 0.0, 0.0, debit=1.0, u=3.0, classe=ClasseStabilite.A)
    # Then — aucun NaN ni inf n'est retourne.
    assert np.isfinite(resultat)
    assert float(resultat) >= 0.0


def test_puff_distance_extreme_ne_produit_pas_de_valeur_non_finie() -> None:
    """Un puff a tres grande distance reste dans le domaine float64."""
    # Given / When — u*t vaut 1e308 sans debordement.
    resultat = concentration_puff(
        1.0e308, 0.0, 0.0, t=1.0e154, masse=1.0, u=1.0e154, classe=ClasseStabilite.A
    )
    # Then — la concentration est finie (eventuellement arrondie a zero).
    assert np.isfinite(resultat)
    assert float(resultat) >= 0.0


@pytest.mark.parametrize("valeur", ["500.0", None, True, 1 + 0j, float("nan"), float("inf")])
def test_sigmas_rejettent_les_types_et_valeurs_non_numeriques(valeur: object) -> None:
    """Les distances des fonctions sigma exigent des valeurs réelles finies."""
    with pytest.raises(ValueError):
        sigma_y(valeur, "D")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        sigma_z(valeur, "D")  # type: ignore[arg-type]


def test_sigma_rejette_un_entier_non_representable() -> None:
    """Un entier arbitrairement grand ne fuit pas OverflowError."""
    with pytest.raises(ValueError, match="representable"):
        sigma_y(10**400, "D")


@pytest.mark.parametrize("champ", ["debit", "u", "hauteur"])
@pytest.mark.parametrize("valeur", ["1.0", None, True, 1 + 0j, float("nan"), float("inf")])
def test_panache_rejette_les_scalaires_non_reels(champ: str, valeur: object) -> None:
    """Les paramètres scalaires du panache sont des réels finis, booléens exclus."""
    parametres: dict[str, object] = {"debit": 1.0, "u": 3.0, "hauteur": 0.0}
    parametres[champ] = valeur
    with pytest.raises(ValueError):
        concentration_panache(500.0, 0.0, 1.0, classe="D", **parametres)  # type: ignore[arg-type]


def test_panache_rejette_un_entier_scalaire_non_representable() -> None:
    """La conversion d'un entier scalaire trop grand est contextualisée."""
    with pytest.raises(ValueError, match="representable"):
        concentration_panache(500.0, 0.0, 1.0, debit=10**400, u=3.0, classe="D")


@pytest.mark.parametrize("axe", ["x", "y", "z"])
@pytest.mark.parametrize("valeur", ["1.0", None, [True], [1 + 0j], [float("nan")], [float("inf")]])
def test_panache_rejette_les_coordonnees_non_reelles(axe: str, valeur: object) -> None:
    """Les tableaux de coordonnées ne subissent pas de coercition implicite."""
    coordonnees: dict[str, object] = {"x": 500.0, "y": 0.0, "z": 1.0}
    coordonnees[axe] = valeur
    with pytest.raises(ValueError):
        concentration_panache(**coordonnees, debit=1.0, u=3.0, classe="D")  # type: ignore[arg-type]


@pytest.mark.parametrize("champ", ["t", "masse", "u", "x0"])
@pytest.mark.parametrize("valeur", ["1.0", None, True, 1 + 0j, float("nan"), float("inf")])
def test_puff_rejette_les_scalaires_non_reels(champ: str, valeur: object) -> None:
    """Les paramètres scalaires du puff sont des réels finis, booléens exclus."""
    parametres: dict[str, object] = {"t": 300.0, "masse": 5.0, "u": 3.0, "x0": 0.0}
    parametres[champ] = valeur
    with pytest.raises(ValueError):
        concentration_puff(900.0, 0.0, 1.0, classe="D", **parametres)  # type: ignore[arg-type]


def test_puff_rejette_un_entier_scalaire_non_representable() -> None:
    """La conversion d'un entier scalaire trop grand est contextualisée."""
    with pytest.raises(ValueError, match="representable"):
        concentration_puff(900.0, 0.0, 1.0, t=300.0, masse=10**400, u=3.0, classe="D")


@pytest.mark.parametrize("axe", ["x", "y", "z"])
@pytest.mark.parametrize("valeur", ["1.0", None, [True], [1 + 0j], [float("nan")], [float("inf")]])
def test_puff_rejette_les_coordonnees_non_reelles(axe: str, valeur: object) -> None:
    """Les tableaux de coordonnées du puff sont des réels finis stricts."""
    coordonnees: dict[str, object] = {"x": 900.0, "y": 0.0, "z": 1.0}
    coordonnees[axe] = valeur
    with pytest.raises(ValueError):
        concentration_puff(**coordonnees, t=300.0, masse=5.0, u=3.0, classe="D")  # type: ignore[arg-type]
