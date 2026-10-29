"""Tests de la valeur source du panache (SourcePanache, docs/41)."""

from dataclasses import FrozenInstanceError, replace

import pytest

from jdriftx.source import SourcePanache
from jdriftx.stabilite import ClasseStabilite


def _source_valide() -> SourcePanache:
    """Retourne une source valide, à modifier dans les rejets."""
    return SourcePanache(debit=1.0, u=3.0, classe="D", hauteur=10.0)


def test_construction_valide() -> None:
    """Une source valide expose ses quatre champs de la valeur partagée."""
    # Given — une source de la famille S0 (docs/41).
    source = _source_valide()
    # When / Then — les quatre champs de la valeur partagée sont portés tels quels.
    assert source.debit == 1.0
    assert source.u == 3.0
    assert source.classe == "D"
    assert source.hauteur == 10.0


def test_classe_reconnue_par_classe_stabilite() -> None:
    """La classe est validée par ClasseStabilite, source unique de vérité."""
    # Given — une source construite avec une classe de Pasquill valide.
    source = _source_valide()
    # When / Then — la classe est reconnue par l'objet ClasseStabilite (docs/24).
    assert ClasseStabilite(source.classe) is ClasseStabilite.D


def test_hauteur_nulle_admise() -> None:
    """Une source au sol (hauteur nulle) est valide."""
    # Given — une source posée au sol.
    source = replace(_source_valide(), hauteur=0.0)
    # When / Then — la hauteur nulle est admise (invariant : positive ou nulle).
    assert source.hauteur == 0.0


@pytest.mark.parametrize(
    ("champ", "valeur", "message_attendu"),
    [
        ("debit", 0.0, "debit"),
        ("u", 0.0, "vent"),
        ("hauteur", -1.0, "hauteur"),
        ("classe", "Z", "Z"),
    ],
)
def test_refuse_valeurs_invalides(champ, valeur, message_attendu) -> None:
    """Un champ invalide est refusé à la construction de la source."""
    # Given — une source de référence valide.
    source = _source_valide()
    # When — un champ est rendu invalide.
    # Then — la construction est refusée avec le message correspondant.
    with pytest.raises(ValueError, match=message_attendu):
        replace(source, **{champ: valeur})


def test_source_immuable() -> None:
    """La source ne peut pas être modifiée après construction."""
    # Given — une source valide.
    source = _source_valide()
    # When / Then — toute mutation est refusée (dataclass figée).
    with pytest.raises(FrozenInstanceError):
        source.debit = 2.0  # type: ignore[misc]


@pytest.mark.parametrize(
    ("champ", "valeur"),
    [
        ("debit", float("nan")),
        ("debit", float("inf")),
        ("u", float("nan")),
        ("u", float("inf")),
        ("hauteur", float("nan")),
        ("hauteur", float("inf")),
    ],
)
def test_refuse_parametres_physiques_non_finis(champ: str, valeur: float) -> None:
    """Given un paramètre physique non fini, when construit, then il est refusé."""
    with pytest.raises(ValueError):
        replace(_source_valide(), **{champ: valeur})
