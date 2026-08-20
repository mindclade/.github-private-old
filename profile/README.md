<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../mindclade-brand-assets/png/mc-lockup-horizontal-dark-1080w.png">
  <source media="(prefers-color-scheme: light)" srcset="../mindclade-brand-assets/png/mc-lockup-horizontal-1080w.png">
  <img alt="Mindclade — frontier models for programmable biology" src="../mindclade-brand-assets/png/mc-lockup-horizontal-1080w.png" width="540">
</picture>

# Mindclade Engineering

Welcome to Mindclade's member-only GitHub home. Start here for the authoritative source of a
control, the path from code to production, and the first place to look during an incident.

[Enterprise](https://github.com/enterprises/mindclade) ·
[Organization](https://github.com/mindclade) ·
[All repositories](https://github.com/orgs/mindclade/repositories)

> **Internal does not mean unrestricted.** Do not put credentials, customer data, production
> configuration, private model material, restricted biological content, or incident-sensitive
> evidence in issues, pull requests, workflow logs, or this profile.

## Find the source of truth

| You need to change | Go to |
| --- | --- |
| Shared CI, starter workflows, or contributor defaults | [`.github`](https://github.com/mindclade/.github) |
| Repositories, teams, access, rulesets, environments, Actions, or OIDC policy | [`github-config`](https://github.com/mindclade/github-config) |
| Ring-0 state, the root GitHub–GCP trust anchor, seed projects, or break-glass recovery | [`bootstrap`](https://github.com/mindclade/bootstrap) |
| Google Cloud organizations, networks, projects, clusters, storage, or workload IAM | [`infrastructure-live`](https://github.com/mindclade/infrastructure-live) |
| Argo CD, Kubernetes desired state, admission policy, or environment promotion | [`gitops`](https://github.com/mindclade/gitops) |
| Product, model, training, data, serving, platform, SDK, or build source | [`mindclade-internal-monorepo`](https://github.com/mindclade/mindclade-internal-monorepo) |

One control has one owner. Do not work around an authoritative repository with a settings-page
change, an unreviewed cloud edit, or a direct cluster mutation.

## How changes reach production

1. Source changes are reviewed and tested in their owning repository.
2. Shared GitHub workflows are consumed only from immutable full-semver `.github` releases.
3. Build outputs are immutable, digest-addressed, and accompanied by provenance and an SBOM.
4. `infrastructure-live` prepares cloud resources and workload identities.
5. `gitops` promotes reviewed artifact digests; Argo CD reconciles the approved desired state.

Cloud authentication uses GitHub OIDC and Google Cloud Workload Identity Federation. Long-lived
service-account JSON keys are not an accepted automation path.

## Incident and recovery entry points

| Situation | First stop |
| --- | --- |
| Live infrastructure or capacity incident | [Infrastructure runbooks](https://github.com/mindclade/infrastructure-live/blob/main/docs/runbooks/README.md) |
| GitHub Enterprise control drift | [Manual controls and drift checklist](https://github.com/mindclade/github-config/blob/main/docs/enterprise-manual-controls.md) |
| Ring-0 or state-backend recovery | [Disaster recovery](https://github.com/mindclade/bootstrap/blob/main/docs/disaster-recovery.md) |
| Break-glass access | [Break-glass procedure](https://github.com/mindclade/bootstrap/blob/main/docs/break-glass.md) |
| Kubernetes policy or promotion failure | [GitOps policy guide](https://github.com/mindclade/gitops/blob/main/policy/README.md) |
| Vulnerability or unsafe model behavior | [Security reporting](https://github.com/mindclade/.github/blob/main/SECURITY.md) |

Use the owning incident-response channel for coordination. Keep sensitive evidence in the
approved incident system; link sanitized identifiers from GitHub when traceability is needed.

## Working agreements

- Changes reach `main` through reviewed pull requests and required checks.
- Third-party GitHub Actions use full commit-SHA pins; internal reusable workflows use immutable full semver.
- CODEOWNERS, rulesets, environments, access, and repository properties are declared in `github-config`; they do not inherit from a profile repository.
- Production changes use protected environments, separate plan/apply identities, and exact reviewed artifacts.
- Security and biosecurity concerns use private reporting channels, never ordinary issues or discussions.

For organization-wide security and support routes, see the canonical
[security policy](https://github.com/mindclade/.github/blob/main/SECURITY.md) and
[support policy](https://github.com/mindclade/.github/blob/main/SUPPORT.md).
