# Mindclade · Agent operating guide

## Purpose and authority

This private GitHub special repository owns only the member organization profile, internal
navigation, and its checked-in brand assets. It has no production authority. Read README.md,
CONTRIBUTING.md, and contracts/repository.yaml before editing.

## Working rules

- Do not add reusable workflows, organization governance, cloud resources, Kubernetes state,
  application source, credentials, or incident records.
- Keep profile/README.md renderable and keep all profile links and assets non-secret.
- Preserve upstream font license files and the immutable source/hash inventory in
  mindclade-brand-assets/fonts/SOURCES.json.
- Do not rename the repository or change its visibility; those are github-config decisions.

## Validation

    make validate
    make lint

The lint target requires actionlint and yamllint. Report it as unavailable rather than
installing unpinned host tools.

## Done

The member profile renders from local assets, repository validation passes, provenance hashes
remain correct, and no authority or sensitive content leaked into the profile.
