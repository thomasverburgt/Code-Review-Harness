# Orchestration Agent Contract

- **Contract designation:** `CONTRACT-AGENT-ORCHESTRATION`
- **Version:** `1.0.0`
- **Extends:** [Universal Agent Contract](universal-agent-contract.md)

`ORCH-*` agents execute versioned workflow policy. They control scheduling and artifact movement, not engineering or governance decisions.

Required extension fields: `workflow_id`, `workflow_version`, `policy_version`, `trigger`, `dependency_state`, `scheduled_agents`, `gate_results`, `retry_state`, `timeout_state`, `partial_input_authorization`, `routing_results`, and `audit_events`.

Orchestration agents MUST validate registered UUID/designation pairs, pin effective contract versions, preserve immutable inputs, emit deterministic audit events, and fail closed on identity, integrity, or policy ambiguity. They MUST NOT alter review conclusions, waive human gates, select business alternatives, or promote artifacts.

Every dispatch MUST pin `execution_mode`, platform designation, accelerator/runtime configuration, container image, model or workload scale, environment-policy version, and known limitations. Production dispatch targets NVIDIA A100 large-cluster infrastructure. Test dispatch targets NVIDIA DGX Spark or an approved equivalent for every development, regression, calibration, integration, security, resilience, rollback, and performance suite. A mode/platform mismatch fails closed. Promotion retains the test evidence and environment delta; scaled test results are never labeled as measured A100 capacity.
