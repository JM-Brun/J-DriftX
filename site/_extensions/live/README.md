# Quarto Live (vendored extension)

This directory vendors the upstream [r-wasm/quarto-live](https://github.com/r-wasm/quarto-live) Quarto extension so that the published site can execute Python in the browser through Pyodide without a Python server.

- Upstream project: https://github.com/r-wasm/quarto-live
- Upstream documentation: https://r-wasm.github.io/quarto-live/
- License: MIT; see [LICENSE.md](LICENSE.md).
- Vendored on: 2026-10-23.

The JavaScript runtime, Lua filter and OJS templates are upstream infrastructure. Do not add J-DriftX scientific equations or model logic to these files. Scientific calculations should remain in the Python package `jdriftx`; OJS should only provide controls and present returned values.

To update the vendored extension, compare the upstream release and its license, replace the complete required extension files together, and run the Quarto CI. The current experience also builds the `jdriftx` wheel into the static site so Pyodide can import the same Python implementation used by the regular test suite.
