"""Tests des contrats d'interface entre éléments du modèle (docs/42)."""

import numpy as np
import pytest

from jdriftx.champ_analytique import ChampFonctionCourant
from jdriftx.contrats import (
    ModeleConcentration,
    PanacheGaussien,
    Relief,
    ReliefMntAscii,
    ReliefPlat,
    ReliefSynthetique,
    SuperpositionPanaches,
    Vent,
    VentDeChampPlan,
    VentProfilPuissance,
    VentUniforme,
)
from jdriftx.similitude import concentration_panache
from jdriftx.source import SourcePanache
from jdriftx.terrain import terrain_surface
from jdriftx.trajectories import integrate_trajectory
from jdriftx.vents import AdaptateurTrajectoire2D

MNT_ASCII = """ncols 3
nrows 3
xllcorner 0.0
yllcorner 0.0
cellsize 10.0
1 2 3
4 5 6
7 8 9
"""

MNT_SANS_DONNEE = """ncols 2
nrows 2
xllcorner 0.0
yllcorner 0.0
cellsize 10.0
nodata_value -9999
1 1
1 -9999
"""


def test_relief_plat_renvoie_zero() -> None:
    """Étant donné le terrain plat, quand on évalue l'altitude, alors elle est nulle."""
    # Given — une grille de points.
    x = np.array([[0.0, 1.0], [2.0, 3.0]])
    # When — on évalue le relief plat.
    z = ReliefPlat().altitude(x, x)
    # Then — l'altitude est nulle et la forme est conservée.
    assert z.shape == x.shape
    assert np.all(z == 0.0)


def test_relief_plat_rejette_formes_differentes() -> None:
    """Étant donné des grilles x et y de formes différentes, la construction est refusée."""
    # Given — des grilles incohérentes.
    # When / Then — l'évaluation est refusée.
    with pytest.raises(ValueError, match="formes identiques"):
        ReliefPlat().altitude(np.zeros((2, 2)), np.zeros((3, 2)))


def test_relief_synthetique_delegue_au_module_terrain() -> None:
    """Étant donné le contrat Relief, quand on évalue une colline, la délégation est exacte."""
    # Given — un relief synthétique de colline.
    relief = ReliefSynthetique(kind="hill", height=3.0, width=2.0, center_x=1.0)
    # When — on évalue l'altitude sur une grille bidimensionnelle.
    grille_x, grille_y = np.meshgrid(np.linspace(-5.0, 5.0, 11), np.linspace(-4.0, 4.0, 9))
    # Then — la valeur délègue au module terrain, sans duplication.
    attendu = terrain_surface(grille_x, grille_y, "hill", height=3.0, width=2.0, center_x=1.0)
    assert np.array_equal(relief.altitude(grille_x, grille_y), attendu)


@pytest.mark.parametrize(
    ("parametres", "message"),
    [
        ({"width": 0.0}, "largeur"),
        ({"height": float("nan")}, "finis"),
        ({"center_x": float("inf")}, "finis"),
        ({"kind": "unknown"}, "inconnu"),
    ],
)
def test_relief_synthetique_rejette_les_parametres_invalides(
    parametres: dict[str, object], message: str
) -> None:
    """Un relief invalide est refusé à la construction, pas à la première évaluation."""
    configuration = {"kind": "hill", **parametres}
    with pytest.raises(ValueError, match=message):
        ReliefSynthetique(**configuration)  # type: ignore[arg-type]


def test_reliefs_rejettent_les_coordonnees_non_finies() -> None:
    """Les implémentations de relief appliquent le même contrat d'entrée."""
    for relief in (ReliefPlat(), ReliefSynthetique(kind="hill")):
        with pytest.raises(ValueError, match="coordonnees doivent etre finies"):
            relief.altitude(np.array([float("nan")]), np.array([0.0]))


def test_mnt_ascii_lit_les_centres_de_cellules() -> None:
    """Étant donné un MNT .asc standard, les centres de cellules sont exacts."""
    # Given — une grille 3 x 3, cellule de 10 m, ligne 0 au nord.
    relief = ReliefMntAscii.depuis_texte(MNT_ASCII)
    # When / Then — les centres de cellules portent l'altitude de leur cellule.
    assert relief.altitude(5.0, 5.0) == pytest.approx(7.0)
    assert relief.altitude(25.0, 25.0) == pytest.approx(3.0)
    assert relief.altitude(15.0, 15.0) == pytest.approx(5.0)


