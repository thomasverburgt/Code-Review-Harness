# Contract Dependency Graph

```mermaid
flowchart BT
  I[Identity Registry] --> U[Universal Agent Contract]
  U --> W[Work Contracts]
  U --> O[Orchestration Contracts]
  U --> S[Specialist Contracts]
  E[Immutable Evidence] --> S
  S --> P[Product Agent Contracts]
  P --> C[Capability Delivery Contracts]
  C --> V[Enterprise Evidence Gate]
  V --> X[Enterprise Agent Contracts]
  S --> R[Risk and FMECA]
  R --> P
  R --> C
  P --> H[Human Review Gates]
  C --> H
  X --> H
```

`ORCH-SCHED` resolves immutable agent identities and pins contract versions. `ORCH-FANOUT` dispatches bounded independent work. `ORCH-FANIN` schedules a parent only when declared prerequisite artifacts are valid and present or a policy-approved `incomplete_input` condition exists. Conflict objects are dependencies, not errors to discard.
