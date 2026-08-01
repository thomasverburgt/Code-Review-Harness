# ADR-0031: Require One Specification per Agent and Generated Registry Catalogs

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: agent-framework and registry maintainers
- Supersedes: none
- Superseded by: none

## Context

The identity registry has one record per agent, but thirteen roles referenced a layer README or shared contract as their specification. Identity, status, and role tables are also repeated across catalogs and framework documents, creating drift risk.

## Evidence

- Three product roles shared `product/README.md`.
- Four capability roles shared `capability/capability-layer-contracts.md`.
- Three work roles and three orchestration roles each shared a layer README.
- The registry otherwise resolves all 55 specifications and has unique UUIDs and designations.

## Decision

1. Every registered agent designation must resolve to one individual role specification.
2. Layer READMEs and frameworks explain shared behavior and link individual specifications; they are not substitutes for a role specification.
3. `agents/agent-identities.json` remains authoritative for UUID, designation, display name, layer, lifecycle status, contract version, aliases, and specification path.
4. Generate machine-readable and Markdown catalogs from the registry. Generated files are not edited directly.
5. Structural CI rejects duplicate identities, missing specifications, shared specification paths, and stale generated catalogs.
6. Human-authored frameworks may retain explanatory role tables, but identity/status/path consumers use the generated catalog and registry.

## Alternatives considered

- **Continue shared placeholder specifications:** rejected because a scheduled role needs explicit inputs, outputs, and authority boundaries.
- **Maintain every catalog manually:** rejected because repeated identity data will drift.
- **Generate entire framework prose:** rejected because methodology and architectural reasoning require deliberate human review.

## Consequences

- Thirteen concise specifications are added immediately.
- Registry changes require catalog regeneration.
- Agent identity and status become easier to inspect and validate.
- Layer frameworks remain the source for shared methodology, while role specifications remain bounded and role-specific.

## Traceability

- [Agent identity registry](../agents/agent-identities.json)
- [Generated agent catalog](../agents/generated/agent-catalog.md)
- [Integrated Agent Framework](../agents/integrated-agent-framework.md)
- [ADR 0006](0006-universal-agent-identity-and-contract-standard.md)

## Validation

- All 55 registry entries have unique specification paths.
- Every specification exists.
- Generated JSON and Markdown catalogs reproduce deterministically.
- Existing runtime and workflow tests continue to pass.

## Unresolved matters

- Whether explanatory framework role tables should eventually be replaced by generated includes in the publication toolchain.

