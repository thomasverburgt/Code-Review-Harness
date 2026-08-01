# Capability Delivery Agents

Capability agents consume immutable product-level review artifacts and evaluate questions that cross product boundaries. They do not rewrite specialist findings, approve releases, or alter production configuration.

The layer topology, coordination and synthesis boundaries, role status, and shared gates are defined in the [Capability Agent Framework](capability-agent-framework.md).

| Agent ID | Agent | Authoritative question |
|---|---|---|
| `CAP-REQ` | Requirements Traceability Reviewer | Do the implemented products and evidence satisfy the declared requirements? |
| `CAP-XPROD` | Cross-Product Reviewer | Do products interact coherently across interfaces, dependencies, and shared assumptions? |
| `CAP-RISK` | Capability Risk Reviewer | What capability-level risks emerge from correlated product evidence? |
| `CAP-MISSION` | Mission Thread Analysis Agent | Can the end-to-end mission thread execute successfully across participating products? |
| `CAP-HCD` | Human-Centered Design Evaluator | Does the end-to-end capability support the operator's mission with acceptable effort, clarity, and resilience? |
| `CAP-ARCH` | Capability Architecture Reviewer | Do participating products form a coherent capability architecture across boundaries and shared services? |
| `CAP-TRADE` | Capability Trade-Study Reviewer | What criterion-level differences and sensitivities follow from the authorized alternatives and method? |
| `CAP-GOV` | Capability Governance Reviewer | Are cross-product obligations, owners, decisions, and exceptions governed by authoritative records? |
| `CAP-PROGRESS` | Capability Progress and Readiness Reviewer | What progress and readiness are demonstrated against declared evidence gates and criteria? |
| `CAP-COORD` | Deterministic Capability Coordinator | Is the declared capability-review input set exact, valid, complete, traceable, and eligible for synthesis dispatch? |
| `CAP-SYNTH` | Capability Synthesis Lead (candidate; unscheduled) | What explicitly sourced capability posture follows from a validated coordinator manifest and its exact immutable inputs? |

All capability agents inherit the [Universal Agent Contract](../../contracts/universal-agent-contract.md), capability-delivery contract, evidence contract, CAPA rules, confidence semantics, and the sandboxed evolution contract. Canonical identities are registered in [agent-identities.json](../agent-identities.json).

Individual specifications: [CAP-ARCH](capability-architecture-reviewer.md), [CAP-TRADE](capability-trade-study-reviewer.md), [CAP-GOV](capability-governance-reviewer.md), and [CAP-PROGRESS](capability-progress-readiness-reviewer.md).