def test_mnt_ascii_interpole_bilineairement() -> None:
    """Étant donné un point entre quatre cellules, l'interpolation est bilinéaire."""
    # Given — le MNT 3 x 3 de 10 m de pas.
    relief = ReliefMntAscii.depuis_texte(MNT_ASCII)
    # When — on évalue aux centres des quatre carrés de 2 x 2 cellules.
    z1 = relief.altitude(10.0, 10.0)
    z2 = relief.altitude(20.0, 10.0)
    # Then — chaque valeur est la moyenne des quatre cellules voisines.
    assert z1 == pytest.approx((7.0 + 8.0 + 4.0 + 5.0) / 4.0)
    assert z2 == pytest.approx((8.0 + 9.0 + 5.0 + 6.0) / 4.0)


def test_mnt_ascii_rejette_hors_emprise() -> None:
    """Étant donné un point hors du MNT, l'évaluation est refusée."""
    # Given — le MNT 3 x 3 (emprise 0 à 30 m en x et y).
    relief = ReliefMntAscii.depuis_texte(MNT_ASCII)
    # When / Then — chaque sortie d'emprise est refusée avec son axe.
    with pytest.raises(ValueError, match="emprise horizontale"):
        relief.altitude(-1.0, 5.0)
    with pytest.raises(ValueError, match="emprise verticale"):
        relief.altitude(5.0, 40.0)


def test_mnt_ascii_rejette_cellule_sans_donnee() -> None:
    """Étant donné une cellule nodata dans l'interpolation, l'évaluation est refusée."""
    # Given — un MNT avec une cellule -9999 au sud-est.
    relief = ReliefMntAscii.depuis_texte(MNT_SANS_DONNEE)
    # When / Then — l'interpolation qui la touche à poids non nul est refusée.
    with pytest.raises(ValueError, match="sans donnee"):
        relief.altitude(10.0, 10.0)
    # Et le centre d'une cellule valide reste lisible.
    assert relief.altitude(5.0, 5.0) == pytest.approx(1.0)


def test_mnt_ascii_rejette_entete_incomplete() -> None:
    """Étant donné un en-tête sans cellsize, la lecture est refusée."""
    # Given — un fichier .asc amputé de cellsize.
    texte_incomplet = MNT_ASCII.replace("cellsize 10.0\n", "")
    # When / Then — la lecture est refusée.
    with pytest.raises(ValueError, match="incomplete"):
        ReliefMntAscii.depuis_texte(texte_incomplet)


def test_mnt_ascii_rejette_entete_invalide() -> None:
    """Étant donné un en-tête invalide, la lecture est refusée."""
    # Given — cellsize nul ou valeur non numérique.
    # When / Then — chaque défaut est refusé.
    with pytest.raises(ValueError, match="cellsize"):
        ReliefMntAscii.depuis_texte(MNT_ASCII.replace("10.0\n1 2 3", "0.0\n1 2 3"))
    with pytest.raises(ValueError, match="Valeur invalide"):
        ReliefMntAscii.depuis_texte(MNT_ASCII.replace("cellsize 10.0", "cellsize dix"))
    with pytest.raises(ValueError, match="ncols et nrows"):
        ReliefMntAscii.depuis_texte(MNT_ASCII.replace("ncols 3", "ncols 2.5"))


def test_mnt_ascii_rejette_grille_incoherente() -> None:
    """Étant donné moins de valeurs que ncols x nrows, la lecture est refusée."""
    # Given — une grille tronquée.
    texte_tronque = MNT_ASCII.replace("7 8 9", "7 8")
    # When / Then — la lecture est refusée.
    with pytest.raises(ValueError, match="ncols x nrows"):
        ReliefMntAscii.depuis_texte(texte_tronque)


