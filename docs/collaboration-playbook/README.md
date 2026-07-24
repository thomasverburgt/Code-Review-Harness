# Collaborative Architecture and Design Playbook

This documentation set defines a repeatable, evidence-led collaboration method for architecture and design work. It is generic by design and may be included in the Code Review Harness repository or another engineering documentation repository.

## Contents

| Document | Purpose |
| --- | --- |
| [Collaboration Protocol](COLLABORATION_PROTOCOL.md) | Normative roles, lifecycle, decision, and commit rules. |
| [Evidence and Traceability](EVIDENCE_AND_TRACEABILITY.md) | Evidence model, source handling, and traceability requirements. |
| [Documentation Governance](DOCUMENTATION_GOVERNANCE.md) | Required updates, versioning, changelog, and ADR practices. |
| [GitHub Document Control](GITHUB_DOCUMENT_CONTROL.md) | Repository-per-project, branch, pull request, review, and merge rules. |
| [Artifact Delivery and Verification](ARTIFACT_DELIVERY_AND_VERIFICATION.md) | Creation, packaging, and verifiable delivery requirements. |
| [Default Connected Collaborator](personas/DEFAULT_CONNECTED_COLLABORATOR.md) | Default interaction style for collaborative architecture and design sessions. |
| [Ruthless QA Evaluator](personas/RUTHLESS_QA_EVALUATOR.md) | High-scrutiny, constructive quality-assurance review persona. |
| [Murphy: Failure-Surface Collaborator](personas/MURPHY_FAILURE_SURFACE_COLLABORATOR.md) | Good-faith adversarial persona for error-path and operational-surface discovery. |
| [Chief Architect](personas/CHIEF_ARCHITECT.md) | Enterprise-level architecture leadership and decision-synthesis persona. |
| [Chief Engineer](personas/CHIEF_ENGINEER.md) | Technical execution, integration, verification, and engineering-readiness persona. |
| [Product Support Manager](personas/PRODUCT_SUPPORT_MANAGER.md) | DoD-informed lifecycle support, affordability, readiness, and continuous-improvement persona. |
| [Session Templates](templates/SESSION_TEMPLATES.md) | Reusable startup, working, commit, and closeout templates. |
| [Session Checklists](templates/SESSION_CHECKLISTS.md) | Facilitator and participant checklists. |
| [Decision Record Template](templates/ADR_TEMPLATE.md) | Template for architecture decision records. |
| [Change Log](CHANGELOG.md) | Version history for this playbook. |

## Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative. A â€œcommitâ€ means an actual, verified update to the designated repository filesâ€”not a conversational agreement, planned change, or retained chat context.

## Adoption

1. Create one GitHub repository for each project and place this directory in it, for example `docs/collaboration-playbook/`.
2. Name the repository, default branch, and authoritative documentation root at each session startup.
3. Use the session templates for new design work.
4. Record accepted material decisions with an ADR and the corresponding documentation updates.
5. Merge reviewed documentation changes through a pull request, as defined in [GitHub Document Control](GITHUB_DOCUMENT_CONTROL.md).

## Session personality

The default session personality is [Default Connected Collaborator](personas/DEFAULT_CONNECTED_COLLABORATOR.md). It governs interaction style, not decision authority, evidence standards, or document-control rules.

