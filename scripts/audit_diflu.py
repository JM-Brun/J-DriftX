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
    request = Request(url, headers={"User-Agent": USER_AGENT})
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


def audit_sampling_csv(path: Path) -> dict[str, Any]:
    """Audit CSV structure and the documented EA/VEGA sampling-bag invariant."""
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise RuntimeError("Sampling file has no CSV header")
        required = {"sampling_type", "sampling_bag_id"}
        missing_columns = sorted(required - set(reader.fieldnames))
        if missing_columns:
            raise RuntimeError(f"Sampling file lacks required columns: {missing_columns}")
        rows = list(reader)

    type_counts = Counter((row.get("sampling_type") or "").strip() for row in rows)
    bag_counts = Counter(
        ((row.get("sampling_type") or "").strip(), (row.get("sampling_bag_id") or "").strip())
        for row in rows
    )
    violations = []
    for row_number, row in enumerate(rows, start=2):
        sampling_type = (row.get("sampling_type") or "").strip()
        bag_id = (row.get("sampling_bag_id") or "").strip()
        if sampling_type == "EA" and bag_id != "NA":
            violations.append({"row": row_number, "rule": "EA sampling_bag_id must be literal NA"})
        elif sampling_type == "VEGA" and (not bag_id or bag_id == "NA"):
            violations.append({"row": row_number, "rule": "VEGA sampling_bag_id must be populated"})
    return {
        "file": path.name,
        "row_count": len(rows),
        "column_count": len(reader.fieldnames),
        "columns": reader.fieldnames,
        "sampling_type_counts": dict(sorted(type_counts.items())),
        "sampling_bag_id_counts": {
            f"{kind}:{bag}": count for (kind, bag), count in sorted(bag_counts.items())
        },
        "semantic_checks": {
            "EA_literal_NA_and_VEGA_populated": "passed" if not violations else "failed",
            "violations": violations,
            "note": (
                "Literal NA is preserved as a domain value for EA; "
                "no global NA normalization is performed."
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
                "The current semantic check covers the documented EA/VEGA sampling_bag_id "
                "rule, not all scientific quality criteria."
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
    return 0 if invariant == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
