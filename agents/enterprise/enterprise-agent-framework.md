# Enterprise Agent Framework

The enterprise layer converts immutable capability evidence into traceable system-of-systems decision support. All roles inherit the [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Enterprise Agent Contract](../../contracts/enterprise-agent-contract.md).

## Canonical workflow

```mermaid
flowchart LR
  C[Capability artifacts] --> V[ENT-EVIDENCE]
  V --> A[ENT-ARCH]
  V --> R[ENT-SYSRISK]
  V --> G[ENT-GOV]
  V --> P[ENT-PORTFOLIO]
  A --> AS[ENT-ARCHSTRAT]
  R --> S[ENT-STRAT]
  G --> S
  P --> M[ENT-MODERNIZE]
  AS --> M
  V --> MA[ENT-MATURITY]
  V --> TD[ENT-TECHDEBT]
  A --> TD
  TD --> M
  MA --> M
  A --> ES[ENT-SYNTH]
  R --> ES
  G --> ES
  S --> ES
  P --> ES
  AS --> ES
  MA --> ES
  TD --> ES
  M --> ES
  ES --> H[Human decision authorities]
  H --> L[ENT-LEARN]
```

`ENT-EVIDENCE` is the normal input gate. A policy-authorized partial review may proceed only with an explicit `incomplete_input` state. Parallel enterprise reviewers do not modify each other's outputs. `ENT-SYNTH` correlates them and exposes disagreement; it does not overrule them.

## Registered roles

| Designation | Role | Primary result |
|---|---|---|
| `ENT-EVIDENCE` | Evidence Validation Gate | Validated enterprise input manifest |
| `ENT-ARCH` | Systems Architecture Reviewer | System-of-systems architecture posture |
| `ENT-SYSRISK` | Systemic Risk Reviewer | Enterprise systemic risk register |
| `ENT-GOV` | Enterprise Governance Reviewer | Cross-capability governance posture |
| `ENT-STRAT` | Strategic Scoring Agent | Traceable strategic confidence distribution |
| `ENT-PORTFOLIO` | Portfolio Analysis Agent | Duplication, concentration, and portfolio options |
| `ENT-ARCHSTRAT` | Architecture Strategy Agent | Target-state and roadmap alignment |
| `ENT-MATURITY` | Maturity Evaluator | Configuration-driven maturity assessment |
| `ENT-TECHDEBT` | Technical Debt Prioritizer | Enterprise debt trajectory and priorities |
| `ENT-MODERNIZE` | Investment and Modernization Advisor | Options, tradeoffs, and sequencing |
| `ENT-LEARN` | Learning and Metrics Agent | Quality, drift, and outcome feedback |
| `ENT-SYNTH` | Enterprise Synthesis Agent | Coherent enterprise posture and decision brief |

## Shared gates

- Identity and schema validation precede scheduling.
- Every derived assertion preserves capability provenance.
- Confidence reconciliation retains distributions, uncertainty, and disagreement.
- Human decisions are separate, immutable linked records.
- Learning output can propose sandbox experiments but cannot alter production agents.
