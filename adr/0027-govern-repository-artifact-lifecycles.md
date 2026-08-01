# ADR-0027: Govern Repository Artifact Lifecycles Before Structural Migration

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: architecture governance and harness maintainers
- Supersedes: none
- Superseded by: none

## Context

The repository has grown through successive architecture and executable vertical increments. Its domain model, contracts, schemas, prompts, and agent registry remain coherent, but authored sources, reusable fixtures, immutable execution evidence, generated deliverables, current status projections, and temporary quality-assurance artifacts are not consistently separated.

Several existing paths and hashes are referenced by contracts, ADRs, retained evidence, test runners, and GX-10 calibration records. A single large directory rewrite would weaken traceability and create avoidable rollback risk.

## Evidence

- The repository contains 1,499 tracked files; 887 are under `training` and 252 are under `fixtures`.
- `training` holds authored material, final deliverables, multiple render passes, contact sheets, and QA intermediates.
- `fixtures` holds both reusable test material and immutable local/GX-10 execution evidence.
- Current status statements in planning and readiness documents have drifted from later human-response records.
- Runtime modules, tests, validation commands, runners, and calibration utilities share one flat `tools` directory.
- The agent registry is internally valid, but some registered roles share layer-wide README files as their specifications.
- The repository had no automated structural workflow at the time of this decision.

## Decision

Adopt the artifact classes and directory responsibilities defined in [Repository Artifact Lifecycle](../docs/repository-artifact-lifecycle.md). Execute the reorganization as bounded sprints in the [Repository Organization Sprint Plan](../planning/repository-organization-sprints.md).

The migration must follow these controls:

1. Establish indexes, lifecycle rules, current-state projections, and automated structural checks before moving artifacts.
2. Treat accepted evidence as immutable. Existing evidence is not rewritten merely to conform to a newer directory convention.
3. Introduce new canonical paths before retiring old paths.
4. Preserve an old-path-to-new-path manifest and SHA-256 verification for every material migration.
5. Retain compatibility wrappers or redirect indexes for at least one reviewed increment when executable or linked paths change.
6. Keep generated current-state views separate from creation-time evidence snapshots.
7. Validate locally and on DGX Spark or an approved equivalent before removing a compatibility path. Production remains targeted to the A100 large cluster.
8. Use a separate reviewed commit for each sprint so a sprint can be reverted without discarding later evidence.

## Alternatives considered

- **Perform one repository-wide move:** rejected because it combines unrelated risks, obscures review, and makes rollback difficult.
- **Leave the repository unchanged:** rejected because status drift, binary growth, duplicated artifacts, and unclear authority boundaries will compound.
- **Delete duplicate evidence and QA output immediately:** rejected because some duplicate evidence is intentionally self-contained and content-addressed, while retention classifications have not yet been assigned.
- **Move all binaries outside Git:** deferred as a universal rule; authored and approved distribution artifacts may still belong in version control or Git LFS.

## Consequences

- Initial sprints add documentation and compatibility material before reducing repository size.
- Historical evidence may continue to use a legacy layout indefinitely, provided it is indexed and clearly labeled as an immutable snapshot.
- CI gains responsibility for navigation, encoding, registries, manifests, schemas, and transient-output policy.
- Later changes to runtime paths require compatibility shims and local/GX-10 regression evidence.
- The repository gains explicit authorities for source, evidence, generated output, current status, and temporary work.

## Traceability

- [ADR 0001: Immutable Artifacts Are Authoritative](0001-immutable-artifacts-are-authoritative.md)
- [ADR 0002: Evidence Is Never Rewritten by a Parent](0002-evidence-is-never-rewritten-by-a-parent.md)
- [ADR 0009: Content-Addressed Artifact and Execution Ledger](0009-content-addressed-artifact-and-execution-ledger.md)
- [Repository Artifact Lifecycle](../docs/repository-artifact-lifecycle.md)
- [Repository Organization Sprint Plan](../planning/repository-organization-sprints.md)

## Validation

- Every sprint identifies scope, migration mapping, validation, and rollback.
- Markdown navigation and controlled manifest references remain valid.
- Retained evidence hashes remain unchanged unless a new superseding artifact is intentionally created.
- Current-state projections cite their authoritative source records and distinguish pending response from pending verification.
- Runtime-path migrations pass the complete local and GX-10 regression suites before legacy removal.

## Unresolved matters

- The exact external storage or Git LFS policy for large training releases.
- Retention periods and storage classes for each evidence class.
- The release at which compatibility paths may be removed.

