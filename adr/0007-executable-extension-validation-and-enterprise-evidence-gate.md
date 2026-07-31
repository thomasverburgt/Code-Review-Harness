# ADR 0007: Executable Extension Validation and Enterprise Evidence Gate

- **Status:** Accepted for the vertical-slice baseline
- **Date:** 2026-07-31
- **Decision owners:** Human architecture maintainers
- **Scope:** `WF-VERTICAL-RISK-001`

## Context

The universal artifact schema prohibits undeclared top-level fields and provides a single open `extensions` object. Layer contracts require additive specialist, product, capability, and enterprise fields. The selected prompts also require role-specific data. A composed full schema that adds top-level properties would weaken or conflict with the universal `additionalProperties: false` boundary.

The agreed semantic path is `SPEC-SECRETS -> PROD-SEC -> CAP-RISK -> ENT-SYSRISK -> human decision request`. The Enterprise Agent Framework separately requires `ENT-EVIDENCE` as the normal gate before enterprise domain reviewers.

## Decision

1. Validate the universal artifact first.
2. Resolve the registered producer layer and validate `extensions.<layer>` against its layer schema.
3. Validate `extensions.<layer>.role` against the schema selected by producer designation.
4. Fan-in succeeds only when universal, layer, and role validation all pass.
5. Keep `ENT-EVIDENCE` as an explicit workflow node between capability publication and `ENT-SYSRISK`; do not collapse it into `ORCH-FANIN`.
6. `ORCH-FANIN` validates artifact fitness at every boundary. `ENT-EVIDENCE` performs the separately attributable enterprise input-gate assessment.

## Consequences

- Universal identity, authority, provenance, confidence, lifecycle, and integrity semantics remain authoritative.
- Layer and role contracts can evolve independently without reopening the universal top-level shape.
- Validators must resolve identity before selecting extension schemas.
- Prompt recommendations such as `extensions.capability.cap_risk` are superseded for this machine baseline by `extensions.capability.role`; their semantic fields remain unchanged.
- The executable workflow contains five agent nodes even though four review prompts define the semantic review path.
- Enterprise review requires both the capability artifact and the `ENT-EVIDENCE` gate artifact.

## Rejected alternatives

- Relaxing the universal top-level boundary was rejected because it weakens deterministic validation.
- A complete duplicated top-level schema per role was rejected because the universal contract could drift.
- Treating `ORCH-FANIN` as `ENT-EVIDENCE` was rejected because it removes an attributable registered assessment.
- Bypassing `ENT-EVIDENCE` was rejected because the slice must prove rather than waive declared gates.

## Validation

`tools/validate_vertical_slice.py` validates the workflow, registry identities, acyclic graph, state machines, universal artifacts, layer extensions, role extensions, lineage/hash references, and human decision request.
