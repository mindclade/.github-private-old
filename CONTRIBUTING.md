<!-- mindclade-doc: contributing@1 -->

# Contributing to Mindclade · `.github-private`

This repository controls the member-only profile shown on the Mindclade organization page.
Keep changes concise, operationally useful, and safe for every organization member to read.

## Change process

1. Create a branch from `main`.
2. Update `profile/README.md` and any repository documentation needed to explain the change.
3. Run `nix flake check --no-update-lock-file` using the committed toolchain lock.
4. Open a pull request using the repository template.
5. Obtain the required approvals, including code-owner review, before merge.

Do not use this repository for GitHub settings, reusable workflow implementations, secrets,
incident timelines, customer data, private model material, restricted biological content, or
production configuration. Put desired state in `github-config`, shared automation in `.github`,
and operational detail in the owning repository.


## Contributor authorization and intellectual property

A contribution may be submitted only by a person authorized under a current
written employment, contractor, assignment, or other contribution agreement
with Mindclade, LLC. Before opening or updating a pull request, the contributor
must confirm that:

- they have the right and authority to submit every part of the contribution;
- first-party work is covered by the contributor's controlling written
  agreement with Mindclade, LLC.;
- third-party code, data, models, media, fonts, specifications, and generated
  material are identified with their source, version, license, provenance, and
  required notices;
- the contribution contains no material whose confidentiality, license,
  consent, acceptable-use terms, export controls, or other restrictions
  prohibit submission; and
- the change description and validation evidence are complete and accurate.

By submitting or updating a pull request, the contributor represents that these
statements are true. Submission is not acceptance and does not by itself alter
ownership, grant a license, or replace the controlling written agreement.
Signed commits establish source identity and integrity; they are not a
substitute for the required written agreement.

If authorization or ownership is unclear, stop before submission and use the
legal or contract channel named in the applicable agreement. Do not place
confidential material in a public issue or an unapproved email.