def test_mnt_ascii_lit_un_fichier(tmp_path) -> None:
    """Étant donné un fichier .asc sur disque, la lecture directe est exacte."""
    # Given — un fichier .asc écrit au format standard.
    chemin = tmp_path / "mnt.asc"
    chemin.write_text(MNT_ASCII, encoding="utf-8")
    # When — on lit le fichier.
    relief = ReliefMntAscii.depuis_fichier(chemin)
    # Then — les centres de cellules sont exacts.
    assert relief.altitude(5.0, 5.0) == pytest.approx(7.0)


@pytest.mark.parametrize(
    ("champs", "message_attendu"),
    [
        ({"altitudes": np.zeros(4), "x0": 0.0, "y0": 0.0, "pas": 1.0}, "bidimensionnelle"),
        (
            {"altitudes": np.array([[0.0, np.nan]]), "x0": 0.0, "y0": 0.0, "pas": 1.0},
            "finies",
        ),
        (
            {"altitudes": np.zeros((2, 2)), "x0": 0.0, "y0": 0.0, "pas": 0.0},
            "pas de grille",
        ),
        (
            {"altitudes": np.zeros((2, 2)), "x0": np.nan, "y0": 0.0, "pas": 1.0},
            "origine",
        ),
    ],
)
def test_mnt_ascii_rejette_geometrie_invalide(champs, message_attendu) -> None:
    """Étant donné une géométrie invalide, la construction du MNT est refusée."""
    # Given — un MNT construit directement avec un paramètre invalide.
    # When / Then — la construction est refusée avec le message correspondant.
    with pytest.raises(ValueError, match=message_attendu):
        ReliefMntAscii(**champs)


def test_vent_uniforme_donne_trois_composantes() -> None:
    """Étant donné le vent uniforme, les trois composantes sont constantes."""
    # Given — un vent uniforme de composantes (2.0, 1.0).
    vent = VentUniforme(u=2.0, v=1.0)
    # When / Then — le contrat Vent renvoie (u, v, w) partout.
    assert vent.vitesse(0.0, 0.0, 5.0) == (2.0, 1.0, 0.0)
    with pytest.raises(ValueError, match="finies"):
        VentUniforme(u=float("nan"), v=1.0)


def test_adaptateur_champ_plan_garantit_w_nul() -> None:
    """Étant donné un champ plan existant, l'adaptateur satisfait le contrat Vent."""
    # Given — le champ cellulaire sinusoïdal (docs/23) adapté au contrat 3D.
    champ = ChampFonctionCourant(amplitude=1.0, longueur=2.0)
    vent = VentDeChampPlan(champ=champ)
    # When — on évalue le vent au point (0.3, 0.4), à toute altitude.
    u, v, w = vent.vitesse(0.3, 0.4, 100.0)
    # Then — les composantes planées sont celles du champ, w est nul.
    attendu = champ.vitesse(0.3, 0.4)
    assert (u, v, w) == (attendu[0], attendu[1], 0.0)


@pytest.mark.parametrize("hauteur", [float("nan"), float("inf")])
def test_vent_profil_puissance_rejette_hauteur_non_finie(hauteur: float) -> None:
    """Le profil ne produit jamais une vitesse non finie à partir de z invalide."""
    vent = VentProfilPuissance(u_reference=5.0, z_reference=10.0, exposant=0.15)
    with pytest.raises(ValueError, match="finie"):
        vent.vitesse(0.0, 0.0, hauteur)


def test_vent_profil_puissance_suit_la_loi_standard() -> None:
    """Étant donné le profil en loi de puissance, u(z) suit la référence à l'exposant."""
    # Given — un profil standard : 5 m/s à 10 m, exposant 0.15.
    vent = VentProfilPuissance(u_reference=5.0, z_reference=10.0, exposant=0.15)
    # When — on évalue le vent à 20 m et 10 m.
    u_haut, v, w = vent.vitesse(0.0, 0.0, 20.0)
    u_ref, _, _ = vent.vitesse(7.0, -3.0, 10.0)
    # Then — la loi de puissance est respectée, v et w sont nuls.
    assert u_haut == pytest.approx(5.0 * 2.0**0.15)
    assert u_ref == pytest.approx(5.0)
    assert (v, w) == (0.0, 0.0)
    with pytest.raises(ValueError, match="strictement positif"):
        vent.vitesse(0.0, 0.0, 0.0)


