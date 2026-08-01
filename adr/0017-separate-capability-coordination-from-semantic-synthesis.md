# ADR-0017: Separate Capability Coordination from Semantic Synthesis

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: capability engineering, orchestration, enterprise consumers, report operations, and governance
- Supersedes: none
- Superseded by: none

## Context

Increment 5 next calls for capability coordination and synthesis. The registry already marks `CAP-COORD` as baseline and `CAP-SYNTH` as planned, but the current `CAP-COORD` description combines deterministic fan-in validation, normalization, traceability-manifest publication, cross-domain correlation, capability narrative, and enterprise handoff. That collapses control-plane checks and semantic model judgment into one role, obscuring which outputs are mechanically verified and which are generated assessments.

The accepted worker harness establishes the correct precedent: deterministic code owns identity, schemas, hashes, lineage, completeness, routing, and publication gates; model-backed agents own bounded analytical content. The capability level should preserve that separation.

ADR-0016 semantic adjudication remains an independent blocked path. This proposal neither resolves its deltas nor changes the accepted `PROD-SEC -> CAP-RISK` baseline.

## Evidence

- `CAP-COORD` is registered baseline with an authoritative question that currently includes coherent assessment.
- `CAP-SYNTH` is registered planned without an executable specification, prompt, role schema, or admission package.
- The capability delivery contract requires cross-product mission, requirement, interface, HCD, readiness, risk, confidence, conflict, and escalation fields.
- `ENT-SYNTH` expects capability coordinator synthesis artifacts, creating ambiguity over which role owns semantic posture.
- ADRs 0010, 0011, 0014, and 0015 demonstrate fail-closed separation between deterministic assembly and generated analytical content.

## Decision record

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes implementation and testing of the deterministic `CAP-COORD` manifest boundary followed by unscheduled `CAP-SYNTH` candidate work. It does not schedule `CAP-SYNTH`, resolve ADR-0016 adjudication, change the accepted baseline, alter reports, authorize deployment, or promote the A100 production workflow.

## Decision

1. Define `CAP-COORD` as a deterministic capability fan-in coordinator. It inventories expected inputs, verifies identity/schema/hash/version/freshness/completeness, records partial-input authorization, preserves conflicts, builds the capability traceability manifest, and emits a validated capability-input manifest plus routing state.
2. Prohibit `CAP-COORD` from generating a capability narrative, resolving disagreement, changing child confidence, deriving risk meaning, recommending a course of action, or producing the enterprise semantic handoff.
3. Define `CAP-SYNTH` as the model-backed semantic capability synthesis agent. It consumes the validated coordinator manifest and exact immutable capability-review artifacts, preserves child assertions, derives explicitly sourced cross-domain assertions, reconciles confidence without averaging away disagreement, and produces the capability posture and enterprise handoff.
4. Keep `CAP-SYNTH` unscheduled and candidate-only until identity, prompt, rubric, role schema, gold/negative packages, deterministic projection, downstream enterprise compatibility, local regression, GX-10 calibration, and a separate scheduling decision pass.
5. Retain human-only authority. Neither role may accept risk, approve readiness, select a course of action, alter requirements, approve release, change a report, authorize deployment, or promote the A100 production workflow.
6. Update `ENT-SYNTH` inputs to distinguish the coordinator's validated manifest from `CAP-SYNTH` semantic posture after the candidate contract is proven.

## Proposed data flow

`immutable capability review artifacts -> CAP-COORD deterministic validation manifest -> CAP-SYNTH semantic posture -> enterprise review agents`

On any invalid, missing, unauthorized-partial, stale, incompatible, or malformed/unpreserved conflict input:

`CAP-COORD -> blocked or incomplete manifest -> CAP-SYNTH not dispatched`

## Alternatives considered

- Keep the combined `CAP-COORD` role: rejected because deterministic validation and generated judgment would share one authority surface.
- Remove `CAP-SYNTH`: rejected because semantic synthesis is a distinct planned function required by the hierarchy.
- Let `CAP-SYNTH` validate its own raw fan-in: rejected because a model must not own the gate that authorizes its input set.
- Reclassify `CAP-COORD` as `ORCH-FANIN`: deferred; the capability-specific manifest is a domain record even though its checks reuse orchestration primitives.

## Consequences

The boundary adds one explicit artifact and dispatch gate but improves auditability, replay, negative testing, least privilege, and rollback. `CAP-SYNTH` prompts become smaller and cannot conceal missing inputs. Enterprise consumers receive both mechanical input-quality state and semantic capability posture. Existing broad prose for `CAP-COORD` must be narrowed after acceptance.

## Rollback

Do not register or dispatch `CAP-SYNTH`; retain the current capability roles and direct enterprise inputs. Candidate prompts, schemas, fixtures, and calibration evidence may remain unscheduled for audit. No accepted baseline artifact, report, governance record, or production configuration requires migration.

## Validation

- executable coordinator-manifest and CAP-SYNTH role schemas;
- deterministic fan-in and exact input-set replay;
- failure cases for missing, extra, stale, incompatible, mutated, partial, dropped/altered conflicts, or invented inputs;
- proof that CAP-SYNTH cannot run without an accepted coordinator manifest;
- preserved child findings, risks, evidence, conflicts, confidence provenance, and human authority;
- enterprise handoff compatibility;
- full local and DGX Spark-equivalent regression and calibration; and
- explicit confirmation that the A100 production baseline remains unchanged.

## Implementation evidence

The deterministic `CAP-COORD` boundary is implemented by the capability-input-manifest schema, coordination contract, coordinator specification, runtime, reference runner, and eight targeted fail-closed tests. The first immutable manifest consumes the sole accepted live `CAP-RISK` artifact, preserves `FINDING-001`, `RISK-001`, and `DC-001` traceability, and is explicitly labeled `single_domain_mechanical_calibration` with a `mechanical_coordination_only` fitness claim.

The complete structural validator and 39-test suite pass locally and on the GX-10 DGX Spark-equivalent platform. The local and GX-10 reference manifests are byte-identical (`sha256:b258935593be8c5e1ce8d6016719c0e0302f5f0d3e1a9821c4853c99881ebe30`). The GX-10 transcript is retained with SHA-256 `7e8fb46668766f1fa2e8f881329d56b0dcfa848a7d42a8d9a3b40525e64a0bb6`; the GX-generated evidence archive is retained with SHA-256 `848a510c6d620f67dc0c89c10429722d763314593937736a045c2368318c325c`.

No accepted workflow, report, governance record, deployment configuration, or A100 production baseline was changed. `CAP-SYNTH` remains planned and unscheduled.

## Remaining gate

The next increment may define and test `CAP-SYNTH` as a candidate consumer of the manifest, but the current `CAP-RISK`-only evidence cannot establish multi-domain synthesis fitness. Scheduling still requires accepted artifacts for a declared multi-domain input set, candidate prompt/schema/rubric/projection admission, enterprise handoff compatibility, GX-10 model calibration, human review, and a separate promotion decision.
