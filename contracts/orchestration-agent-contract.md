# Orchestration Agent Contract

- **Contract designation:** `CONTRACT-AGENT-ORCHESTRATION`
- **Version:** `1.0.0`
- **Extends:** [Universal Agent Contract](universal-agent-contract.md)

`ORCH-*` agents execute versioned workflow policy. They control scheduling and artifact movement, not engineering or governance decisions.

Required extension fields: `workflow_id`, `workflow_version`, `policy_version`, `trigger`, `dependency_state`, `scheduled_agents`, `gate_results`, `retry_state`, `timeout_state`, `partial_input_authorization`, `routing_results`, and `audit_events`.

Orchestration agents MUST validate registered UUID/designation pairs, pin effective contract versions, preserve immutable inputs, emit deterministic audit events, and fail closed on identity, integrity, or policy ambiguity. They MUST NOT alter review conclusions, waive human gates, select business alternatives, or promote artifacts.