@pytest.mark.parametrize(
    ("champs", "message_attendu"),
    [
        ({"u_reference": 0.0, "z_reference": 10.0, "exposant": 0.1}, "vitesse de reference"),
        ({"u_reference": 5.0, "z_reference": 0.0, "exposant": 0.1}, "hauteur de reference"),
        ({"u_reference": 5.0, "z_reference": 10.0, "exposant": 1.5}, "exposant"),
    ],
)
def test_vent_profil_puissance_rejete_parametres_invalides(champs, message_attendu) -> None:
    """Étant donné un profil invalide, la construction est refusée."""
    # Given — un profil hors de son domaine.
    # When / Then — la construction est refusée avec le message correspondant.
    with pytest.raises(ValueError, match=message_attendu):
        VentProfilPuissance(**champs)


def test_panache_gaussien_egale_la_solution_de_similitude() -> None:
    """Étant donné un panache composé, les concentrations délèguent à la similitude."""
    # Given — une source S0 et sa grille d'évaluation.
    source = SourcePanache(debit=2.0, u=3.0, classe="C", hauteur=1.0)
    panache = PanacheGaussien(source=source)
    x = np.array([100.0, 200.0, 400.0])
    y = np.array([-50.0, 0.0, 50.0])
    z = np.array([1.5, 1.5, 1.5])
    # When — on évalue les concentrations du contrat.
    concentrations = panache.concentration(x, y, z)
    # Then — elles sont celles de la solution de similitude, sans duplication.
    attendu = concentration_panache(x, y, z, debit=2.0, u=3.0, classe="C", hauteur=1.0)
    assert np.array_equal(concentrations, attendu)


def test_superposition_est_lineaire_h8() -> None:
    """Étant donné deux panaches, la superposition est la somme exacte (H8)."""
    # Given — deux panaches gaussiens de sources différentes.
    source_1 = SourcePanache(debit=2.0, u=3.0, classe="C", hauteur=1.0)
    source_2 = SourcePanache(debit=1.0, u=3.0, classe="D", hauteur=10.0)
    panache_1 = PanacheGaussien(source=source_1)
    panache_2 = PanacheGaussien(source=source_2)
    superposition = SuperpositionPanaches(panaches=(panache_1, panache_2))
    x = np.array([100.0, 400.0])
    y = np.array([0.0, 30.0])
    z = np.array([1.5, 2.0])
    # When — on évalue la superposition.
    total = superposition.concentration(x, y, z)
    # Then — la concentration est la somme des deux panaches.
    attendu = panache_1.concentration(x, y, z) + panache_2.concentration(x, y, z)
    assert np.allclose(total, attendu)
    # Et une superposition imbriquée reste une somme.
    imbriquee = SuperpositionPanaches(panaches=(superposition, panache_1))
    attendu_imbrique = attendu + panache_1.concentration(x, y, z)
    assert np.allclose(imbriquee.concentration(x, y, z), attendu_imbrique)


def test_superposition_exige_un_panache() -> None:
    """Étant donné une superposition vide, la construction est refusée."""
    # Given / When / Then — au moins un panache est exigé.
    with pytest.raises(ValueError, match="au moins un panache"):
        SuperpositionPanaches(panaches=())


def test_superposition_refuse_une_collection_mutable() -> None:
    """La collection doit respecter le tuple annoncé et l'immuabilité du modèle."""
    panache = PanacheGaussien(source=SourcePanache(debit=1.0, u=3.0, classe="C", hauteur=1.0))
    with pytest.raises(TypeError, match="tuple"):
        SuperpositionPanaches(panaches=[panache])  # type: ignore[arg-type]


def test_superposition_refuse_un_objet_hors_protocole() -> None:
    """Un élément incompatible est rejeté dès la construction."""
    with pytest.raises(TypeError, match="ModeleConcentration"):
        SuperpositionPanaches(panaches=(object(),))  # type: ignore[arg-type]


def test_superposition_refuse_une_methode_non_appelable() -> None:
    """Le protocole exige une méthode concentration effectivement appelable."""

    class ModeleSansMethode:
        concentration = 42

    with pytest.raises(TypeError, match="ModeleConcentration"):
        SuperpositionPanaches(panaches=(ModeleSansMethode(),))  # type: ignore[arg-type]


