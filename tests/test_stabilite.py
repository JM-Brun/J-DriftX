"""Tests du modele objet des classes de stabilite de Pasquill."""

import pytest

from jdriftx.similitude import CLASSES, sigma_y, sigma_z
from jdriftx.stabilite import ClasseStabilite, FormeSigmaZ


def test_les_six_classes_dans_l_ordre() -> None:
    """L'enum porte exactement les six classes de Pasquill, de A a F."""
    # Given — la nomenclature historique a six classes.
    # When — les membres de l'enum sont enumeres.
    membres = [classe.value for classe in ClasseStabilite]
    # Then — l'ordre et le contenu sont A a F, identiques a CLASSES.
    assert membres == ["A", "B", "C", "D", "E", "F"]
    assert CLASSES == ("A", "B", "C", "D", "E", "F")


def test_regime_de_chaque_classe() -> None:
    """Chaque classe porte son regime de stabilite documente."""
    # Given — les regimes attendus, classe par classe.
    attendus = [
        (ClasseStabilite.A, "tres instable"),
        (ClasseStabilite.B, "moderement instable"),
        (ClasseStabilite.C, "faiblement instable"),
        (ClasseStabilite.D, "neutre"),
        (ClasseStabilite.E, "faiblement stable"),
        (ClasseStabilite.F, "stable"),
    ]
    # When / Then — chaque classe expose son regime.
    for classe, regime in attendus:
        assert classe.regime == regime


def test_conditions_typiques_renseignees() -> None:
    """Chaque classe documente des conditions typiques non vides."""
    # Given — les six classes.
    # When / Then — chaque condition typique est une phrase non vide.
    for classe in ClasseStabilite:
        assert isinstance(classe.conditions_typiques, str)
        assert len(classe.conditions_typiques) > 20
        assert classe.conditions_typiques == classe.conditions_typiques.strip()


def test_formes_sigma_z_trois_membres() -> None:
    """FormeSigmaZ expose les trois formes avec leurs identifiants historiques."""
    # Given — les identifiants du socle (selecteur historique de similitude).
    # When — les membres de l'enum sont enumeres.
    membres = {forme.value for forme in FormeSigmaZ}
    # Then — exactement lin, sqrt, inv.
    assert membres == {"lin", "sqrt", "inv"}


@pytest.mark.parametrize(
    ("classe", "attendu"),
    [
        (ClasseStabilite.A, (0.22, 0.0001)),
        (ClasseStabilite.B, (0.16, 0.0001)),
        (ClasseStabilite.C, (0.11, 0.0001)),
        (ClasseStabilite.D, (0.08, 0.0001)),
        (ClasseStabilite.E, (0.06, 0.0001)),
        (ClasseStabilite.F, (0.04, 0.0001)),
    ],
)
def test_coefficients_sigma_y_historiques(
    classe: ClasseStabilite, attendu: tuple[float, float]
) -> None:
    """Les coefficients de Briggs de sigma_y sont exactement ceux du socle."""
    # Given — les coefficients historiques du depot (tables Briggs rurales).
    # When — la classe expose ses coefficients.
    coefficients = classe.coeff_sigma_y
    # Then — ils sont inchanges par rapport au socle d'avant refactorisation.
    assert coefficients == attendu


@pytest.mark.parametrize(
    ("classe", "attendu"),
    [
        (ClasseStabilite.A, (FormeSigmaZ.LINEAIRE, 0.20, 0.0)),
        (ClasseStabilite.B, (FormeSigmaZ.LINEAIRE, 0.12, 0.0)),
        (ClasseStabilite.C, (FormeSigmaZ.RACINE, 0.08, 0.0002)),
        (ClasseStabilite.D, (FormeSigmaZ.RACINE, 0.06, 0.0015)),
        (ClasseStabilite.E, (FormeSigmaZ.INVERSE, 0.03, 0.0003)),
        (ClasseStabilite.F, (FormeSigmaZ.INVERSE, 0.016, 0.0003)),
    ],
)
def test_coefficients_sigma_z_historiques(
    classe: ClasseStabilite, attendu: tuple[FormeSigmaZ, float, float]
) -> None:
    """Les formes et coefficients de Briggs de sigma_z sont exactement ceux du socle."""
    # Given — les formes et coefficients historiques du depot.
    # When — la classe expose forme et coefficients.
    forme, b, d = classe.coeff_sigma_z
    # Then — forme et valeurs sont inchanges par rapport au socle.
    assert (forme, b, d) == attendu


def test_formes_sigma_z_par_famille() -> None:
    """Les formes suivent les familles A-B lineaire, C-D racine, E-F inverse."""
    # Given — les familles de lois de Briggs par groupe de classes.
    familles = [
        (ClasseStabilite.A, FormeSigmaZ.LINEAIRE),
        (ClasseStabilite.B, FormeSigmaZ.LINEAIRE),
        (ClasseStabilite.C, FormeSigmaZ.RACINE),
        (ClasseStabilite.D, FormeSigmaZ.RACINE),
        (ClasseStabilite.E, FormeSigmaZ.INVERSE),
        (ClasseStabilite.F, FormeSigmaZ.INVERSE),
    ]
    # When / Then — la forme exposee par chaque classe est celle de sa famille.
    for classe, forme in familles:
        assert classe.coeff_sigma_z[0] is forme


def test_enum_acceptee_par_les_fonctions_de_similitude() -> None:
    """sigma_y et sigma_z acceptent l'enum comme la lettre equivalente."""
    # Given — un point de calcul et la classe D sous ses deux formes.
    x = 1000.0
    # When — les fonctions sont appelees avec la lettre puis avec l'enum.
    sy_lettre, sz_lettre = sigma_y(x, "D"), sigma_z(x, "D")
    sy_enum, sz_enum = sigma_y(x, ClasseStabilite.D), sigma_z(x, ClasseStabilite.D)
    # Then — les resultats coincident exactement.
    assert sy_enum == sy_lettre
    assert sz_enum == sz_lettre


def test_classe_inconnue_refusee_message_inchange() -> None:
    """Une classe hors nomenclature est refusee, message historique inchange."""
    # Given — une classe hors nomenclature.
    # When / Then — l'appel est refuse avec le message historique.
    with pytest.raises(ValueError, match="Classe de stabilite inconnue : 'Z'"):
        sigma_y(100.0, "Z")
    with pytest.raises(ValueError, match="Classe de stabilite inconnue : 'Z'"):
        sigma_z(100.0, "Z")
