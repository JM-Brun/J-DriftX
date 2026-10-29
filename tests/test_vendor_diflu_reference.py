"""Offline tests for staging the compact DIFLU reference corpus."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts.vendor_diflu_reference import CORE_FILES, load_verified_records, stage


def _write_audit_fixture(audit_dir: Path) -> dict[str, bytes]:
    """Create a minimal audit report and the three exact-byte source fixtures."""
    audit_dir.mkdir(parents=True)
    payloads = {
        filename: f"fixture for {filename}\n".encode()
        for filename in CORE_FILES
    }
    records = []
    for index, (filename, payload) in enumerate(payloads.items(), start=1):
        (audit_dir / filename).write_bytes(payload)
        records.append(
            {
                "dataverse_label": filename,
                "original_filename": filename,
                "dataverse_file_id": 758565 + index,
                "download_url": f"https://entrepot.recherche.data.gouv.fr/api/access/datafile/{758565 + index}?format=original",
                "integrity": {
                    "expected_size_bytes": len(payload),
                    "actual_size_bytes": len(payload),
                    "expected_md5": hashlib.md5(payload, usedforsecurity=False).hexdigest(),
                    "actual_md5": hashlib.md5(payload, usedforsecurity=False).hexdigest(),
                    "size_verified": True,
                    "md5_verified": True,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                },
            }
        )
    (audit_dir / "audit-report.json").write_text(
        json.dumps({"dataset_pid": "doi:10.57745/A9YC3C", "files": records}),
        encoding="utf-8",
    )
    return payloads


def test_stage_copies_original_bytes_and_writes_manifest(tmp_path: Path) -> None:
    audit_dir = tmp_path / "audit"
    output_dir = tmp_path / "reference"
    payloads = _write_audit_fixture(audit_dir)

    manifest = stage(audit_dir, output_dir)

    assert {record["filename"] for record in manifest["files"]} == set(CORE_FILES)
    for filename, payload in payloads.items():
        assert (output_dir / filename).read_bytes() == payload
    persisted = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert persisted["license"] == "Etalab Open Licence 2.0"
    assert len(persisted["files"]) == 3


def test_staging_rejects_source_changed_after_audit(tmp_path: Path) -> None:
    audit_dir = tmp_path / "audit"
    _write_audit_fixture(audit_dir)
    (audit_dir / CORE_FILES[0]).write_bytes(b"changed after audit")

    with pytest.raises(RuntimeError, match="Size changed|MD5 changed|SHA-256 changed"):
        load_verified_records(audit_dir)


def test_staging_requires_official_size_and_md5_verification(tmp_path: Path) -> None:
    audit_dir = tmp_path / "audit"
    _write_audit_fixture(audit_dir)
    report_path = audit_dir / "audit-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["files"][0]["integrity"]["md5_verified"] = False
    report_path.write_text(json.dumps(report), encoding="utf-8")

    with pytest.raises(RuntimeError, match="size and MD5 must both be verified"):
        load_verified_records(audit_dir)


def test_staging_refuses_to_overwrite_different_existing_bytes(tmp_path: Path) -> None:
    audit_dir = tmp_path / "audit"
    output_dir = tmp_path / "reference"
    _write_audit_fixture(audit_dir)
    output_dir.mkdir()
    (output_dir / CORE_FILES[0]).write_bytes(b"not the official bytes")

    with pytest.raises(RuntimeError, match="Refusing to overwrite different existing file"):
        stage(audit_dir, output_dir)



def test_staging_is_idempotent_for_identical_sources(tmp_path: Path) -> None:
    """Repeated staging must preserve the same manifest and source bytes."""
    audit_dir = tmp_path / "audit"
    output_dir = tmp_path / "reference"
    _write_audit_fixture(audit_dir)

    first = stage(audit_dir, output_dir)
    first_manifest = (output_dir / "manifest.json").read_bytes()
    second = stage(audit_dir, output_dir)

    assert first == second
    assert (output_dir / "manifest.json").read_bytes() == first_manifest