def test_superposition_refuse_une_forme_de_sortie_incoherente() -> None:
    """Une sortie ne doit pas être implicitement diffusée par NumPy."""

    class ModeleFormeIncoherente:
        def concentration(self, x: object, y: object, z: object) -> np.ndarray:
            return np.zeros((1,), dtype=float)

    panache = PanacheGaussien(source=SourcePanache(debit=1.0, u=3.0, classe="C", hauteur=1.0))
    superposition = SuperpositionPanaches(panaches=(panache, ModeleFormeIncoherente()))
    with pytest.raises(ValueError, match="forme"):
        superposition.concentration(np.full((2, 1), 100.0), np.zeros((1, 3)), 0.0)


def test_superposition_accepte_le_broadcasting_des_entrees() -> None:
    """Les entrées broadcastables produisent la forme commune attendue."""
    panache = PanacheGaussien(source=SourcePanache(debit=1.0, u=3.0, classe="C", hauteur=1.0))
    superposition = SuperpositionPanaches(panaches=(panache,))
    resultat = superposition.concentration(np.full((2, 1), 100.0), np.zeros((1, 3)), 1.0)
    assert resultat.shape == (2, 3)


def test_superposition_refuse_une_sortie_non_ndarray() -> None:
    """Le protocole exige un ndarray, pas une liste Python."""

    class ModeleListe:
        def concentration(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> list[float]:
            return [0.0]

    superposition = SuperpositionPanaches(panaches=(ModeleListe(),))  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="ndarray"):
        superposition.concentration(np.array([0.0]), np.array([0.0]), np.array([0.0]))


def test_superposition_refuse_une_sortie_non_reelle() -> None:
    """Une concentration complexe ne satisfait pas le contrat physique réel."""

    class ModeleComplexe:
        def concentration(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
            return np.array([1.0 + 2.0j])

    superposition = SuperpositionPanaches(panaches=(ModeleComplexe(),))  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="flottant réel"):
        superposition.concentration(np.array([0.0]), np.array([0.0]), np.array([0.0]))


def test_superposition_refuse_des_entrees_non_broadcastables() -> None:
    """Les formes d'entrée incompatibles sont refusées explicitement."""
    panache = PanacheGaussien(source=SourcePanache(debit=1.0, u=3.0, classe="C", hauteur=1.0))
    superposition = SuperpositionPanaches(panaches=(panache,))
    with pytest.raises(ValueError, match="broadcastables"):
        superposition.concentration(np.zeros((2, 2)), np.zeros((3,)), 0.0)


def test_superposition_rejette_le_debordement_sans_avertissement_numpy() -> None:
    """Un overflow de somme devient ValueError, même sous errstate strict."""

    class PanacheConstant:
        def __init__(self, valeur: float) -> None:
            self.valeur = valeur

        def concentration(self, x: object, y: object, z: object) -> np.ndarray:
            return np.full(np.shape(x), self.valeur)

    superposition = SuperpositionPanaches(
        panaches=(PanacheConstant(1.5e308), PanacheConstant(1.5e308))
    )
    with (
        np.errstate(over="raise", invalid="raise"),
        pytest.raises(ValueError, match="doit rester finie"),
    ):
        superposition.concentration(0.0, 0.0, 0.0)


def test_adaptateur_vent_stationnaire_alimente_les_trajectoires_2d() -> None:
    """Un vent horizontal est utilisable sans adapter chaque appelant."""
    # Given — un vent stationnaire horizontal échantillonné à hauteur fixe.
    adaptateur = AdaptateurTrajectoire2D(
        vent=VentUniforme(u=2.0, v=-1.0),
        hauteur=10.0,
    )

    # When — l'intégrateur 2D consomme directement l'adaptateur callable.
    temps, x, y = integrate_trajectory(adaptateur, 0.0, 0.0, 0.0, 1.0, 0.25)

    # Then — la trajectoire respecte exactement le champ uniforme.
    assert np.allclose(x, 2.0 * temps)
    assert np.allclose(y, -temps)


