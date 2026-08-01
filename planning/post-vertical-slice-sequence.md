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

## Increment 3: Report distribution and external decision reconciliation

Depends on: Increment 1; may proceed in parallel with late Increment 2 work.

**Status:** Complete for the reference vertical. ADR 0012 was accepted by the project maintainer on 2026-07-31. The previously tested direct in-system decision candidate is superseded and retained only as design evidence. The accepted implementation packages the complete report, controls leadership-review and approved-distribution exports, records external distribution and expert decisions through authenticated administrators, requires independent verification, and keeps all effects record-only. The full five-gate local and GX-10 conformance suites pass.

Implement:

- immutable report package and controlled exports;
- external leadership distribution-approval attestation;
- external expert-decision attestation and exact report-item reconciliation;
- independent records verification;
- conflict and partial-input presentation;
- role-based access; and
- immutable, derived governance-state views.

Exit criteria:

- every distributed report is bound to its exact technical sources and approval record;
- decision-maker, recorder, and verifier identities remain separate;
- external decisions remain separate linked records with hashed sources;
- the interface cannot represent recommendations, review exports, or administrative entry as approval; and
- conflict, confidence, coverage, and evidence limits remain visible.

Completion evidence:

- `fixtures/vertical-risk-slice/evidence/governance-increment3-report-reconciliation-2026-07-31/` records the passing GX-10 five-gate run, deterministic report/export/attestation chain, independent verification, reconciliation view, and immutable ledger.

## Increment 4: Reproducible evidence localization and expert-review packets

Depends on: Increments 1-3.

**Status:** Complete. ADR 0013 was accepted by the project maintainer on 2026-07-31. The executable evidence-locator and expert-review-packet boundary passes the complete six-gate local and GX-10 suites without changing the ADR-0012 report package or hash.

Implement:

- immutable repository, revision, path, line/section, fingerprint, access, and reproduction locators;
- explicit evidence bindings for every finding, risk, CAPA, and recommendation;
- a separately hashed expert-review packet and human-readable evidence annex;
- safe redaction without loss of source location; and
- fail-closed reviewability when evidence cannot be reproduced.

Exit criteria:

- every actionable report item resolves to at least one exact `source_located` locator;
- the approved technical report and package hash remain unchanged;
- missing, ambiguous, mutable, unsafe, or altered locations fail closed;
- deterministic packet and annex generation passes local and GX-10 conformance; and
- the packet cannot express distribution approval, expert disposition, risk acceptance, or change authorization.

Completion evidence:

- `fixtures/vertical-risk-slice/evidence/evidence-locator-increment4-2026-07-31/` retains the deterministic packet, human-readable annex, GX-10 six-gate output, and GX-generated reference archive.
- Seven actionable report items resolve through explicit bindings to two lineage-preserving evidence identities and one exact `uds-core` source location at commit `329ade01852f9e570d31cb7b19d9979152938c17`, file `docs/getting-started/local-demo/integrate-your-package.mdx`, line 153.
- Missing, unverified, mutable-revision, path-traversal, reversed-line, changed-hash, incomplete-binding, and altered-direct-reference cases fail closed.

## Increment 5: Agent and workflow expansion

Depends on: Increments 1-3 and calibrated gold packages.

**Status:** In progress. ADR 0014 was accepted by the project maintainer on 2026-07-31, authorizing `PROD-SYNTH` candidate validation and live-model calibration while explicitly withholding baseline scheduling authority. Identity, prompt integrity, executable role schema, gold/negative packages, deterministic replay, and `CAP-RISK` handoff compatibility pass locally and on GX-10. A first live response failed closed on an invented universal-record binding; after adding an explicit runtime allow-list without weakening validation, the second live `qwen3-32b` run produced an accepted candidate artifact. The baseline workflow remains unchanged and a later promotion decision remains the scheduling gate.

Increment 5 evidence to date:

- `fixtures/product-synth-admission/evidence/2026-07-31/` retains the deterministic candidate/handoff package and GX-10 output.
- `fixtures/product-synth-admission/evidence/2026-07-31/live-calibration/` retains the failed-closed first-attempt summary, successful live artifact, complete output archive, and eight-gate GX-10 transcript.
- The direct `PROD-SEC -> CAP-RISK` route remains active and is the tested rollback path.
- ADR 0015 was accepted on 2026-07-31 and authorizes isolated shadow integration before any baseline cutover. Shadow artifacts remain comparison-only and cannot enter report, governance, deployment, or authoritative baseline state.
- ADR 0015 implementation completed its deterministic and model-backed GX-10 shadow increment. The live comparison is blocked on human adjudication of CAP-RISK semantic differences, so the accepted baseline remains unchanged and no cutover ADR should be proposed until those differences are resolved.
- ADR 0016 was accepted on 2026-08-01. Its immutable, record-only semantic adjudication packet separates expert semantic judgment from later project-maintainer workflow promotion and keeps cutover blocked pending an external enterprise-risk response.
- ADR 0017 was accepted and its deterministic `CAP-COORD` increment completed on 2026-08-01. Exact-set validation, immutable manifest/ledger generation, traceability, conflict preservation, partial-input blocking, and CAP-SYNTH dispatch gating pass the structural validator and all 39 tests locally and on GX-10. The initial `CAP-RISK`-only evidence is mechanical calibration, not multi-domain synthesis fitness; `CAP-SYNTH` remains planned and unscheduled.
- The next capability-layer increment is `CAP-SYNTH` candidate admission: identity/specification, prompt, role schema, rubric, deterministic projection, gold/negative packages, exact coordinator-manifest binding, enterprise-consumer compatibility, and GX-10 calibration. It must not schedule the candidate or alter the accepted direct enterprise/report path.
- ADR 0018 was accepted and implemented on 2026-08-01. CAP-SYNTH candidate identity, prompt, schema, rubric, projection, adjudicated multi-domain fixtures, negative cases, exact CAP-COORD binding, comparison-only enterprise handoff, and isolated live calibration pass all 47 tests locally and on GX-10. The live `CAP-RISK`-only Qwen3-32B run passed as `protocol_lineage_smoke_only`; CAP-SYNTH remains unscheduled.
- ADR 0019 was accepted and implemented on 2026-08-01. CAP-REQ candidate contracts, immutable source/locator binding, honest zero-population semantics, negative cases, CAP-COORD compatibility, and live Qwen3-32B calibration pass all 55 tests locally and on GX-10. The technically valid artifact remains pending human requirements acceptance; CAP-SYNTH remains unscheduled.
- ADR 0020 was accepted on 2026-08-01. The increment implements an immutable review packet bound to the retained live GX-10 CAP-REQ artifact, an external requirements-authority response, independent record verification, and deterministic rollback-safe eligibility. No external disposition has been supplied, so CAP-REQ remains blocked from accepted multi-domain use and CAP-SYNTH remains unscheduled.
- ADR 0021 was accepted and implemented on 2026-08-01. Enterprise registry status now matches executable reality: `ENT-EVIDENCE` and `ENT-SYSRISK` remain baseline, `ENT-ARCH` is candidate, and the other prose-only enterprise roles are planned. Exact gate/input binding, strict schema/projection controls, negative cases, deterministic two-capability contract fixtures, and live single-capability Qwen3-32B protocol calibration pass all 72 tests locally and on GX-10. ENT-ARCH remains unscheduled, the ADR-0020 gate was not bypassed, and accepted workflow/report state is unchanged.
- ADR 0022 was accepted and implemented on 2026-08-01. `ENT-GOV` is now an isolated, unscheduled candidate whose sole obligation entry point is a content-addressed governance-source manifest controlled by a registered human authority. Exact source, applicability, gate, capability, exception, and approval bindings; strict schemas; complete obligation-to-capability matrices; fail-closed negative cases; deterministic replay; and live single-capability Qwen3-32B source/protocol calibration pass all 82 tests locally and on GX-10. Missing evidence remains `insufficient_evidence`, no compliance or exception authority was created, and the accepted baseline, report, ADR-0020 state, CAP-SYNTH schedule, and ENT-ARCH schedule remain unchanged.
- ADR 0023 was accepted and implemented on 2026-08-01. `ENT-STRAT` is now an isolated, unscheduled candidate behind human-controlled strategic-objective and scoring-method manifests. Exact authority, objective, method, gate, posture, evidence-tier, missingness, and weight bindings; strict schemas; fail-closed mutations; deterministic replay; and live single-domain Qwen3-32B protocol calibration pass all 92 tests locally and on GX-10. The authorized method prohibits a composite score, missing evidence is not imputed, and accepted workflow, report, ADR-0020 state, ENT-ARCH schedule, and ENT-GOV schedule remain unchanged.
- ADR 0024 was accepted and implemented on 2026-08-01. `ENT-SYNTH` is now an isolated, unscheduled candidate behind an exact tiered synthesis-input manifest. Domain-role snapshots and contribution maps preserve source authority; candidate and fixture inputs remain comparison-only; report packaging, distribution approval, expert decisions, and administrative recording remain separate. All 102 tests pass locally and on GX-10, and the live Qwen3-32B mixed-tier run passed as protocol/lineage evidence only without changing the accepted report, distribution state machine, baseline, or candidate schedules.
- ADR 0025 was accepted and implemented on 2026-08-01. The deterministic enterprise-shadow readiness manifest records six exact prerequisites and is `blocked_as_designed`: ADR-0016 and ADR-0020 await verified external decisions, while ENT-ARCH, ENT-GOV, ENT-STRAT, and ENT-SYNTH lack accepted-live multi-domain semantic evaluations. Zero prerequisites are satisfied, no protocol or fixture evidence is promoted, rollback is explicit, and the accepted route remains unchanged. All 110 tests and structural validation pass locally and on GX-10.
- ADR 0026 was accepted and implemented on 2026-08-01. The immutable human readiness action dossier binds all six prerequisites to the exact ADR-0025 manifest. Two existing packets await separate external responses; four domain evidence-gap packets remain `not_ready_for_review` and reject premature responses. Dossier-level and batch approval are prohibited, independent verification remains mandatory, and no readiness, scheduling, report, or deployment state changes. All 118 tests and structural validation pass locally and on GX-10.

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

## Increment 6: External integrations

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

## Increment 7: Production deployment and scaling

Depends on: Increments 1-6 and approved deployment ADRs.

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
