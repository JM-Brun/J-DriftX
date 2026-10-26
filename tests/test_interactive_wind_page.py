"""Contrat de la visualisation Pyodide des champs de vent."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

import pytest

PAGE_PATH = Path(__file__).parents[1] / "site/projet/experiences-interactives.qmd"


def _pyodide_code() -> str:
    """Extrait le calcul Python embarqué dans la page interactive."""
    page = PAGE_PATH.read_text(encoding="utf-8")
    fence = "`" * 3
    block = page.split(f"{fence}{{pyodide}}\n", 1)[1].split(f"\n{fence}", 1)[0]
    return "\n".join(line for line in block.splitlines() if not line.startswith("#|"))


@pytest.mark.parametrize(
    ("field_kind", "expected_vector"),
    [
        ("Uniforme", "(2.00, 0.00)"),
        ("Cisaillement linéaire", "(2.25, 0.00)"),
        ("Radial (source / puits)", "(0.70, 0.35)"),
    ],
)
def test_interactive_page_uses_python_vector_field(field_kind: str, expected_vector: str) -> None:
    """La page délègue chaque famille au code Python testé du paquet."""
    page = PAGE_PATH.read_text(encoding="utf-8")

    assert "from jdriftx.figures.wind_field_explorer import" in page
    assert "render_wind_field_explorer_html" in page
    assert "vector_field(" not in page
    assert "np." not in page
    assert "<svg" not in page
    assert "Math." not in page

    namespace = {
        "fieldKind": field_kind,
        "baseSpeed": 2.0,
        "angleDeg": 0.0,
        "shear": 0.25,
        "radialStrength": 0.35,
        "probeX": 2.0,
        "probeY": 1.0,
    }
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(_pyodide_code(), str(PAGE_PATH), "exec"), namespace)  # noqa: S102

    rendered = output.getvalue()
    assert "<svg" in rendered
    assert 'class="vector-field-svg"' in rendered
    assert expected_vector in rendered
    assert "Divergence moyenne estimée" in rendered
