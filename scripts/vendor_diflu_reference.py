#!/usr/bin/env python3
"""Stage the compact, checksum-verified DIFLU source corpus for Git versioning.

The script never downloads data and never parses or rewrites source bytes. Run
scripts/audit_diflu.py first, then stage its verified original files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

DATASET_PID = "doi:10.57745/A9YC3C"
DATASET_URL = "https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi%3A10.57745%2FA9YC3C"
CORE_FILES = (
    "DIFLU_helium_release_sampling.tab",
    "DIFLU_media_dictionary.tab",
    "DIFLU_variables_dictionary.tab",
)
LICENSE = "Etalab Open Licence 2.0"


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of a file's exact bytes."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def md5_file(path: Path) -> str:
    """Return the MD5 digest used by Dataverse to identify original files."""
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_verified_records(audit_dir: Path) -> list[dict[str, Any]]:
    """Load audit metadata and verify every required source file before staging."""
    report_path = audit_dir / "audit-report.json"
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read audit report {report_path}: {exc}") from exc

    if report.get("dataset_pid") != DATASET_PID:
        raise RuntimeError(f"Unexpected dataset PID in {report_path}")

    records = report.get("files")
    if not isinstance(records, list):
        raise RuntimeError("Audit report has no files list")
    by_name = {
        record.get("dataverse_label"): record
        for record in records
        if isinstance(record, dict)
    }

    verified: list[dict[str, Any]] = []
    for filename in CORE_FILES:
        record = by_name.get(filename)
        if not isinstance(record, dict):
            raise RuntimeError(f"Audit report is missing required file: {filename}")
        integrity = record.get("integrity")
        if not isinstance(integrity, dict):
            raise RuntimeError(f"Missing integrity metadata for {filename}")
        if integrity.get("size_verified") is not True or integrity.get("md5_verified") is not True:
            raise RuntimeError(
                f"Dataverse size and MD5 must both be verified before staging {filename}"
            )

        original_filename = record.get("original_filename")
        if not isinstance(original_filename, str) or Path(original_filename).name != original_filename:
            raise RuntimeError(f"Unsafe original filename for {filename}")
        source = audit_dir / original_filename
        if not source.is_file():
            raise RuntimeError(f"Verified source file is missing: {source}")

        actual_size = source.stat().st_size
        actual_md5 = md5_file(source)
        actual_sha256 = sha256_file(source)
        if actual_size != integrity.get("actual_size_bytes"):
            raise RuntimeError(f"Size changed since audit for {filename}")
        if actual_md5.lower() != str(integrity.get("actual_md5", "")).lower():
            raise RuntimeError(f"MD5 changed since audit for {filename}")
        if actual_sha256.lower() != str(integrity.get("sha256", "")).lower():
            raise RuntimeError(f"SHA-256 changed since audit for {filename}")

        verified.append(
            {
                "dataverse_label": filename,
                "original_filename": original_filename,
                "source": source,
                "size_bytes": actual_size,
                "md5": actual_md5,
                "sha256": actual_sha256,
                "dataverse_file_id": record.get("dataverse_file_id"),
                "download_url": record.get("download_url"),
            }
        )
    return verified


def stage(audit_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Copy verified original bytes and write a provenance manifest."""
    records = load_verified_records(audit_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    staged_records = []

    for record in records:
        source = record["source"]
        destination = output_dir / record["original_filename"]
        payload = source.read_bytes()
        if destination.exists():
            if destination.read_bytes() != payload:
                raise RuntimeError(
                    f"Refusing to overwrite different existing file: {destination}"
                )
        else:
            destination.write_bytes(payload)

        staged_records.append(
            {
                "filename": record["original_filename"],
                "dataverse_label": record["dataverse_label"],
                "dataverse_file_id": record["dataverse_file_id"],
                "download_url": record["download_url"],
                "size_bytes": record["size_bytes"],
                "md5": record["md5"],
                "sha256": record["sha256"],
            }
        )

    manifest = {
        "dataset_pid": DATASET_PID,
        "dataset_url": DATASET_URL,
        "license": LICENSE,
        "method": "Byte-for-byte copy of Dataverse originalFileName payloads after audit size/MD5/SHA-256 verification.",
        "files": staged_records,
        "limitations": [
            "Integrity checks do not establish scientific validity.",
            "The manifest timestamp records staging time, not a new dataset release.",
            "Source bytes are not normalized; literal values such as NA are preserved.",
        ],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if manifest_path.exists() and manifest_path.read_bytes() != manifest_bytes:
        raise RuntimeError(
            f"Refusing to overwrite existing manifest with different content: {manifest_path}"
        )
    manifest_path.write_bytes(manifest_bytes)
    return manifest


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-dir", type=Path, default=Path("data/raw/diflu-audit"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tests/fixtures/diflu/source"),
    )
    args = parser.parse_args()
    try:
        manifest = stage(args.audit_dir, args.output_dir)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Staged {len(manifest['files'])} verified DIFLU source files in {args.output_dir}")
    for record in manifest["files"]:
        print(f"  {record['filename']}: {record['size_bytes']} bytes, sha256={record['sha256']}")
    print(f"Manifest: {args.output_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
