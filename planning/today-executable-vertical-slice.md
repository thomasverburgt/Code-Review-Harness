# Today's Work: Executable Agent Vertical Slice

- **Date:** 2026-07-31
- **Status:** Live vertical completed and validated on GX-10
- **Primary objective:** Prove the Code Review Harness contracts and orchestration through one deterministic, end-to-end execution path before expanding the platform.
- **Reference chain:** `SPEC-SECRETS -> PROD-SEC -> CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK -> human decision request`

## Decision

Build the smallest executable harness slice that proves orchestration and contract behavior across specialist, product, capability, and enterprise layers.

This work precedes broad harness services, user interfaces, production integrations, deployment scaling, and additional prompt expansion. The slice must expose incorrect assumptions while schemas, state transitions, routing rules, and agent boundaries are still inexpensive to change.

## Work sequence

### 1. Executable contracts and reference workflow

**Status:** Completed

Deliver:

- additive artifact schemas for specialist, product, capability, and enterprise layers;
- role-extension schemas for `SPEC-SECRETS`, `PROD-SEC`, `CAP-RISK`, and `ENT-SYSRISK`;
- schemas for dispatch envelopes, workflow definitions, dependency state, gate results, audit events, partial-input authorization, routing results, and human decision requests;
- a declarative, acyclic dependency graph and policy for the reference chain;
- explicit state-transition definitions for `ORCH-SCHED`, `ORCH-FANOUT`, and `ORCH-FANIN`;
- one complete reference workflow with pinned identity, contract, prompt, rubric, policy, schema, model, and tool versions; and
- example artifacts showing the expected handoff at every layer.

Exit criteria:

- every example artifact validates against the universal schema and its applicable extensions;
- UUID/designation and version mismatches fail closed;
- every derived assertion preserves its contributing artifact and evidence identifiers;
- the workflow graph is acyclic and declares every prerequisite and consumer;
- normative lifecycle states remain `complete`, `incomplete_input`, `failed`, or `superseded`; and
- every decision request names a human authority.

### 2. Minimal orchestration runner

**Status:** Completed for the deterministic reference runner

Deliver:

- deterministic identity and version resolution;
- workflow and policy loading;
- prerequisite scheduling;
- bounded fan-out dispatch;
- fan-in validation for schema, integrity, lineage, freshness, completeness, conflicts, CAPA, and partial-input authority;
- immutable artifact routing;
- retry, timeout, failure, escalation, and supersession handling;
- deterministic audit events; and
- replay from pinned inputs and configuration.

Exit criteria:

- the four-agent chain can execute or be simulated from one signed workflow definition;
- invalid identity, schema, integrity, dependency, or policy state stops downstream scheduling;
- authorized partial execution remains visibly `incomplete_input` through every consumer;
- parallel or repeated execution does not mutate source artifacts; and
- replay produces equivalent routing, validation, and audit outcomes.

### 3. Gold-package evaluation and failure testing

**Status:** Completed for the baseline fixture suite

Deliver:

- one adjudicated success package;
- negative fixtures for missing input, inaccessible evidence, stale evidence, bad hashes, schema incompatibility, UUID/designation mismatch, incompatible versions, undeclared dependency, graph cycle, unresolved conflict, incomplete CAPA, restricted-data leakage, and unauthorized partial input;
- expected gate, lifecycle, routing, escalation, and decision-request results for every fixture; and
- repeatability and regression checks.

Exit criteria:

- positive and negative paths produce their adjudicated outcomes;
- no failure is represented as a complete assessment;
- source artifact identifiers and meanings survive every layer;
- authority violations are rejected;
- results are reproducible from retained inputs and version pins; and
- observed gaps are converted into contract, schema, workflow, or implementation changes with traceable rationale.

### 4. Broader harness services

**Status:** Sequenced; implementation is a later increment

Use the slice results to design and prioritize:

- artifact persistence and indexing;
- evidence storage and least-privilege retrieval;
- workflow operations, monitoring, and recovery;
- human review and decision-record interfaces;
- dashboards and reporting;
- policy administration;
- prompt, rubric, contract, and model version management; and
- operational security and observability.

