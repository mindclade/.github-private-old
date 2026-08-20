# Contributing

This repository controls the member-only profile shown on the Mindclade organization page.
Keep changes concise, operationally useful, and safe for every organization member to read.

## Change process

1. Create a branch from `main`.
2. Update `profile/README.md` and any repository documentation needed to explain the change.
3. Run `make validate`; run `make lint` when actionlint and yamllint are installed.
4. Open a pull request using the repository template.
5. Obtain the required approvals, including code-owner review, before merge.

Do not use this repository for GitHub settings, reusable workflow implementations, secrets,
incident timelines, customer data, private model material, restricted biological content, or
production configuration. Put desired state in `github-config`, shared automation in `.github`,
and operational detail in the owning repository.
