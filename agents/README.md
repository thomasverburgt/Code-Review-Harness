# Agents

Agent-specific material is organized here: identity, registry, capability coverage, hierarchy, and role contracts. Shared artifact semantics live in [contracts](../contracts/README.md).

All agents have an immutable UUID and canonical designation in the [machine identity registry](agent-identities.json). The [Agent Naming and Identity Standard](agent-naming-and-identity-standard.md) defines reserved namespaces, aliases, and version rules. The [generated agent catalog](generated/agent-catalog.md) is the current registry-derived human view; the historical [Agent Catalog](agent-registry.md) provides additional narrative.

## Agent layers

- [Specialist agent framework](specialists/specialist-agent-framework.md)
- [Product agent framework](product/product-agent-framework.md)
- [Capability agent framework](capability/capability-agent-framework.md)
- [Enterprise agent framework](enterprise/enterprise-agent-framework.md)
- [Reusable work agents](work/README.md)
- [Orchestration agent framework](orchestration/orchestration-agent-framework.md)

Every role inherits the [Universal Agent Contract](../contracts/universal-agent-contract.md). Use the [hierarchical architecture](hierarchical-agent-architecture.md) for layer boundaries and the [capability matrix](capability-matrix.md) for primary concerns and consumers.

The [Integrated Agent Framework](integrated-agent-framework.md) provides the single end-to-end view across specialist, product, capability, enterprise, and orchestration layers.
