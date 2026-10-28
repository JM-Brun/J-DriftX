# Conservation in travel-time coordinates: what can be derived

> **Status — partial mathematical result, not a reconstruction of the historical Drift-X model.**  
> This note derives the general balance law under a regular change of coordinates. It does not establish that the historical construction satisfies the assumptions below, nor that the pollutant flux through every iso-travel-time surface equals the emitted quantity.

## 1. Question and quantities that must not be conflated

Let \(c(x,t)\) be a scalar concentration, \(u(x,t)\) a velocity field, and \(D(x,t)\) a diffusion tensor. Three distinct quantities may arise:

1. **Scalar mass in a volume**: \(M_\Omega(t)=\int_\Omega c\,dx\) (units depend on the scalar and on whether \(c\) is a mass or number concentration).
2. **Scalar flux through a surface**: \(\int_\Sigma (cu-D\nabla c)\cdot n\,dS\), with units of scalar amount per unit time.
3. **Volumetric flow rate**: \(\int_\Sigma u\cdot n\,dS\), with units of volume per unit time.

They are not interchangeable. In particular, incompressibility (\(\nabla\cdot u=0\)) concerns the third quantity; it does not by itself conserve the first or the second.

The historical sources motivate a conservation constraint, but the passages audited so far do not establish that this constraint is exactly the scalar flux through every surface of constant \(\tau\). The derivation below therefore starts from a general scalar balance rather than assuming that stronger conclusion.

## 2. Starting point: the conservative scalar balance

Write the total scalar flux as
\[
F = cu-D\nabla c,
\]
and allow a volumetric source/sink term \(s\). A conservative advection–diffusion balance is
\[
\partial_t c + \nabla_x\cdot F=s.
\tag{1}
\]

For a fixed control volume \(\Omega\) with outward normal \(n\), the divergence theorem gives
\[
\frac{d}{dt}\int_\Omega c\,dx
= -\int_{\partial\Omega}F\cdot n\,dS
  +\int_\Omega s\,dx.
\tag{2}
\]

Equation (2) is the mass balance. It says that the amount inside a volume changes according to net boundary flux and sources/sinks. It does **not** say that the flux across an arbitrary internal surface is constant. Such a conclusion needs additional geometry and assumptions.

## 3. Regular travel-time coordinates

Suppose a map
\[
x=\chi(\tau,\eta_1,\eta_2)
\]
is a \(C^1\) diffeomorphism on a coordinate patch. Here \(\tau\) is a coordinate and \((\eta_1,\eta_2)\) label points on a coordinate surface. Let
\[
J=\left|\det D\chi\right|>0,
\qquad
\nabla_x\tau \text{ be defined on the patch}.
\]

The change of variables gives
\[
dx=J\,d\tau\,d\eta_1\,d\eta_2.
\]
The contravariant flux in the \(\tau\)-direction is
\[
F^\tau=J\,F\cdot\nabla_x\tau.
\tag{3}
\]
This is the flux density associated with the coordinate surfaces; it is not generally equal to \(cu\cdot n\), because it includes diffusion and because the surface measure and normal are encoded by the coordinate transformation.

The Piola transformation of (1), for a time-independent coordinate map, is
\[
\partial_t(Jc)
+\partial_\tau F^\tau
+\partial_{\eta_1}F^{\eta_1}
+\partial_{\eta_2}F^{\eta_2}
=Js,
\tag{4}
\]
where \(F^{\eta_i}=J F\cdot\nabla_x\eta_i\). Equation (4) is a coordinate form of the same conservation law, not a new conservation principle.

If the coordinate map depends on time, additional geometric transport terms are required; (4) must not be used unchanged.

## 4. When is the flux across \(\tau=\text{constant}\) conserved?

Define the integrated coordinate flux through a patch of the \(\tau\)-surface by
\[
\Phi(\tau,t)=\int_A F^\tau(\tau,\eta,t)\,d\eta_1d\eta_2.
\]

Integrating (4) over a slab \([\tau_1,\tau_2]\times A\) yields
\[
\Phi(\tau_2,t)-\Phi(\tau_1,t)
=\int_{\text{slab}}\!
\left(Js-\partial_t(Jc)
-\partial_{\eta_1}F^{\eta_1}
-\partial_{\eta_2}F^{\eta_2}\right)
\,d\tau d\eta_1d\eta_2.
\tag{5}
\]
The tangential derivative terms can equivalently be expressed as boundary fluxes along the sides of the coordinate patch.

Consequently, equality of the two integrated fluxes follows only when the right-hand side of (5) vanishes—for example, under a steady balance, no sources/sinks in the slab, and zero net lateral flux through the sides of the patch. Other physical boundary conditions may yield other balances. These conditions must be demonstrated for the domain and model under study; they cannot be inferred from \(\nabla\cdot u=0\) alone.

