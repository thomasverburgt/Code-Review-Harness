# Enterprise Agents

Enterprise agents consume immutable capability-level assessments and produce strategic, system-of-systems, portfolio, governance, risk, maturity, and investment decision support.

They do not replace capability reviewers or exercise approval authority.

## Shared authority boundary

Enterprise agents may produce strategic assessments, correlations, findings, risks, CAPAs, alternatives, and decision requests. They do not approve or reject capabilities; accept, close, transfer, avoid, or mitigate risk; establish or modify enterprise strategy; grant policy exceptions or waivers; approve investments, releases, roadmaps, or target states; rewrite capability findings or evidence; or silently resolve conflicting assessments.

Every enterprise output must declare:

```yaml
decision_authority: human
```

Every derived assertion must cite contributing capability artifact IDs, evidence references, rubric versions, and confidence provenance. Enterprise scores must not be unexplained averages; aggregation must define normalization, weighting, reconciliation logic, uncertainty, and unresolved disagreement.

## Initial enterprise contracts

- [ENT-SYNTH — Enterprise Synthesis Agent](enterprise-synthesis-agent.md)
- [ENT-SYSRISK — Systemic Risk Reviewer](systemic-risk-reviewer.md)
- [ENT-GOV — Enterprise Governance Reviewer](enterprise-governance-reviewer.md)

## Planned enterprise agents

- Systems Architecture Reviewer
- Strategic Scoring Agent
- Evidence Validation Gate
- Portfolio Analysis Agent
- Architecture Strategy Agent
- Maturity Evaluator
- Technical Debt Prioritizer
- Investment and Modernization Advisor
- Learning and Metrics Agent

All enterprise outputs inherit the base agent contract, enterprise synthesis contract, evidence contract, CAPA contract, traceability rules, confidence semantics, and human-authority boundary.