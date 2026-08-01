# ADR-0030: Introduce a Compatibility-First Python Package Boundary

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: harness runtime and test maintainers
- Supersedes: none
- Superseded by: none

## Context

Runtime modules, validators, reference runners, calibration commands, and 118 tests currently share a flat `tools` directory. Many modules use bare sibling imports, and retained evidence and GX-10 commands identify their current paths. Moving every implementation and test in one commit would create a wide import-path change with weak rollback characteristics.

## Evidence

- `tools` contains 67 files, including runtime implementations, runners, builders, validators, and tests.
- `worker_runtime.py` is the largest shared implementation module and has many downstream consumers.
- Existing local and GX-10 evidence invokes scripts by their `tools` paths.
- ADR 0027 requires compatibility paths and local/GX-10 validation before legacy removal.

## Decision

1. Establish `src/code_harness` as the supported Python package boundary and add a standards-based `pyproject.toml`.
2. Provide package modules for the ledger and each current runtime through an explicit compatibility loader. Bundle the legacy `tools` implementation package in the compatibility distribution so installed use does not depend on the repository working directory.
3. Expose structural and vertical validation as package CLI entry points.
4. Add a dedicated `tests` tree that verifies the package boundary, while retaining the existing regression tests under `tools` during the compatibility release.
5. Keep existing `tools` implementation and command paths unchanged in this sprint. The package loader resolves those modules from the repository root and marks the boundary as transitional.
6. Physically move implementations only after imports, entry points, local tests, GX-10 tests, and retained command references have been migrated. Existing `tools` paths then become thin wrappers for at least one release before removal.
7. Split `worker_runtime.py` by queue, adapters, assembly, publication, and telemetry during the physical-migration increment rather than mixing decomposition with package-boundary creation.

## Alternatives considered

- **Move every module and test immediately:** rejected because a single import rewrite would combine packaging, decomposition, and compatibility risk.
- **Leave `tools` as the permanent import surface:** rejected because runners, tests, and reusable implementation would remain indistinguishable.
- **Duplicate implementation into `src`:** rejected because two editable copies would create behavioral drift.
- **Use symbolic links:** rejected because installation, archives, and Windows behavior would be unreliable.

## Consequences

- Consumers can begin using `code_harness` imports and CLI entry points immediately.
- The package temporarily delegates to legacy implementations, which keeps old paths valid but is not the final source layout.
- CI must exercise both package-boundary tests and the legacy regression suite.
- The eventual physical move remains a separately reversible change with GX-10 evidence.

## Traceability

- [ADR 0027: Govern Repository Artifact Lifecycles](0027-govern-repository-artifact-lifecycles.md)
- [Repository Organization Sprint Plan](../planning/repository-organization-sprints.md)
- [Harness Tools](../tools/README.md)
- [Python Package](../src/code_harness/README.md)

## Validation

- `code_harness` imports representative ledger and runtime APIs through the compatibility boundary.
- Package CLI validation returns the same result as direct `tools` invocation.
- Dedicated package tests and all 118 legacy tests pass.
- No existing runtime, fixture, evidence, report, or scheduling behavior changes.

## Unresolved matters

- Exact module decomposition for `worker_runtime.py`.
- The compatibility release after which legacy test and implementation locations may be retired.
