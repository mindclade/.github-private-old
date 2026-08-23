<!-- mindclade-doc: governance@1 -->

# Mindclade governance · `.github-private`

| Document control | Value |
| --- | --- |
| Owner | Mindclade Platform |
| Version | 1.0 |
| Last reviewed | August 21, 2026 |
| Authority | Member-only organization profile and checked-in brand distribution |

## Authority boundary

This repository is authoritative only for the member profile in
`profile/README.md` and the canonical files under
`mindclade-brand-assets/`. It does not govern repositories, GitHub settings,
cloud resources, Kubernetes desired state, application source, or incident
records. Those boundaries are declared in [contracts/repository.yaml](contracts/repository.yaml).

## Decisions and approvals

Routine editorial changes require a passing validation run, one approval, and
code-owner review. Changes to logos, wordmarks, color tokens, font sources,
license texts, asset provenance, or visibility require the owning brand or
legal reviewer in addition to the required code owner. Repository visibility
must remain private.

## Evidence and publication

A pull request records the member impact, information classification, exact
validation commands, asset source and digest, and rollback. Only
`profile/README.md` is published as the member profile. A local preview is
evidence of rendering, not authorization to distribute a brand asset.

## Exceptions and review

No emergency process permits exposing this repository, bypassing third-party
font terms, or placing secrets or incident evidence here. Any temporary process
exception needs a named owner, approver, exact scope, reason, expiry, and
follow-up record.

Code ownership, member links, brand provenance, font licenses, and rendering
are reviewed at least quarterly and whenever the source manifest changes.
Organization-wide governance is defined in
[`mindclade/.github/GOVERNANCE.md`](https://github.com/mindclade/.github/blob/main/GOVERNANCE.md).
