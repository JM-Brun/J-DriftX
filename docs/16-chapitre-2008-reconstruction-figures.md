# Chapter 14 (2008): technical map for reconstructing the figures

**Primary source:** J.-M. Brun & B. Mohammadi, “Reduced-Order Modelling of Dispersion”, in *Partial Differential Equations: Modelling and Numerical Simulation*, Springer (2008), pp. 245–256, DOI [10.1007/978-1-4020-8758-5_14].

This is an original technical synthesis, not a verbatim transcription of the chapter. Page numbers below are printed page numbers. The publicly viewable PDF was used to inspect the chapter structure and figure captions; the plotted images do not expose all numerical input data. Therefore, an original synthetic reconstruction is feasible for every figure, but an exact numerical reproduction is not yet established.

## 1. Mathematical structure to preserve

### 1.1 Multi-level model

The chapter's central architecture is hierarchical: a local injection/near-field model supplies an inlet quantity to the long-range transport model. The motivation is to reduce the search space using prior physical knowledge rather than generating a large collection of full-PDE snapshots first.

The interface between levels must be made explicit in a modern implementation: units, scalar quantity passed upward, averaging/integration domain, time interval, and assumptions. Do not couple two independently coded levels through undocumented scaling constants.

### 1.2 Plume similarity and directed transport geometry

The chapter describes a passive-scalar field in a uniform flow through a longitudinal centreline profile and a transverse spread profile. In its generalized representation, the long-range scalar has the schematic form

\[
c_g(B) = c_c(d(A,B))\, f\!\left(d_E^\perp(B),\delta(d(A,B))\right),
\]

where the directed travel coordinate is based on migration time along a characteristic, and the transverse coordinate is Euclidean distance normal to the characteristic near the projected point. This formula records the structure of the model, not all constants or the full historical parameterization.

Important distinctions:

- The travel-time coordinate is directed and depends on the wind field; it is not ordinary Euclidean distance.
- The chapter projects a target point onto the characteristic passing through the source. It assumes a unique relevant characteristic and states a rule for a non-unique projection.
- The construction may fail or become ambiguous near sources/sinks, attraction points, recirculation, separatrices, or complex characteristic topology.
- The text approximates characteristics by polynomial curves, initially cubic and with increasing order if the local velocity constraint is not met.
- It then approximates the target as lying on the characteristic and applies a correction factor to migration time; transverse distance is approximated separately. These are numerical heuristics to reproduce and stress-test, not universal geometric identities.

**Required tests:** uniform-flow analytical cases; downstream/upstream reversal; target points off a characteristic; multiple candidate projections; zero or near-zero speed; grid and polynomial-order sensitivity. Keep the historical projected pseudo-distance separate from any alternative true arrival-time solver.

### 1.3 Wind field and terrain

The chapter reconstructs a near-ground wind field from sparse observations under a divergence-free assumption and extends the horizontal flow vertically using wall-law ideas. In the presence of terrain, the flow is locally rotated to remain parallel to the ground.

The text extraction of the displayed flow-reconstruction equation is typographically ambiguous. Do not encode a guessed objective function as the authors' exact equation. Before claiming a faithful implementation, transcribe the equation from a high-resolution page image and independently derive its units and boundary assumptions.

Terrain is represented by an elevation function \(\psi(x,y)\). The chapter introduces a slope/wind-alignment quantity based on the projection of the terrain gradient onto the near-ground wind and scales migration times by a positive monotone decreasing function normalized to one for zero slope. The exact correction law and its valid range must be recovered and tested before implementation. A terrain surface rendered under a constant wind is not, by itself, a terrain-aware transport model.

### 1.4 Calibration and source identification

The chapter distinguishes parameter identification (fit model parameters to available wind/scalar observations) from source identification (search for source locations compatible with detected pollution). It describes a sensitivity-based approach and emphasizes the low computational cost of evaluating sensitivities.

A sensitivity field is not a posterior probability map. A modern reconstruction should define the observation functional, parameterization, noise assumptions, gradient method, and identifiability diagnostics. It should include deliberately ambiguous examples where distinct sources fit the same sparse observations.

## 2. Numerical scales reported in the chapter

