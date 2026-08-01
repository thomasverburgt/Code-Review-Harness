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
| `CAP-COORD` | Deterministic Capability Coordinator | Is the declared capability-review input set exact, valid, complete, traceable, and eligible for synthesis dispatch? |
| `CAP-SYNTH` | Capability Synthesis Lead (candidate; unscheduled) | What explicitly sourced capability posture follows from a validated coordinator manifest and its exact immutable inputs? |

All capability agents inherit the [Universal Agent Contract](../../contracts/universal-agent-contract.md), capability-delivery contract, evidence contract, CAPA rules, confidence semantics, and the sandboxed evolution contract. Canonical identities are registered in [agent-identities.json](../agent-identities.json).
