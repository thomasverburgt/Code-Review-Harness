# CAP-REQ Human Acceptance Contract

Version: 2.0.0
Decision: [ADR-0020](../adr/0020-human-acceptance-of-capability-requirements-artifact.md), superseded in part by [ADR-0033](../adr/0033-project-owner-finalization-without-mandatory-second-verifier.md)

## Purpose

This contract governs the boundary between a technically valid CAP-REQ artifact and its use as an accepted capability input. It prevents the harness or a model from substituting for the human requirements authority while recognizing the project owner's final authority over harness state.

## Inputs

The packet generator consumes the exact retained live CAP-REQ artifact, its immutable requirement-source manifest, the reproducible source locator, and the artifact's model, prompt, rubric, projection, and toolchain pins. All content and integrity hashes must validate before a packet is emitted.

The zero declared-requirement population has one permitted interpretation: requirement satisfaction is unassessable. It must never be represented as zero-percent or one-hundred-percent satisfaction.

## Records and authority

1. The harness deterministically emits an immutable `requirements-acceptance-packet` with effect `review_request_only`.
2. Only the external `requirements-acceptance-authority` may issue a response. Its response is record-only and must bind the exact packet and CAP-REQ artifact.
3. The registered `project-owner` finalizes the response's packet, artifact, source, authority, scope, and record-integrity bindings. The project owner may be the same person as the requirements authority; no second verifier is required.
4. The harness deterministically derives eligibility. Only `accept_review_as_complete` plus a valid project-owner finalization yields `eligible_for_accepted_capability_input`.
5. Every other disposition, failed finalization, absent record, or revoked eligibility fails closed as not eligible.

The response dispositions are `accept_review_as_complete`, `supply_authoritative_requirements`, `require_scope_correction`, `reject_artifact`, and `insufficient_evidence`.

## Meaning of acceptance

Acceptance means only that the bounded CAP-REQ review is complete enough to be used as an accepted input. It does not assert that any requirement exists or is satisfied. It grants no capability-readiness, enterprise-risk, report-distribution, deployment, production, or scheduling authority. CAP-SYNTH remains unscheduled and requires a separate later decision.

## State and rollback

The normative state machine is [requirements-acceptance.state-machine.json](../orchestration/state-machines/requirements-acceptance.state-machine.json). Packet, response, project-owner finalization, and optional historical verification records are immutable. Rollback creates a revoked derived eligibility record; it does not delete or alter the authoritative history. Consumers must select the latest valid derived record and treat revoked or missing eligibility as not eligible.

## Deployment and testing

The production target is the A100 large cluster. All conformance and integration testing runs on a DGX Spark or approved equivalent, currently the GX-10. The acceptance boundary is deterministic and model-independent, but must pass the same deployment-platform regression gate as the rest of the harness.
