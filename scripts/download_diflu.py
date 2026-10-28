#!/usr/bin/env python3
"""Download a reproducible, checksummed subset of the public DIFLU Dataverse dataset.

Uses only the Python standard library. Raw data are written locally and should not
be committed to Git; the JSON manifest records provenance and SHA-256 digests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

BASE_URL = "https://entrepot.recherche.data.gouv.fr"
DATASET_PID = "doi:10.57745/A9YC3C"
FILE_LIST_ENDPOINT = f"{BASE_URL}/api/datasets/:persistentId/versions/:latest/files"
USER_AGENT = "J-DriftX-DIFLU-audit/1.0 (reproducible research data retrieval)"

# Small files needed to begin the audit. Use --list to inspect all available files.
DEFAULT_FILES = (
    "DIFLU_helium_release_sampling.tab",
    "DIFLU_media_dictionary.tab",
    "DIFLU_instrument_locations.tab",
    "DIFLU_instrument_metadata.tab",
    "DIFLU_helium_ambient_real_time_ASM_1.tab",
    "DIFLU_helium_ambient_real_time_ASM_2.tab",
)


def request_bytes(
    url: str, *, timeout: float, retries: int = 3
) -> tuple[bytes, dict[str, str], str]:
    """Fetch bytes with bounded retries and return content, headers, and final URL."""
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "entrepot.recherche.data.gouv.fr":
        raise ValueError(f"Refusing URL outside the official HTTPS host: {url}")

    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})  # noqa: S310
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                payload = response.read()
                headers = {key.lower(): value for key, value in response.headers.items()}
                return payload, headers, response.geturl()
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if isinstance(exc, HTTPError) and exc.code < 500 and exc.code != 429:
                break
            if attempt + 1 < retries:
                time.sleep(2**attempt)
    message = f"Request failed after {retries} attempt(s): {url}: {last_error}"
    raise RuntimeError(message) from last_error


def remote_file_name(item: dict[str, Any]) -> str | None:
    """Extract the file name from the Dataverse file-list response."""
    data_file = item.get("dataFile", {})
    if isinstance(data_file, dict):
        name = data_file.get("filename") or item.get("label")
        if isinstance(name, str):
            return name
    name = item.get("label")
    return name if isinstance(name, str) else None


def index_files(items: list[Any]) -> dict[str, list[dict[str, Any]]]:
    """Index API file records by their published filename."""
    by_name: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        if isinstance(item, dict):
            name = remote_file_name(item)
            if name:
                by_name.setdefault(name, []).append(item)
    return by_name


def fetch_listing(output_dir: Path, timeout: float) -> tuple[list[Any], dict[str, str], str]:
    """Fetch and preserve the current published version's file listing."""
    list_url = f"{FILE_LIST_ENDPOINT}?{urlencode({'persistentId': DATASET_PID})}"
    payload, headers, final_url = request_bytes(list_url, timeout=timeout)
    try:
        listing = json.loads(payload)
    except json.JSONDecodeError as exc:
        (output_dir / "diflu-files-response.json").write_bytes(payload)
        raise RuntimeError("Dataverse file listing is not valid JSON; response preserved.") from exc

    items = listing.get("data") if isinstance(listing, dict) else None
    if not isinstance(items, list):
        (output_dir / "diflu-files-response.json").write_bytes(payload)
        raise RuntimeError(
            "Dataverse response has no 'data' list; response preserved for schema inspection."
        )
    (output_dir / "diflu-files.json").write_bytes(payload)
    return items, headers, final_url


def list_remote_files(by_name: dict[str, list[dict[str, Any]]], output_path: Path) -> None:
    """Print the remote file names, sizes, and identifiers."""
    print(f"Dataset: {DATASET_PID}")
    print(f"Files listed: {sum(len(records) for records in by_name.values())}")
    for name in sorted(by_name):
        item = by_name[name][0]
        data_file = item.get("dataFile", {})
        if not isinstance(data_file, dict):
            data_file = {}
        size = data_file.get("filesize", "?")
        file_id = data_file.get("id", "?")
        print(f"{size!s:>12} bytes  id={file_id!s:<10} {name}")
    print(f"Saved API response to {output_path}")


