# ADR-0029: Separate Reusable Fixtures from Retained Evidence

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: evidence-governance, test, and harness maintainers
- Supersedes: none
- Superseded by: none

## Context

The `fixtures` tree contains both reusable test material and immutable evidence retained from local and GX-10 executions. Some fixture artifacts are copied into multiple self-contained scenarios. Some evidence packages also contain identical bytes by design. Path uniformity and byte deduplication cannot be allowed to weaken scenario replay or evidence retention.

## Evidence

- Eleven scenario roots contain reusable inputs, expected results, and 228 legacy evidence files.
- Evidence layouts include both dated ADR directories and older descriptive paths.
- Exact duplicate artifacts occur across reusable scenarios and self-contained retained packages.
- ADRs 0001, 0002, and 0009 require immutable authority, preserved lineage, and content-addressed verification.

## Decision

1. Reserve `fixtures` for reusable synthetic or bounded test material and expected results.
2. Reserve the top-level `evidence` directory for future immutable execution, review, response, verification, and calibration packages.
3. Use `evidence/YYYY-MM-DD/adrNNNN/<scenario>/<run-id>` as the canonical future package layout.
4. Require every future package to contain or reference an evidence manifest with package identity, source revision, environment, artifact hashes, authority state, retention class, and supersession information.
5. Index all existing `fixtures/*/evidence` packages in place. They are legacy evidence paths, not reusable fixtures, and are not moved or rewritten by this sprint.
6. Maintain a deterministic legacy-path map and package inventory hashes so consumers can distinguish a retained snapshot from a living status projection.
7. Create a content-addressed index for exact reusable-fixture duplicates outside evidence paths. The index may nominate a canonical source for future reuse, but existing scenario copies remain until replay and compatibility gates approve their replacement.
8. Do not deduplicate self-contained immutable evidence merely because its bytes match another package.

## Alternatives considered

- **Move every evidence package immediately:** rejected because recorded paths and external review references would change at once.
- **Keep fixtures and evidence permanently mixed:** rejected because mutability and retention obligations remain ambiguous.
- **Deduplicate every identical file:** rejected because independent evidence packages may intentionally retain identical content.
- **Use symbolic links for shared fixtures:** rejected because cross-platform packaging, archival, and Windows behavior would complicate replay.

## Consequences

- New evidence has one predictable root and path convention.
- Legacy packages remain visible but explicitly classified and inventory-hashed.
- Reusable duplicates can later become content-addressed references without changing evidence retention.
- The repository temporarily retains duplicate bytes while compatibility is validated.
- Living state continues under `status`, not inside creation-time evidence packages.

## Traceability

- [ADR 0001: Immutable Artifacts Are Authoritative](0001-immutable-artifacts-are-authoritative.md)
- [ADR 0002: Evidence Is Never Rewritten by a Parent](0002-evidence-is-never-rewritten-by-a-parent.md)
- [ADR 0009: Content-Addressed Artifact and Execution Ledger](0009-content-addressed-artifact-and-execution-ledger.md)
- [ADR 0027: Govern Repository Artifact Lifecycles](0027-govern-repository-artifact-lifecycles.md)
- [Fixtures Index](../fixtures/README.md)
- [Evidence Index](../evidence/README.md)

## Validation

- Artifact catalogs regenerate deterministically and remain clean under `--check`.
- Every indexed legacy root exists and reproduces its inventory hash.
- Content-addressed reusable-fixture groups contain only existing paths with matching hashes.
- Existing vertical and admission tests continue to pass without path changes.
- Any later physical migration must pass local and GX-10 replay before legacy removal.

## Unresolved matters

- Production evidence retention periods and archive storage classes.
- The first execution increment that will write directly to the canonical evidence root.

