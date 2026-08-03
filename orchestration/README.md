# Orchestration

Workflow execution, policy evaluation, state machines, fan-out/fan-in behavior, recovery, and related orchestration decisions are maintained here.

ADR-0015 adds `appendices/candidate-workflows/prod-synth-cap-risk-shadow.workflow.json`. It is an isolated comparison workflow: its artifacts use a shadow ledger namespace and cannot enter report publication, governance reconciliation, deployment authorization, or the authoritative baseline without a later cutover ADR.

ADR-0016 adds `state-machines/semantic-adjudication.state-machine.json` and the record-only semantic adjudication runtime. It converts blocked shadow differences into exact external-human review requests while withholding all workflow-promotion authority.

## Executable vertical-slice baseline

- `state-machines/orch-sched.state-machine.json` resolves identity and versions and rejects invalid or cyclic graphs.
- `state-machines/orch-fanout.state-machine.json` validates prerequisites and creates bounded dispatch envelopes.
- `state-machines/orch-fanin.state-machine.json` validates universal, layer, role, integrity, lineage, freshness, conflicts, CAPA, authority, partial-input, and routing state.
- `../appendices/example-workflows/vertical-risk-slice.workflow.json` is the reference workflow.
- `../tools/validate_vertical_slice.py` performs zero-dependency structural and semantic validation.

## Persistent execution baseline

- [Persistent Artifact and Execution Ledger](persistent-artifact-and-execution-ledger.md) defines content-addressed storage, immutable indexes, traceability, audit chaining, supersession, and replay semantics.
- `../tools/artifact_ledger.py` is the zero-dependency filesystem reference implementation.
- `../tools/persist_vertical_slice.py` persists, verifies, and replays retained executions.
- `../tools/test_artifact_ledger.py` is the DGX Spark-equivalent persistence conformance suite.

## Worker and adapter baseline

- [Worker Execution and Model/Tool Adapters](worker-execution-and-adapters.md) defines queue, version resolution, adapter, fan-in, publication, and telemetry behavior.
- `../tools/worker_runtime.py` implements the reference worker, queue, fixture/vLLM model adapters, least-privilege evidence adapter, and contract-gated publication.
- `../tools/test_worker_runtime.py` is the Increment 2 DGX Spark-equivalent conformance suite.

## Report governance baseline

- [Report Governance and External Decision Reconciliation](human-review-and-governance.md) defines immutable report packaging, controlled distribution approval, external decision recording, project-owner finalization, and reconciliation.
- `../tools/report_governance_runtime.py` implements the record-only reference boundary.
- `../tools/test_report_governance_runtime.py` is the Increment 3 DGX Spark-equivalent conformance suite.

## Requirements acceptance boundary

- [CAP-REQ Human Acceptance Contract](../contracts/requirements-acceptance-contract.md) defines the separation among technical validation, requirements acceptance, project-owner finalization, derived eligibility, and scheduling.
- `state-machines/requirements-acceptance.state-machine.json` fails closed from live candidate validation through review, verification, eligibility, and revocation.
- `../tools/requirements_acceptance_runtime.py` emits the exact review packet and validates response and verification records.
- `../tools/test_requirements_acceptance.py` is the ADR-0020 DGX Spark/GX-10 conformance suite. Production remains targeted to the A100 large cluster.
