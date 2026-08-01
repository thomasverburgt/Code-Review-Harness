# ORCH-SCHED: Contract Scheduler

- UUID: `c48c1f0f-ba69-414d-9606-5401373f9da8`
- Layer: orchestration
- Status: planned
- Contract: [Orchestration Agent Contract](../../contracts/orchestration-agent-contract.md)

## Purpose

Resolve which registered agents and pinned contracts are eligible and required for a trigger and policy context.

## Inputs and outputs

Consumes a trigger, source revision, policy, registry, dependency state, authority context, and resource constraints. Produces an auditable schedule with UUIDs, designations, versions, gates, dependencies, concurrency groups, and reasons for exclusions.

## Boundaries

Do not alter policy, register or substitute an agent, waive a gate, infer eligibility, grant credentials, or approve execution beyond the declared scheduling authority.