Do not commit to a broad platform shape until the reference slice identifies the actual runtime, storage, validation, and operator requirements.

### 5. Agent expansion, integrations, and deployment

**Status:** Sequenced; implementation is a later increment

Proceed in this order:

1. add production prompts and role schemas for additional agents;
2. add representative workflows for additional product, capability, and enterprise concerns;
3. implement GitLab, Platform Factory, ServiceNow, and release-management integrations;
4. implement the A100 large-cluster Kubernetes deployment and DGX Spark-equivalent test-environment designs, including model serving, storage, scaling, GPU allocation, and promotion evidence; and
5. validate throughput, resilience, security, rollback, and operational support before wider release.

## Today's operating constraints

- Execute all development, regression, calibration, integration, security, resilience, rollback, and performance test suites on NVIDIA DGX Spark or an approved equivalent; reserve the A100 large cluster for production deployment verification and operations.
- Prefer one complete, replayable path over broad partial implementation.
- Treat prompts as versioned implementations of contracts, not as standalone prose.
- Treat schemas and validation behavior as executable architecture.
- Preserve immutable artifacts and stable identifiers across every boundary.
- Do not silently repair, merge, reinterpret, or promote invalid inputs.
- Keep agent recommendations separate from human decisions.
- Record assumptions and unresolved design choices instead of hiding them in code.
- Add an ADR for any material platform, orchestration, persistence, identity, integrity, or governance decision.

## Today's completion evidence

Completed deliverables:

- layer-extension schemas in `appendices/schemas/*-extension.schema.json`;
- role schemas for `SPEC-SECRETS`, `PROD-SEC`, `CAP-RISK`, `ENT-EVIDENCE`, and `ENT-SYSRISK`;
- workflow, dispatch, gate-result, audit-event, human-decision-request, and state-machine schemas;
- `appendices/example-workflows/vertical-risk-slice.workflow.json`;
- `appendices/policy-examples/vertical-risk-slice.policy.json`;
- explicit state machines for `ORCH-SCHED`, `ORCH-FANOUT`, and `ORCH-FANIN`;
- five immutable gold artifacts and one human decision request under `fixtures/vertical-risk-slice/gold`;
- fifteen negative cases under `fixtures/vertical-risk-slice/negative`;
- `tools/validate_vertical_slice.py`, `tools/run_vertical_slice.py`, and `tools/test_vertical_slice.py`; and
- ADR 0007 documenting extension composition and the explicit `ENT-EVIDENCE` node.

Validated results:

- universal, layer, role, workflow, state-machine, and decision-request validation passed;
- the workflow contains five registered, UUID-matched nodes and is acyclic;
- all five gold artifacts preserve cross-layer lineage and declared hashes;
- fifteen of fifteen negative cases fail for their adjudicated reason;
- complete, authorized `incomplete_input`, retry-success, timeout-failure, and supersession-failure runtime scenarios match expected outcomes;
- deterministic replay produces byte-identical output files; and
- the final result routes one decision request to `enterprise-risk-acceptance-authority`.

Execution commands:

```powershell
python tools/validate_vertical_slice.py
python tools/test_vertical_slice.py
python tools/run_vertical_slice.py --output-dir <run-directory>
```

Design discovery:

- The four selected review prompts are not the complete executable enterprise path. `ENT-EVIDENCE` is a required explicit fifth node and cannot be silently replaced by `ORCH-FANIN`.
- The formal machine composition uses `extensions.<layer>.role`, superseding provisional prompt placement recommendations while retaining their semantic fields.

Next-session entry point:

Increment 2 now has a complete live reference vertical on the approved GX-10/DGX Spark-equivalent platform, including the deterministic ENT-EVIDENCE gate and canonical ENT-SYSRISK projection. Begin Increment 3 with the immutable human-decision record and governance interface boundary; do not fold human disposition into the agent artifact or model output.

The dependent implementation increments are sequenced in [Post-Vertical-Slice Implementation Sequence](post-vertical-slice-sequence.md).
