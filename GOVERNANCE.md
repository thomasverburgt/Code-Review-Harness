# Project Governance

Code Review Harness is maintained as an evidence-driven architecture and software project. Governance exists to preserve technical coherence, traceability, security, and human decision authority while allowing useful outside contribution.

## Roles

The project maintainer owns repository administration, release decisions, roadmap priority, licensing decisions, and final acceptance of changes.

Contributors propose and implement changes, provide evidence, participate in review, and retain responsibility for their submissions under the Developer Certificate of Origin.

Reviewers assess correctness, architecture, security, licensing, documentation, evidence, and downstream impact. Review is advisory until an authorized maintainer accepts or rejects the change.

Automated agents may analyze, recommend, draft, test, and identify conflicts. They do not approve pull requests, accept risk, change requirements, grant exceptions, or exercise project authority.

## Decision process

Routine corrections may be accepted through normal pull-request review. Material decisions require an ADR, including changes to:

- architectural boundaries or system decomposition;
- agent authority, contracts, stable IDs, or orchestration;
- artifact schemas, evidence semantics, confidence, or traceability;
- security, privacy, risk, release, or human-review controls;
- licensing, contribution policy, or governance;
- compatibility guarantees or supported deployment models.

Decisions must identify evidence, alternatives, consequences, affected artifacts, decision authority, and unresolved risks. Silence is not consent, and unresolved disagreement must not be hidden through averaging or editorial simplification.

## Change acceptance

Acceptance considers technical quality, mission fit, evidence strength, compatibility, security, maintainability, testability, documentation, and alignment with approved architecture. Maintainers may accept, reject, defer, or request revision.

## Releases

Releases use semantic versioning once executable distributions begin. Until then, the architecture library is identified as `v0.1.0` and evolves through reviewed repository changes. Release approval is a human decision and must identify the commit, included artifacts, known limitations, and applicable license.

## Amendments

Governance changes require an ADR and maintainer approval. The repository history is the authoritative record.