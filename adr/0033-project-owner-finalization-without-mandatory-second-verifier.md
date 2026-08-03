# ADR-0033: Project-Owner Finalization Replaces Mandatory Second-Person Verification

- Status: accepted
- Date: 2026-08-02
- Decision authority: project owner
- Project owner: `thomasverburgt`
- Owners: project governance, orchestration, evidence governance, and harness maintainers
- Supersedes: ADR-0012 mandatory second-verifier provisions; ADR-0020 independent-verification prerequisite; ADR-0026 independent-verification prerequisite
- Superseded by: none

## Context

The harness currently requires a second `governance-records-verifier` after several human decisions have already been made and immutably recorded. That rule was introduced to separate substantive authority, administrative recording, and integrity checking. In this project, however, the project owner is the final authority for whether a correctly bound governance record becomes effective in the harness. Requiring another person creates an operational veto and prevents the owner from advancing an otherwise complete decision.

The project owner directed on 2026-08-02 that no second verifier be required. This decision changes the authorization model, not the evidence model. Exact source, packet, response, artifact, authority, hash, timestamp or decision-date, and audit bindings remain mandatory. Domain experts still provide substantive decisions where a contract names them; the project owner controls finalization within this harness.

Historical verification records remain immutable evidence of the policy that applied when they were created. They are not deleted or rewritten.

## Decision

1. Remove mandatory second-person verification as a prerequisite for report distribution, external-decision reconciliation, semantic adjudication, requirements acceptance, domain acceptance, readiness derivation, scheduling proposals, and other project-governance transitions.
2. Register `project-owner` as the finalization authority for this repository. The current project owner is `thomasverburgt`.
3. A project-owner finalization may be recorded by the same person who made, approved, or administratively entered the underlying decision. No distinct-subject constraint applies.
4. Require a content-addressed project-owner finalization record for consequential machine-state changes. It must bind the exact target record ID and hash, source and authority checks, project-owner identity, decision date or timestamp, disposition, and finalization hash.
5. Permit direct eligibility derivation when the underlying response was itself made by the registered project owner and all contract bindings validate. A separate finalization record may still be emitted for audit, but it is not a second-person gate.
6. Preserve named domain authority. The project owner does not cause a model recommendation to become an expert decision and does not erase a contractually required external expert response. Project-owner finalization determines whether a valid decision record becomes effective in this harness.
7. Keep optional independent review available as assurance evidence. It may inform the project owner but cannot block an otherwise valid owner-finalized record unless a later ADR explicitly restores that control.
8. Replace `pending_independent_verification` states with `pending_project_owner_finalization`, `owner_finalized`, `rejected`, or another contract-specific terminal state.
9. Preserve fail-closed behavior for missing, malformed, unauthorized, stale, superseded, revoked, hash-mismatched, or scope-mismatched records.
10. Do not rewrite historical ADRs, evidence packages, verification records, or creation-time readiness manifests. Living contracts, state machines, status projections, and runtimes must cite this ADR as the superseding authority.

## Consequences

The project owner can advance valid governance records without waiting for a second person. The harness retains tamper evidence, source binding, explicit authority, deterministic derivation, revocation, and audit history, but it no longer claims dual control.

This concentrates finalization authority in one person. The tradeoff is explicit: operational continuity and accountable ownership are preferred over mandatory separation of duties for this project. Deployments governed by external law, regulation, customer policy, or accreditation may add an independent-review requirement at that boundary without changing this repository-wide default.

## Rollback

A later ADR may restore mandatory independent verification for selected decision classes. Existing project-owner finalizations remain immutable historical records. Rollback changes the eligibility rule prospectively and does not delete or rewrite decisions, exports, attestations, or evidence.

## Validation

- the project-owner identity and allowed actions resolve through the authority registry;
- every finalization binds the exact target record and content hash;
- invalid authority, source, integrity, scope, stale, superseded, or revoked records fail closed;
- the same human may make and finalize a decision without a distinct-subject error;
- optional historical verifier records remain readable and replayable;
- current state no longer blocks on a mandatory second verifier;
- no model or agent receives human decision authority;
- rollback and revocation remain deterministic; and
- all local and GX-10 regression tests pass before promotion.

## Decision record

Accepted by `thomasverburgt`, project owner, on 2026-08-02. This acceptance removes mandatory second-person verification and authorizes implementation of project-owner finalization throughout the harness.
