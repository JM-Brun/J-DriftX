"""Offline regression tests for the DIFLU audit workflow."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pytest

from scripts.audit_diflu import audit_sampling_csv, verify_original


def test_verify_original_accepts_matching_size_and_md5() -> None:
    payload = b"example,content\n1,2\n"
    metadata = {
        "originalFileSize": len(payload),
        "md5": hashlib.md5(payload, usedforsecurity=False).hexdigest(),
    }

    result = verify_original(payload, metadata, "example.csv")

    assert result["size_verified"] is True
    assert result["md5_verified"] is True
    assert result["sha256"] == hashlib.sha256(payload).hexdigest()


def test_verify_original_rejects_size_mismatch() -> None:
    with pytest.raises(RuntimeError, match="Original size mismatch"):
        verify_original(b"abc", {"originalFileSize": 4}, "example.csv")


def test_verify_original_rejects_md5_mismatch() -> None:
    with pytest.raises(RuntimeError, match="Original MD5 mismatch"):
        verify_original(b"abc", {"md5": "00000000000000000000000000000000"}, "example.csv")


def test_audit_preserves_ea_na_and_requires_vega_bag_id(tmp_path: Path) -> None:
    path = tmp_path / "sampling.csv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["sampling_type", "sampling_bag_id"])
        writer.writeheader()
        writer.writerow({"sampling_type": "EA", "sampling_bag_id": "NA"})
        writer.writerow({"sampling_type": "VEGA", "sampling_bag_id": "V1_1"})

    report = audit_sampling_csv(path)

    assert report["row_count"] == 2
    assert report["sampling_type_counts"] == {"EA": 1, "VEGA": 1}
    assert report["semantic_checks"]["EA_literal_NA_and_VEGA_populated"] == "passed"
    assert report["sampling_bag_id_counts"] == {"EA:NA": 1, "VEGA:V1_1": 1}


def test_audit_reports_invalid_vega_bag_id(tmp_path: Path) -> None:
    path = tmp_path / "sampling.csv"
    path.write_text(
        "sampling_type,sampling_bag_id\nEA,NA\nVEGA,NA\n",
        encoding="utf-8",
    )

    report = audit_sampling_csv(path)

    assert report["semantic_checks"]["EA_literal_NA_and_VEGA_populated"] == "failed"
    assert report["semantic_checks"]["violations"] == [
        {"row": 3, "rule": "VEGA sampling_bag_id must be populated"}
    ]



def test_audit_reports_descriptive_counts_and_detection_flag_consistency(tmp_path: Path) -> None:
    path = tmp_path / "sampling.csv"
    path.write_text(
        "experiment_id,sampling_type,sampling_bag_id,sampling_id,sampling_start_time,"
        "sampling_end_time,helium_concentration_sampling_bg_corrected_flag,"
        "helium_concentration_sampling_bg_corrected,"
        "helium_concentration_sampling_bg_passage_corrected\n"
        "E1,EA,NA,A1,2026-01-01T00:00:00Z,2026-01-01T00:15:00Z,significant,0.001,0.002\n"
        "E1,EA,NA,A2,2026-01-01T00:15:00Z,2026-01-01T00:30:00Z,< LC,NA,NA\n",
        encoding="utf-8",
    )

    report = audit_sampling_csv(path)

    assert report["unique_experiment_count"] == 1
    assert report["flag_counts"] == {"< LC": 1, "significant": 1}
    assert report["time_checks"]["duration_seconds_counts"] == {"900": 2}
    assert report["time_checks"]["invalid_timestamp_rows"] == []
    assert report["time_checks"]["reversed_interval_rows"] == []
    assert report["duplicate_identity_check"]["duplicate_key_row_count"] == 0
    assert report["semantic_checks"]["detection_flag_consistency"] == "passed"
    assert report["missingness"]["helium_concentration_sampling_bg_corrected"]["literal_NA"] == 1


def test_versioned_diflu_fixture_has_reproducible_audit_summary() -> None:
    fixture = Path(__file__).parent / "fixtures/diflu/source/DIFLU_helium_release_sampling.csv"
    if not fixture.exists():
        pytest.skip("Versioned DIFLU fixture is unavailable in this checkout")

    report = audit_sampling_csv(fixture)

    assert report["row_count"] == 387
    assert report["column_count"] == 21
    assert report["unique_experiment_count"] == 19
    assert report["sampling_type_counts"] == {"EA": 234, "VEGA": 153}
    assert report["flag_counts"] == {"< LC": 64, "significant": 323}
    assert report["time_checks"]["invalid_timestamp_rows"] == []
    assert report["time_checks"]["reversed_interval_rows"] == []
    assert report["duplicate_identity_check"]["duplicate_key_row_count"] == 0
    assert report["semantic_checks"]["EA_literal_NA_and_VEGA_populated"] == "passed"
    assert report["semantic_checks"]["detection_flag_consistency"] == "passed"
