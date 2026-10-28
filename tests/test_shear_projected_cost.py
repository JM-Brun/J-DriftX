"""Analytical regression tests for the projected travel-time shear counterexample.

See issue #123 and docs/32-conservation-coordonnees-travel-time.md.
This test records a limitation of the pairwise projected construction; it is
not a general validation or refutation of every variable-field model.
"""

from __future__ import annotations

import math

import pytest


def _projected_cost(x: float, x_a: float, v_at_source: float) -> float:
    """Projected cost downstream for u(x, y) = (v(y), 0)."""
    if v_at_source <= 0:
        raise ValueError("The shear profile must be positive at the source.")
    return (x - x_a) / v_at_source


def _directional_transport_residual(
    v_at_point: float, v_at_source: float
) -> float:
    """Return u · grad(d_A) for the analytical projected cost."""
    if v_at_source <= 0:
        raise ValueError("The shear profile must be positive at the source.")
    return v_at_point / v_at_source


def test_projected_cost_has_expected_downstream_value() -> None:
    """Check the closed-form cost at a downstream point."""
    x_a, y_a = 1.0, 0.0
    x, y = 4.0, 1.0

    # Positive, non-constant profile v(y) = 1 + y**2.
    v = lambda ordinate: 1.0 + ordinate**2
    cost = _projected_cost(x=x, x_a=x_a, v_at_source=v(y_a))

    assert cost == pytest.approx(3.0, rel=0.0, abs=1e-12)
    assert math.isfinite(cost)
    assert v(y) > 0.0


def test_shear_counterexample_violates_unit_transport_identity() -> None:
    """A non-uniform shear makes u · grad(d_A) differ from one."""
    y_a, y = 0.0, 1.0

    # v(y) = 1 + y**2 is smooth, strictly positive, and non-constant.
    v = lambda ordinate: 1.0 + ordinate**2
    residual = _directional_transport_residual(
        v_at_point=v(y), v_at_source=v(y_a)
    )

    assert residual == pytest.approx(2.0, rel=0.0, abs=1e-12)
    assert not math.isclose(residual, 1.0, rel_tol=0.0, abs_tol=1e-12)


def test_uniform_flow_is_the_control_case() -> None:
    """For constant positive v, the same identity equals one."""
    v_constant = 2.5
    residual = _directional_transport_residual(
        v_at_point=v_constant, v_at_source=v_constant
    )

    assert residual == pytest.approx(1.0, rel=0.0, abs=1e-12)
