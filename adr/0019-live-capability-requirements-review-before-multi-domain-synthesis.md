# ADR-0019: Establish Live Capability Requirements Review Before Multi-Domain Synthesis

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: capability engineering, requirements authorities, orchestration, validation, and enterprise consumers
- Depends on: ADR-0017 and ADR-0018
- Supersedes: none
- Superseded by: none

## Context

ADR-0018 proves the CAP-SYNTH candidate contract with adjudicated multi-domain fixtures and proves live protocol/lineage behavior with the sole accepted `CAP-RISK` artifact. Neither is sufficient for live multi-domain synthesis. The next honest promotion dependency is another independently produced and accepted live capability-review artifact.

`CAP-REQ` is the best next domain because requirement traceability is structurally distinct from risk, directly affects capability closure, and can expose absent or ambiguous requirements without inventing them. The registry labels `CAP-REQ` baseline, but the role does not yet have a complete prompt/schema/projection/gold-negative/live calibration package in the executable harness.

## Proposed decision

1. Implement `CAP-REQ` as an executable capability-review role with a dedicated specification, prompt, role schema, rubric, deterministic projection, gold/negative package, and exact immutable input policy.
2. Require declared requirement sources and implementation/evidence bindings. Missing requirement declarations, unverifiable mappings, or insufficient evidence must remain explicit `unknown`, `not_reviewed`, or incomplete traceability states; the model cannot invent a requirement or mark one satisfied by implication.
3. Produce a complete review artifact even when the reviewed requirement posture is unresolved, provided the declared review population was processed honestly. Artifact completion means the review ran successfully, not that requirements are satisfied.
4. Use the clean read-only `uds-core` clone and its pinned revision only as test evidence. Do not commit, push, open a PR, or represent the harness as a contributor to that repository.
5. Run all development, regression, negative, and live-model calibration on GX-10/DGX Spark-equivalent infrastructure. Retain the A100 large cluster as the production target without representing GX-10 capacity as A100 performance.
6. Keep the resulting artifact candidate/test evidence until a named human requirements authority reviews and accepts it for use in a live multi-domain CAP-COORD manifest.
7. Do not schedule CAP-SYNTH or alter the accepted enterprise/report path as part of this increment.

## Alternatives considered

- Promote CAP-SYNTH from the adjudicated fixture: rejected because fixture provenance is not accepted live evidence.
- Treat the CAP-RISK-only smoke as multi-domain fitness: rejected because it contains no cross-domain semantic task.
- Implement several capability domains simultaneously: rejected because a single additional vertical gives clearer lineage, rollback, and calibration evidence.
- Use undocumented inferred requirements: rejected because inferred intent cannot become an authoritative requirement silently.

## Consequences

This delays multi-domain synthesis promotion but produces a real, independently governed second domain and exercises unknown/incomplete requirement semantics. It also establishes the reusable requirement-to-source-to-implementation evidence boundary needed by later capability and enterprise reviews.

## Rollback

Disable CAP-REQ candidate dispatch and retain its prompts, schemas, fixtures, artifacts, telemetry, and GX-10 evidence for audit. Continue using the accepted CAP-RISK path and keep CAP-SYNTH unscheduled. No accepted report, governance record, deployment configuration, or A100 production baseline requires migration.

## Validation required

- exact identity, prompt, rubric, model, schema, projection, and input pins;
- immutable requirement source and evidence locators;
- declared-population completeness with honest denominators and unknown states;
- no invented requirements, satisfaction claims, evidence, lineage, or authority;
- preserved conflicts, decisions requested, confidence provenance, and human acceptance boundary;
- deterministic replay and CAP-COORD compatibility;
- complete local and GX-10 regression plus live-model calibration;
- explicit human acceptance before use as accepted live multi-domain synthesis input; and
- proof that CAP-SYNTH scheduling, reports, governance, deployment, and the A100 baseline remain unchanged.

## Decision requested

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes `CAP-REQ` executable candidate implementation and GX-10 calibration as the next live capability-domain vertical. Acceptance does not itself accept the resulting artifact for synthesis or authorize CAP-SYNTH scheduling.

## Implementation evidence

CAP-REQ now has an executable candidate specification, prompt, role schema, rubric, workflow, model manifest, deterministic projection, reference runner, immutable requirements-source manifest, exact retained UDS evidence locator, and eight targeted negative/immutability tests. The bounded source manifest declares zero authoritative requirements. The complete review therefore emits zero requirement records, no satisfaction rate, one exact traceability gap, and `pending_human_requirements_acceptance`; it does not convert documentation or findings into requirements.

The structural validator and all 55 tests pass locally and on GX-10. The deterministic candidate file is byte-identical across platforms with SHA-256 `2cce27fad172421360bc96245f07036d1dedd2d3b5cf201b5907458227bbe8dd`. The GX conformance transcript has SHA-256 `68c6a71ff9a70a254fd9b223d5e928f3af02a814b4ae4da79d78e32e031f6d40`; the GX deterministic archive has SHA-256 `a6eebc6af94122396c722fff2e5f2be944826e7609322ac1c85ce7e67e066d8a`.

The isolated live Qwen3-32B calibration passed with 2,312 input tokens and 363 output tokens. It preserved the zero declared population, emitted no invented requirement or satisfaction claim, retained the exact locator gap, and preserved human-only acceptance. The live summary has SHA-256 `26d201b36df8f3ddfec1f30dcb6d449d093b61c97f63a89b2f70da1ff5d31b81`; the live archive has SHA-256 `0ec268dcc78f9c448cee43b75ffc01dfe857308b320d825f8bb59a85b4f78189`.

No `uds-core` file was modified and no commit, push, issue, or PR was created there. CAP-SYNTH remains unscheduled. Reports, governance state, deployment configuration, and the A100 production baseline remain unchanged.

## Remaining acceptance dependency

The live CAP-REQ artifact is technically valid but is not yet an accepted live capability-review input. A human requirements authority must review the exact artifact, source manifest, locator, zero-population interpretation, and traceability gap before CAP-COORD may include it in an accepted multi-domain manifest.