Even if \(\Phi\) is constant in \(\tau\), identifying its value with the total emitted amount \(Q\) additionally requires a compatible source boundary/control-volume balance, consistent units and normalization, and treatment of all losses and boundaries.

## 5. Why the historical construction is not yet covered

The above derivation assumes a single regular, locally invertible coordinate map \(\chi\). It does not apply automatically to a pairwise projected cost built by projecting a target onto a characteristic through a source. Such a construction need not define a global travel-time coordinate:

- a characteristic projection may be non-unique or fail to exist;
- the projected cost can fail separation or the triangle inequality;
- the cost may not satisfy the local eikonal/transport relation \(u\cdot\nabla\tau=1\);
- stagnation, closed orbits, domain exits and finite-time blow-up can obstruct a global coordinate system;
- diffusion, deposition, reflection, source terms and open boundaries change the scalar balance.

A previously documented shear counterexample illustrates one obstruction. For \(u(x,y)=(v(y),0)\), \(v(y)>0\), the historical projected cost from \(A=(x_A,y_A)\) downstream is
\[
d_A(x,y)=\frac{x-x_A}{v(y_A)},
\qquad
 u\cdot\nabla d_A=\frac{v(y)}{v(y_A)}.
\]
For non-constant \(v\), the last expression is not identically one. Therefore this projected cost cannot simply be substituted for a global travel-time coordinate in (3)–(5).

## 6. Primary-source transcription and dimensional audit (2009 article)

The publisher's open-access HTML for Bozon & Mohammadi (2009), *Applied Geomatics*, exposes the following statements and equations directly. They are transcribed here as printed; no suspected typo is silently repaired.

### Published definitions

The paper states that the total injected quantity over \\( [0,T] \\) is
\\[
K=\\int_0^T c_{\\rm inj}(t)\\,dt. \\tag{29}
\\]
It then defines the amount reaching the ground by
\\[
C_g(x,y)=\\int_{z\\leq z_0} c(x,y,z)\\,dz, \\tag{30}
\\]
and the amount remaining in the atmosphere beyond source distance \\(R_0\\) by
\\[
C_a=K-\\int_{R\\geq R_0} C_g(x,y)\\,dV, \\tag{31}
\\]
with \\(R=\\sqrt{x^2+y^2}\\). The printed integration element in Eq. (31) is \\(dV\\), not \\(dx\\,dy\\).

### Dimensional audit under the conventional interpretation

Assume, provisionally, that \\(c\\) is a volumetric mass concentration with units \\([M L^{-3}]\\), and that \\(c_{\\rm inj}\\) is a mass emission rate with units \\([M T^{-1}]\\). Then:

| Quantity | Printed definition | Implied units | Assessment |
|---|---|---|---|
| \\(K\\) | \\(\\int c_{\\rm inj}(t)dt\\) | \\([M]\\) | Consistent with total emitted mass under the stated assumption |
| \\(C_g\\) | \\(\\int c\\,dz\\) | \\([M L^{-2}]\\) | Areal mass density after vertical integration |
| \\(\\int C_g\\,dV\\) in Eq. (31) | Integrates \\(C_g\\) against a volume element | \\([M L]\\) | **Dimensionally inconsistent with \\(K\\)** under this interpretation |
| \\(\\int C_g\\,dx\\,dy\\) | Not what the paper prints | \\([M]\\) | Would be dimensionally compatible, but is only a possible correction, not an established authorial intent |

The same paper's Eq. (28) states that the “total mass” in a subdomain satisfies
\\[
\\int_{\\omega^i} c^i\\,dV
=
\\int_{\\partial\\omega^i}
c^i\\left(\\frac{\\vec u^i}{\\|\\vec u^i\\|}\\cdot\\vec n^i\\right)dS.
\\tag{28}
\\]
With \\(c^i\\) interpreted as a volumetric concentration, the left side has units of mass, while the right side has units of mass per length: the normalized velocity and normal are dimensionless, leaving concentration times area. This is another dimensional mismatch as printed. The later Eqs. (38)–(40) also define an incoming quantity through an average of concentration multiplied by a dimensionless directional factor, then equate it to a volume integral of concentration; those expressions likewise need a clarification of the intended units/normalization.

### What this establishes—and what it does not

- **Established from the publisher text:** the equations above are printed in the 2009 article; the apparent unit mismatches are reproducible from their displayed definitions.
- **Established conditionally:** under the conventional volumetric-concentration interpretation, Eqs. (28), (31), and the Eqs. (38)–(40) sequence are not dimensionally homogeneous as printed.
- **Not established:** whether this reflects typographical errors, a nonstandard definition of \\(c\\), omitted normalization, or a deeper derivation issue. The text alone does not decide among these explanations.
- **Not authorized:** silently replacing \\(dV\\) with \\(dx\\,dy\\), inserting a velocity factor, or treating the published equations as a validated mass-conservation proof.

