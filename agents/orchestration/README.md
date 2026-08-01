# Orchestration Agents

Orchestration agents inherit the [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Orchestration Agent Contract](../../contracts/orchestration-agent-contract.md).

The control-plane topology, state-machine relationship, role status, and shared gates are defined in the [Orchestration Agent Framework](orchestration-agent-framework.md).

## `ORCH-SCHED` — Contract Scheduler

**Question:** Which registered agents and pinned contracts must execute for this trigger and policy context?

Resolves UUIDs and designations, evaluates eligibility and dependencies, pins versions, and produces an auditable schedule. It cannot alter policy or substitute an unregistered agent.

Role details are defined in [contract-scheduler.md](contract-scheduler.md).

## `ORCH-FANOUT` — Parallel Dispatch Controller

**Question:** Which independent scheduled work can safely execute in parallel with immutable, least-privilege inputs?

Creates bounded work packets, enforces scope and credential boundaries, records dispatch state, and handles retry/timeout policy. It cannot broaden scope or modify an agent contract.

Role details are defined in [parallel-dispatch-controller.md](parallel-dispatch-controller.md).

## `ORCH-FANIN` — Artifact Aggregation Controller

**Question:** Are prerequisite artifacts valid, compatible, complete enough, and correctly routed for the next contract?

Validates identity, schema, integrity, freshness, dependencies, conflicts, and partial-input authorization before routing. It cannot reconcile findings, average scores, or waive a human gate.

Role details are defined in [artifact-aggregation-controller.md](artifact-aggregation-controller.md).
