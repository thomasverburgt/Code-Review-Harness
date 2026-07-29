# Contributing

Thank you for contributing to Code Review Harness. Contributions should preserve the project's evidence-first architecture, human decision authority, traceability, and reviewability.

## Before opening a change

Use an issue or architecture decision record for material changes to agent boundaries, artifact contracts, governance, orchestration, schemas, licensing, or repository structure. Small corrections may proceed directly by pull request.

Security vulnerabilities must follow `SECURITY.md` and must not be reported in public issues.

## Development workflow

1. Create a focused branch from the current `main`.
2. Keep each change bounded and explain its intent.
3. Update affected contracts, schemas, diagrams, registries, indexes, and traceability references together.
4. Add or update validation evidence appropriate to the change.
5. Open a pull request using the repository template.
6. Resolve review findings without rewriting or hiding material disagreement.

## Architectural changes

A material architecture change requires an ADR under `adr/`. The ADR must state context, decision, alternatives, consequences, authority, evidence, and supersession relationships.

Agent and contract changes must preserve stable identifiers or document an explicit migration. Changes that alter decision authority, confidence semantics, evidence lineage, risk handling, or human review gates require maintainer approval.

## Licensing

Unless explicitly documented otherwise, contributions are licensed under `AGPL-3.0-only`.

Do not contribute code, text, prompts, diagrams, data, or other material unless you have the right to license it under the project terms. Identify third-party material and its license in the pull request.

## Developer Certificate of Origin

This project uses Developer Certificate of Origin 1.1. By adding a `Signed-off-by` line to a commit, you certify that you created the contribution or otherwise have the right to submit it under the indicated open-source license, and that the contribution and sign-off record may be maintained and redistributed indefinitely.

Sign commits with:

```bash
git commit -s
```

The resulting commit message must contain:

```text
Signed-off-by: Your Name <your.email@example.com>
```

Only the human contributor may add the sign-off. AI tools must not certify the DCO on a person's behalf. The human submitter is responsible for reviewing AI-assisted work and confirming its provenance, accuracy, security, and licensing.

## Commit and pull-request quality

Commits should be intentional, readable, and narrowly scoped. Pull requests must describe what changed, why it changed, affected authority boundaries, validation performed, remaining uncertainty, and follow-on work.

Maintainers may request changes, split oversized submissions, or decline changes that weaken traceability, governance, safety, maintainability, or project direction.