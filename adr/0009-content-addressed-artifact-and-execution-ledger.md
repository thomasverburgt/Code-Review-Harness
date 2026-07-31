# ADR-0009: Content-Addressed Artifact and Execution Ledger

- **Status:** Accepted
- **Date:** 2026-07-31
- **Decision authority:** project maintainer
- **Owners:** harness architecture and orchestration
- **Scope:** Increment 1 persistence reference implementation
- **Decision record:** Project maintainer concurrence, 2026-07-31

## Context

The deterministic runner proves contracts and routing but writes disposable files. Increment 1 requires immutable artifact storage, metadata and traceability indexes, append-only audit ordering, supersession records, retention/access metadata, and replay from retained references without weakening the vertical-slice invariants.

## Decision

Use canonical JSON content addressed by SHA-256 as the persistence primitive. Bind stable record IDs and execution IDs to immutable object hashes through write-once indexes. Represent an execution with a versioned manifest over the workflow, source artifacts, schedule, dispatches, gates, audit events, routing, decision request, and summary.

Hash-chain audit events in deterministic sequence order. Represent supersession as a separate immutable record linking prior and successor artifacts and human authority. Treat replay as verified materialization of retained records, not agent re-execution.

The filesystem implementation is the conformance reference, not the production storage technology. A later production implementation must demonstrate equivalent behavior against the same tests.

## Alternatives considered

- Mutable execution directories were rejected because they cannot prove stable identity or detect record replacement.
- Database-generated identifiers were rejected as the reference semantic because they obscure deterministic fixture identity and portable replay.
- Rewriting an artifact's lifecycle to record supersession was rejected because it violates source-artifact immutability.
- Treating workflow re-execution as replay was rejected because inference or tool execution may introduce new evidence and must produce a new execution record.

## Consequences

- Exact retained content is independently integrity-verifiable.
- Duplicate writes are idempotent, while stable-ID mutation fails closed.
- Traceability and supersession remain queryable without rewriting artifacts.
- Storage is duplicated when semantically equivalent JSON differs canonically; canonicalization rules therefore become a compatibility boundary.
- Production storage must add concurrency control, durable authorization, backup, replication, and operational recovery without changing these semantics.

## Validation

`tools/test_artifact_ledger.py` covers persistence, idempotency, reload verification, semantic replay, mutation rejection, object tampering, audit reordering, supersession retention, and classification denial. It must run on NVIDIA DGX Spark or an approved equivalent under ADR 0008.

The 2026-07-31 GX-10 execution passed this suite together with the vertical-slice structural validator and runtime/negative-case suite. The retained evidence is `fixtures/vertical-risk-slice/evidence/gx10-conformance-2026-07-31.txt` with SHA-256 `965d35d0fa4e69367acb34718e935bae7a0cd2ca1b709dd7ea129559f9659fc1`.

## Unresolved matters

- Production object store, metadata database, queue, transaction, and locking technologies.
- Cryptographic signer and key-management design beyond the reference self-attestation.
- Classification taxonomy and authorization-provider integration.
- Retention schedules, legal hold, backup, restore, replication, and disaster-recovery objectives.
