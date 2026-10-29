# Conservation in travel-time coordinates: what can be derived

> **Status — partial mathematical result, not a reconstruction of the historical Drift-X model.**  
> This note derives the general balance law under a regular change of coordinates. It does not establish that the historical construction satisfies the assumptions below, nor that the pollutant flux through every iso-travel-time surface equals the emitted quantity. The 2006 paper explicitly states a global volume-integral constraint, which is not the same proposition as constant flux through every iso-travel-time surface; see the [critical audit of the 2006 source](45-audit-article-mohammadi-brun-2006.md).

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

The analytical regression test for this example is documented in [the shear-counterexample test note](33-test-contre-exemple-cisaillement.md). The dimensional consequences of the audited 2008/2009 formulas are covered separately, under explicit conventional-unit assumptions, in [the documentary dimensional audit tests](../tests/test_documentary_dimensional_audit.py). It checks the closed-form projected cost, the non-unit transport residual for a non-constant profile, and the uniform-flow control case. The test is deliberately independent of a numerical solver; it freezes this mathematical counterexample rather than validating the full historical model.

## 6. Primary-source transcription and dimensional audit (2009 article)

**Source-identity caveat added 29 October 2026:** the equations numbered (28)–(31) below are not present in the accessible 17-page STIC & Environnement manuscript `hal-00468863`, which uses bracketed equation labels [1]–[7] in §2. The earlier attribution in this note to “Bozon & Mohammadi (2009), *Applied Geomatics*” has not been reconciled with the distinct JESA 2010 record (`hal-02594312`, DOI `10.3166/jesa.44.445-461`) or backed by a source PDF in the current project files. Therefore, treat the following as a provisional transcription from a previously consulted publisher-text source whose exact bibliographic identity still needs verification; do **not** cite Eqs. (28)–(31) as equations of either the STIC 2009 manuscript or JESA 2010 until that identity is resolved. No new acquisition was performed for this audit.

### Published definitions

The paper states that the total injected quantity over \( [0,T] \) is
\[
K=\int_0^T c_{\rm inj}(t)\,dt. \tag{29}
\]
It then defines the amount reaching the ground by
\[
C_g(x,y)=\int_{z\leq z_0} c(x,y,z)\,dz, \tag{30}
\]
and the amount remaining in the atmosphere beyond source distance \(R_0\) by
\[
C_a=K-\int_{R\geq R_0} C_g(x,y)\,dV, \tag{31}
\]
with \(R=\sqrt{x^2+y^2}\). The printed integration element in Eq. (31) is \(dV\), not \(dx\,dy\).

### 2008 chapter: definition of the conserved quantity

The accessible scan of Brun & Mohammadi (2008), §2.1–2.2 (printed pp. 247–248; chapter PDF pp. 244–245), provides a more direct comparison. In §2.1, Eq. (2), the local model imposes
\[
\nabla\cdot u_l=0,\qquad u_l\cdot\nabla c_l=0,\qquad
\int_{\mathbb R^3}c_l\,dV=\text{given}.
\tag{BM08-2}
\]
The last condition identifies the local integral of \(c_l\) over volume as the given quantity. Under the usual mass-concentration interpretation, \(c_l\) therefore has units \([M L^{-3}]\) and the integral has units of mass. The first two conditions state incompressibility and steady advection of the scalar along the local velocity; they are not, by themselves, a full advection–diffusion balance with sources, deposition, or boundary losses.