def test_adaptateur_vent_refuse_une_composante_verticale_non_nulle() -> None:
    """Un intégrateur 2D ne doit pas masquer une vitesse verticale."""

    class VentVertical:
        def vitesse(self, x: float, y: float, z: float) -> tuple[float, float, float]:
            return 1.0, 0.0, 0.1

    adaptateur = AdaptateurTrajectoire2D(vent=VentVertical(), hauteur=10.0)
    with pytest.raises(ValueError, match="vent vertical"):
        adaptateur(0.0, 0.0, 0.0)


def test_le_typage_structurel_reconnait_les_contrats() -> None:
    """Étant donné les implémentations, chacune satisfait son protocole (PEP 544)."""
    # Given — un objet de chaque contrat.
    champ = ChampFonctionCourant(amplitude=1.0, longueur=2.0)
    reliefs = [ReliefPlat(), ReliefSynthetique(kind="hill"), ReliefMntAscii.depuis_texte(MNT_ASCII)]
    vents = [
        VentUniforme(u=1.0, v=0.0),
        VentDeChampPlan(champ=champ),
        VentProfilPuissance(u_reference=5.0, z_reference=10.0, exposant=0.15),
    ]
    panache = PanacheGaussien(source=SourcePanache(debit=1.0, u=3.0, classe="D", hauteur=10.0))
    modeles = [panache, SuperpositionPanaches(panaches=(panache,))]
    # When / Then — le typage structurel reconnaît chaque contrat, et rien d'autre.
    for relief in reliefs:
        assert isinstance(relief, Relief)
    for vent in vents:
        assert isinstance(vent, Vent)
    for modele in modeles:
        assert isinstance(modele, ModeleConcentration)
    assert not isinstance(42, Relief)
    assert not isinstance(42, Vent)
    assert not isinstance(42, ModeleConcentration)


def test_mnt_ascii_copie_et_protege_sa_grille() -> None:
    """La grille est possédée par le relief et ne peut pas être mutée après validation."""
    # Given — une grille source mutable transmise au constructeur.
    altitudes = np.arange(4, dtype=float).reshape(2, 2)
    relief = ReliefMntAscii(altitudes=altitudes, x0=0.0, y0=0.0, pas=1.0)

    # When — le tableau d'origine est modifié après construction.
    altitudes[0, 0] = 99.0

    # Then — le relief conserve les données validées et expose une grille en lecture seule.
    assert relief.altitudes[0, 0] == 0.0
    with pytest.raises(ValueError, match="read-only"):
        relief.altitudes[0, 0] = 42.0
    with pytest.raises(ValueError, match="WRITEABLE"):
        relief.altitudes.setflags(write=True)


@pytest.mark.parametrize(
    ("champ", "valeur"),
    [
        ("sans_donnee", float("nan")),
        ("sans_donnee", float("inf")),
    ],
)
def test_mnt_ascii_rejette_sentinelle_sans_donnee_non_finie(champ: str, valeur: float) -> None:
    """Une sentinelle nodata doit être finie pour permettre une comparaison fiable."""
    # Given — une grille valide et une sentinelle non finie.
    valeurs: dict[str, object] = {
        "altitudes": np.zeros((2, 2)),
        "x0": 0.0,
        "y0": 0.0,
        "pas": 1.0,
        champ: valeur,
    }

    # When / Then — la construction rejette la sentinelle.
    with pytest.raises(ValueError, match=r"sans donnee.*finie"):
        ReliefMntAscii(**valeurs)  # type: ignore[arg-type]


@pytest.mark.parametrize("coordonnees", [(float("nan"), 0.0), (0.0, float("inf"))])
def test_mnt_ascii_rejette_coordonnees_non_finies(
    coordonnees: tuple[float, float],
) -> None:
    """L'interpolation refuse les coordonnées non finies avant tout calcul d'index."""
    # Given — un MNT valide et une coordonnée non finie.
    relief = ReliefMntAscii.depuis_texte(MNT_ASCII)

    # When / Then — l'évaluation est refusée explicitement.
    with pytest.raises(ValueError, match=r"coordonnees.*finies"):
        relief.altitude(*coordonnees)


