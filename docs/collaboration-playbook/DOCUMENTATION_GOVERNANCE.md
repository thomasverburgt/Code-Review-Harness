# Documentation Governance

## 1. Authoritative document set

Each project MUST have its own GitHub repository. That repository is the authoritative system of record for project documentation, decisions, evidence indexes, templates, and release artifacts. Documents are managed with the same branch, review, merge, and history discipline as code. See [GitHub Document Control](GITHUB_DOCUMENT_CONTROL.md).

For an architecture/design effort, maintain at minimum:

| Artifact | Required use |
| --- | --- |
| `README.md` | Scope, navigation, ownership, and current baseline. |
| `CHANGELOG.md` | Human-readable history of published documentation changes. |
| `adr/` | Accepted, superseded, and rejected material decisions. |
| `design/` | Architecture, contracts, models, and supporting specifications. |
| `evidence/` | Evidence index, traceability records, and validated references. |
| `templates/` | Reusable session, ADR, review, and handoff templates. |

## 2. Required updates for a documentation commit

Every documentation commit MUST update the primary artifact and MUST also update:

- the changelog;
- the context handoff when scope, decisions, or open questions change;
- relevant indexes or registries;
- an ADR for architectural or governance decisions;
- version metadata when published contract, interface, or process semantics change.

## 3. Versioning

Use semantic versioning for stable document sets where practical:

- **MAJOR:** incompatible process or contract change.
- **MINOR:** new compatible protocol, template, or required section.
- **PATCH:** clarification, typo, or non-semantic correction.

Use an explicit baseline tag for a first established set, such as `v0.1.0`. A document may also carry its own version when it evolves independently.

## 4. Changelog practice

Changelog entries MUST be dated and include: change ID, artifact(s), classification, concise description, and ADR reference where applicable. Do not use “committed” to describe intended work; use it only after verification.

## 5. ADR practice

Create an ADR when a decision:

- changes architecture, interfaces, standards, risk posture, governance, or lifecycle rules;
- has significant reversibility, cost, security, or operational impact;
- resolves a recurring ambiguity; or
- supersedes a prior material decision.

ADR status values: `proposed`, `accepted`, `rejected`, `superseded`, `deprecated`. An ADR MUST preserve the context, decision, alternatives, consequences, evidence, and validation approach. Use [the ADR template](templates/ADR_TEMPLATE.md).

## 6. Review and quality gate

Before delivery, the document custodian MUST verify:

- all required sections are present;
- internal links and referenced file paths resolve;
- decision, recommendation, and evidence IDs are unique;
- no proposal is labeled as an accepted decision without authority;
- changelog and ADR state match the documents;
- package manifest matches delivered contents.

## 7. GitHub merge requirement

No documentation change is part of the project baseline until its pull request is approved and merged to the default branch. A ZIP may support review or distribution, but it MUST be traceable to the merged commit SHA and MUST NOT replace the GitHub repository as the authoritative record.

