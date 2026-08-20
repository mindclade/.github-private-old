<!-- mindclade-doc: repository-home@1 -->

# Mindclade · Member Organization Profile

> **Member experience · Internal navigation and operating guidance**  
> The private profile rendered to Mindclade organization members by GitHub Enterprise Cloud.

| Repository contract | Value |
| --- | --- |
| Enterprise | [`mindclade`](https://github.com/enterprises/mindclade) |
| Organization | [`mindclade`](https://github.com/mindclade) |
| Repository index | [Mindclade repositories](https://github.com/orgs/mindclade/repositories) |
| Repository | [`mindclade/.github-private`](https://github.com/mindclade/.github-private) |
| Class | `enterprise-control` |
| Visibility | `private` |
| Production authority | `false` |
| Change model | Pull request to `main` with code-owner review |
| Rendered source | [`profile/README.md`](profile/README.md) |

GitHub renders `profile/README.md` in the member view of the Mindclade organization. This
repository is intentionally private: the name, visibility, and path are part of GitHub's
activation contract and must not be changed independently.

## Authority boundary

This repository owns only:

- the member-only organization profile;
- internal navigation to authoritative repositories, runbooks, and support routes; and
- validation that keeps the profile renderable and the repository free of obvious unsafe artifacts.

It does not own GitHub Enterprise desired state, reusable workflows, community-health defaults,
cloud or Kubernetes resources, application source, credentials, or incident records.

| Concern | Authoritative repository |
| --- | --- |
| Shared workflows and community health | [`mindclade/.github`](https://github.com/mindclade/.github) |
| GitHub organization governance | [`mindclade/github-config`](https://github.com/mindclade/github-config) |
| Ring-0 trust and recovery | [`mindclade/bootstrap`](https://github.com/mindclade/bootstrap) |
| Google Cloud desired state | [`mindclade/infrastructure-live`](https://github.com/mindclade/infrastructure-live) |
| Kubernetes and Argo CD desired state | [`mindclade/gitops`](https://github.com/mindclade/gitops) |
| Product and model source | [`mindclade/mindclade-internal-monorepo`](https://github.com/mindclade/mindclade-internal-monorepo) |

## Repository layout

```text
.github-private/
├── .github/
│   ├── CODEOWNERS
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/validate.yml
├── contracts/repository.yaml
├── mindclade-brand-assets/
├── profile/README.md
├── scripts/validate_repository.py
├── CONTRIBUTING.md
├── SECURITY.md
├── SUPPORT.md
└── README.md
```

## Validation

CI and local development run the same credential-free command:

```sh
make validate
```

When actionlint and yamllint are installed, also run:

```sh
make lint
```

The workflow grants only `contents: read`, persists no checkout credential, uses no secrets,
and pins its only external action to a full commit SHA.

## Provisioning

`github-config` is the authoritative creator and settings manager for this repository. Its
catalog entry must keep the repository private, disable issues and projects, attach the normal
enterprise rulesets and custom properties, and grant Platform maintain, Security push, and
Engineering pull access.

Publishing, committing, pushing, and opening a pull request are separate operator actions and
are intentionally not performed by this repository's validation tooling.

The flattened PNG lockups in `mindclade-brand-assets/` are used for the rendered profile so
GitHub does not depend on local fonts to reproduce the brand correctly. The asset bundle is
proprietary and remains subject to `LICENSE`.

The web handoff under `mindclade-brand-assets/web/` is fully self-hosted. Its head snippet
preloads the local Instrument Sans WOFF2 face and loads JetBrains Mono on demand, along with
tokens, icons, manifest, and social image from the
`/mindclade-brand-assets/` deployment path; it makes no Google Fonts request. Upstream font
commits, file hashes, and OFL license mappings are recorded in
`mindclade-brand-assets/fonts/SOURCES.json`.