def download_one(
    name: str, item: dict[str, Any], output_dir: Path, timeout: float
) -> dict[str, Any]:
    """Download one unambiguous file, validate its response, and save its digest."""
    data_file = item.get("dataFile", {})
    if not isinstance(data_file, dict) or not isinstance(data_file.get("id"), int):
        raise RuntimeError(f"Missing numeric Dataverse file ID for {name}")

    file_id = data_file["id"]
    download_url = f"{BASE_URL}/api/access/datafile/{file_id}"
    payload, headers, final_url = request_bytes(download_url, timeout=timeout)
    content_type = headers.get("content-type", "").lower()
    prefix = payload.lstrip()[:200].lower()
    if not payload or "text/html" in content_type or prefix.startswith(b"<!doctype html"):
        raise RuntimeError(f"Response for {name} is empty or looks like an HTML error page.")
    if prefix.startswith((b'{"status":', b'{"message":', b'{"error":')):
        raise RuntimeError(f"Response for {name} looks like a JSON error.")

    expected_size = data_file.get("filesize")
    if isinstance(expected_size, int) and expected_size != len(payload):
        # Preserve the received bytes and response metadata for diagnosis, but do not
        # save them under the canonical filename or treat them as an audited dataset.
        diagnostic_path = output_dir / f"{name}.size-mismatch"
        diagnostic_path.write_bytes(payload)
        diagnostic = {
            "filename": name,
            "dataverse_file_id": file_id,
            "download_url": download_url,
            "final_url": final_url,
            "response_headers": headers,
            "api_filesize_bytes": expected_size,
            "downloaded_size_bytes": len(payload),
            "size_difference_bytes": len(payload) - expected_size,
            "api_file_metadata": data_file,
            "received_payload_sha256": hashlib.sha256(payload).hexdigest(),
            "diagnostic_payload_path": str(diagnostic_path),
            "note": (
                "Preserved for diagnosis only. This file is not accepted as the canonical "
                "dataset because the API size metadata and received bytes disagree."
            ),
        }
        diagnostic_path.with_suffix(diagnostic_path.suffix + ".json").write_text(
            json.dumps(diagnostic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        raise RuntimeError(
            f"Size mismatch for {name}: API={expected_size}, downloaded={len(payload)} "
            f"(difference {len(payload) - expected_size}). "
            f"Received bytes and headers preserved at {diagnostic_path} and "
            f"{diagnostic_path}.json; inspect before retrying."
        )

    destination = output_dir / name
    destination.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    (output_dir / f"{name}.sha256").write_text(f"{digest}  {name}\n", encoding="utf-8")
    print(f"OK {name}: {len(payload)} bytes SHA-256 {digest}")
    return {
        "filename": name,
        "dataverse_file_id": file_id,
        "download_url": download_url,
        "final_url": final_url,
        "http_status": 200,
        "content_type": content_type,
        "expected_size_bytes": expected_size,
        "downloaded_size_bytes": len(payload),
        "sha256": digest,
        "local_path": str(destination),
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/diflu"),
        help="local output directory (default: data/raw/diflu)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list all files advertised by the current published version; do not download data",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="download every file in the dataset (may require about 381 MB or more)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="per-request timeout in seconds (default: 60)",
    )
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    return args


def main() -> int:
    """Run the listing or download workflow."""
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    try:
        items, listing_headers, listing_url = fetch_listing(args.output_dir, args.timeout)
    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    by_name = index_files(items)
    listing_path = args.output_dir / "diflu-files.json"
    if args.list:
        list_remote_files(by_name, listing_path)
        return 0

    selected_names = sorted(by_name) if args.all else list(DEFAULT_FILES)
    missing = [name for name in selected_names if name not in by_name]
    if missing:
        print(
            "ERROR: requested filename(s) not found: " + ", ".join(missing),
            file=sys.stderr,
        )
        print(f"Inspect {listing_path} or run again with --list.", file=sys.stderr)
        return 2

    manifest: dict[str, Any] = {
        "dataset_pid": DATASET_PID,
        "dataset_url": (
            "https://entrepot.recherche.data.gouv.fr/dataset.xhtml?"
            "persistentId=doi%3A10.57745%2FA9YC3C"
        ),
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "file_list_url": listing_url,
        "file_list_http_content_type": listing_headers.get("content-type"),
        "file_list_sha256": hashlib.sha256(
            (args.output_dir / "diflu-files.json").read_bytes()
        ).hexdigest(),
        "files": [],
        "warning": (
            "SHA-256 identifies downloaded bytes only; it does not establish scientific "
            "validity or completeness. Verify file-level licence and metadata."
        ),
    }

    for name in selected_names:
        matches = by_name[name]
        if len(matches) != 1:
            print(
                f"ERROR: {len(matches)} entries named {name!r}; refusing ambiguity.",
                file=sys.stderr,
            )
            return 2
        try:
            record = download_one(name, matches[0], args.output_dir, args.timeout)
            manifest["files"].append(record)
        except (RuntimeError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2

    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Manifest: {manifest_path}")
    print(f"API file list: {listing_path}")
    print("Raw data remain local; do not commit them to the repository.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
