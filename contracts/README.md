# Contracts

Shared contracts define the evidence, findings, CAPA, pattern, synthesis, validation, and delivery semantics used throughout the agent system.

## Normative hierarchy

1. [Universal Agent Contract](universal-agent-contract.md) — required artifact envelope and semantics for every agent.
2. Layer contracts — [specialist](specialist-agent-contract.md), [product](product-agent-contract.md), [capability](capability-delivery-contract.md), [enterprise](enterprise-agent-contract.md), [work](work-agent-contract.md), and [orchestration](orchestration-agent-contract.md).
3. Role specifications under [agents](../agents/README.md).
4. Supporting semantic contracts for [evidence](evidence-contract.md), [CAPA](capa-contract.md), and [patterns/insights](pattern-and-insight-contract.md).
5. The [Report Distribution and External Decision Reconciliation Contract](human-decision-contract.md) keeps immutable reports, external authorities, administrative recording, independent verification, and downstream effects separate.
6. The [Shadow Semantic Adjudication Contract](semantic-adjudication-contract.md) turns blocked shadow differences into exact human review requests without granting cutover authority.
7. The [Deterministic Capability Coordination Contract](capability-coordination-contract.md) separates capability fan-in validation from model-backed semantic synthesis.
8. The [CAP-REQ Human Acceptance Contract](requirements-acceptance-contract.md) keeps technical validity, external requirements acceptance, independent verification, derived eligibility, and scheduling authority separate.

The [contract catalog](contract-catalog.md), [dependency graph](contract-dependency-graph.md), and [style and validation rules](style-and-validation.md) define discovery and conformance.
