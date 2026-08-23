#!/usr/bin/env python3
# Copyright © 2026 Mindclade, LLC. All Rights Reserved.
# Mindclade Proprietary and Confidential.
# SPDX-License-Identifier: LicenseRef-Mindclade-Proprietary

"""Verify and build the deterministic checked-in brand asset distribution."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import sys
import tarfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "mindclade-brand-assets"
MANIFEST = ASSET_ROOT / "MANIFEST.json"
VERSION_RE = re.compile(r"^[0-9]{4}\.[0-9]{2}\.[0-9]{2}\.[1-9][0-9]*$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
MEDIA_TYPES = {
    ".css": "text/css",
    ".html": "text/html",
    ".json": "application/json",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".ttf": "font/ttf",
    ".txt": "text/plain",
    ".woff2": "font/woff2",
    ".webmanifest": "application/manifest+json",
}


class BrandBundleError(ValueError):
    """The checked-in brand distribution violated its integrity contract."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def asset_files() -> list[Path]:
    return sorted(
        (
            path
            for path in ASSET_ROOT.rglob("*")
            if path.is_file() and path != MANIFEST
        ),
        key=lambda path: path.relative_to(ASSET_ROOT).as_posix(),
    )


def build_manifest(version: str) -> dict[str, Any]:
    if not VERSION_RE.fullmatch(version):
        raise BrandBundleError("version must be YYYY.MM.DD.N")
    effective_date = version.rsplit(".", 1)[0].replace(".", "-")
    files = []
    for path in asset_files():
        suffix = path.suffix.lower()
        if suffix not in MEDIA_TYPES:
            raise BrandBundleError(f"unrecognized asset media type: {path.name}")
        files.append(
            {
                "path": path.relative_to(ASSET_ROOT).as_posix(),
                "sha256": sha256(path),
                "size": path.stat().st_size,
                "media_type": MEDIA_TYPES[suffix],
            }
        )
    return {
        "schema_version": 1,
        "distribution_id": "mindclade-checked-in-brand-assets",
        "version": version,
        "effective_date": effective_date,
        "authority": "checked-in-distribution-not-brand-governance-authority",
        "license_provenance": {
            "source_manifest": "fonts/SOURCES.json",
            "licenses": [
                "fonts/InstrumentSans-OFL.txt",
                "fonts/JetBrainsMono-OFL.txt",
            ],
        },
        "files": files,
    }


def load_manifest() -> dict[str, Any]:
    try:
        value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BrandBundleError(f"cannot load {MANIFEST}: {exc}") from exc
    if not isinstance(value, dict):
        raise BrandBundleError("brand manifest must be an object")
    return value


def verify_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema_version",
        "distribution_id",
        "version",
        "effective_date",
        "authority",
        "license_provenance",
        "files",
    }
    if set(manifest) != expected_keys:
        errors.append("brand manifest top-level keys are not exact")
        return errors
    version = manifest.get("version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        errors.append("brand manifest version must be YYYY.MM.DD.N")
        return errors
    expected = build_manifest(version)
    if manifest != expected:
        errors.append("brand manifest differs from the deterministic asset inventory")
    for record in manifest.get("files", []):
        if not SHA256_RE.fullmatch(str(record.get("sha256", ""))):
            errors.append(f"invalid asset digest: {record.get('path', '<unknown>')}")
    return errors


def write_manifest(version: str) -> None:
    MANIFEST.write_text(
        json.dumps(build_manifest(version), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_archive(manifest: dict[str, Any], output: Path) -> str:
    errors = verify_manifest(manifest)
    if errors:
        raise BrandBundleError("; ".join(errors))
    entries = [(MANIFEST, Path("MANIFEST.json"))]
    entries.extend(
        (ASSET_ROOT / record["path"], Path(record["path"]))
        for record in manifest["files"]
    )
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for source, name in sorted(entries, key=lambda item: item[1].as_posix()):
            payload = source.read_bytes()
            info = tarfile.TarInfo(name.as_posix())
            info.size = len(payload)
            info.mode = 0o644
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            archive.addfile(info, io.BytesIO(payload))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            compressed.write(buffer.getvalue())
    return sha256(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    refresh = subparsers.add_parser("refresh")
    refresh.add_argument("--version", required=True)
    refresh.add_argument("--write", action="store_true")
    subparsers.add_parser("verify")
    build = subparsers.add_parser("build")
    build.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "refresh":
            expected = build_manifest(args.version)
            if args.write:
                write_manifest(args.version)
                print(f"brand distribution manifest refreshed: {args.version}")
            elif not MANIFEST.is_file() or load_manifest() != expected:
                raise BrandBundleError("manifest refresh required; rerun with --write")
        elif args.command == "verify":
            errors = verify_manifest(load_manifest())
            if errors:
                raise BrandBundleError("; ".join(errors))
            print(f"brand distribution verified: {load_manifest()['version']}")
        else:
            digest = build_archive(load_manifest(), args.output.resolve())
            print(f"{digest}  {args.output}")
    except BrandBundleError as exc:
        print(f"brand distribution validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
