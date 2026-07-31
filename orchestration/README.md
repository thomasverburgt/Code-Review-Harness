# Orchestration

Workflow execution, policy evaluation, state machines, fan-out/fan-in behavior, recovery, and related orchestration decisions are maintained here.

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
