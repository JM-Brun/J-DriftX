# Graph contribution workflow

**Status (2026-10-27):** the first public pilot is implemented in J-DriftX. [PR #100](https://github.com/JM-Brun/J-DriftX/pull/100) provides the typed TOML registry, validator, Mermaid generator and static page; [PR #101](https://github.com/JM-Brun/J-DriftX/pull/101) adds the structural extractor. Both are merged. Automatic reconciliation with semantic metadata is not implemented.

## Current commands and boundary

Regenerate the reviewed semantic graph after editing the TOML registry:

```bash
uv run python -m jdriftx.graphe_connaissances
```

Extract a deterministic inventory of structural facts:

```bash
uv run python -m jdriftx.extraction_graphe --sortie /tmp/graphe-extrait.json
```

The reconciliation diagnostics proposed in the current PR compare only local file locators, not the meaning of nodes or edges:

```bash
uv run python -m jdriftx.diagnostic_graphe --sortie /tmp/diagnostic-graphe.json
```

The report separates:
- **mapped files:** an extracted source file has a registry node pointing to the same path;
- **unmapped files:** an extracted source file is not directly referenced by a registry node;
- **registry locators without extracted facts:** a local path under an extracted source area does not appear in the inventory.

These are diagnostics, not automatically failing errors. Some files may intentionally be absent from the curated semantic graph. Existing registry validation remains responsible for general local-link existence and semantic registry consistency.

## Objective

The generated graph is a view of source-controlled material, not an independent source of truth. Prefer mechanical extraction for facts that can be observed safely, and human-reviewed metadata for meaning.

## What should be automatic?

| Source | Safe initial extraction | Do not infer automatically |
|---|---|---|
| Python | Module, class, function and test names with line locators | Scientific validity, proof, or that a test proves a general claim |
| Quarto/Markdown | Page title, headings, citation occurrences, links | That a citation supports a nearby statement or that a link is a semantic dependency |
| Registry | Types, nodes, edges, local locators and declared provenance | Truth of an edge merely because it passes schema validation |

## Rollout

1. Review the registry against the MVP-S 1D traceability matrix.
2. Exercise the structural extractor on a clean checkout.
3. Review the locator reconciliation report and decide which uncovered files merit curated nodes.
4. Keep navigation links distinct from semantic edges.
5. Make evidence scope explicit; do not equate a test with a proof or scientific validation.
6. Extend to `llm-lab` and the public portfolio only after the pilot proves maintainable.