@pytest.mark.parametrize(
    ("ligne", "valeur"),
    [
        ("ncols 3", "ncols inf"),
        ("ncols 3", "ncols nan"),
        ("nrows 3", "nrows inf"),
        ("nrows 3", "nrows nan"),
    ],
)
def test_mnt_ascii_rejette_dimensions_non_finies(ligne: str, valeur: str) -> None:
    """Étant donné un en-tête .asc à dimension non finie, la lecture est refusée.

    Sans garde, ncols inf déborde int() en OverflowError et nan en
    ValueError interne : le contrat de lecture garde son message explicite.
    """
    # Given — un MNT dont ncols ou nrows vaut inf ou nan.
    texte = MNT_ASCII.replace(ligne, valeur)
    # When / Then — la lecture est refusée avec le message du contrat.
    with pytest.raises(ValueError, match="ncols et nrows doivent etre finis"):
        ReliefMntAscii.depuis_texte(texte)


@pytest.mark.parametrize(("z", "z_reference"), [(1e308, 1e-308), (1e307, 1.0)])
def test_vent_profil_puissance_rejette_le_debordement(z: float, z_reference: float) -> None:
    """Étant donné des entrées finies extrêmes, le profil refuse le débordement.

    Le quotient z / z_reference puis le produit par u_reference peuvent
    déborder vers l'infini alors que chaque entrée reste finie : le contrat
    Vent lève ValueError plutôt que de retourner une vitesse infinie.
    """
    # Given — un profil valide et des entrées finies mais extrêmes.
    vent = VentProfilPuissance(u_reference=1e5, z_reference=z_reference, exposant=1.0)
    # When / Then — le débordement du profil est refusé explicitement.
    with pytest.raises(ValueError, match="doit rester fini"):
        vent.vitesse(0.0, 0.0, z)


def test_adaptateur_champ_plan_rejette_composantes_non_finies() -> None:
    """Un champ plan délégué ne doit pas fuiter une vitesse non finie."""
    # Given — un champ plan dont la composante u déborde.

    class ChampInfini:
        """Champ plan minimal : fonction_courant nulle, u infinie."""

        def fonction_courant(self, x: float, y: float) -> float:
            return 0.0

        def vitesse(self, x: float, y: float) -> tuple[float, float]:
            return float("inf"), 0.0

    vent = VentDeChampPlan(champ=ChampInfini())  # type: ignore[arg-type]

    # When / Then — l'adaptateur refuse la composante non finie.
    with pytest.raises(ValueError, match="deux composantes finies"):
        vent.vitesse(0.0, 0.0, 10.0)


def test_superposition_rejette_le_debordement_de_somme() -> None:
    """Étant donné des panaches finis extrêmes, la somme ne déborde pas en silence.

    Chaque concentration reste finie, mais leur somme dépasse le plus
    grand float64 : la superposition lève ValueError au lieu de retourner
    +inf (frontière NumPy, hypothèse H8 de linéarité).
    """
    # Given — deux modèles constants finis dont la somme déborde.

    class PanacheConstant:
        """Modèle minimal : concentration constante et finie, paramétrée."""

        def __init__(self, valeur: float) -> None:
            self.valeur = valeur

        def concentration(self, x: object, y: object, z: object) -> np.ndarray:
            return np.full(np.shape(x), self.valeur)

    superposition = SuperpositionPanaches(
        panaches=(PanacheConstant(1.5e308), PanacheConstant(1.5e308))
    )

    # When / Then — le débordement de la somme est refusé explicitement.
    with pytest.raises(ValueError, match="doit rester finie"):
        superposition.concentration(0.0, 0.0, 0.0)


def test_mnt_ascii_interpolation_preserves_the_finite_convex_bound() -> None:
    """Une moyenne convexe d'altitudes finies ne doit pas déborder."""
    # Given — les quatre sommets d'une cellule valent le maximum float64.
    maximum = np.finfo(float).max
    relief = ReliefMntAscii(
        altitudes=np.full((2, 2), maximum),
        x0=0.0,
        y0=0.0,
        pas=1.0,
    )
    # When — l'altitude est interpolée à l'intérieur de la cellule.
    altitude = relief.altitude(0.1, 0.2)
    # Then — les poids bilinéaires forment une combinaison convexe finie.
    assert np.isfinite(altitude)
    assert altitude == maximum


