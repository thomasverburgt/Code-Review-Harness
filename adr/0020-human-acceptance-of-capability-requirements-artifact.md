# ADR-0020: Require Human Acceptance of the CAP-REQ Artifact Before Multi-Domain Use

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Required external authority: requirements-acceptance-authority
- Depends on: ADR-0019

## Context

ADR-0019 produced a technically valid live CAP-REQ candidate artifact. Its bounded source manifest contains no authoritative requirements, so the artifact correctly records zero requirement records, no satisfaction rate, and a source-located traceability gap. Technical validation cannot determine whether the zero-population boundary is acceptable requirements practice or whether another authoritative source must be supplied.

CAP-COORD must not treat this candidate as an accepted live synthesis input until a human requirements authority reviews the exact evidence and records that decision. Project-maintainer acceptance of the implementation is not requirements acceptance of the artifact.

## Proposed decision

1. Generate an immutable requirements-acceptance review packet bound to the exact live CAP-REQ artifact hash, requirement-source manifest hash, locator hash, model/prompt/rubric/projection pins, zero-population interpretation, traceability gap, limitations, and rollback state.
2. Permit only a `requirements-acceptance-authority` to record one disposition: `accept_review_as_complete`, `supply_authoritative_requirements`, `require_scope_correction`, `reject_artifact`, or `insufficient_evidence`.
3. Keep the response record-only. Acceptance means the bounded review artifact may become an accepted CAP-REQ input; it does not mean any requirement is satisfied, approve capability readiness, accept risk, or schedule CAP-SYNTH.
4. Require exact packet/artifact/source hashes, authority identity, rationale, timestamp, and independent administrative verification before deriving eligibility.
5. Keep CAP-REQ out of accepted multi-domain CAP-COORD manifests unless the disposition is `accept_review_as_complete` and verification passes.
6. Require a later separate decision for live multi-domain CAP-SYNTH calibration and another later decision for scheduling.

## Rollback

Ignore or revoke derived eligibility while retaining the immutable packet and response for audit. CAP-REQ remains candidate-only, CAP-RISK remains the sole accepted live capability input, and CAP-SYNTH remains unscheduled. No report, governance, deployment, or A100 production state requires migration.

## Validation required

- exact immutable packet and source bindings;
- authorized, independently verified response;
- missing, mutated, stale, mismatched, unauthorized, or incomplete responses fail closed;
- no requirement-satisfaction, readiness, risk, scheduling, report, deployment, or production authority;
- full local and GX-10 regression; and
- deterministic derived eligibility with rollback.

## Decision requested

Approve or reject implementation of the record-only requirements-acceptance boundary. Acceptance authorizes packet generation, response validation, and test evidence; it does not supply the external human disposition.

## Decision

Accepted by the project maintainer on 2026-08-01. This acceptance authorizes implementation and conformance testing only. It does not constitute the external `requirements-acceptance-authority` disposition.

## External requirements-acceptance result

On 2026-08-01, `thomasverburgt`, acting as the `requirements-acceptance-authority`, recorded `accept_review_as_complete` for the exact ADR-0020 packet and CAP-REQ artifact. The response preserves the interpretation that zero declared requirements is unassessable rather than satisfied, and it leaves `GAP-REQ-001` and `DC-REQ-001` explicit.

This is a record-only expert disposition. It does not establish requirement satisfaction, capability readiness, risk acceptance, scheduling, deployment, or production authority. The state is `response_recorded`; accepted-input eligibility remains fail-closed until a different `governance-records-verifier` independently verifies the response.
