# Agents

Agent-specific material is organized here: identity, registry, capability coverage, hierarchy, and role contracts. Shared artifact semantics live in [contracts](../contracts/README.md).

All agents have an immutable UUID and canonical designation in the [machine identity registry](agent-identities.json). The [Agent Naming and Identity Standard](agent-naming-and-identity-standard.md) defines reserved namespaces, aliases, and version rules. The human-readable [Agent Catalog](agent-registry.md) summarizes the registered roles.

## Agent layers

- [Product specialist agents](specialists/)
- [Product synthesis agents](product/README.md)
- [Capability delivery agents](capability/)
- [Enterprise agents](enterprise/)
- [Reusable work agents](work/README.md)
- [Orchestration agents](orchestration/README.md)

Every role inherits the [Universal Agent Contract](../contracts/universal-agent-contract.md). Use the [hierarchical architecture](hierarchical-agent-architecture.md) for layer boundaries and the [capability matrix](capability-matrix.md) for primary concerns and consumers.
