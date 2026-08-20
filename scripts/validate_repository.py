#!/usr/bin/env python3
# Copyright © 2026 Mindclade, LLC. All Rights Reserved.
# Mindclade Proprietary and Confidential.
# SPDX-License-Identifier: LicenseRef-Mindclade-Proprietary
#
"""Validate the member-profile repository without network access or credentials."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate.yml",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "contracts/repository.yaml",
    "mindclade-brand-assets/README.txt",
    "mindclade-brand-assets/png/mc-lockup-horizontal-1080w.png",
    "mindclade-brand-assets/png/mc-lockup-horizontal-dark-1080w.png",
    "profile/README.md",
}
FORBIDDEN_PARTS = {".terraform", ".terragrunt-cache", "__MACOSX", "__pycache__", "credentials"}
USES_RE = re.compile(r"^\s*(?:-\s*)?uses:\s*([^\s#]+)", re.MULTILINE)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_RE = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def repository_files() -> list[Path]:
    return sorted(
        candidate
        for candidate in ROOT.rglob("*")
        if candidate.is_file() and ".git" not in candidate.parts
    )


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
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible credential in {rel.as_posix()}")

    contract_path = ROOT / "contracts/repository.yaml"
    if contract_path.is_file():
        contract = contract_path.read_text(encoding="utf-8")
        for expected in ("repository: .github-private", "visibility: private"):
            if expected not in contract:
                errors.append(f"repository contract lacks {expected!r}")

    profile_path = ROOT / "profile/README.md"
    if profile_path.is_file():
        profile = profile_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^# \S", profile):
            errors.append("profile/README.md must contain a level-one heading")
        if len(profile.encode("utf-8")) > 1_000_000:
            errors.append("profile/README.md exceeds the 1 MB profile budget")
        if "https://github.com/Mindclade/" not in profile:
            errors.append("profile/README.md must link to the Mindclade repository estate")

    for markdown_path in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown_path.parts:
            continue
        markdown = markdown_path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(markdown):
            destination = match.group(1).strip().split("#", 1)[0]
            if not destination or "://" in destination or destination.startswith("mailto:"):
                continue
            target = (markdown_path.parent / destination).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"Markdown link escapes repository in {relative(markdown_path)}: {destination}")
                continue
            if not target.exists():
                errors.append(f"broken local Markdown link in {relative(markdown_path)}: {destination}")

    workflow_dir = ROOT / ".github/workflows"
    for workflow_path in sorted(workflow_dir.glob("*.y*ml")):
        workflow = workflow_path.read_text(encoding="utf-8")
        if "permissions:" not in workflow:
            errors.append(f"workflow lacks explicit permissions: {relative(workflow_path)}")
        if "pull_request_target:" in workflow:
            errors.append(f"pull_request_target is forbidden: {relative(workflow_path)}")
        for use in USES_RE.findall(workflow):
            if use.startswith("./"):
                continue
            target, separator, version = use.rpartition("@")
            if not separator:
                errors.append(f"unversioned action in {relative(workflow_path)}: {use}")
            elif target.startswith("Mindclade/.github/.github/workflows/"):
                if not SEMVER_RE.fullmatch(version):
                    errors.append(f"internal workflow lacks full semver in {relative(workflow_path)}: {use}")
            elif not SHA_RE.fullmatch(version):
                errors.append(f"external action is not SHA-pinned in {relative(workflow_path)}: {use}")

    if errors:
        for message in sorted(set(errors)):
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"{len(set(errors))} validation error(s)", file=sys.stderr)
        return 1

    print(".github-private: member profile contract passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
