"""Contrat de la visualisation Pyodide des champs de vent."""

from __future__ import annotations

from pathlib import Path

import pytest
from IPython import display as ipython_display
from IPython.display import HTML

PAGE_PATH = Path(__file__).parents[1] / "site/projet/experiences-interactives.qmd"


def _page_python_code() -> str:
    """Extrait l'import Python de la page rendue par Quarto."""
    page = PAGE_PATH.read_text(encoding="utf-8")
    fence = "`" * 3
    block = page.split(f"{fence}{{python}}\n", 1)[1].split(f"\n{fence}", 1)[0]
    return "\n".join(line for line in block.splitlines() if not line.startswith("#|"))


def test_interactive_page_embeds_python_generated_scenarios(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """La page importe seulement la galerie calculée par le paquet Python."""
    page = PAGE_PATH.read_text(encoding="utf-8")

    assert "format: html" in page
    assert "from jdriftx.figures.wind_field_explorer import" in page
    assert "default_wind_field_scenarios" in page
    assert "render_wind_field_scenario_gallery_html" in page
    assert "vector_field(" not in page
    assert "np." not in page
    assert "<svg" not in page
    assert "pyodide" not in page
    assert "Math." not in page

    captured: list[HTML] = []
    monkeypatch.setattr(ipython_display, "display", captured.append)
    exec(compile(_page_python_code(), str(PAGE_PATH), "exec"), {})  # noqa: S102

    assert len(captured) == 1
    rendered = captured[0].data
    assert rendered.count("<svg") == 4
    assert rendered.count('class="wind-field-scenario"') == 4
    assert "Divergence moyenne estimée" in rendered
