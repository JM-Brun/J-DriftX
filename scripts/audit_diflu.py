#!/usr/bin/env python3
"""Fetch and audit the core DIFLU files reproducibly from Recherche Data Gouv.

Raw files are written locally. The script verifies original-file size/checksum when
Dataverse publishes them, then writes a machine-readable manifest and audit report.
Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

BASE_URL = "https://entrepot.recherche.data.gouv.fr"
DATASET_PID = "doi:10.57745/A9YC3C"
LIST_URL = f"{BASE_URL}/api/datasets/:persistentId/versions/:latest/files"
USER_AGENT = "J-DriftX-DIFLU-audit/1.0"
CORE_FILES = (
    "DIFLU_helium_release_sampling.tab",
    "DIFLU_media_dictionary.tab",
    "DIFLU_variables_dictionary.tab",
)


def fetch_bytes(url: str, timeout: float) -> tuple[bytes, dict[str, str], str]:
    """Fetch a URL from the official HTTPS host and return body, headers and final URL."""
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "entrepot.recherche.data.gouv.fr":
        raise ValueError(f"Refusing non-official URL: {url}")
    request = Request(url, headers={"User-Agent": USER_AGENT})  # noqa: S310
    try:
        # The URL is restricted to the official HTTPS host above.
        with urlopen(request, timeout=timeout) as response:  # noqa: S310
            return (
                response.read(),
                {key.lower(): value for key, value in response.headers.items()},
                response.geturl(),
            )
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Request failed: {url}: {exc}") from exc


def json_response(payload: bytes, description: str) -> dict[str, Any]:
    """Decode an API JSON object, rejecting unexpected response shapes."""
    try:
        value = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"{description} did not return valid JSON") from exc
    if not isinstance(value, dict) or value.get("status") == "ERROR":
        raise RuntimeError(f"{description} returned an API error or unexpected JSON")
    return value


def verify_original(payload: bytes, metadata: dict[str, Any], filename: str) -> dict[str, Any]:
    """Verify original bytes against the original size and MD5 published by Dataverse."""
    expected_size = metadata.get("originalFileSize")
    expected_md5 = metadata.get("md5")
    actual_md5 = hashlib.md5(payload, usedforsecurity=False).hexdigest()
    checks: dict[str, Any] = {
        "expected_size_bytes": expected_size,
        "actual_size_bytes": len(payload),
        "expected_md5": expected_md5,
        "actual_md5": actual_md5,
    }
    if isinstance(expected_size, int) and len(payload) != expected_size:
        raise RuntimeError(
            f"Original size mismatch for {filename}: expected {expected_size}, got {len(payload)}"
        )
    if isinstance(expected_md5, str) and actual_md5.lower() != expected_md5.lower():
        raise RuntimeError(f"Original MD5 mismatch for {filename}")
    checks["size_verified"] = isinstance(expected_size, int)
    checks["md5_verified"] = isinstance(expected_md5, str)
    checks["sha256"] = hashlib.sha256(payload).hexdigest()
    return checks


def _value(row: dict[str, str | None], column: str) -> str:
    """Return a trimmed field while preserving literal domain values such as NA."""
    return (row.get(column) or "").strip()


def _missingness(rows: list[dict[str, str | None]], fieldnames: list[str]) -> dict[str, Any]:
    """Count literal NA, blank cells, and detection-limit markers separately by column."""
    result = {}
    for column in fieldnames:
        counts = {
            "literal_NA": sum(_value(row, column) == "NA" for row in rows),
            "blank": sum(_value(row, column) == "" for row in rows),
            "below_detection_marker": sum(_value(row, column) == "< LC" for row in rows),
        }
        if any(counts.values()):
            result[column] = counts
    return result


def _audit_detection_flags(
    rows: list[dict[str, str | None]], fieldnames: list[str]
) -> tuple[dict[str, int], list[dict[str, Any]]]:
    """Check consistency between detection flags and their documented concentration fields."""
    flag_column = "helium_concentration_sampling_bg_corrected_flag"
    corrected_column = "helium_concentration_sampling_bg_corrected"
    passage_column = "helium_concentration_sampling_bg_passage_corrected"
    if flag_column not in fieldnames:
        return {}, []

    flag_counts = dict(sorted(Counter(_value(row, flag_column) for row in rows).items()))
    violations = []
    for row_number, row in enumerate(rows, start=2):
        flag = _value(row, flag_column)
        corrected = _value(row, corrected_column) if corrected_column in fieldnames else ""
        passage = _value(row, passage_column) if passage_column in fieldnames else ""
        if flag == "< LC" and corrected_column in fieldnames and corrected != "NA":
            violations.append(
                {
                    "row": row_number,
                    "rule": "< LC flag requires literal NA in background-corrected concentration",
                }
            )
        elif (
            flag == "significant"
            and corrected_column in fieldnames
            and corrected in {"", "NA", "< LC"}
        ):
            violations.append(
                {
                    "row": row_number,
                    "rule": (
                        "significant flag requires a numeric background-corrected concentration"
                    ),
                }
            )
        if flag == "< LC" and passage_column in fieldnames and passage != "NA":
            violations.append(
                {
                    "row": row_number,
                    "rule": "< LC flag requires literal NA in passage-corrected concentration",
                }
            )
    return flag_counts, violations


def _audit_times(rows: list[dict[str, str | None]], fieldnames: list[str]) -> dict[str, Any]:
    """Summarize sampling durations and report malformed or reversed time intervals."""
    start_column, end_column = "sampling_start_time", "sampling_end_time"
    if start_column not in fieldnames or end_column not in fieldnames:
        return {}
    durations = Counter()
    invalid_rows, reversed_rows = [], []
    for row_number, row in enumerate(rows, start=2):
        try:
            start = datetime.fromisoformat(_value(row, start_column).replace("Z", "+00:00"))
            end = datetime.fromisoformat(_value(row, end_column).replace("Z", "+00:00"))
            duration = int((end - start).total_seconds())
            durations[str(duration)] += 1
            if duration < 0:
                reversed_rows.append(row_number)
        except (ValueError, TypeError):
            invalid_rows.append(row_number)
    return {
        "duration_seconds_counts": dict(sorted(durations.items(), key=lambda item: int(item[0]))),
        "invalid_timestamp_rows": invalid_rows,
        "reversed_interval_rows": reversed_rows,
    }


def _audit_duplicate_keys(
    rows: list[dict[str, str | None]], fieldnames: list[str]
) -> dict[str, Any]:
    """Count repeated sample keys without assuming they are scientifically independent."""
    columns = [
        "experiment_id",
        "sampling_type",
        "sampling_id",
        "sampling_bag_id",
        "sampling_start_time",
        "sampling_end_time",
    ]
    if not all(column in fieldnames for column in columns):
        return {}
    keys = [tuple(_value(row, column) for column in columns) for row in rows]
    return {"identity_columns": columns, "duplicate_key_row_count": len(keys) - len(set(keys))}


def _numeric_ranges(
    rows: list[dict[str, str | None]], fieldnames: list[str]
) -> dict[str, dict[str, float | int]]:
    """Summarize observed numeric ranges without imputing or coercing nonnumeric markers."""
    columns = [
        "helium_release_height",
        "helium_release_flow",
        "sampling_latitude",
        "sampling_longitude",
        "sampling_height",
        "sampling_flowrate",
        "helium_concentration_decision_threshold",
        "helium_concentration_sampling_bg_corrected",
        "helium_concentration_sampling_bg_passage_corrected",
    ]
    result = {}
    for column in columns:
        if column not in fieldnames:
            continue
        parsed = []
        for row in rows:
            raw = _value(row, column)
            if raw in {"", "NA", "< LC"}:
                continue
            try:
                number = float(raw)
            except ValueError:
                continue
            if math.isfinite(number):
                parsed.append(number)
        if parsed:
            result[column] = {
                "min": min(parsed),
                "max": max(parsed),
                "numeric_count": len(parsed),
            }
    return result


def _audit_passage_correction(
    rows: list[dict[str, str | None]], fieldnames: list[str]
) -> dict[str, Any]:
    """Check the EA passage-time factor; describe VEGA coverage without assuming a rule."""
    required = {
        "sampling_type",
        "helium_concentration_sampling_bg_corrected_flag",
        "helium_concentration_sampling_bg_corrected",
        "helium_concentration_sampling_bg_passage_corrected",
        "sampling_start_time",
        "sampling_end_time",
        "helium_release_start_time",
        "helium_release_end_time",
    }
    if not required.issubset(fieldnames):
        return {}

    ea_significant = 0
    ea_with_correction = 0
    vega_significant = 0
    vega_with_correction = 0
    max_relative_error = 0.0
    violations: list[dict[str, Any]] = []
    relative_tolerance = 0.01

    for row_number, row in enumerate(rows, start=2):
        kind = _value(row, "sampling_type")
        flag = _value(row, "helium_concentration_sampling_bg_corrected_flag")
        if flag != "significant":
            continue

        passage_raw = _value(row, "helium_concentration_sampling_bg_passage_corrected")
        if kind == "VEGA":
            vega_significant += 1
            if passage_raw not in {"", "NA"}:
                vega_with_correction += 1
            continue
        if kind != "EA":
            continue

        ea_significant += 1
        if passage_raw not in {"", "NA"}:
            ea_with_correction += 1

        try:
            sample_start = datetime.fromisoformat(
                _value(row, "sampling_start_time").replace("Z", "+00:00")
            )
            sample_end = datetime.fromisoformat(
                _value(row, "sampling_end_time").replace("Z", "+00:00")
            )
            release_start = datetime.fromisoformat(
                _value(row, "helium_release_start_time").replace("Z", "+00:00")
            )
            release_end = datetime.fromisoformat(
                _value(row, "helium_release_end_time").replace("Z", "+00:00")
            )
            sample_duration = (sample_end - sample_start).total_seconds()
            release_duration = (release_end - release_start).total_seconds()
            background_corrected = float(
                _value(row, "helium_concentration_sampling_bg_corrected")
            )
            passage_corrected = float(passage_raw)
        except (ValueError, TypeError):
            violations.append(
                {
                    "row": row_number,
                    "rule": "EA significant row lacks parseable times or concentrations",
                }
            )
            continue

        if (
            sample_duration <= 0
            or release_duration <= 0
            or background_corrected == 0
            or not math.isfinite(background_corrected)
            or not math.isfinite(passage_corrected)
        ):
            violations.append(
                {
                    "row": row_number,
                    "rule": (
                        "EA passage correction requires positive durations and "
                        "nonzero concentration"
                    ),
                }
            )
            continue

        expected_ratio = sample_duration / release_duration
        observed_ratio = passage_corrected / background_corrected
        relative_error = abs(observed_ratio - expected_ratio) / expected_ratio
        max_relative_error = max(max_relative_error, relative_error)
        if relative_error > relative_tolerance:
            violations.append(
                {
                    "row": row_number,
                    "rule": (
                        "EA passage-correction ratio differs from sampling-duration/"
                        "release-duration ratio"
                    ),
                    "relative_error": relative_error,
                }
            )

    return {
        "ea_significant_rows": ea_significant,
        "ea_rows_with_passage_correction": ea_with_correction,
        "ea_ratio_check": (
            "not_applicable"
            if not ea_significant
            else "passed" if not violations else "failed"
        ),
        "relative_tolerance": relative_tolerance,
        "max_relative_error": max_relative_error if ea_significant else None,
        "ea_violations": violations,
        "vega_significant_rows": vega_significant,
        "vega_rows_with_passage_correction": vega_with_correction,
        "vega_interpretation": (
            "Coverage is reported descriptively; no correction rule is inferred for VEGA."
        ),
    }


def audit_sampling_csv(path: Path) -> dict[str, Any]:
    """Audit structure and emit descriptive data-quality checks without rewriting source values."""
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise RuntimeError("Sampling file has no CSV header")
        fieldnames = list(reader.fieldnames)
        required = {"sampling_type", "sampling_bag_id"}
        missing_columns = sorted(required - set(fieldnames))
        if missing_columns:
            raise RuntimeError(f"Sampling file lacks required columns: {missing_columns}")
        rows = list(reader)

    type_counts = Counter(_value(row, "sampling_type") for row in rows)
    bag_counts = Counter(
        (_value(row, "sampling_type"), _value(row, "sampling_bag_id")) for row in rows
    )
    bag_violations = []
    for row_number, row in enumerate(rows, start=2):
        kind, bag = _value(row, "sampling_type"), _value(row, "sampling_bag_id")
        if kind == "EA" and bag != "NA":
            bag_violations.append(
                {
                    "row": row_number,
                    "rule": "EA sampling_bag_id must be literal NA",
                }
            )
        elif kind == "VEGA" and (not bag or bag == "NA"):
            bag_violations.append(
                {
                    "row": row_number,
                    "rule": "VEGA sampling_bag_id must be populated",
                }
            )

    experiment_counts = {}
    if "experiment_id" in fieldnames:
        experiment_counts = dict(
            sorted(Counter(_value(row, "experiment_id") for row in rows).items())
        )
    flag_counts, flag_violations = _audit_detection_flags(rows, fieldnames)
    return {
        "file": path.name,
        "row_count": len(rows),
        "column_count": len(fieldnames),
        "columns": fieldnames,
        "sampling_type_counts": dict(sorted(type_counts.items())),
        "sampling_bag_id_counts": {
            f"{kind}:{bag}": count for (kind, bag), count in sorted(bag_counts.items())
        },
        "unique_experiment_count": (
            len(experiment_counts) if "experiment_id" in fieldnames else None
        ),
        "rows_per_experiment": experiment_counts,
        "flag_counts": flag_counts,
        "missingness": _missingness(rows, fieldnames),
        "time_checks": _audit_times(rows, fieldnames),
        "duplicate_identity_check": _audit_duplicate_keys(rows, fieldnames),
        "numeric_ranges": _numeric_ranges(rows, fieldnames),
        "passage_correction_check": _audit_passage_correction(rows, fieldnames),
        "semantic_checks": {
            "EA_literal_NA_and_VEGA_populated": "passed" if not bag_violations else "failed",
            "sampling_bag_violations": bag_violations,
            "detection_flag_consistency": "passed" if not flag_violations else "failed",
            "detection_flag_violations": flag_violations,
            "note": (
                "Literal NA is preserved as a domain value for EA and is reported per column; "
                "no global NA normalization is performed. Descriptive counts do not establish "
                "scientific validity or independence of experiments."
            ),
        },
    }


def run(output_dir: Path, timeout: float) -> dict[str, Any]:  # noqa: PLR0915
    """Download core files, verify original bytes, and produce the audit report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    listing_url = f"{LIST_URL}?{urlencode({'persistentId': DATASET_PID})}"
    listing_payload, listing_headers, listing_final_url = fetch_bytes(listing_url, timeout)
    listing = json_response(listing_payload, "Dataverse file listing")
    items = listing.get("data")
    if not isinstance(items, list):
        raise RuntimeError("Dataverse listing has no data array")
    (output_dir / "diflu-files.json").write_bytes(listing_payload)

    indexed: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        label = item.get("label")
        data_file = item.get("dataFile")
        name = data_file.get("filename") if isinstance(data_file, dict) else None
        name = name or label
        if isinstance(name, str):
            indexed.setdefault(name, []).append(item)

    records = []
    local_by_remote_name: dict[str, Path] = {}
    for remote_name in CORE_FILES:
        matches = indexed.get(remote_name, [])
        if len(matches) != 1:
            raise RuntimeError(
                f"Expected one listing entry for {remote_name}; found {len(matches)}"
            )
        item = matches[0]
        data_file = item.get("dataFile")
        if not isinstance(data_file, dict) or not isinstance(data_file.get("id"), int):
            raise RuntimeError(f"Missing file ID for {remote_name}")
        file_id = data_file["id"]

        metadata_url = f"{BASE_URL}/api/files/{file_id}"
        metadata_payload, _, metadata_final_url = fetch_bytes(metadata_url, timeout)
        envelope = json_response(metadata_payload, f"metadata for {remote_name}")
        metadata = (
            envelope.get("data", {}).get("dataFile")
            if isinstance(envelope.get("data"), dict)
            else None
        )
        if not isinstance(metadata, dict):
            raise RuntimeError(f"Missing detailed metadata for {remote_name}")
        original_name = metadata.get("originalFileName")
        if not isinstance(original_name, str) or not original_name:
            raise RuntimeError(f"Dataverse does not publish originalFileName for {remote_name}")
        # Use only the server-provided basename; never allow a metadata path to escape output_dir.
        safe_name = Path(original_name).name
        if safe_name != original_name or safe_name in {"", ".", ".."}:
            raise RuntimeError(f"Unsafe original filename in metadata: {original_name!r}")

        download_url = f"{BASE_URL}/api/access/datafile/{file_id}?format=original"
        payload, headers, final_url = fetch_bytes(download_url, timeout)
        if not payload or "text/html" in headers.get("content-type", "").lower():
            raise RuntimeError(f"Empty or HTML response for {remote_name}")
        integrity = verify_original(payload, metadata, remote_name)
        destination = output_dir / safe_name
        destination.write_bytes(payload)
        local_by_remote_name[remote_name] = destination
        records.append(
            {
                "dataverse_label": remote_name,
                "dataverse_file_id": file_id,
                "metadata_url": metadata_url,
                "metadata_final_url": metadata_final_url,
                "download_url": download_url,
                "final_url": final_url,
                "original_filename": original_name,
                "original_format": metadata.get("originalFormatLabel"),
                "dataverse_export_filename": metadata.get("filename"),
                "dataverse_export_size_bytes": metadata.get("filesize"),
                "integrity": integrity,
                "local_path": str(destination),
            }
        )

    audit = audit_sampling_csv(local_by_remote_name["DIFLU_helium_release_sampling.tab"])
    report = {
        "dataset_pid": DATASET_PID,
        "dataset_url": (f"{BASE_URL}/dataset.xhtml?persistentId={DATASET_PID.replace(':', '%3A')}"),
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "listing_url": listing_final_url,
        "listing_content_type": listing_headers.get("content-type"),
        "listing_sha256": hashlib.sha256(listing_payload).hexdigest(),
        "download_representation": "Dataverse originalFileName bytes (?format=original)",
        "files": records,
        "sampling_audit": audit,
        "limitations": [
            (
                "The report checks transport integrity and documented structural invariants; "
                "it does not establish scientific validity."
            ),
            (
                "Original-file checks are only enforced when Dataverse publishes original size "
                "and MD5 metadata."
            ),
            (
                "The report includes descriptive missingness, time, duplicate-key, range and "
                "detection-flag checks; these diagnostics do not establish scientific validity."
            ),
        ],
    }
    (output_dir / "audit-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw/diflu-audit"))
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        report = run(args.output_dir, args.timeout)
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Audit report: {args.output_dir / 'audit-report.json'}")
    print(f"Sampling rows: {report['sampling_audit']['row_count']}")
    print(f"Sampling types: {report['sampling_audit']['sampling_type_counts']}")
    invariant = report["sampling_audit"]["semantic_checks"]["EA_literal_NA_and_VEGA_populated"]
    print(f"EA/VEGA invariant: {invariant}")
    flag_check = report["sampling_audit"]["semantic_checks"]["detection_flag_consistency"]
    print(f"Detection-flag consistency: {flag_check}")
    return 0 if invariant == "passed" and flag_check == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
