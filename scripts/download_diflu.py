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
from urllib.parse import urlencode
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


def request_bytes(url: str, *, timeout: float, retries: int = 3) -> tuple[bytes, dict[str, str], str]:
    """Fetch bytes with bounded retries and return content, headers, and final URL."""
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=timeout) as response:
                payload = response.read()
                headers = {key.lower(): value for key, value in response.headers.items()}
                return payload, headers, response.geturl()
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if isinstance(exc, HTTPError) and exc.code < 500 and exc.code != 429:
                break
            if attempt + 1 < retries:
                time.sleep(2**attempt)
    raise RuntimeError(f"Request failed after {retries} attempt(s): {url}: {last_error}") from last_error


def remote_file_name(item: dict[str, Any]) -> str | None:
    """Extract the file name from the Dataverse file-list response."""
    data_file = item.get("dataFile", {})
    if isinstance(data_file, dict):
        name = data_file.get("filename") or item.get("label")
        if isinstance(name, str):
            return name
    name = item.get("label")
    return name if isinstance(name, str) else None


def main() -> int:
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
        help="list all files advertised by the current published dataset version; do not download data",
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

    list_url = f"{FILE_LIST_ENDPOINT}?{urlencode({'persistentId': DATASET_PID})}"
    try:
        listing_bytes, listing_headers, listing_final_url = request_bytes(
            list_url, timeout=args.timeout
        )
        listing = json.loads(listing_bytes)
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot retrieve/parse Dataverse file list: {exc}", file=sys.stderr)
        return 2

    items = listing.get("data")
    if not isinstance(items, list):
        print(
            "ERROR: Dataverse response has no 'data' list; preserve the response and inspect the API schema.",
            file=sys.stderr,
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "diflu-files-response.json").write_bytes(listing_bytes)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    listing_path = args.output_dir / "diflu-files.json"
    listing_path.write_bytes(listing_bytes)

    by_name: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        if isinstance(item, dict):
            name = remote_file_name(item)
            if name:
                by_name.setdefault(name, []).append(item)

    if args.list:
        print(f"Dataset: {DATASET_PID}")
        print(f"File listing: {listing_final_url}")
        print(f"Files listed: {len(items)}")
        for name in sorted(by_name):
            item = by_name[name][0]
            data_file = item.get("dataFile", {})
            size = data_file.get("filesize") if isinstance(data_file, dict) else None
            file_id = data_file.get("id") if isinstance(data_file, dict) else None
            print(f"{size if size is not None else '?':>12} bytes  id={file_id!s:<10} {name}")
        print(f"Saved API response to {listing_path}")
        return 0

    selected_names = sorted(by_name) if args.all else list(DEFAULT_FILES)
    missing = [name for name in selected_names if name not in by_name]
    if missing:
        print(
            "ERROR: requested filename(s) not found in current API response: "
            + ", ".join(missing),
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
        "file_list_url": listing_final_url,
        "file_list_http_content_type": listing_headers.get("content-type"),
        "file_list_sha256": hashlib.sha256(listing_bytes).hexdigest(),
        "files": [],
        "warning": (
            "SHA-256 identifies the downloaded bytes only; it does not establish "
            "scientific validity or completeness. Verify file-level licence and metadata."
        ),
    }

    for name in selected_names:
        matches = by_name[name]
        if len(matches) != 1:
            print(
                f"ERROR: {len(matches)} entries named {name!r}; refusing ambiguous download.",
                file=sys.stderr,
            )
            return 2
        item = matches[0]
        data_file = item.get("dataFile", {})
        if not isinstance(data_file, dict) or not isinstance(data_file.get("id"), int):
            print(f"ERROR: missing numeric Dataverse file ID for {name}", file=sys.stderr)
            return 2

        file_id = data_file["id"]
        download_url = f"{BASE_URL}/api/access/datafile/{file_id}"
        try:
            payload, headers, final_url = request_bytes(download_url, timeout=args.timeout)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2

        # Detect common HTML/JSON error pages before saving them under a .tab filename.
        prefix = payload.lstrip()[:200].lower()
        content_type = headers.get("content-type", "").lower()
        if not payload or "text/html" in content_type or prefix.startswith(b"<!doctype html"):
            print(
                f"ERROR: response for {name} looks empty or like an HTML error page; not saving it.",
                file=sys.stderr,
            )
            return 2
        if prefix.startswith((b'{"status":', b'{"message":', b'{"error":')):
            print(
                f"ERROR: response for {name} looks like a JSON error; not saving it.",
                file=sys.stderr,
            )
            return 2

        expected_size = data_file.get("filesize")
        if isinstance(expected_size, int) and expected_size != len(payload):
            print(
                f"ERROR: size mismatch for {name}: API={expected_size}, downloaded={len(payload)}.",
                file=sys.stderr,
            )
            return 2

        destination = args.output_dir / name
        destination.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        (args.output_dir / f"{name}.sha256").write_text(
            f"{digest}  {name}\n", encoding="utf-8"
        )
        manifest["files"].append(
            {
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
        )
        print(f"OK {name}: {len(payload)} bytes SHA-256 {digest}")

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