def test_mnt_ascii_interpolation_preserves_a_tiny_active_corner() -> None:
    """Un sommet de poids un conserve sa valeur malgré les autres échelles."""
    # Given — le coin sud-ouest est subnormal et les trois autres coins sont énormes.
    minimum = np.nextafter(0.0, 1.0)
    maximum = np.finfo(float).max
    relief = ReliefMntAscii(
        altitudes=np.array([[maximum, maximum], [minimum, maximum]]),
        x0=0.0,
        y0=0.0,
        pas=1.0,
    )
    # When — on évalue exactement au centre du coin sud-ouest.
    altitude = relief.altitude(0.0, 0.0)
    # Then — le poids un du coin actif doit préserver sa valeur subnormale.
    assert altitude == minimum


def test_mnt_ascii_interpolation_preserves_tiny_corner_at_grid_node() -> None:
    """Un sommet subnormal conserve sa valeur à un nœud de la grille."""
    # Given — le coin sud-est est subnormal et les autres coins valent float64.max.
    minimum = np.nextafter(0.0, 1.0)
    maximum = np.finfo(float).max
    relief = ReliefMntAscii(
        altitudes=np.array([[maximum, maximum], [maximum, minimum]]),
        x0=0.0,
        y0=0.0,
        pas=1.0,
    )
    # When — on évalue exactement au nœud sud-est du MNT.
    altitude = relief.altitude(1.0, 0.0)
    # Then — l'interpolation restitue exactement le sommet actif.
    assert altitude == minimum


def test_mnt_ascii_interpolation_handles_opposite_sign_extremes() -> None:
    """Une interpolation entre signes opposés reste finie aux extrêmes float64."""
    # Given — les sommets alternent entre les deux extrêmes représentables.
    maximum = np.finfo(float).max
    relief = ReliefMntAscii(
        altitudes=np.array([[maximum, -maximum], [-maximum, maximum]]),
        x0=0.0,
        y0=0.0,
        pas=1.0,
    )

    # When — on évalue au centre géométrique de la cellule.
    altitude = relief.altitude(0.5, 0.5)

    # Then — les contributions symétriques s'annulent sans débordement.
    assert np.isfinite(altitude)
    assert altitude == 0.0


def test_mnt_ascii_rejette_une_cle_entete_dupliquee() -> None:
    """Le parseur refuse les clés d'en-tête répétées."""
    texte = MNT_ASCII.replace("ncols 3", "ncols 2\nncols 3")
    with pytest.raises(ValueError, match="dupliquee"):
        ReliefMntAscii.depuis_texte(texte)


def test_mnt_ascii_rejette_une_cellule_non_numerique() -> None:
    """Le parseur contextualise les valeurs raster non numériques."""
    texte = MNT_ASCII.replace("7 8 9", "7 huit 9")
    with pytest.raises(ValueError, match="non numerique"):
        ReliefMntAscii.depuis_texte(texte)


def test_mnt_ascii_normalise_les_coordonnees_sans_debordement() -> None:
    """Une différence intermédiaire supérieure à float64.max reste calculable."""
    maximum = np.finfo(float).max
    relief = ReliefMntAscii(
        altitudes=np.array([[0.0, 2.0, 4.0]]),
        x0=-0.75 * maximum,
        y0=0.0,
        pas=0.8 * maximum,
    )
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        altitude = relief.altitude(0.75 * maximum, 0.0)
    assert altitude == 3.75


def test_mnt_ascii_rejette_une_coordonnees_extreme_hors_emprise() -> None:
    """Un indice hors emprise reste une ValueError, même si sa différence déborde."""
    maximum = np.finfo(float).max
    relief = ReliefMntAscii(
        altitudes=np.array([[0.0, 2.0, 4.0]]),
        x0=-0.75 * maximum,
        y0=0.0,
        pas=0.8 * maximum,
    )
    with (
        np.errstate(over="raise", invalid="raise", divide="raise"),
        pytest.raises(ValueError, match="emprise horizontale"),
    ):
        relief.altitude(maximum, 0.0)

