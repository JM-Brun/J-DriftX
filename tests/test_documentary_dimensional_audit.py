"""Dimensional and arithmetic regression checks for audited historical formulas.

These tests encode conclusions under explicitly stated conventional units.
They do not verify the visual transcription or establish the authors' intent.
See docs/46-registre-erreurs-incoherences-documentaires.md.
"""

from __future__ import annotations

import pytest

# Dimension vector order: mass, length, time. Exponents are integers for
# the quantities used in this audit (M^a L^b T^c).
Dimension = tuple[int, int, int]

MASS: Dimension = (1, 0, 0)
VOLUMETRIC_CONCENTRATION: Dimension = (1, -3, 0)
MASS_FLOW_RATE: Dimension = (1, 0, -1)
DIMENSIONLESS: Dimension = (0, 0, 0)


def _multiply_dimensions(*dimensions: Dimension) -> Dimension:
    """Multiply physical quantities by adding their dimension exponents."""
    return (
        sum(dimension[0] for dimension in dimensions),
        sum(dimension[1] for dimension in dimensions),
        sum(dimension[2] for dimension in dimensions),
    )


def _integrate_over_length(quantity: Dimension) -> Dimension:
    """Apply a length measure dz to a dimensional quantity."""
    return _multiply_dimensions(quantity, (0, 1, 0))


def _integrate_over_time(quantity: Dimension) -> Dimension:
    """Apply a time measure dt to a dimensional quantity."""
    return _multiply_dimensions(quantity, (0, 0, 1))


def _integrate_over_area(quantity: Dimension) -> Dimension:
    """Apply an area measure dσ to a dimensional quantity."""
    return _multiply_dimensions(quantity, (0, 2, 0))


def _integrate_over_volume(quantity: Dimension) -> Dimension:
    """Apply a volume measure dV to a dimensional quantity."""
    return _multiply_dimensions(quantity, (0, 3, 0))


def test_2008_alternative_definitions_of_c_plus_are_not_dimensionally_equivalent() -> None:
    """The two printed c+ alternatives differ under volumetric concentration units."""
    # Given — c_l is mass per volume; u_l+ is dimensionless.
    integrated_profile = _integrate_over_length(VOLUMETRIC_CONCENTRATION)
    product_profile = _multiply_dimensions(DIMENSIONLESS, VOLUMETRIC_CONCENTRATION)

    # When — each alternative is integrated over the horizontal area.
    integrated_mass = _integrate_over_area(integrated_profile)
    product_integral = _integrate_over_area(product_profile)

    # Then — only the vertical-integral branch has units of mass.
    assert integrated_mass == MASS
    assert product_integral == (1, -1, 0)
    assert integrated_mass != product_integral


def test_2009_equation_31_volume_measure_is_incompatible_with_injected_mass() -> None:
    """C_g dV has mass×length units, unlike K, under conventional definitions."""
    # Given — c_inj is a mass flow rate and c is mass per volume.
    injected_quantity = _integrate_over_time(MASS_FLOW_RATE)
    ground_column = _integrate_over_length(VOLUMETRIC_CONCENTRATION)

    # When — the printed Eq. (31) measure dV is applied to C_g.
    printed_integral = _integrate_over_volume(ground_column)

    # Then — K is mass while the printed integral is mass×length.
    assert injected_quantity == MASS
    assert printed_integral == (1, 1, 0)
    assert injected_quantity != printed_integral


def test_reported_two_thirds_decimal_is_arithmetically_inconsistent() -> None:
    """The reported transcription '2/3 = 0.636' is not a valid equality."""
    # Given — the arithmetic expression and the decimal reported in the audit.
    exact_fraction = 2.0 / 3.0
    printed_decimal = 0.636

    # Then — the difference is far larger than rounding at three decimal places.
    assert exact_fraction == pytest.approx(0.667, abs=0.0005)
    assert abs(exact_fraction - printed_decimal) > 0.03
    assert printed_decimal != pytest.approx(2.0 / 3.0, abs=0.0005)
