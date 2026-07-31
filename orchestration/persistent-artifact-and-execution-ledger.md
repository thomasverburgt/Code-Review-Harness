# Persistent Artifact and Execution Ledger

## Purpose

The reference ledger turns a deterministic vertical-slice run into immutable, reloadable architecture evidence. It preserves the runner as the conformance oracle while placing persistence behind the existing workflow, artifact, dispatch, gate, audit, routing, and human-decision contracts.

The filesystem implementation in `tools/artifact_ledger.py` is a semantic reference. A production object store, database, or event service may replace it only if it preserves the same immutability, hashing, ordering, access, replay, and failure behavior.

## Storage model

```text
ledger/
  objects/sha256/<prefix>/<digest>.json
  indexes/<record-family>/<stable-id>.json
  indexes/traceability/<artifact-id>.json
  executions/<execution-id>.json
```

Objects are canonical JSON addressed by SHA-256. An identity index binds a stable record ID to exactly one object hash. Repeating the same write is idempotent; attempting to bind that ID to different content fails closed. Execution pointers bind an execution ID to one immutable manifest.

The execution manifest retains:

- workflow definition and version;
- source artifacts;
- schedule, dispatch, gate, routing, summary, and decision-request records;
- individually addressed audit events;
- classification and retention metadata;
- the audit-ledger object and final chain hash; and
- a content-addressed self-attestation.

## Traceability

Each retained agent artifact receives a traceability index containing its stable ID, type, producer, lifecycle, object hash, parent/child/peer links, input references, and declared consumers. Supersession is a separate immutable record that links the prior and successor artifact IDs and hashes with the human authority, time, and reason. Neither artifact is rewritten.

## Audit ordering

Audit events retain their schema-valid event IDs and deterministic sequence numbers. The ledger hashes each event, then constructs a chain entry containing the event hash and prior chain hash. Verification rejects missing objects, noncontiguous ordering, predecessor changes, event mutation, or a mismatched chain head.

## Replay semantics

Ledger replay means materializing the retained workflow and records from verified object hashes. It does not invoke agents or reinterpret evidence. A separately requested workflow re-execution is a new execution with a new execution ID and may be compared with the retained record through normal conformance checks.

## Inputs and outputs

Persistence inputs are a completed reference-run directory, the pinned workflow, immutable source artifacts, execution identity, classification, retention metadata, and the ADR-0008 environment record carried by the schedule and dispatch envelopes.

Outputs are content-addressed objects, immutable identity and traceability indexes, one execution manifest and pointer, a hash-chained audit ledger, and replayed JSON records when requested.

## Failure behavior

The ledger fails closed on:

- stable-ID reuse with different content;
- execution-ID reuse with a different manifest;
- missing or mutated content-addressed objects;
- invalid or reordered audit chains;
- self-supersession or a supersession referencing an unknown artifact;
- access above the caller's declared clearance; or
- replay into a nonempty directory.

## Reference commands

Run these commands only on NVIDIA DGX Spark or an approved equivalent test platform:

```powershell
python tools/run_vertical_slice.py --output-dir <run-dir> --ledger-dir <ledger-dir>
python tools/persist_vertical_slice.py --ledger-dir <ledger-dir> verify --execution-id <execution-id>
python tools/persist_vertical_slice.py --ledger-dir <ledger-dir> replay --execution-id <execution-id> --output-dir <replay-dir>
python tools/test_artifact_ledger.py
```

The default runner environment record is a deterministic DGX Spark reference target. It is metadata for the conformance fixture and does not claim that a non-approved workstation executed the suite or that the fixture measures A100 capacity.
