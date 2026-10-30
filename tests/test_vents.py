"""Tests des profils de vent et de leurs limites numériques."""

import numpy as np
import pytest

from jdriftx.vents import VentProfilPuissance


def test_ratio_sous_debordant_preserve_une_vitesse_representable() -> None:
    """Un rapport z/z_ref sous-normal ne doit pas annuler une vitesse représentable."""
    # Given — le rapport des hauteurs sous-déborde, mais sa racine est représentable.
    vent = VentProfilPuissance(u_reference=1.0, z_reference=1.0e308, exposant=0.5)

    # When — la vitesse est évaluée à une hauteur positive très faible.
    u, v, w = vent.vitesse(0.0, 0.0, 1.0e-308)

    # Then — la loi de puissance donne une vitesse de l'ordre de 1e-308 m/s.
    assert u == pytest.approx(1.0e-308, rel=1.0e-12)
    assert (v, w) == (0.0, 0.0)


def test_ratio_debordant_preserve_une_vitesse_representable() -> None:
    """Un rapport z/z_ref débordant ne doit pas invalider un produit fini."""
    # Given — le rapport déborde, mais u_ref * (z/z_ref) vaut 1e308.
    vent = VentProfilPuissance(u_reference=1.0e-308, z_reference=1.0e-308, exposant=1.0)

    # When — la vitesse est évaluée à une hauteur très élevée mais finie.
    u, v, w = vent.vitesse(0.0, 0.0, 1.0e308)

    # Then — la vitesse finale reste représentable.
    assert u == pytest.approx(1.0e308, rel=1.0e-12)
    assert (v, w) == (0.0, 0.0)


def test_vitesse_reellement_sous_representable_est_refusee() -> None:
    """Une vitesse positive mathématique mais nulle en float64 est refusée."""
    # Given — une loi dont la vitesse attendue est inférieure au plus petit subnormal.
    vent = VentProfilPuissance(u_reference=1.0, z_reference=1.0e308, exposant=1.0)

    # When / Then — le résultat non représentable n'est pas retourné comme un zéro.
    with pytest.raises(ValueError, match="doit rester finie et strictement positive"):
        vent.vitesse(0.0, 0.0, np.nextafter(0.0, 1.0))
