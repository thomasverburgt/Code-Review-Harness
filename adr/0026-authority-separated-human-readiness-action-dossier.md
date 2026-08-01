# ADR-0026: Create an Authority-Separated Human Readiness Action Dossier

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Required external authorities: the authority named by each readiness prerequisite
- Depends on: ADR-0012, ADR-0016, ADR-0020, ADR-0025

## Context

ADR-0025 proves that enterprise shadow integration is blocked by six explicit prerequisites. Two already have immutable human-review packets, while four require accepted-live multi-domain evidence and independent semantic evaluation. Leaving these records distributed across evidence directories makes coordination harder, but combining them carelessly could imply that one reviewer or one signature can satisfy unrelated authorities.

## Proposed decision

1. Generate one immutable readiness action dossier that indexes all six prerequisites by exact readiness-manifest ID/hash, source artifact/archive hash, current state, required authority, required response schema, and independent verification requirement.
2. Embed or reference the existing ADR-0016 and ADR-0020 review packets without changing them.
3. Generate separate domain-acceptance packet templates for ENT-ARCH, ENT-GOV, ENT-STRAT, and ENT-SYNTH. Each template must identify the additional accepted-live multi-domain evidence still required before a response can be valid.
4. Keep decisions atomic and authority-separated. No dossier-level approval, batch signature, majority vote, project-maintainer statement, or administrative action may satisfy a domain prerequisite.
5. Require each response to bind the exact packet, evidence artifacts, scope, rubric, evaluator identity and authority, disposition, rationale, limitations, timestamp, expiration or supersession state, and response hash.
6. Require an authenticated records administrator and a distinct independent verifier before a response may derive a satisfied readiness prerequisite.
7. Make absent evidence produce `not_ready_for_review`, not a prefilled approval request. Protocol-smoke and fixture evidence remain contextual only.
8. Derive a successor readiness manifest only from individually verified records. The dossier itself cannot schedule a shadow workflow, modify reports, record risk acceptance, approve distribution, or authorize deployment.
9. Preserve rollback by retaining every packet and record while revoking only derived readiness eligibility. The accepted route remains unchanged.
10. Target production deployment to the A100 large cluster and perform all dossier, verification, rollback, and regression testing on DGX Spark or an approved equivalent, currently GX-10.

## Alternatives considered

- **Ask one leader to approve the complete readiness manifest:** rejected because the prerequisites belong to different domain authorities.
- **Send only the two currently actionable packets:** rejected because reviewers and program owners also need a precise inventory of missing domain evidence.
- **Generate approval templates for missing evidence:** rejected because that encourages decisions before a reviewable evidence package exists.
- **Wait without creating a coordination artifact:** rejected because the block is valid but should still be operationally actionable.

## Consequences

The project gains one reviewable work queue without centralizing decision authority. Some entries will remain `not_ready_for_review` until new multi-domain evidence exists. This is useful state, not an implementation failure.

## Rollback

Stop generating the dossier and retain all component packets, responses, verifications, and prior readiness manifests. Revoke derived eligibility if necessary. No accepted workflow, report, candidate schedule, or deployment state changes.

## Validation required

- exact readiness-manifest, packet, evidence, authority, response, and verification bindings;
- no dossier-level or cross-domain authority;
- missing evidence remains `not_ready_for_review`;
- independently verified atomic responses only;
- fail-closed missing, duplicate, stale, mutated, unauthorized, expired, superseded, or bundled decisions;
- deterministic dossier, immutable ledger, and rollback-safe derived readiness;
- unchanged baseline, report, distribution, scheduling, and deployment state; and
- full local and GX-10 regression.

## Decision requested

Approve, reject, or amend the authority-separated human readiness action dossier. Approval would authorize packet/index generation and validation only; it would not supply evidence, make a human disposition, satisfy a prerequisite, schedule shadow integration, or authorize A100 deployment.

## Decision

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes deterministic dossier and packet-template generation, validation, immutable persistence, and conformance testing only. It does not create evidence, make or bundle a disposition, satisfy readiness, schedule integration, modify a report, or authorize deployment.