In §2.2, the chapter then prints two alternatives for the quantity supplied to the long-range model:
\[
c^+(x,y)=\int_{z>H}c_l\,dz
\quad\text{or}\quad
c^+(x,y)=u_l^+c_l,
\qquad
u_l^+=\max\left(0,\frac{u\cdot z}{\|u\|}\right),
\tag{BM08-3}
\]
followed by
\[
C=\int_{\mathbb R^2}c^+(x,y)\,d\sigma,
\tag{BM08-4}
\]
which “should be conserved” by the reduced-order transport model (the chapter's Eq. (2.2), printed p. 248). The factor \(u_l^+\) as defined is dimensionless.

With \(c_l\) in \([M L^{-3}]\), the first alternative for \(c^+\) has units \([M L^{-2}]\), and its integral over \(d\sigma\) has units of mass. The second alternative \(u_l^+c_l\) retains units \([M L^{-3}]\), so its integral over an area has units \([M L^{-1}]\), not mass. **The two printed alternatives are therefore not dimensionally equivalent under the same conventional definition of \(c_l\).** The source does not explain a different convention or an additional length factor in the displayed definition.

This does not establish which alternative the authors intended or prove that the implementation is invalid. It establishes that the conservation target is stated, but the notation as transcribed does not uniquely specify a dimensionally consistent conserved quantity without an additional definition or correction from the authors/source.

### Dimensional audit under the conventional interpretation

Assume, provisionally, that \(c\) is a volumetric mass concentration with units \([M L^{-3}]\), and that \(c_{\rm inj}\) is a mass emission rate with units \([M T^{-1}]\). Then:

| Quantity | Printed definition | Implied units | Assessment |
|---|---|---|---|
| \(K\) | \(\int c_{\rm inj}(t)dt\) | \([M]\) | Consistent with total emitted mass under the stated assumption |
| \(C_g\) | \(\int c\,dz\) | \([M L^{-2}]\) | Areal mass density after vertical integration |
| \(\int C_g\,dV\) in Eq. (31) | Integrates \(C_g\) against a volume element | \([M L]\) | **Dimensionally inconsistent with \(K\)** under this interpretation |
| \(\int C_g\,dx\,dy\) | Not what the paper prints | \([M]\) | Would be dimensionally compatible, but is only a possible correction, not an established authorial intent |

The same paper's Eq. (28) states that the “total mass” in a subdomain satisfies
\[
\int_{\omega^i} c^i\,dV
=
\int_{\partial\omega^i}
c^i\left(\frac{\vec u^i}{\|\vec u^i\|}\cdot\vec n^i\right)dS.
\tag{28}
\]
With \(c^i\) interpreted as a volumetric concentration, the left side has units of mass, while the right side has units of mass per length: the normalized velocity and normal are dimensionless, leaving concentration times area. This is another dimensional mismatch as printed. The later Eqs. (38)–(40) also define an incoming quantity through an average of concentration multiplied by a dimensionless directional factor, then equate it to a volume integral of concentration; those expressions likewise need a clarification of the intended units/normalization.

### What this establishes—and what it does not

- **Established from the accessible STIC 2009 manuscript:** Eqs. [1]–[7] are printed in §2; the multi-level mass identity after Eq. [4] and the Eq. [31]-style integral expression must not be conflated. The manuscript's mass identity has the same dimensional mismatch under the conventional volumetric-concentration interpretation.
- **Provisional, source identity unresolved:** the displayed Eqs. (28), (31), and (38)–(40) are not in the accessible STIC 2009 manuscript. Their dimensional mismatches are reproducible from the displayed definitions, but their attribution to a specific publication is not yet verified.
- **Not established:** whether this reflects typographical errors, a nonstandard definition of \(c\), omitted normalization, or a deeper derivation issue. The text alone does not decide among these explanations.
- **Not authorized:** silently replacing \(dV\) with \(dx\,dy\), inserting a velocity factor, or treating the published equations as a validated mass-conservation proof.

The article does describe the global velocity construction as divergence-free and presents conservation as a constraint, but divergence-free velocity alone does not imply conservation of a passive scalar. The displayed equations require a consistent scalar definition and measure before they can be used as a physical mass balance.

The versioned 2006 PDF is now visually inspected for equations (1), (2) and (4); the audit in [45](45-audit-article-mohammadi-brun-2006.md) records the literal transcription and the ambiguity in (4). The 2008 Springer chapter has been inspected from an accessible scan, but that scan is not a publisher-hosted copy. The accessible STIC 2009 manuscript is a separate source. The JESA 2010 PDF has not been made available in the current project-file context, and the earlier publisher-text attribution for equations (28)–(31) remains unresolved; do not conflate these sources.

## 7. Primary-source transcription: Mohammadi & Brun (2006)

The open-access publisher PDF of the founding Note is available from the Comptes Rendus site (DOI [10.1016/j.crme.2006.06.007](https://doi.org/10.1016/j.crme.2006.06.007); direct PDF: https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf) and was retrieved and transcribed on 28 October 2026. **Extraction caveat:** the PDF text layer garbles some math glyphs (integrals, radicals, exponents, sum signs); the equations below are reconstructions from the text layer and the surrounding prose, and this is flagged wherever it matters. They must be checked against the typeset PDF before being cited as verbatim. No suspected typo is silently repaired.

### Assimilation setting and transport assumption (§1)

The model parameters \(p\) — computation-domain definition, topography, meteo conditions, source locations, nozzle characteristics — are determined through the assimilation objective

\[
\min_{p\in\mathcal O} J(p)=\|\vec u(p)-\vec u_{\rm obs}\|^2+\|c(p,\vec u(p))-c_{\rm obs}\|^2,
\tag{MB06-1}
\]

(the exponents and norm bars are not visible in the text layer; the printed equation is a sum of two norms). The article then states that \(\vec u(p)\) est « un champ de vitesse à divergence nulle servant au transport de \(c(p,\vec u(p))\) »: the transport velocity is divergence-free **by assumption** in this Note, not by a construction given there.

### Similitude solution in a uniform flow (§2)

The scalar emitted at the origin and transported by a planar uniform flow \(U\) is modelled by

\[
c(x,y)=c_c(x)\,f\left(y,\delta(x)\right),
\qquad
c_c(x)\sim\exp(-a(U)x),
\qquad
f\left(y,\delta(x)\right)\sim\exp\left(-b(U,\delta(x))\,y^2\right),
\tag{MB06-2}
\]

with \(a(\cdot)\) positive monotone decreasing and \(b(\cdot,\cdot)\) positive, increasing in \(U\), decreasing in \(\delta\); \(c_c\) is the axis distribution of the plume of thickness \(\delta(x)\), with the jet analogy recalled by the authors (parabolic in laminar, linear in turbulent). This uniform-flow solution is what §3 generalizes.

### Directed cost and global conservation constraint (§3)

After recalling a symmetric metric distance \(d_M(AB)=\int_0^1(\overrightarrow{AB}^{\,T}M(A+t\,\overrightarrow{AB})\overrightarrow{AB})^{1/2}dt\) (Eq. (3) of the article, reconstructed from the text layer), the Note introduces the pseudo-distance: if \(A\) is upstream of \(B\), then \(d(B,A)=\infty\) and

\[
d(A,B)=\int_A^{B^\perp}\frac{ds}{u},
\]

the migration time from \(A\) to \(B^\perp\) along the characteristic through \(A\), « que l'on supposera unique, écartant les sources et puits ». \(B^\perp\) is the projection of \(B\) onto that characteristic; non-unique projections are resolved by choosing the projection direction that best satisfies \((\vec u\cdot\nabla c=0)\) at \(B\). This is the founding printed definition of the projected cost analysed as \(T_{\rm proj}\) in docs/19 and docs/30.

The conservation statement follows, transcribed in full (the integration element is not visible in the text layer; a volume element, as in the 2008 chapter's corresponding constraint transcribed in the previous section, is the natural reading):

> « On introduit, par ailleurs, une condition de conservation globale pour la quantité transportée \(\int_{\mathbb R^3} c(p,u(p))=\) quantité totale émise, solution d'un modèle de traitement au niveau du rang de culture [1]. »

The article then states explicitly that the construction is **not** a distance: \(d(A,B)=0\nRightarrow A=B\), non-symmetry \(d(A,B)\neq d(B,A)\), and possible failure of the triangle inequality.

### Velocity completion from sparse observations (§3, Eq. 4)

\[
\vec u=\nabla\varphi,
\qquad
-\Delta\varphi=\sum_{i=1,\dots,n_{\rm obs}}\|\nabla\varphi-\vec u_{\rm obs}\|,
\tag{MB06-4}
\]

as extracted (the text layer does not show how the observation points enter the terms inside the sum); the article presents this as the completion of the velocity field from \(n_{\rm obs}\) observation points, and offers as an alternative a coarse migration-time grid with interpolation. The equation is not dimensionally homogeneous as reconstructed — a pointwise-source or optimality reading may be intended — and is transcribed without repair.

### Generalized similitude ansatz (§3, Eq. 5)

\[
c=c_c\left(d(p)\right)\,f\left(d^\perp(p),\,\delta\left(d(p)\right)\right),
\tag{MB06-5}
\]

where \(d^\perp\) is the Euclidean distance in the local normal direction to the source characteristic (direction \(BB^\perp\)). The directed cost \(d\) enters (i) as the argument of the axis profile \(c_c\) and (ii) as the argument of the growth law \(\delta\): it replaces the axial variable of the uniform-flow solution (MB06-2). No per-surface flux statement is attached to this ansatz in the article.

### Calibration of the deposition sink (§5)

In the validation examples, the reference PDE (transport–diffusion–deposition, stabilized finite elements, explicit RK2 in time) uses a deposition sink which « a été calé pour un champ de vitesse uniforme pour retrouver la solution de dispersion analytique (2) par la solution de l'EDP », and the similitude solutions are accumulated by linearity to treat a moving source. The sink term is thus **calibrated on the uniform case**, not derived from a balance law.

### What the 2006 source adds to the conservation question

1. **The 2006 conservation statement is global, not per-surface.** It is a volume integral of \(c\) over \(\mathbb R^3\), set equal to the total emitted quantity. **No flux conservation across iso-\(\tau\) surfaces is claimed anywhere in the article.** The per-surface reading is therefore not supported by the founding source.
2. **It is dimensionally consistent as printed** — under the conventional \(c\in[M\,L^{-3}]\), the integral is a mass — in contrast with the printed Eqs. (28)/(31) of the 2009 article transcribed in the previous section.
3. **As a physical claim it conflicts with deposition.** §5 calibrates a deposition sink; with a sink active, the atmospheric inventory \(\int_{\mathbb R^3}c\,dV\) falls below the emitted mass once deposition starts. Pending the thesis [1], the constraint is therefore best read as a **normalization/calibration convention of the reduced model** — the emitted quantity being itself « solution d'un modèle de traitement au niveau du rang de culture » — not as a theorem derived from a balance law.
4. **The three audited sources state three different conservation objects as printed:** 2006 — global volume integral of \(c\) over \(\mathbb R^3\); 2008 — \(C=\int_{\mathbb R^2}c^+\,d\sigma\) with two printed alternatives for \(c^+\) (not dimensionally equivalent); 2009 — \(K\), \(C_g\), \(C_a\) with printed element mismatches. A single unambiguous historical conserved quantity has **not** been identified across the corpus as printed; the reconstruction must not average or silently reconcile the three.
5. **The founding Note itself documents the metric failures** (non-separation, non-symmetry, triangle inequality), consistent with the project's audited understanding of \(T_{\rm proj}\).
6. **Thesis date evidence.** Reference [1] of the article cites « J.-M. Brun, Modélisation à complexité réduite de la dérive, Thèse université Montpellier II, 2007 »: the founding Note's own bibliography dates the thesis **2007** (the repository cites 2006; the 2007 date is corroborated by this primary source).

## 8. What remains to be established from the primary model

A complete historical reconstruction still requires the equations and assumptions of the near-/far-field model, not only the general balance law above.

| Item | Status in this note |
|---|---|
| Conservative scalar balance and control-volume identity | Derived from (1) |
| Coordinate transformation and Jacobian terms for a regular chart | Derived conditionally on a time-independent diffeomorphism |
| Conditions for constant integrated flux across coordinate surfaces | Derived conditionally in (5) |
| Identification of that flux with emitted quantity \(Q\) | **Not established** |
| Historical definition of \\(C\\), its units and integration domain reconciled across sources | **Partially reconstructed** — the thesis (2007 per bibliographic records), §7.3, Eqs. (7.12)–(7.13), p. 129, confirms the two alternative definitions of \\(c^+\\) and the intended conservation of \\(M_C\\); their dimensional mismatch remains unresolved. See [thesis audit](43-audit-these-brun-conservation-g0s.md). |
| Applicability of a regular \((\tau,\eta_1,\eta_2)\) chart to the historical projected pseudo-distance | **Not established; counterexamples show it cannot be assumed generally** |
| Treatment of source/sink, diffusion, deposition, ground reflection and open boundaries in the historical model | **Still to reconstruct** |
| Correction factor printed as “2/3 = 0.636” in Brun & Mohammadi (2008, chapter p. 251) and Bozon & Mohammadi (2009, publisher version of record); also present in the accessible Bozon, Sinfort & Mohammadi (2010) author manuscript | **Arithmetic inconsistency confirmed in two published sources**: $2/3 \approx 0.667$, whereas $0.636 \approx 2/\pi$. Both 2008 and 2009 describe the factor as a stochastic averaged cosine for angles between 0 and $\pi$, but neither inspected passage supplies a derivation of the averaging distribution that resolves the discrepancy. $2/\pi$ is plausible, not proven as the intended factor; do not silently rewrite any source. |

## 9. Decision and next evidence required

This derivation establishes a conditional conservation statement for a regular coordinate chart; it does **not** validate the historical model or prove a universal iso-\(\tau\) conservation claim.

To resolve the historical question:

1. Obtain verifiable full text for the primary sources and transcribe their governing near-/far-field equations and definitions verbatim, preserving notation. Status: 2006 §1–§5 transcribed from the open-access publisher PDF (§7 above), with text-layer caveats; 2008 §2.1–2.2 transcribed from an accessible scan (§6; publisher-hosted copy still unavailable); 2009 transcribed from the publisher version of record (§6); thesis §7.1.3 and §7.3 transcribed from a third-party mirror and summarized in [the thesis audit](43-audit-these-brun-conservation-g0s.md). Still to authenticate the thesis binary in Git against HAL and to transcribe the JESA 2010 version of record.
2. Inspect the versioned thesis binary and verify its title page, pagination, identity and redistribution rights. The thesis text found in the mirror explicitly gives Eqs. (7.12)–(7.13), p. 129, but the mirror is not proof that the Git binary is identical to the HAL file.
3. **Decision for the J-DriftX reconstruction (not an attribution of historical intent):** use a mass inventory, not a flux, for the (c^+,M_C) definition. Retain the vertically integrated branch (c^+(x,y)=\int_{z>H}c_{loc}(x,y,z)\,dz), then define (M_C=\int_{\Omega_{xy}}c^+\,dx\,dy). Under ([c_{loc}]=\mathrm{kg\,m^{-3}}), this gives ([c^+]=\mathrm{kg\,m^{-2}}) and ([M_C]=\mathrm{kg}). Do not retain (u^+_{loc}c_{loc}) as an equivalent branch: it is dimensionally incompatible because (u^+_{loc}) is dimensionless. The editorial corrections and their limits are documented in [the thesis audit, §3.2](43-audit-these-brun-conservation-g0s.md#32-correction-recommandee-pour-une-reconstruction-coherente-avec-impact-minimal-sur-la-these). The original printed equations remain transcribed unchanged in the audit; this is a reconstruction decision, not proof of authorial intent or of conservation by the historical model.
4. Derive the specific coordinate map and its Jacobian only if the historical equations define a regular map on the stated domain. The one setting where the map is fully explicit — the uniform reference field — is now constructed in [docs/37](37-transformation-tau-eta-cas-uniforme.md), together with the conditional flux theorem and the rate/inventory distinction.
5. Add each physical source, sink and boundary term to the balance before claiming conservation.
6. Conclude with one of three outcomes: proof under explicit assumptions, a restricted result, or a documented statement that the claim cannot be reconstructed from available evidence.

No variable-field solver or new benchmark should be justified by this note alone.

## References

- Mohammadi, B. & Brun, J.-M. (2006). “Similitude généralisée et modélisation géométrique à complexité réduite.” *Comptes Rendus Mécanique*, 334(10), 634–638. https://doi.org/10.1016/j.crme.2006.06.007. Open PDF: https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2006.06.007.pdf (open-access publisher PDF; retrieved and transcribed in §7; the article’s reference [1] dates the thesis 2007).
- Brun, J.-M. (2007 according to bibliographic records). *Modèles à complexité réduite de transport pour applications environnementales*, thesis, Université Montpellier II. AGRIS/INRAE: https://agris.fao.org/search/en/providers/122439/records/647471f379cbb2c2c1b2123c. Thesis audit of Eqs. (7.12)–(7.13): [docs/43](43-audit-these-brun-conservation-g0s.md). The equations were read from a third-party mirror, not authenticated against the Git binary.
- Brun, J.-M. & Mohammadi, B. (2008). “Reduced-Order Modelling of Dispersion.” In *Partial Differential Equations: Modelling and Numerical Simulation*, CSM vol. 16, chap. 14, pp. 245–256. https://doi.org/10.1007/978-1-4020-8758-5_14
  Accessible scan used for the transcription: https://www.sgo.fi/~j/baylie/Partial%20Differential%20Equations%20-%20Modelling%20and%20Numerical%20Simulation%20-%20R.%20Glowinski%2C%20P.%20Neittaanmaki%20%28Springer%2C%202008%29%20WW.pdf
- Bozon, N. & Mohammadi, B. (2009). “GIS-based atmospheric dispersion modelling: Forecasting the pesticide atmospheric spray drift from a vineyard plot to a watershed.” *Applied Geomatics*, 1, 59–74. https://doi.org/10.1007/s12518-009-0006-0. Publisher version of record; its online text prints `2/3 = 0.636` and describes the factor as a stochastic averaged cosine.
- Project source reconciliation and shear counterexample: [PR #122](https://github.com/JM-Brun/J-DriftX/pull/122).
- Follow-up tracking issue: [#123](https://github.com/JM-Brun/J-DriftX/issues/123).
