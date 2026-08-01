# ADR-0018: Capability Synthesis Candidate Admission Requires Proven Input Tiers

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: capability engineering, orchestration, enterprise consumers, contract governance, and validation
- Depends on: ADR-0017
- Supersedes: none
- Superseded by: none

## Context

ADR-0017 now provides a passing deterministic `CAP-COORD` manifest and dispatch boundary, but `CAP-SYNTH` remains planned without a dedicated specification, prompt, role schema, rubric, projection, gold/negative package, or enterprise compatibility evidence. The only accepted live capability-review artifact in the current vertical is `CAP-RISK`. That input is sufficient to prove coordination mechanics, but a single risk-domain artifact cannot demonstrate cross-domain capability synthesis quality.

Candidate admission and scheduling therefore need separate evidence tiers. Adjudicated multi-domain fixtures can exercise the semantic contract and negative cases before more live capability roles exist. A live `CAP-RISK`-only run may verify model protocol and exact manifest binding, but it must remain labeled single-domain and cannot support a fitness or scheduling claim.

## Proposed decision

1. Register `CAP-SYNTH` as a candidate only after it has a dedicated role specification, executable role schema, pinned prompt, rubric, deterministic projection, gold package, negative cases, and explicit enterprise handoff contract.
2. Permit candidate inputs only through a hash-valid, `ready_for_cap_synth` `CAP-COORD` manifest and the exact immutable artifacts listed by that manifest. The model cannot validate or widen its own input set.
3. Establish two distinct evidence tiers:
   - `adjudicated_multi_domain_contract_fixture`: two or more schema-valid capability-review fixtures used to test cross-domain preservation, derivation, conflict handling, confidence provenance, and enterprise compatibility; and
   - `accepted_live_input_calibration`: accepted live artifacts used for GX-10 model calibration. A one-domain live set is a protocol/lineage smoke test only.
4. Require every derived assertion to cite source artifact IDs and child record IDs. Preserve child findings, risks, evidence references, confidence provenance, conflicts, unknowns, and decision requests without silent normalization or deletion.
5. Keep all model-generated capability posture advisory. `CAP-SYNTH` cannot accept risk, approve readiness, alter requirements, select a course of action, approve release or distribution, change reports, authorize deployment, or promote the A100 production workflow.
6. Keep `CAP-SYNTH` unscheduled and isolated from the accepted enterprise/report path throughout candidate admission and calibration.
7. Withhold any later scheduling proposal until a declared multi-domain set of accepted live capability-review artifacts passes exact coordinator binding, GX-10 semantic calibration, enterprise-consumer compatibility, human review, full regression, and rollback rehearsal.

## Candidate data flow

`adjudicated fixtures or accepted live capability artifacts -> CAP-COORD immutable manifest -> isolated CAP-SYNTH candidate -> deterministic projection/validation -> comparison-only enterprise handoff`

Any missing, extra, stale, incompatible, hash-mutated, non-manifest, invented-lineage, authority-bearing, or evidence-tier-misrepresented input fails closed before publication.

## Alternatives considered

- Schedule from the passing `CAP-RISK`-only manifest: rejected because mechanical single-domain calibration is not evidence of semantic synthesis fitness.
- Wait to define the candidate until all live capability reviewers exist: rejected because contract and integration risks can be reduced safely with adjudicated multi-domain fixtures.
- Let the model ingest raw capability artifacts without `CAP-COORD`: rejected because the semantic agent must not control its own admission gate.
- Treat adjudicated fixtures as live operational evidence: rejected because it would erase provenance and overstate readiness.

## Consequences

This adds explicit evidence-tier metadata and delays scheduling, but it permits bounded progress on the prompt, schema, projection, and enterprise handoff without making a false multi-domain production claim. It also makes the missing live capability domains a visible promotion dependency rather than an implicit weakness in the evaluation.

## Rollback

Return `CAP-SYNTH` to `planned`, disable all candidate dispatch, and retain candidate prompts, schemas, fixtures, artifacts, comparisons, telemetry, and GX-10 evidence for audit. Continue using the accepted capability artifacts and direct enterprise/report path. No accepted report, governance record, deployment configuration, or A100 production baseline requires migration.

## Validation required

- candidate identity, prompt hash, rubric, model pin, and projection integrity;
- executable universal, capability, and `CAP-SYNTH` role validation;
- exact coordinator-manifest and immutable child-artifact binding;
- adjudicated fixture provenance that cannot be represented as accepted live evidence;
- preserved child assertions, evidence, confidence, conflicts, unknowns, and decision requests;
- explicit source bindings for every derived correlation and enterprise-handoff assertion;
- failure cases for incomplete, extra, stale, incompatible, mutated, invented, authority-bearing, or incorrectly tiered inputs;
- deterministic replay and enterprise-consumer compatibility;
- complete local and GX-10/DGX Spark-equivalent regression plus model calibration; and
- proof that scheduling, reports, governance state, deployment, and the A100 production baseline remain unchanged.

## Decision requested

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes contract implementation, adjudicated fixture construction, isolated GX-10 calibration, and comparison-only enterprise compatibility testing. It does not authorize workflow scheduling, report changes, deployment, or A100 production promotion.

## Implementation evidence

The candidate identity, dedicated specification, prompt, role schema, rubric, candidate workflow, model manifest, deterministic projection, reference runner, and eight targeted negative/immutability tests are implemented. An adjudicated `CAP-RISK` plus `CAP-REQ` fixture set produces a hash-bound coordinator manifest and comparison-only candidate artifact with five preserved records and one explicitly sourced cross-domain assertion. Its evidence tier is `adjudicated_multi_domain_contract_fixture` and its fitness claim is `contract_fixture_only`.

The structural validator and all 47 tests pass locally and on the GX-10 DGX Spark-equivalent platform. The deterministic reference candidate is byte-identical across platforms with file SHA-256 `19c1148b74cbb4d64d4c8fd401c741bb75bb806b3118c1849a8a2edfbb061f6f`. The GX-10 conformance transcript has SHA-256 `a43be4fcd02cee6cfe2478f558d1dd3d6181d4059d45767047a74a244615a0f5`; the GX reference archive has SHA-256 `321ae4279ddc61f01db3a3c2b459b1dfc9fed5cf0a3097c3f98c8fd67246dffe`.

An isolated live Qwen3-32B run against the sole accepted `CAP-RISK` artifact passed schema, manifest, protocol, exact-lineage, human-authority, and comparison-only validation. It used 3,130 input tokens and 855 output tokens. Its evidence tier is `accepted_live_input_calibration`, but its mandatory fitness claim is only `protocol_lineage_smoke_only`. The retained live summary has SHA-256 `63ca45f9d5aa40922f7f519eb371f3de9cba3228db9cf8fc3daf406681587791`; the live evidence archive has SHA-256 `8b67c30143db2e55b04dbe88e093877e69298a93746f23477d403929c1c4f343`.

`CAP-SYNTH` remains unscheduled. No accepted workflow, report, governance record, deployment configuration, or A100 production baseline changed.

## Remaining promotion dependency

A second accepted live capability-review domain is required before multi-domain live calibration can begin. Adjudicated fixtures and the passing single-domain smoke run cannot satisfy that dependency. A later scheduling decision still requires accepted live multi-domain inputs, human semantic review, enterprise-consumer compatibility, full regression, and rollback rehearsal.
