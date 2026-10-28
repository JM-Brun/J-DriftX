# Explicit travel-time chart for the uniform reference field, and what it does not establish

> **Status — explicit conditional construction for the uniform reference field only.** This note answers a precise sub-question of [#123](https://github.com/JM-Brun/J-DriftX/issues/123): it makes the transformation $(\tau,\eta_1,\eta_2)$, its domain, regularity and Jacobian fully explicit in the one setting where they are unambiguous — a uniform flow — states the corresponding conservation theorem with explicit hypotheses, and records the verdict for the historical corpus. It does **not** reconstruct the historical variable-field model, does not derive a model-specific Jacobian for it, and does not silently emend any printed source. Companion note: [docs/32](32-conservation-coordonnees-travel-time.md).

## 1. Three objects kept separate

Following the tracking issue [#123](https://github.com/JM-Brun/J-DriftX/issues/123), this note never conflates:

1. **The general conditional result** of [docs/32](32-conservation-coordonnees-travel-time.md): a balance law in an abstract regular chart, with no specific map constructed.
2. **The printed historical claims** (2006, 2008, 2009), transcribed verbatim in docs/32, sections 6 and 7.
3. **The hypotheses needed to link them.** These are stated explicitly below and, for the historical variable-field construction, they fail.

## 2. The uniform reference field and its chart

Let the velocity be uniform, $\vec u(x)=U\,\hat e_x$ with $U>0$ constant, and let the source lie on the plane $x=0$. Define

$$
\tau(x,y,z)=\frac{x}{U},\qquad \eta_1=y,\qquad \eta_2=z,
$$

that is, the inverse map

$$
\chi(\tau,\eta_1,\eta_2)=(U\tau,\;\eta_1,\;\eta_2).
$$

Properties, all verified in closed form:

- $\chi$ is a $C^\infty$ diffeomorphism of $\mathbb R^3$ onto itself; in particular it is a regular chart in the sense of docs/32, section 3, on the whole domain.
- The Jacobian is $J=\lvert\det D\chi\rvert=U>0$, constant. Incompressibility $\nabla\cdot\vec u=0$ is here equivalent to $J$ being independent of $\tau$.
- $\nabla_x\tau=\hat e_x/U$, hence $\vec u\cdot\nabla_x\tau=1$ everywhere: the transport relation holds **exactly**. The obstruction documented by the shear counterexample (docs/32, section 5; regression test of PR #213) cannot arise in this setting.
- The chart time $\tau$ is precisely the diffusion variable $x/U$ of the uniform-flow similitude solution (equation MB06-2, docs/32 section 7): the axis variable of the 2006 reference solution **is** the travel time. This is the historical anchor of the chart, and it is valid for the uniform case only.

## 3. Coordinate flux in the uniform chart

Take the scalar balance of docs/32, equation (1), with total flux $\vec F=c\,\vec u-D\nabla c$ and isotropic diffusion $D=D\,I$. The contravariant $\tau$-flux (docs/32, equation (3)) becomes, in closed form,

$$
F^\tau = J\,\vec F\cdot\nabla_x\tau
       = U\,c - D\,\partial_x c .
$$

In the purely advective limit $D=0$ this reduces to $F^\tau=U\,c$: the travel-time flux density through a cross-section is velocity times concentration. The coordinate machinery of docs/32 therefore reproduces the standard advective flux exactly in this chart — a useful sanity check that the general formalism and the elementary computation agree.

## 4. Theorem (conditional): equality of cross-sectional fluxes

**Hypotheses.**

- **(H1)** Uniform field: $\vec u=U\hat e_x$, $U>0$, on the slab $\Omega=(x_1,x_2)\times\mathbb R^2$ (full cross-sections).
- **(H2)** Steady state: $\partial_t c=0$ on $\Omega$.
- **(H3)** No sources or sinks in the slab: $s=0$ on $\Omega$.
- **(H4)** Vanishing net lateral flux: the boundary flux through the lateral sides of the control volume is zero (satisfied in particular if the plume has compact support or sufficiently fast decay in $(y,z)$).

**Statement.** Under (H1)–(H4), the integrated flux

$$
\Phi(x)=\int_{\mathbb R^2}\bigl(U\,c-D\,\partial_x c\bigr)\,dy\,dz
$$

is independent of $x$ on $(x_1,x_2)$; equivalently $\Phi(\tau)=\Phi(U\tau)$ is constant in $\tau$.

**Proof.** Integrate the steady balance $\nabla\cdot\vec F=0$ over the control volume between the planes $x_1$ and $x_2$ and apply the divergence theorem. The lateral contribution vanishes by (H4); the two remaining boundary terms give $\Phi(x_2)-\Phi(x_1)=0$. $\blacksquare$

**Remarks.**

- The proof is a control-volume argument: the chart is not needed for the theorem itself. The chart is what expresses the result in travel-time form and connects it to the one-dimensional structure of the reduced model.
- Diffusion does **not** need to vanish. It redistributes $c$ between cross-sections but does not change the total steady flux through complete cross-sections.
- A perfectly reflective ground ($z=0$, Neumann condition $\partial_z c=0$) is compatible with (H4) on the half-space $z>0$: reflection neither creates nor destroys scalar, so the ground contributes zero net flux and can be treated as an inert lateral boundary.

## 5. How the equality breaks under a sink

If (H3) is dropped and a deposition sink $s\le 0$ is active, the same argument yields

$$
\Phi(x_2)-\Phi(x_1)=\int_{\Omega}s\,dV\le 0,
\qquad\text{i.e.}\qquad
\frac{d\Phi}{dx}=\int_{\mathbb R^2}s\;dy\,dz\;\le 0 .
$$

With deposition, the cross-sectional flux strictly decreases downstream. This formalizes the conflict recorded in docs/32, section 7, point 3: the 2006 global conservation constraint coexists, in the same article, with a deposition sink calibrated on the uniform case, and the two cannot both hold as exact physical statements. The flux equality is an idealization of the lossless steady case, not a general property.

## 6. The identity "flux = emitted quantity" is a separate statement

Even when $\Phi$ is constant, identifying its value with the emitted quantity requires three further, distinct steps:

1. **Object match.** $\Phi$ is a rate ($[M\,T^{-1}]$); the 2006 printed constraint is an inventory ($\int_{\mathbb R^3}c\,dV$, $[M]$). A rate can equal an inventory only through an emission rate $q$ or a duration convention. The two objects must not be conflated.
2. **Source balance.** $\Phi(0^+)=q$ requires the source to inject exactly $q$ into the domain, with no loss at injection.
3. **Normalization.** Units and any dimensionless weighting (for example the $u_l^+$ factor printed in the 2008 chapter) must be defined consistently.

Under (H1)–(H4) plus these three conditions, the precise statement is: **for a continuous release at rate $q$, the steady lossless cross-sectional flux equals $q$ for every downstream cross-section.** For a transient release (a puff), no steady state exists, $\Phi$ depends on $t$, and the constant-flux statement does not apply; only the time-integrated balance relates the emitted mass to downstream inventories. This rate/inventory and steady/transient distinction is absent from the printed historical statements audited so far.

## 7. What this note covers — and what it does not

- **Covered (demonstrated):** the explicit chart, its Jacobian, the exact transport relation, the conditional cross-sectional flux theorem, the sink breakdown, and the precise lossless-steady form of the "flux = emission" identity, for the uniform reference field.
- **Not covered:** the historical projected cost in variable fields. The shear counterexample (PR #213) shows that the projected cost satisfies $\vec u\cdot\nabla\tau=1$ only in the uniform case; in general it defines no global regular chart, so the hypotheses of section 4 fail there. No Jacobian is derived for the historical variable-field construction, and none should be until the sources define the transformation and the conserved quantity unambiguously.
- **Historical claims, kept as printed:** the three audited sources state three different conservation objects (2006: global volume integral; 2008: $C=\int c^+\,d\sigma$ with two printed, dimensionally inequivalent alternatives; 2009: $K$, $C_g$, $C_a$ with printed element mismatches). None is silently reconciled here; see docs/32, sections 6 and 7.

## 8. Status table

| Claim | Status |
|---|---|
| Chart $(\tau,\eta_1,\eta_2)$, Jacobian $J=U$, transport relation $\vec u\cdot\nabla\tau=1$ for the uniform reference field | **Demonstrated** (closed form, section 2) |
| Equality of cross-sectional fluxes under (H1)–(H4) | **Demonstrated** (control-volume proof, section 4) |
| Flux decay under a deposition sink | **Demonstrated** (section 5) |
| Identification $\Phi=q$ in the steady lossless case | **Demonstrated conditionally** (section 6), with the rate/inventory distinction made explicit |
| Constant-flux statement for a transient puff | **Not established** (no steady state, section 6) |
| Existence of a regular global chart for the historical projected cost in variable fields | **Not established; refuted as a general assumption** by the tested shear counterexample (PR #213) |
| 2006 printed constraint $\int_{\mathbb R^3}c\,dV=$ emitted quantity | **Historically asserted** (docs/32, section 7); conflicts with the calibrated deposition sink; best reading to date: normalization convention |
| 2008 printed $C=\int_{\mathbb R^2}c^+\,d\sigma$ | **Historically asserted**, with a dimensional ambiguity between the two printed alternatives (docs/32, section 6) |
| 2009 printed $K$, $C_g$, $C_a$ balance | **Historically asserted**, with printed element mismatches (docs/32, section 6) |
| A single unambiguous historical conserved quantity across the corpus | **Not established** |
| "Flux through every iso-$\tau$ surface $=$ emitted quantity" for the historical generalized model | **Not established** (chart undefined, quantity ambiguous, deposition unaccounted) |

## 9. Consequence for the G0-S question

**Verdict of this note:** a conservation theorem is available for the uniform reference case under explicit hypotheses; for the historical generalized similitude, the transformation $(\tau,\eta_1,\eta_2)$ is not defined by the sources as printed, so the general conditional result (docs/32) and the historical claims remain **distinct objects**. Linking them would require, at minimum: an unambiguous historical definition of the conserved quantity and its units, a transformation defined on the stated domain, and a balance accounting for deposition and boundaries. None of these is currently available from the transcribed sources.

Remaining evidence, unchanged and owner-side: the thesis (2007), the JESA 2010 version of record, and a page-by-page check of the typeset 2006 PDF against the text-layer transcription of docs/32, section 7.

No solver, benchmark, or silent emendation of any published source follows from this note.

## References

- Mohammadi, B. & Brun, J.-M. (2006). *C. R. Mécanique* 334, 634–638. DOI [10.1016/j.crme.2006.06.007](https://doi.org/10.1016/j.crme.2006.06.007) — transcribed in docs/32, section 7.
- Brun, J.-M. & Mohammadi, B. (2008). "Reduced-Order Modelling of Dispersion", chap. 14 — transcribed in docs/32, section 6.
- Bozon, N. & Mohammadi, B. (2009). *Applied Geomatics* 1, 59–74. DOI [10.1007/s12518-009-0006-0](https://doi.org/10.1007/s12518-009-0006-0) — transcribed in docs/32, section 6.
- General conditional balance in a regular chart: [docs/32](32-conservation-coordonnees-travel-time.md).
- Shear counterexample and regression test: [PR #213](https://github.com/JM-Brun/J-DriftX/pull/213).
- Tracking issue: [#123](https://github.com/JM-Brun/J-DriftX/issues/123).
