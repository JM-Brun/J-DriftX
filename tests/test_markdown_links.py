"""Tests for source Markdown link validation."""

from pathlib import Path

from scripts.check_markdown_links import check_markdown_links


def test_valid_local_file_and_anchor_are_accepted(tmp_path: Path) -> None:
    """A relative Markdown target and its heading anchor should resolve."""
    docs = tmp_path / "docs"
    docs.mkdir()
    target = docs / "target.md"
    target.write_text("# Valid heading\n", encoding="utf-8")
    source = docs / "source.md"
    source.write_text("[target](target.md#valid-heading)\n", encoding="utf-8")

    assert check_markdown_links(tmp_path, [source]) == []


def test_missing_file_and_anchor_are_reported(tmp_path: Path) -> None:
    """Missing local paths and missing Markdown anchors should be diagnosed."""
    docs = tmp_path / "docs"
    docs.mkdir()
    target = docs / "target.md"
    target.write_text("# Existing heading\n", encoding="utf-8")
    source = docs / "source.md"
    source.write_text(
        "[missing](absent.md) and [bad anchor](target.md#no-such-heading)\n",
        encoding="utf-8",
    )

    diagnostics = check_markdown_links(tmp_path, [source])

    assert len(diagnostics) == 2
    assert any("local target not found" in item for item in diagnostics)
    assert any("anchor #no-such-heading not found" in item for item in diagnostics)


def test_encoded_spaces_and_external_links_are_handled(tmp_path: Path) -> None:
    """Encoded spaces resolve locally while external links are ignored."""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "target file.md").write_text("# Heading\n", encoding="utf-8")
    source = docs / "source.md"
    source.write_text(
        "[encoded](target%20file.md#heading) "
        "[external](https://example.org/not-local.md#external)\n",
        encoding="utf-8",
    )

    assert check_markdown_links(tmp_path, [source]) == []


def test_links_inside_fenced_code_are_ignored(tmp_path: Path) -> None:
    """Markdown examples inside fenced code blocks must not be checked."""
    docs = tmp_path / "docs"
    docs.mkdir()
    source = docs / "source.md"
    source.write_text(
        "Example:\n\n```markdown\n[broken](missing.md)\n```\n",
        encoding="utf-8",
    )

    assert check_markdown_links(tmp_path, [source]) == []


def test_directory_links_and_accented_heading_anchors(tmp_path: Path) -> None:
    """Directory targets and accent-insensitive GitHub heading slugs resolve."""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "bibliographie").mkdir()
    target = docs / "target.md"
    target.write_text("### 3.2 Correction recommandée\n", encoding="utf-8")
    source = docs / "source.md"
    source.write_text(
        "[directory](bibliographie/) [heading](target.md#32-correction-recommandee)\n",
        encoding="utf-8",
    )

    assert check_markdown_links(tmp_path, [source]) == []

def test_em_dash_and_quotes_match_github_heading_slug(tmp_path: Path) -> None:
    """Em dashes remain separators; typographic quotes do not add separators."""
    docs = tmp_path / "docs"
    docs.mkdir()
    target = docs / "target.md"
    target.write_text(
        "### Complément d'analyse — deux sens distincts de « multi-niveaux »\n",
        encoding="utf-8",
    )
    source = docs / "source.md"
    source.write_text(
        "[heading](target.md#complement-danalyse--deux-sens-distincts-de-multi-niveaux)\n",
        encoding="utf-8",
    )

    assert check_markdown_links(tmp_path, [source]) == []

