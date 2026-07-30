# Agent Naming and Identity Standard

## Identity tuple

Every agent is registered once in [agent-identities.json](agent-identities.json) with:

| Field | Mutability | Purpose |
|---|---|---|
| `agent_uuid` | Immutable | Machine identity for orchestration, traceability, evidence graphs, and metrics |
| `designation` | Immutable and never reused | Canonical human-facing identifier |
| `display_name` | Evolvable | Readable role name |
| `contract_version` | Versioned | Semantic version of the agent's effective contract |

Artifacts carry both `agent_uuid` and the canonical `designation`. Consumers MUST join on UUID, MUST verify the designation against the registry, and MUST retain the designation snapshot for audit readability.

## Designation grammar

```text
<NAMESPACE>-<FUNCTION>[-<QUALIFIER>...]
```

Segments use uppercase ASCII letters and digits. The full designation matches:

```regex
^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$
```

Reserved namespaces:

| Namespace | Scope |
|---|---|
| `SPEC-*` | Bounded product specialist review |
| `PROD-*` | Product-level correlation and synthesis |
| `CAP-*` | Cross-product capability assessment |
| `ENT-*` | Enterprise system-of-systems decision support |
| `WORK-*` | Reusable evidence-processing work roles |
| `ORCH-*` | Workflow scheduling and aggregation control roles |

Namespace ownership is architectural. A contributor MUST NOT introduce a new top-level namespace without an ADR.

## Immutability and migration

- A designation is not renamed in place.
- A superseding designation receives or retains the logical agent UUID only through an approved migration record.
- A retired designation is stored in `legacy_designations`, remains resolvable, and is never assigned to another UUID.
- The initial migration maps every `SPC-*` designation to `SPEC-*` and `PRD-SYNTH` to `PROD-SYNTH`.
- `CAP-MTHREAD`, which appeared in one capability workflow document, is normalized as a documentation alias of canonical `CAP-MISSION`.

## Version rules

- Patch: editorial clarification with no semantic effect.
- Minor: backward-compatible fields, outputs, or validation.
- Major: changed meaning, removed requirements, authority-boundary changes, or incompatible schema changes.

UUID and designation changes are not version bumps; they require an ADR and explicit registry migration.

## Registration gate

A new agent is not schedulable until:

1. Its UUID and designation are unique.
2. Its specification and effective layer contracts are named.
3. Its authoritative question and prohibited authority are documented.
4. Its status is `seed`, `planned`, `baseline`, `candidate`, `active`, `deprecated`, or `retired`.
5. The identity registry and affected workflow validate.
