# Repository Organization Sprint Plan

ADR 0027 governs this sequence. Each sprint is independently reviewable and reversible. Existing immutable evidence is never rewritten to make the tree look uniform.

## Sprint 0: Governance baseline

**Outcome:** Formalize ADRs 0001–0005, accept ADR 0027, and define the lifecycle taxonomy and migration controls.

**Gate:** Normative ADR index and governance register agree; all links resolve.

**Rollback:** Revert only the documentation commit. No artifact paths or runtime behavior change.

## Sprint 1: Navigation, status, encoding, and structural CI

**Outcome:** Add missing domain indexes, establish `status` as the living projection layer, correct stale status prose, normalize damaged UTF-8 text, and add automated structural and regression checks.

**Gate:** Markdown links resolve; mojibake detection passes; schemas, agent specifications, and prompt pins validate; the full local test suite and vertical validator pass.

**Rollback:** Revert the Sprint 1 commit. Historical evidence remains untouched.

## Sprint 2: Training and deliverable lifecycle

**Outcome:** Identify authored training source, released packages, final QA evidence, and disposable renders. Track reproducible document builders and introduce release manifests. Decide Git LFS or external release storage before relocating large binaries.

**Gate:** Approved outputs reproduce from retained source; file hashes and release states are recorded; no approved distribution artifact is lost.

**Rollback:** Preserve the old tree for the first increment and restore consumers through the migration manifest.

## Sprint 3: Fixture and evidence separation

**Outcome:** Define canonical reusable-fixture and retained-evidence roots, standardize future evidence paths, and add content-addressed references for deliberately shared inputs.

**Gate:** All scenarios replay; immutable hashes are unchanged; self-contained evidence packages remain resolvable; GX-10 validation passes.

**Rollback:** New indexes point back to legacy locations. No legacy evidence is deleted in the migration sprint.

## Sprint 4: Python package and test layout

**Outcome:** Add `pyproject.toml`, move importable code under `src/code_harness`, mirror it under `tests`, and retain command wrappers under `tools` or `scripts`.

**Gate:** All tests pass through the package entry points and compatibility wrappers locally and on GX-10; retained evidence source references remain explainable.

**Rollback:** Restore imports to the compatibility modules. The previous tool paths remain until a later retirement sprint.

## Sprint 5: Agent specifications and generated catalogs

**Outcome:** Give every registered role an individual specification and generate repeated role, schema, and prompt catalog views from machine-readable authorities.

**Gate:** Registry-to-spec validation is exact; generated views are reproducible and clean after regeneration.

**Rollback:** Retain existing framework tables until generated replacements receive human review.

## Sprint 6: Legacy retirement and repository compaction

**Outcome:** Remove superseded compatibility paths and approved transient artifacts, adopt the selected large-file policy, and clean unreachable Git temporary objects.

**Gate:** One full release increment has used the new paths; local and GX-10 validation pass; migration mappings and archive locations are reviewed.

**Rollback:** Restore from the pre-migration tag or archived release using the verified mapping manifest.

## Program completion criteria

- Every top-level domain has an owner-facing index.
- Authored source, reusable fixture, immutable evidence, generated deliverable, current projection, and temporary work are distinguishable.
- Living status is machine-readable and traceable to immutable authority records.
- Runtime code is packaged and tests are discoverable through one documented command.
- Repeated catalogs are generated from canonical registries.
- Large binaries and transient QA output follow an approved retention policy.

