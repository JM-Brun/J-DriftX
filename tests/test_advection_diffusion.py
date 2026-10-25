"""Tests for the Gaussian advection-diffusion reference solution."""

import numpy as np
import pytest

from jdriftx.advection_diffusion import gaussian_advection_diffusion


def test_zero_diffusivity_is_translated_initial_gaussian() -> None:
    """À diffusivité nulle, la solution est la gaussienne initiale translatée."""
    # Given — une grille et le même profil évalué à l'instant translaté.
    x = np.array([1.0, 2.0, 3.0])
    # When — la solution est évaluée à t = 1 avec une diffusivité nulle.
    actual = gaussian_advection_diffusion(
        x, 1.0, initial_center=0.0, velocity=1.0, diffusivity=0.0, initial_sigma=0.5
    )
    expected = gaussian_advection_diffusion(
        x - 1.0, 0.0, initial_center=0.0, velocity=1.0, diffusivity=0.0, initial_sigma=0.5
    )
    # Then — la solution translatée coïncide avec la solution initiale.
    assert np.allclose(actual, expected)


def test_mass_is_conserved_on_a_domain_capturing_gaussian_tails() -> None:
    """La masse est conservée sur un domaine couvrant les queues de gaussienne."""
    # Given — un domaine large et une gaussienne de masse 3 advectée et diffusée.
    x = np.linspace(-10.0, 10.0, 20001)
    # When — la solution est évaluée à t = 2.
    concentration = gaussian_advection_diffusion(
        x, 2.0, mass=3.0, initial_center=0.0, velocity=0.8, diffusivity=0.2, initial_sigma=0.4
    )
    # Then — l'intégrale trapézoïdale restitue la masse à 1e-5 relatif.
    assert np.trapezoid(concentration, x) == pytest.approx(3.0, rel=1e-5)


def test_diffusion_increases_variance() -> None:
    """La variance croît selon la loi exacte sigma0^2 + 2*K*t."""
    # Given — une gaussienne de sigma0 = 0,5, diffusivité 0,3, évaluée à t = 2.
    sigma0, diffusivity, time = 0.5, 0.3, 2.0
    x = np.linspace(-10.0, 10.0, 20001)
    # When — la solution est évaluée puis les moments mesurés par intégration.
    concentration = gaussian_advection_diffusion(
        x, time, diffusivity=diffusivity, initial_sigma=sigma0
    )
    mass = np.trapezoid(concentration, x)
    mean = np.trapezoid(x * concentration, x) / mass
    variance = np.trapezoid((x - mean) ** 2 * concentration, x) / mass
    # Then — la variance mesurée vaut sigma0^2 + 2*K*t à 1e-4 relatif.
    assert variance == pytest.approx(sigma0**2 + 2 * diffusivity * time, rel=1e-4)


def test_negative_diffusivity_is_rejected() -> None:
    """Une diffusivité négative est refusée."""
    # Given / When / Then — une diffusivité négative déclenche le refus.
    with pytest.raises(ValueError, match="non-negative"):
        gaussian_advection_diffusion(np.array([0.0]), 1.0, diffusivity=-0.1)
