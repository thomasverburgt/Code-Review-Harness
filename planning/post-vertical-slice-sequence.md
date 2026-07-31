# Post-Vertical-Slice Implementation Sequence

- **Baseline dependency:** `WF-VERTICAL-RISK-001` conformance suite remains green.
- **Sequencing rule:** Do not weaken universal, layer, role, lineage, lifecycle, integrity, partial-input, or human-authority invariants to accelerate a later increment.

## Increment 1: Persistent artifact and execution ledger

Depends on: validated schemas, deterministic runner, stable audit-event shape.

**Status:** Complete. Reference implementation and GX-10/DGX Spark-equivalent conformance execution passed; ADR 0009 accepted by the project maintainer on 2026-07-31.

Implement:

- immutable artifact object storage;
- metadata and traceability index;
- workflow, dispatch, gate, audit, routing, decision-request, and supersession records;
- canonical hashing and attestation;
- retention and access classification; and
- deterministic replay from retained input references and version pins.

Exit criteria:

- a gold run can be persisted, reloaded, revalidated, and replayed without changing identifiers or meaning;
- append-only audit ordering is deterministic;
- superseded artifacts remain retrievable and linked; and
- unauthorized mutation and access fail closed.

Completion evidence:

- `fixtures/vertical-risk-slice/evidence/gx10-conformance-2026-07-31.txt` records successful structural validation, all 15 negative cases, all five runtime scenarios, deterministic replay, persistence, idempotency, integrity, access-control, audit-chain, and supersession checks on the approved GX-10 test platform.

## Increment 2: Worker execution and model/tool adapters

Depends on: Increment 1.

**Status:** Complete for the reference vertical. ADR 0010 and rollback-qualified ADR 0011 are accepted. The deterministic envelope, versioned canonical contracts, assembly records, telemetry pins, fail-closed disclosure limits, and retained `full_artifact` rollback mode pass GX-10 conformance. SPEC-SECRETS, PROD-SEC, CAP-RISK, the deterministic ENT-EVIDENCE gate, and ENT-SYSRISK now pass as one live chain with exact immutable lineage and human-only risk disposition.

Implement:

- queue and worker boundaries;
- model-serving adapter with pinned model/configuration;
- least-privilege evidence/tool adapters;
- timeout, retry, cancellation, and idempotency controls;
- prompt/rubric/tool version resolution; and
- resource, cost, and execution telemetry.

Exit criteria:

- the four designed review prompts can replace adjudicated fixture artifacts one node at a time;
- model output cannot bypass fan-in validation;
- retries do not duplicate or mutate accepted artifacts; and
- failure and resource telemetry preserve execution lineage.

Completion evidence to date:

- `fixtures/vertical-risk-slice/evidence/gx10-increment2-conformance-2026-07-31.txt` records successful one-node fixture-backed execution for all four designed prompts, fan-in bypass rejection, ledger publication, retry/idempotency, timeout, cancellation, least-privilege access, telemetry lineage, authenticated vLLM protocol behavior, and a live `qwen3-32b` smoke response.
- The remaining calibration gate must evaluate actual model-generated contract artifacts for each candidate prompt; fixture-backed adapter success is not represented as prompt-quality evidence.
- `fixtures/vertical-risk-slice/evidence/live-prompt-calibration-2026-07-31/` records four live `qwen3-32b` passes using redacted evidence from a clean, read-only `uds-core` clone. The passes localized request-size, truncation, lineage, schema-shape, grammar-compatibility, and full-schema timeout failures while confirming fail-closed publication behavior.
- `fixtures/vertical-risk-slice/evidence/adr11-role-payload-2026-07-31/` records the passing dual-mode/rollback conformance gate and the failed targeted role-payload calibration attempts. No live payload reached assembly and no live artifact was published.
- `fixtures/vertical-risk-slice/evidence/canonical-spec-secrets-2026-07-31/` records the passing topology-reduced SPEC-SECRETS run: 872 output tokens, deterministic projection, complete lifecycle, final fan-in acceptance, and retained payload/assembly/telemetry lineage.
- `fixtures/vertical-risk-slice/evidence/canonical-prod-sec-2026-07-31/` records the passing canonical PROD-SEC run against that accepted specialist artifact: 1,230 output tokens, exact upstream lineage, deterministic product projection, and final fan-in acceptance.
- `fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/` records the passing canonical CAP-RISK run against the accepted product artifact: 1,790 output tokens, deterministic capability-risk projection, exact upstream lineage, and human-only risk authority.
- `fixtures/vertical-risk-slice/evidence/canonical-ent-sysrisk-2026-07-31/` records the passing enterprise increment: deterministic ENT-EVIDENCE replay, strict CAP-RISK/gate binding, 1,633-token live ENT-SYSRISK generation, deterministic enterprise projection, complete lifecycle, and preserved human-only disposition authority.

