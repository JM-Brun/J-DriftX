# DIFLU compact source corpus

This directory is intended to contain the **exact original bytes** of the three small
Dataverse files needed for offline audits:

- `DIFLU_helium_release_sampling.csv`
- `DIFLU_media_dictionary.csv`
- `DIFLU_variables_dictionary.csv`

The binary/text payloads must not be edited, normalized, re-exported, or truncated.
In particular, preserve the literal `NA` values in the source data. The generated
`manifest.json` records file IDs, source URLs, byte sizes, MD5 and SHA-256 digests.

## Provenance

- Dataset: [DIFLU — DOI 10.57745/A9YC3C](https://doi.org/10.57745/A9YC3C)
- Official landing page: [Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C)
- License stated in the dataset notice: Etalab Open Licence 2.0
- Publication context: Laguionie et al. (2022), *Atmosphere*, 13(8), 1223,
  [https://doi.org/10.3390/atmos13081223](https://doi.org/10.3390/atmos13081223)

## Populate this directory

From the repository root, first download and verify the originals:

```bash
uv run python scripts/audit_diflu.py
```

Then copy the verified bytes and generate the manifest:

```bash
uv run python scripts/vendor_diflu_reference.py
```

Review the resulting files, then commit the three source files and `manifest.json`.
Do not commit the downloaded directory under `data/raw/`.

## Scope and caveats

This is a small reproducibility corpus, not a mirror of the complete dataset. The full
deposit includes much larger files that are deliberately excluded. File integrity and
structural checks do not establish scientific validity or justify an ML benchmark.
