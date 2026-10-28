# Analytical regression test: projected cost in a shear flow

**Status:** narrow mathematical regression test. This note documents what the test establishes and, equally importantly, what it does not establish.

Related tracking: [issue #211](https://github.com/JM-Brun/J-DriftX/issues/211), [issue #123](https://github.com/JM-Brun/J-DriftX/issues/123), and [test module](../tests/test_shear_projected_cost.py).

## 1. Question under test

The historical projected construction assigns a downstream point B=(x,y), relative to a source A=(x_A,y_A), the cost obtained by projecting B onto the characteristic through A. For the shear field

\[
u(x,y)=(v(y),0), \qquad v(y)>0,
\]

the characteristic through A is horizontal and the projected cost is

\[
d_A(x,y)=\frac{x-x_A}{v(y_A)}.
\]

The question is whether this pairwise cost satisfies the local travel-time identity

\[
u(x,y)\cdot\nabla d_A(x,y)=1.
\]

This identity is expected of a differentiable travel-time field transported at unit rate along the velocity field. The test asks whether the projected expression above satisfies it in a non-uniform shear.

## 2. Analytical derivation

Since d_A depends on x but not on y,

\[
\nabla d_A=\left(\frac{1}{v(y_A)},0\right).
\]

Therefore,

\[
u\cdot\nabla d_A
=(v(y),0)\cdot\left(\frac{1}{v(y_A)},0\right)
=\frac{v(y)}{v(y_A)}.
\]

For the smooth, strictly positive profile v(y)=1+y², choose y_A=0 and evaluate at y=1. Then v(y_A)=1, v(y)=2, and

\[
u\cdot\nabla d_A=\frac{2}{1}=2\ne1.
\]

The projected cost is thus **not** a solution of this local transport identity for this point in this shear field. This is a counterexample to the general assumption that the projected construction automatically has the unit-rate property in variable velocity fields.

## 3. What the tests cover

| Test | Expected result | Purpose |
|---|---:|---|
| `test_projected_cost_has_expected_downstream_value` | d_A(4,1)=3, for A=(1,0) | Guards the explicit projected-cost formula and a finite output |
| `test_shear_counterexample_violates_unit_transport_identity` | u·∇d_A=2, not 1 | Freezes the analytical counterexample |
| `test_uniform_flow_is_the_control_case` | u·∇d_A=1 for constant positive speed | Ensures the identity is recovered in the uniform-flow control case |

The numerical tolerance is explicit (abs=1e-12, rel=0.0) because these assertions evaluate closed-form expressions, not an approximate PDE solution. This tight tolerance is not a claim about numerical-solver accuracy.

Run the focused test:

```bash
uv run pytest -q tests/test_shear_projected_cost.py
```

Run the full test suite before merging:

```bash
uv run pytest
```

## 4. Scope and limitations

This is an **analytical regression test**, not a solver benchmark.

It establishes that:
- the stated projected-cost formula gives the expected downstream value in the chosen example;
- its directional transport residual is 2, not 1, at the selected point in the non-uniform shear;
- the same algebra gives 1 for a uniform positive velocity.

It does **not** establish that:
- every possible variable-field travel-time model is invalid;
- the historical implementation necessarily uses this formula in every regime;
- a numerical solver is accurate or inaccurate;
- conservation of scalar mass or flux follows or fails in every model;
- J-DriftX has or lacks scientific value overall.

The helper functions in the test module are intentionally small, local representations of the formulas. They are not production APIs and should not be reused as a substitute for a physical model.

## 5. Why this test is useful

The example is a compact falsification test for a specific mathematical assumption. It makes a subtle limitation executable and reviewable, without introducing discretization, boundary conditions, diffusion, source terms, or benchmark-data dependencies that would obscure the point.

The test should remain separate from future solver validation. If a numerical implementation is later added, it will need its own tests for discretization, convergence, boundary conditions, and comparison with analytical or independently computed references.

## References

- [Conservation and travel-time coordinates: derivation and limits](32-conservation-coordonnees-travel-time.md), especially §5.
- [Issue #211](https://github.com/JM-Brun/J-DriftX/issues/211): requested analytical unit test.
- [Issue #123](https://github.com/JM-Brun/J-DriftX/issues/123): broader reconstruction of the projected-cost construction.
