# Specialist Human Shadow Calibration Contract

- **Contract designation:** `CONTRACT-SPECIALIST-HUMAN-SHADOW-CALIBRATION`
- **Version:** `1.0.0`
- **Governing decision:** [ADR-0039](../adr/0039-build-specialist-candidates-for-human-shadow-calibration.md)
- **Extends:** [Universal Agent Contract](universal-agent-contract.md), [Specialist Agent Contract](specialist-agent-contract.md), and [Evidence Contract](evidence-contract.md)

This contract governs unscheduled `SPEC-*` candidate construction, GX-10 or DGX Spark-equivalent calibration, and comparison-only human review. It creates no deployment, scheduling, product fan-in, report, release, risk-acceptance, or A100 production authority.

## Exact candidate admission

Every dispatch binds the registered specialist identity and contract version; one current specification; exact focus-profile ID, version, and hash; source-specification hash; prompt; role schema; rubric; model manifest; tool policy; environment policy; immutable repository revision; admitted evidence population; access classification; and comparison-only lifecycle. Any missing, stale, substituted, revoked, or mismatched binding fails before dispatch.

The evidence adapter is least privilege. The candidate receives only the admitted evidence needed for its authoritative question. Repository modification is prohibited. A target repository cannot be committed to, pushed to, or changed by the harness.

## Output and lifecycle boundary

Raw model output, harness-owned projection, validation result, evidence locators, telemetry, and rollback records remain separate immutable objects. Deterministic projection may enforce identity, bindings, schema shape, prohibited effects, and lineage; it may not silently change semantic meaning.

Every candidate artifact and derivative packet is `comparison_only`, `unscheduled`, ineligible for product fan-in and reports, and unauthorized for deployment or A100 production. A candidate may be retained, revised, adjudicated, superseded, or revoked without changing the accepted baseline.

## Human review packet

Every distributed observation, finding, recommendation, unknown, or pattern binds its original specialist record ID, statement, confidence meaning, evidence references, and one or more evidence locators. A locator preserves repository, immutable revision, safe path, line or section, fingerprint, access class, safe excerpt, redaction state, reproduction steps, and integrity hash.

Packet generation fails closed when required evidence is missing, mutable, altered, unsafe, inaccessible to the intended reviewer, or not precisely located. Redaction never includes a raw restricted value and never removes source identity.

## Reviewer response

The reviewer binds the exact packet and every item. Allowed dispositions are `supported`, `partially_supported`, `unsupported`, `duplicate`, `outside_specialist_scope`, and `unable_to_determine`. The response also records locator correctness, severity and recommendation reasonableness, missing evidence, rationale, review duration, experience, domain qualifications, access, and conflicts of interest.

Intern and general engineering feedback is classified `non_authoritative_human_review` with effect `calibration_evidence_only`. It may measure reviewability and apparent correctness but cannot establish professional truth, approve an agent, accept risk, determine compliance, authorize a change, or alter harness state. Appropriately qualified subject-matter adjudication is required before a response becomes gold, negative, or promotion evidence. Project-owner finalization remains separate.

## Metrics

Metrics bind exact packets and responses. They may report dispositions, locator outcomes, review duration, agreement, evidence requests, and usability. They must not represent agreement or acceptance rate as correctness. Raw reviewer records remain available for reconstruction.

## Failure and rollback

Invalid candidates and review artifacts are retained as failed calibration evidence and cannot be routed downstream. Rollback disables candidate discovery, dispatch, and packet export; revokes active review eligibility; and retains all source, execution, review, metric, and audit records. The accepted workflow, reports, distribution, deployment, and production state remain unchanged.
