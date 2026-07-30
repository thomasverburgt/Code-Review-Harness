# SPEC-IAC — Infrastructure-as-Code Reviewer

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Specialist Agent Contract](../../contracts/specialist-agent-contract.md)

**Question:** Is desired infrastructure correctly, securely, and recoverably defined? **Boundary:** Reviews design and desired state; it does not substitute for runtime-health monitoring.

## Domain extension

Record `infrastructure_layer_owner`, `module`, `module_maturity` (experimental, supported, blessed), `observed_state`, `desired_state`, `expected_state`, `change_intent`, `idempotency`, `state_management`, `drift_readiness`, `policy_inheritance`, `dependency_order`, `partial_deployment_failure_mode`, `recovery_consideration`, and `change_blast_radius_prediction`. Candidate composable infrastructure patterns are allowed.

## Measures

Managed-resource coverage; policy conformance; drift-detection readiness; idempotency confidence; partial-deployment recovery coverage; and ownership clarity.