The article does describe the global velocity construction as divergence-free and presents conservation as a constraint, but divergence-free velocity alone does not imply conservation of a passive scalar. The displayed equations require a consistent scalar definition and measure before they can be used as a physical mass balance.

The official 2006 article is available from *Comptes Rendus Mécanique* (DOI \\([10.1016/j.crme.2006.06.007](https://doi.org/10.1016/j.crme.2006.06.007)\\)); its publisher PDF could not be retrieved through the current source interface for a reliable equation-by-equation transcription. The 2008 Springer chapter's full publisher text is also not available in the accessible record. Therefore, the 2009 transcription above must not be presented as if it resolved the exact notation in the 2006 paper or the 2008 chapter.

## 7. What remains to be established from the primary model

A complete historical reconstruction still requires the equations and assumptions of the near-/far-field model, not only the general balance law above.

| Item | Status in this note |
|---|---|
| Conservative scalar balance and control-volume identity | Derived from (1) |
| Coordinate transformation and Jacobian terms for a regular chart | Derived conditionally on a time-independent diffeomorphism |
| Conditions for constant integrated flux across coordinate surfaces | Derived conditionally in (5) |
| Identification of that flux with emitted quantity \(Q\) | **Not established** |
| Historical definition of \(C\), its units and integration domain reconciled across sources | **Still to reconstruct** |
| Applicability of a regular \((\tau,\eta_1,\eta_2)\) chart to the historical projected pseudo-distance | **Not established; counterexamples show it cannot be assumed generally** |
| Treatment of source/sink, diffusion, deposition, ground reflection and open boundaries in the historical model | **Still to reconstruct** |
| Correction factor printed as “2/3 = 0.636” in the accessible Bozon, Sinfort & Mohammadi (2010) manuscript; a related published paper by Bozon & Mohammadi (2009) also prints it | **Arithmetic inconsistency confirmed in published text**: $2/3 \approx 0.667$, whereas $0.636 \approx 2/\pi$. The 2009 paper describes the factor as a stochastic averaged cosine, but does not provide a formal derivation on the accessible page. This supports—but does not prove—the inference that $2/\pi$ was intended. Whether the same expression appears in Brun & Mohammadi (2008) remains unverified; do not silently rewrite any source. |

## 8. Decision and next evidence required

This derivation establishes a conditional conservation statement for a regular coordinate chart; it does **not** validate the historical model or prove a universal iso-\(\tau\) conservation claim.

To resolve the historical question:

1. Obtain verifiable full text for Mohammadi & Brun (2006, §3) and Brun & Mohammadi (2008, §2.2); transcribe their governing near-/far-field equations and definitions verbatim, preserving notation. The 2009 publisher equations above are a separate related source, not a substitute.
2. Recover and inspect the thesis or an authoritative implementation if available; verify bibliographic metadata separately.
3. Identify precisely what \(c^+\) and \(C\) denote, their units, and their integration domains.
4. Derive the specific coordinate map and its Jacobian only if the historical equations define a regular map on the stated domain.
5. Add each physical source, sink and boundary term to the balance before claiming conservation.
6. Conclude with one of three outcomes: proof under explicit assumptions, a restricted result, or a documented statement that the claim cannot be reconstructed from available evidence.

No variable-field solver or new benchmark should be justified by this note alone.

## References

- Mohammadi, B. & Brun, J.-M. (2006). “Similitude généralisée et modélisation géométrique à complexité réduite.” *Comptes Rendus Mécanique*, 334(10), 634–638. https://doi.org/10.1016/j.crme.2006.06.007. Open PDF: https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf
- Brun, J.-M. & Mohammadi, B. (2008). “Reduced-Order Modelling of Dispersion.” In *Partial Differential Equations: Modelling and Numerical Simulation*, CSM vol. 16, chap. 14, pp. 245–256. https://doi.org/10.1007/978-1-4020-8758-5_14
- Bozon, N. & Mohammadi, B. (2009). “GIS-based atmospheric dispersion modelling: Forecasting the pesticide atmospheric spray drift from a vineyard plot to a watershed.” *Applied Geomatics*, 1, 59–74. https://doi.org/10.1007/s12518-009-0006-0. Publisher version of record; its online text prints `2/3 = 0.636` and describes the factor as a stochastic averaged cosine.
- Project source reconciliation and shear counterexample: [PR #122](https://github.com/JM-Brun/J-DriftX/pull/122).
- Follow-up tracking issue: [#123](https://github.com/JM-Brun/J-DriftX/issues/123).
