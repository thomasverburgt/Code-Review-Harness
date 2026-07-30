# ADR 0006: Universal Agent Identity and Contract Standard

- **Status:** accepted
- **Date:** 2026-07-30
- **Decision authority:** project maintainer
- **Contract baseline:** `1.0.0`

## Context

The architecture already used stable human-facing IDs, but it did not define an immutable machine identity, reserved namespaces, a universal artifact envelope, or a schema-backed migration rule. The enterprise layer also mixed shared synthesis semantics with role-specific contracts.

## Decision

Every registered agent has four identity elements:

1. `agent_uuid`: immutable UUID machine identity.
2. `designation`: immutable canonical human-facing identity.
3. `display_name`: evolvable descriptive name.
4. `contract_version`: semantic version of the agent contract.

Canonical designations use reserved hierarchical namespaces described in [Agent Naming and Identity Standard](../agents/agent-naming-and-identity-standard.md). Existing `SPC-*` and `PRD-*` designations are retired aliases of their `SPEC-*` and `PROD-*` successors. Retired values remain resolvable and may never be reassigned.

All agent outputs conform to the [Universal Agent Contract](../contracts/universal-agent-contract.md) and its JSON Schema. Layer contracts are additive extensions. Enterprise roles additionally conform to the [Enterprise Agent Contract](../contracts/enterprise-agent-contract.md).

## Consequences

- Orchestration, evidence graphs, and metrics key agents by UUID and retain designation snapshots.
- Historical artifacts remain traceable through immutable aliases.
- A designation rename is a migration that creates a new canonical designation mapping; it is never an in-place reuse.
- Contract validation becomes a required fan-in and promotion gate.
- Enterprise roles share one authority boundary while retaining role-specific outputs.

## Alternatives considered

- **Continue using designation alone:** rejected because display/name evolution and migration could break machine joins.
- **Generate UUIDs at runtime:** rejected because the same logical agent could receive different identities.
- **Rename legacy IDs without aliases:** rejected because it would orphan evidence and audit history.
- **Use one monolithic enterprise agent:** rejected because synthesis, risk, governance, strategy, evidence validation, and advisory functions require separable authority and provenance.

## Validation and supersession

The identity registry must validate against `agent-identity-registry.schema.json`; agent artifacts must validate against `universal-agent-artifact.schema.json`. A later ADR may supersede this decision but must preserve UUIDs, aliases, and historical resolution.