The numerical-results section describes example treated fields of approximately 0.01–0.1 km² in a calculation region of 400 km², crop rows about 1.5 m apart, vehicle speed around 1 m/s, injection velocity around 7–10 m/s, and a representative treatment amount of 100 kg/km². The paper also discusses an intended application regime that avoids treatment under high wind or high temperature (examples given are wind above 20 km/h and air temperature above 30°C).

These values provide scale checks for a synthetic reconstruction; they are not a complete parameter file for any particular figure. Do not silently assign them to all six figures. Preserve their provenance and uncertainty in metadata.

## 3. Figure-by-figure reconstruction contract

| Figure | Printed page | Scientific objects to reconstruct | Minimum acceptance test |
|---|---:|---|---|
| 1 | 253 | Vehicle trajectory; treated plot (~10,000 m²) inside a ~400 km² domain; two wind observations; reconstructed divergence-free flow at about 3 m height | Plot and domain areas/units are consistent; divergence is verified numerically or guaranteed by analytic construction |
| 2 | 253 | Euclidean symmetric distance vs directed migration-time distance | Show both directions explicitly; test cases where historical projected cost is infinite or zero for distinct points |
| 3 | 254 | Generalized similarity solution vs direct transport-diffusion PDE solution for the same wind, compared on the reference mesh nodes | Same wind/source/domain and compatible conditions; report mesh convergence, mass balance and error norms |
| 4 | 254 | Two sources, affected regions, flow reconstructed from three measurements | Test linear superposition only under stated linear-model assumptions; show source contributions separately |
| 5 | 254–255 | Digital terrain model over ~2 km × 2 km; northward uniform wind; comparison with/without ground model | Separate terrain geometry, wind correction and transport effects using ablations and identical colour scales |
| 6 | 255 | Constructed flow, dispersion from a vineyard, sensitivity to pollution observed in lower-left corner | Define the objective and gradient; demonstrate at least one non-identifiability case; label output as sensitivity, not probability |

Figure captions and page assignments were checked against the accessible PDF. The exact original terrain grid, wind measurements, source coordinates, colour scales, and complete PDE setup are not available as machine-readable data in the chapter text inspected so far.

## 4. Recommended implementation order

1. **Figure 2 first.** Reuse the uniform-flow case from the scientific MVP. Produce an explanatory diagram, a directed cost map, and edge-case panels. Avoid coupling figure work to a new, incompatible pseudo-distance definition.
2. **Figure 1.** Use an analytic 2D divergence-free field, for example one derived from a smooth streamfunction. Add sparse observations and a schematic multi-scale domain. State that two observations do not uniquely identify a real wind field.
3. **Figure 4.** Add two source terms and compare individual fields with their sum. Confirm the assumed linearity in the governing equation.
4. **Figure 5.** Start with a deterministic synthetic terrain (smooth hill, then slope/valley). Use ablations to isolate the effects of terrain on geometry, wind and concentration.
5. **Figure 3.** Define a well-posed advection-diffusion reference problem and solve it independently; compare with the reduced representation under identical inputs. If original coefficients/boundary conditions remain unknown, label the result R1 (synthetic), not an exact reproduction.
6. **Figure 6.** Implement a transparent objective and sensitivity method; show uncertainty and source ambiguity.

## 5. Provenance and reproducibility

Each generated figure should have a machine-readable manifest containing: figure ID, source/page, fidelity level (R0 explanatory / R1 conceptual synthetic / R2 quantitative reproduction), model version, configuration, units, random seed if relevant, input provenance/licence, generation command, test results, limitations, and status.

Generate final images from versioned code. Store numerical arrays or compact reference data for regression tests; do not rely only on pixel comparisons. Use fixed colour scales when comparing panels. No figure from the copyrighted Springer volume should be copied into the public gallery. Create original visualizations and cite the source.

## 6. What this work does and does not establish

A visual match can help detect coding and conceptual errors, but it is not by itself a physical validation. A synthetic divergence-free field does not validate the historical wind reconstruction; a visually similar plume does not validate source terms or boundary conditions; and a sensitivity map does not establish unique source identification. The chapter's examples are demonstrations on selected cases, not a broad independent benchmark.

This track should support, not displace, the 1D mathematical MVP and the literature review on directed travel-time geometry. See public tracking issue [#57](https://github.com/JM-Brun/J-DriftX/issues/57).