## Increment 3: Human review and governance interfaces

Depends on: Increment 1; may proceed in parallel with late Increment 2 work.

Implement:

- decision inbox and evidence viewer;
- immutable human dispositions;
- risk, exception, CAPA, release, and promotion gates;
- conflict and partial-input presentation;
- role-based access; and
- decision due-date, escalation, and aging views.

Exit criteria:

- every agent decision request reaches a named authority;
- human decisions remain separate linked records;
- the interface cannot represent recommendations as approvals; and
- conflict, confidence, coverage, and evidence limits remain visible.

## Increment 4: Agent and workflow expansion

Depends on: Increments 1-3 and calibrated gold packages.

Sequence:

1. complete product synthesis roles and schemas;
2. complete capability coordination/synthesis roles and schemas;
3. add enterprise architecture, governance, strategic scoring, and synthesis workflows;
4. add remaining specialist concerns according to risk-based policy; and
5. add work agents only where bounded delegation measurably improves throughput or quality.

Exit criteria for each added role:

- registered baseline or candidate identity;
- approved prompt, rubric, layer extension, role schema, dependencies, consumers, gold package, negative cases, and human gate;
- no regression in protected invariants; and
- downstream compatibility demonstrated before scheduling promotion.

## Increment 5: External integrations

Depends on: stable artifacts, execution ledger, human decisions, and operational security controls.

Sequence:

1. GitLab repository and merge-request evidence ingestion;
2. GitLab CI/CD and Platform Factory workflow triggers;
3. ServiceNow risk, change, CAPA, and decision-record integration;
4. release-management handoff; and
5. approved runtime, Kubernetes, document, and telemetry evidence connectors.

Exit criteria:

- integrations exchange references and immutable records without becoming an authority bypass;
- retries and webhook replay are idempotent;
- credentials and restricted evidence remain least privilege; and
- external outages preserve recoverable workflow state.

## Increment 6: Production deployment and scaling

Depends on: Increments 1-5 and approved deployment ADRs.

Implement:

- Kubernetes control and worker planes;
- A100 large-cluster/vLLM production model-serving topology;
- DGX Spark or approved-equivalent test topology for all development, regression, calibration, integration, security, resilience, rollback, and performance test execution;
- GPU allocation, batching, concurrency, and backpressure;
- highly available storage and queueing;
- secrets, identity, network, supply-chain, and runtime security;
- observability, capacity, cost, backup, restore, disaster recovery, and rollback; and
- staged environments with promotion controls.

Exit criteria:

- throughput and latency meet declared workload objectives without violating deterministic controls;
- failure, recovery, scaling, security, rollback, and performance test suites pass on DGX Spark or an approved equivalent, with any scaled configuration and hardware limitation recorded;
- A100 deployment smoke checks, health checks, configuration verification, and operational monitoring pass without using the production cluster as the general test environment;
- reviewer calibration and drift monitoring operate in the deployed environment; and
- production promotion is authorized by the named human authorities.

## Continuous cross-cutting work

Across every increment:

- maintain gold packages and negative fixtures;
- run prompt, contract, model, rubric, and tool regression suites;
- measure schema validity, repeatability, evidence fidelity, confidence calibration, false-positive/negative behavior, CAPA quality, and human override patterns;
- record material decisions in ADRs; and
- preserve rollback to the last validated version.
