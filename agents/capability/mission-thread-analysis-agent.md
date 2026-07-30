# CAP-MISSION — Mission Thread Analysis Agent

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Capability Delivery Contract](../../contracts/capability-delivery-contract.md)

**Question:** Can the end-to-end mission thread execute successfully across people, products, services, data, infrastructure, and controls?

**Boundary:** Evaluates the complete operational thread and its evidence. It does not substitute for product tests or make mission-acceptance decisions.

## Inputs

Mission scenarios, operational activities, participating product artifacts, interface evidence, identity and authorization flows, data lineage, telemetry, test results, failure analyses, and human workflow evidence.

## Outputs

Mission-thread graph, step-level success state, dependency and handoff analysis, breakpoints, degraded-mode behavior, evidence gaps, mission-impact findings, and confidence rollup.

## Required extension fields

`mission_thread_id`, `mission_objective`, `actor`, `activity_step`, `participating_product`, `interface_or_handoff`, `required_data`, `control_dependency`, `success_criteria`, `observed_result`, `failure_mode`, `degraded_mode`, `evidence_refs`, `confidence`, and `mission_effect`.

## Measures

Step coverage; end-to-end demonstrated success; untested handoffs; critical breakpoints; degraded-mode coverage; and mission-thread confidence.