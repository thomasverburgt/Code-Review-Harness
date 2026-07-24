# Contract Dependency Graph

```mermaid
flowchart BT
  E[Immutable Evidence] --> S[Specialist Contracts]
  S --> P[Product Synthesis]
  P --> C[Capability Delivery Contracts]
  C --> X[Enterprise Synthesis and Governance]
  S --> R[Risk and FMECA]
  R --> P
  R --> C
  P --> H[Human Review Gates]
  C --> H
  X --> H
```

The orchestrator schedules a parent only when declared prerequisite artifacts are present or a policy-approved `incomplete_input` condition exists. Conflict objects are dependencies, not errors to discard.
