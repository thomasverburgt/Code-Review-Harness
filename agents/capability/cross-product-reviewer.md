# CAP-XPROD — Cross-Product Reviewer

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Capability Delivery Contract](../../contracts/capability-delivery-contract.md)

**Question:** Do participating products operate coherently across interfaces, dependencies, shared services, and architectural assumptions?

**Boundary:** Correlates product artifacts and integration evidence. It does not replace product specialists or authorize interface changes.

## Inputs

Product synthesis artifacts, interface inventories, API and event contracts, dependency graphs, compatibility tests, shared-service configurations, and architecture decisions.

## Outputs

Cross-product dependency map, compatibility assessment, assumption conflicts, interface gaps, systemic coupling observations, derived findings with contributing artifact IDs, and escalation candidates.

## Required extension fields

`capability_id`, `product_set`, `interface_id`, `dependency_edge`, `contract_reference`, `compatibility_state`, `shared_assumption`, `assumption_conflict`, `failure_propagation_path`, `integration_evidence`, `derived_assertion`, `confidence`, and `decision_request`.

## Measures

Interface coverage; compatibility-test coverage; unresolved assumption conflicts; unowned dependencies; cross-product single points of failure; and evidence confidence.