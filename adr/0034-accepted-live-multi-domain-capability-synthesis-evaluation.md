# ADR-0034: Require Accepted-Live Multi-Domain Evaluation Before CAP-SYNTH Scheduling

- Status: accepted
- Date: 2026-08-02
- Decision authority: project owner
- Owners: capability engineering, orchestration, evidence governance, enterprise consumers, and validation
- Depends on: ADR-0017, ADR-0018, ADR-0019, ADR-0020, ADR-0026, and ADR-0033
- Supersedes: none
- Superseded by: none

## Context

ADR-0018 admitted `CAP-SYNTH` as an isolated candidate and proved its contract with adjudicated multi-domain fixtures. Its live execution used `CAP-RISK` alone and therefore proved protocol and lineage behavior, not multi-domain semantic fitness. ADR-0019 produced a technically valid live `CAP-REQ` artifact, and ADR-0020 recorded the project owner's `accept_review_as_complete` response while preserving zero declared requirements as unassessable rather than satisfied.

ADR-0033 removes the mandatory second-verifier gate. Once the project-owner finalization and derived CAP-REQ eligibility records validate, the accepted `CAP-RISK` and eligible `CAP-REQ` artifacts can form the first honest accepted-live, two-domain capability input set.

## Proposed decision

1. Derive CAP-REQ eligibility from the exact ADR-0020 response and ADR-0033 project-owner finalization. Preserve `GAP-REQ-001`, `DC-REQ-001`, the zero-population interpretation, and every limitation.
2. Build a `CAP-COORD` manifest whose declared and received designations are exactly `CAP-RISK` and `CAP-REQ`. Bind accepted live artifact IDs and output hashes, CAP-REQ eligibility, freshness, compatibility, conflicts, and complete child-record traceability.
3. Reject dispatch when either input is missing, extra, stale, incompatible, mutated, revoked, fixture-tier, or not the artifact named by the governing records.
4. Execute the pinned CAP-SYNTH candidate on GX-10 or another approved DGX Spark equivalent using only the exact accepted-live artifacts admitted by CAP-COORD. Label the result `accepted_live_multi_domain_candidate_evaluation`.
5. Preserve every source assertion, conflict, unknown, confidence provenance, evidence reference, and decision request. Zero declared requirements must not become satisfied requirements, positive coverage, or capability readiness.
6. Produce a deterministic comparison and semantic-review packet. A named human semantic authority must disposition the exact packet; the project owner finalizes its effect under ADR-0033.
7. Demonstrate comparison-only compatibility with `ENT-ARCH`, `ENT-GOV`, `ENT-STRAT`, and `ENT-SYNTH` without scheduling any enterprise candidate.
8. Keep CAP-SYNTH unscheduled. Preserve `CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK` as the accepted and tested rollback route. Do not change reports, distribution state, deployment, or the A100 production baseline.

## Proposed flow

`owner-finalized ADR-0020 response -> CAP-REQ eligibility -> accepted CAP-RISK + eligible CAP-REQ -> CAP-COORD -> isolated GX-10 CAP-SYNTH candidate -> human semantic review -> project-owner finalization -> later scheduling ADR`

Any absent or failed gate blocks the flow without modifying the accepted route.

## Alternatives considered

- Promote from adjudicated fixtures: rejected because fixtures prove contract behavior, not accepted-live semantics.
- Run before CAP-REQ eligibility: rejected because the evidence tier would be false.
- Schedule immediately after a passing GX-10 run: rejected because schema validity is not semantic acceptance.
- Evaluate all enterprise candidates simultaneously: rejected because the capability boundary should be independently reviewable and reversible first.

## Rollback

Revoke derived CAP-REQ eligibility, disable the accepted-live CAP-SYNTH candidate workflow, retain all immutable evidence, and continue the accepted direct enterprise route. No report or deployment state requires migration.

## Validation required

- exact owner-finalized CAP-REQ eligibility;
- exact accepted-live CAP-RISK and CAP-REQ admission;
- fail-closed negative, revocation, and tier-confusion cases;
- complete lineage, conflict, uncertainty, and authority preservation;
- pinned GX-10 execution and deterministic projection;
- human semantic-review and project-owner finalization records;
- comparison-only enterprise compatibility;
- tested rollback; and
- unchanged scheduling, reports, distribution, deployment, and A100 production baseline.

## Decision requested

Approve, reject, or amend the accepted-live multi-domain capability synthesis evaluation. Approval authorizes isolated implementation and GX-10 evaluation; it does not authorize CAP-SYNTH scheduling, enterprise shadow integration, report changes, deployment, or A100 production promotion.

## Decision

Accepted by `thomasverburgt`, project owner, on 2026-08-02. Acceptance authorizes the bounded implementation, local conformance, GX-10 model-backed evaluation, semantic-review packet generation, enterprise compatibility checks, and rollback rehearsal described above. It does not authorize CAP-SYNTH scheduling or any report, deployment, or A100 production change.

## Implementation results

The deterministic reference package and exact owner-finalized eligibility gate passed locally. The full local tool suite passed 130 tests. The scoped GX-10 structural, ADR-0034, and CAP-SYNTH regression suites passed 14 tests.

The first credential-discovery attempt failed closed without producing a candidate. A subsequent schema-valid model run exposed a stale derived-assertion ID in the harness-owned enterprise handoff; that run is retained as a pre-lineage-tightening attempt and is not the review candidate. The projection and validator now require exact agreement among model-derived assertion IDs, preserved source-record IDs, decision-request IDs, and the enterprise handoff.

The tightened Qwen3-32B run passed on GX-10. Its exact candidate is `0cbe961f-82da-5cf5-92bd-2674c07459ef` with output hash `sha256:32af60e0eb9ab3f397496abc4a55876ce4e7d8c97354c568841ac9f714fbe269`. It preserves zero declared requirements as unassessable, cites the accepted CAP-RISK and eligible CAP-REQ artifacts, and exports matching `DERIVED-001` lineage. The exact semantic-review packet is `3ea2c228-d55f-5d62-bd66-64e0e6037499` with hash `sha256:49b85c84b96ca7d148c067ddaf39cda7970c8008b2656a394b8af4e400d7447f`.

On 2026-08-02, `thomasverburgt` dispositioned the exact packet `accept_semantically_faithful`. Disposition `3eec7ec3-d012-57fe-9858-7a870bb10123`, finalization `09a017fc-b318-5c7a-af3c-1a49022c7ba0`, and derived eligibility `5f3e8885-b5df-578c-87b2-c22fab03342c` make the exact candidate eligible for enterprise candidate evaluation only. CAP-SYNTH remains unscheduled. The accepted route, reports, distribution state, deployment, and A100 production baseline remain unchanged.
