# ADR-0032: Defer Legacy Retirement and Retain Training and QA

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: repository, runtime, evidence, training, and release maintainers
- Supersedes: ADR-0028 decisions 4-6 only for the current retention state of existing training and QA paths
- Superseded by: none

## Context

Sprints 2-5 established release manifests, evidence catalogs, a Python package boundary, and generated agent catalogs. The final organization sprint contemplated removal of legacy runtime paths and transient training artifacts. The project maintainer has directed that training and QA remain with the repository for now. Runtime compatibility retirement still requires a compatibility release, GX-10 validation, migration mappings, and explicit human approval.

GX access credentials are operator-managed local material outside the repository. The repository records only whether remote validation ran; it does not retain credential contents, filenames, or machine-specific paths.

## Evidence

- Existing `tools` paths remain referenced by tests, commands, and retained evidence.
- The `code_harness` package boundary has been locally validated but has not yet completed an observed compatibility release.
- Training release manifests classify the retained QA and render paths and preserve their repository provenance.
- Eleven legacy evidence roots remain immutable and inventory-hashed in place.
- ADR 0027 prohibits legacy removal before its rollback and validation gates pass.

## Decision

1. Do not remove legacy `tools` implementations or tests in PR 8.
2. Retain the current training and QA trees in the repository. They are not retirement candidates. Any later externalization, relocation, or removal requires a separate ADR and explicit maintainer approval; selecting an archive alone is insufficient authority.
3. Do not move legacy evidence merely to normalize paths; retain it in place unless a later separately approved migration has an exact mapping and replay evidence.
4. Maintain a deterministic retirement-readiness manifest that distinguishes removal candidates from repository-retained content and names each gate, state, and rollback treatment.
5. Permit safe local Git maintenance of unreachable temporary objects because it does not alter reachable commits or tracked artifacts.
6. Reassess runtime compatibility retirement after one compatibility release and full local and GX-10 validation. Removal requires a later commit and explicit evidence that every gate is satisfied.

## Alternatives considered

- **Delete or externalize existing training and QA now:** rejected because repository retention is the maintainer's current decision.
- **Move implementations immediately after local tests:** rejected because the GX-10 and observation gates are unsatisfied.
- **Declare Sprint 6 complete without removals:** rejected; the readiness work may complete, but legacy retirement remains gated.

## Consequences

- The repository intentionally retains the training and QA footprint for provenance, review, and operational continuity.
- No rollback or evidence-replay path is weakened for cosmetic organization.
- The remaining work is explicit and machine-readable rather than informally deferred.
- A later retirement increment can be small, evidence-backed, and independently reversible.

## Traceability

- [ADR 0027](0027-govern-repository-artifact-lifecycles.md)
- [ADR 0028](0028-binary-release-and-transient-render-retention.md)
- [ADR 0029](0029-separate-reusable-fixtures-from-retained-evidence.md)
- [ADR 0030](0030-compatibility-first-python-package-boundary.md)
- [Retirement Readiness](../migration/retirement-readiness.json)

## Validation

- The retirement manifest regenerates deterministically.
- Every named path exists or is explicitly classified as retained content or local-only maintenance.
- `removal_authorized` remains false while any required gate is false.
- All local tests and structural checks pass with legacy paths intact.

## Unresolved matters

- Operator-provided local GX-10 access or another approved remote test route.
- Compatibility release identifier and observation period.
