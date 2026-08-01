# ORCH-FANIN: Artifact Aggregation Controller

- UUID: `907b26fd-7cfb-4254-8c32-0bec8467ff76`
- Layer: orchestration
- Status: planned
- Contract: [Orchestration Agent Contract](../../contracts/orchestration-agent-contract.md)

## Purpose

Determine whether prerequisite artifacts are valid, compatible, complete enough, and correctly routed for a declared downstream contract.

## Inputs and outputs

Consumes exact execution results, artifacts, manifests, schemas, policies, and gate criteria. Produces artifact-set validation, compatibility and freshness checks, conflicts, authorized partial-input state, routing decisions, and audit events.

## Boundaries

Do not rewrite findings, reconcile analytical disagreement, average scores, fabricate missing inputs, waive a human gate, or exercise the downstream agent's synthesis authority.

