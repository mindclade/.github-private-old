#!/usr/bin/env python3
# Copyright © 2026 Mindclade, LLC. All Rights Reserved.
# Mindclade Proprietary and Confidential.
# SPDX-License-Identifier: LicenseRef-Mindclade-Proprietary
#
"""Validate the member-profile repository without network access or credentials."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate.yml",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "NOTICE",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "contracts/repository.yaml",
    "mindclade-brand-assets/README.txt",
    "mindclade-brand-assets/fonts/InstrumentSans-Variable.ttf",
    "mindclade-brand-assets/fonts/InstrumentSans-Variable.woff2",
    "mindclade-brand-assets/fonts/InstrumentSans-OFL.txt",
    "mindclade-brand-assets/fonts/JetBrainsMono-Medium.ttf",
    "mindclade-brand-assets/fonts/JetBrainsMono-Medium.woff2",
    "mindclade-brand-assets/fonts/JetBrainsMono-OFL.txt",
    "mindclade-brand-assets/fonts/JetBrainsMono-Regular.ttf",
    "mindclade-brand-assets/fonts/JetBrainsMono-Regular.woff2",
    "mindclade-brand-assets/fonts/SOURCES.json",
    "mindclade-brand-assets/png/mono-wordmark-1080w.png",
    "mindclade-brand-assets/png/mono-wordmark-dark-1080w.png",
    "mindclade-brand-assets/png/mc-lockup-horizontal-1080w.png",
    "mindclade-brand-assets/png/mc-lockup-horizontal-dark-1080w.png",
    "mindclade-brand-assets/web/fonts.css",
    "mindclade-brand-assets/web/head-snippet.html",
    "mindclade-brand-assets/web/site.webmanifest",
    "mindclade-brand-assets/web/tokens.css",
    "profile/README.md",
}
FORBIDDEN_PARTS = {
    ".terraform",
    ".terragrunt-cache",
    "__MACOSX",
    "__pycache__",
    "credentials",
}
USES_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)", re.MULTILINE)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_RE = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CSS_URL_RE = re.compile(r"url\([\"']?([^\"')]+)")
LOCAL_ASSET_RE = re.compile(
    r'(?:href|content)="(?:https://mindclade\.com)?(/mindclade-brand-assets/[^\"]+)"'
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_FONT_FILES = {
    "InstrumentSans-Variable.ttf",
    "InstrumentSans-Variable.woff2",
    "JetBrainsMono-Medium.ttf",
    "JetBrainsMono-Medium.woff2",
    "JetBrainsMono-Regular.ttf",
    "JetBrainsMono-Regular.woff2",
}
EXPECTED_LICENSE_FILES = {
    "InstrumentSans-OFL.txt",
    "JetBrainsMono-OFL.txt",
}
REQUIRED_HEAD_ASSETS = {
    "/mindclade-brand-assets/fonts/InstrumentSans-Variable.woff2",
    "/mindclade-brand-assets/png/apple-touch-icon-180.png",
    "/mindclade-brand-assets/png/favicon-16-M.png",
    "/mindclade-brand-assets/png/favicon-32.png",
    "/mindclade-brand-assets/png/favicon-64.png",
    "/mindclade-brand-assets/png/mc-og-1200x630.png",
    "/mindclade-brand-assets/web/fonts.css",
    "/mindclade-brand-assets/web/site.webmanifest",
    "/mindclade-brand-assets/web/tokens.css",
}
EXPECTED_WEB_FONT_URLS = {
    "../fonts/InstrumentSans-Variable.woff2",
    "../fonts/JetBrainsMono-Medium.woff2",
    "../fonts/JetBrainsMono-Regular.woff2",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
)
LEGACY_GITHUB_IDENTITIES = (
    "Mind" + "clade/",
    "github.com/" + "Mind" + "clade",
    "/orgs/" + "Mind" + "clade",
)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def repository_files() -> list[Path]:
    return sorted(
        candidate
        for candidate in ROOT.rglob("*")
        if candidate.is_file() and ".git" not in candidate.parts
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    errors: list[str] = []
    files = repository_files()
    names = {relative(candidate) for candidate in files}

    for missing in sorted(REQUIRED_FILES - names):
        errors.append(f"missing required file: {missing}")

    for candidate in files:
        rel = Path(relative(candidate))
        if any(part in FORBIDDEN_PARTS for part in rel.parts):
            errors.append(f"forbidden local or sensitive artifact: {rel.as_posix()}")
        if candidate.is_symlink():
            errors.append(f"symlink is not allowed: {rel.as_posix()}")
        if candidate.stat().st_size > 2_000_000:
            continue
        text = candidate.read_text(encoding="utf-8", errors="ignore")
        if any(legacy in text for legacy in LEGACY_GITHUB_IDENTITIES):
            errors.append(
                f"noncanonical GitHub organization identity: {rel.as_posix()}"
            )
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible credential in {rel.as_posix()}")

    contract_path = ROOT / "contracts/repository.yaml"
    if contract_path.is_file():
        contract = contract_path.read_text(encoding="utf-8")
        for expected in ("repository: .github-private", "visibility: private"):
            if expected not in contract:
                errors.append(f"repository contract lacks {expected!r}")
        for canonical_url in (
            "https://github.com/enterprises/mindclade",
            "https://github.com/mindclade",
            "https://github.com/orgs/mindclade/repositories",
            "https://github.com/mindclade/.github-private",
        ):
            if canonical_url not in contract:
                errors.append(
                    f"repository contract omits canonical GitHub URL: {canonical_url}"
                )

    profile_path = ROOT / "profile/README.md"
    if profile_path.is_file():
        profile = profile_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^# \S", profile):
            errors.append("profile/README.md must contain a level-one heading")
        if len(profile.encode("utf-8")) > 1_000_000:
            errors.append("profile/README.md exceeds the 1 MB profile budget")
        if "https://github.com/mindclade/" not in profile:
            errors.append(
                "profile/README.md must link to the Mindclade repository estate"
            )

    brand_root = ROOT / "mindclade-brand-assets"
    font_root = brand_root / "fonts"
    sources_path = font_root / "SOURCES.json"
    if sources_path.is_file():
        try:
            sources = json.loads(sources_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid font source manifest: {exc}")
            sources = {}
        if sources.get("schema_version") != 1:
            errors.append("font source manifest must use schema_version 1")
        for section in ("fonts", "licenses"):
            entries = sources.get(section, {})
            if not isinstance(entries, dict) or not entries:
                errors.append(f"font source manifest has no {section}")
                continue
            expected_names = (
                EXPECTED_FONT_FILES if section == "fonts" else EXPECTED_LICENSE_FILES
            )
            if set(entries) != expected_names:
                errors.append(
                    f"font source manifest has an unexpected {section} inventory"
                )
            for name, metadata in entries.items():
                target = font_root / name
                if not target.is_file():
                    errors.append(
                        f"font source manifest references missing file: {name}"
                    )
                    continue
                expected_hash = metadata.get("sha256", "")
                if not SHA256_RE.fullmatch(expected_hash):
                    errors.append(
                        f"font source manifest has invalid SHA-256 for {name}"
                    )
                elif sha256(target) != expected_hash:
                    errors.append(
                        f"font or license hash differs from SOURCES.json: {name}"
                    )
                if not COMMIT_RE.fullmatch(metadata.get("commit", "")):
                    errors.append(
                        f"font source manifest has an unpinned commit for {name}"
                    )
                if section == "fonts":
                    expected_magic = (
                        b"wOF2" if target.suffix == ".woff2" else b"\x00\x01\x00\x00"
                    )
                    if target.read_bytes()[:4] != expected_magic:
                        errors.append(f"font has invalid binary signature: {name}")
                    license_name = metadata.get("license", "")
                    if not (font_root / license_name).is_file():
                        errors.append(f"font has no local license mapping: {name}")

    head_path = brand_root / "web/head-snippet.html"
    if head_path.is_file():
        head = head_path.read_text(encoding="utf-8")
        if "fonts.googleapis.com" in head or "fonts.gstatic.com" in head:
            errors.append("head snippet must not load fonts from a third-party CDN")
        if re.search(r'<link\b[^>]*\bhref="https?://', head):
            errors.append(
                "head snippet styles, fonts, manifest, and icons must be local"
            )
        if head.count('rel="preload"') != 1:
            errors.append("head snippet must preload only Instrument Sans")
        if 'type="font/woff2"' not in head:
            errors.append("head snippet font preload must use WOFF2")
        if re.search(r'<link\b[^>]*\brel="preload"[^>]*JetBrainsMono', head):
            errors.append("head snippet must load JetBrains Mono on demand")
        local_assets = set(LOCAL_ASSET_RE.findall(head))
        for missing in sorted(REQUIRED_HEAD_ASSETS - local_assets):
            errors.append(f"head snippet lacks required local asset: {missing}")
        for reference in sorted(local_assets):
            if not (ROOT / reference.lstrip("/")).is_file():
                errors.append(
                    f"head snippet references missing local asset: {reference}"
                )

    fonts_css_path = brand_root / "web/fonts.css"
    if fonts_css_path.is_file():
        fonts_css = fonts_css_path.read_text(encoding="utf-8")
        if fonts_css.count("@font-face") != 3:
            errors.append("fonts.css must declare exactly three local font faces")
        font_destinations = set(CSS_URL_RE.findall(fonts_css))
        if font_destinations != EXPECTED_WEB_FONT_URLS:
            errors.append("fonts.css must use only the three WOFF2 web fonts")
        for destination in font_destinations:
            target = (fonts_css_path.parent / destination).resolve()
            try:
                target.relative_to(brand_root)
            except ValueError:
                errors.append(
                    f"font stylesheet URL escapes brand assets: {destination}"
                )
                continue
            if not target.is_file():
                errors.append(
                    f"font stylesheet references missing asset: {destination}"
                )

    manifest_path = brand_root / "web/site.webmanifest"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid web manifest: {exc}")
            manifest = {}
        for icon in manifest.get("icons", []):
            destination = icon.get("src", "")
            target = (manifest_path.parent / destination).resolve()
            try:
                target.relative_to(brand_root)
            except ValueError:
                errors.append(f"web manifest icon escapes brand assets: {destination}")
                continue
            if not target.is_file():
                errors.append(f"web manifest references missing icon: {destination}")

    for markdown_path in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown_path.parts:
            continue
        markdown = markdown_path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(markdown):
            destination = match.group(1).strip().split("#", 1)[0]
            if (
                not destination
                or "://" in destination
                or destination.startswith("mailto:")
            ):
                continue
            target = (markdown_path.parent / destination).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"Markdown link escapes repository in {relative(markdown_path)}: {destination}"
                )
                continue
            if not target.exists():
                errors.append(
                    f"broken local Markdown link in {relative(markdown_path)}: {destination}"
                )

    workflow_dir = ROOT / ".github/workflows"
    for workflow_path in sorted(workflow_dir.glob("*.y*ml")):
        workflow = workflow_path.read_text(encoding="utf-8")
        if "permissions:" not in workflow:
            errors.append(
                f"workflow lacks explicit permissions: {relative(workflow_path)}"
            )
        if "pull_request_target:" in workflow:
            errors.append(
                f"pull_request_target is forbidden: {relative(workflow_path)}"
            )
        for use in USES_RE.findall(workflow):
            if use.startswith("./"):
                continue
            target, separator, version = use.rpartition("@")
            if not separator:
                errors.append(f"unversioned action in {relative(workflow_path)}: {use}")
            elif target.startswith("mindclade/.github/.github/workflows/"):
                if not (SEMVER_RE.fullmatch(version) or SHA_RE.fullmatch(version)):
                    errors.append(
                        f"internal workflow lacks an immutable semver or commit in "
                        f"{relative(workflow_path)}: {use}"
                    )
            elif not SHA_RE.fullmatch(version):
                errors.append(
                    f"external action is not SHA-pinned in {relative(workflow_path)}: {use}"
                )

    if errors:
        for message in sorted(set(errors)):
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"{len(set(errors))} validation error(s)", file=sys.stderr)
        return 1

    print(".github-private: member profile contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
