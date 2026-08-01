# ADR 0001: Immutable Artifacts Are Authoritative

- **Status:** accepted
- **Date:** 2026-07-24
- **Decision authority:** project maintainer
- **Owners:** architecture governance and harness maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

The harness produces review artifacts, evidence records, findings, risks, CAPAs, patterns, reports, and human decision records that must remain reproducible and auditable. Query indexes, dashboards, search stores, and correlation databases can improve discovery, but they can be rebuilt, reconfigured, or corrupted independently of the evidence they describe.

Without a single authority rule, a mutable index could silently replace the reviewed record, historical results could change after approval, and replay could produce a different evidence graph from the one presented to a human authority.

## Evidence

- Git preserves versioned Markdown and JSON records with reviewable history.
- Content hashes provide deterministic integrity checks for machine artifacts.
- The [Universal Agent Contract](../contracts/universal-agent-contract.md) requires immutable inputs, artifact identity, integrity hashes, retention state, and explicit lineage.
- The [Persistent Artifact and Execution Ledger](../orchestration/persistent-artifact-and-execution-ledger.md) implements content-addressed objects, immutable indexes, audit chaining, supersession, verification, and replay.
- Search and correlation indexes are useful operational projections but do not inherently preserve the complete signed record or its historical context.

## Decision

Git-versioned Markdown and JSON artifacts, together with their retained content-addressed objects and immutable human records, are the authoritative record of review.

Indexes, dashboards, caches, vector stores, databases, and materialized views may accelerate query, navigation, reporting, and correlation. They remain derived projections and must not become the source of truth.

An accepted artifact is never edited in place. Correction or evolution creates a new artifact or decision record linked through explicit supersession, while the prior record remains retained. A derived index must be reproducible from authoritative artifacts and must preserve their IDs, hashes, versions, lineage, lifecycle, and authority state.

## Alternatives considered

- **Use a database as the sole authoritative record:** rejected because mutable operational state can obscure review history and weaken repository-based inspection and replay.
- **Permit in-place correction of accepted artifacts:** rejected because it changes the evidence that supported earlier assessments and decisions.
- **Treat Git and operational indexes as co-equal authorities:** rejected because disagreement would have no deterministic resolution rule.
- **Avoid indexes entirely:** rejected because immutable authority does not preclude efficient derived search, correlation, or reporting.

## Consequences

- Every authoritative artifact requires stable identity, integrity, retention, and lineage metadata.
- Storage and audit history grow because accepted records are superseded rather than overwritten.
- Indexes must expose source artifact references and be rebuildable from retained records.
- A query result is not independently authoritative; consumers must be able to resolve it back to the exact artifact.
- Backup, migration, replay, and disaster-recovery procedures must protect authoritative artifacts before derived stores.

## Traceability

- [Universal Agent Contract](../contracts/universal-agent-contract.md)
- [Evidence Contract](../contracts/evidence-contract.md)
- [Persistent Artifact and Execution Ledger](../orchestration/persistent-artifact-and-execution-ledger.md)
- [ADR 0009: Content-Addressed Artifact and Execution Ledger](0009-content-addressed-artifact-and-execution-ledger.md)
- `tools/artifact_ledger.py`

## Validation

- Mutation of an existing content-addressed object or immutable index is rejected.
- Artifact and decision hashes reproduce from canonical content.
- Retained executions can be verified and replayed without relying on a mutable query index.
- Rebuilt indexes resolve to the same authoritative artifact IDs and hashes.
- Supersession preserves both the previous and successor records and the authority for the transition.

## Unresolved matters

- Production retention periods and archival storage classes for each artifact classification.
- Disaster-recovery objectives for the authoritative ledger and Git repository.
- Which operational indexes will be deployed and how often each is rebuilt and reconciled.
