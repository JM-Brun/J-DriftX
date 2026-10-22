"""Tests for the Gaussian advection-diffusion reference solution."""

import numpy as np
import pytest

from jdriftx.advection_diffusion import gaussian_advection_diffusion


def test_zero_diffusivity_is_translated_initial_gaussian() -> None:
    x = np.array([1.0, 2.0, 3.0])
    actual = gaussian_advection_diffusion(
        x, 1.0, initial_center=0.0, velocity=1.0, diffusivity=0.0, initial_sigma=0.5
    )
    expected = gaussian_advection_diffusion(
        x - 1.0, 0.0, initial_center=0.0, velocity=1.0, diffusivity=0.0, initial_sigma=0.5
    )
    assert np.allclose(actual, expected)


def test_mass_is_conserved_on_a_domain_capturing_gaussian_tails() -> None:
    x = np.linspace(-10.0, 10.0, 20001)
    concentration = gaussian_advection_diffusion(
        x, 2.0, mass=3.0, initial_center=0.0, velocity=0.8, diffusivity=0.2, initial_sigma=0.4
    )
    assert np.trapezoid(concentration, x) == pytest.approx(3.0, rel=1e-5)


def test_diffusion_increases_variance() -> None:
    sigma0, diffusivity, time = 0.5, 0.3, 2.0
    x = np.linspace(-10.0, 10.0, 20001)
    concentration = gaussian_advection_diffusion(
        x, time, diffusivity=diffusivity, initial_sigma=sigma0
    )
    mass = np.trapezoid(concentration, x)
    mean = np.trapezoid(x * concentration, x) / mass
    variance = np.trapezoid((x - mean) ** 2 * concentration, x) / mass
    assert variance == pytest.approx(sigma0**2 + 2 * diffusivity * time, rel=1e-4)


def test_negative_diffusivity_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        gaussian_advection_diffusion(np.array([0.0]), 1.0, diffusivity=-0.1)
