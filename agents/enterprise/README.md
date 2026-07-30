# Enterprise Agents

Enterprise agents consume immutable capability-level assessments and produce strategic, system-of-systems, portfolio, governance, risk, maturity, learning, and investment decision support. The [Enterprise Agent Framework](enterprise-agent-framework.md) defines their workflow and coordination.

All roles inherit the [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Enterprise Agent Contract](../../contracts/enterprise-agent-contract.md). They do not replace capability reviewers or exercise approval authority.

## Shared authority boundary

Enterprise agents may produce strategic assessments, correlations, findings, risks, CAPAs, alternatives, and decision requests. They do not approve or reject capabilities; accept, close, transfer, avoid, or mitigate risk; establish or modify enterprise strategy; grant policy exceptions or waivers; approve investments, releases, roadmaps, or target states; rewrite capability findings or evidence; or silently resolve conflicting assessments.

Every enterprise output must declare:

```yaml
decision_authority: human
```

Every derived assertion must cite contributing capability artifact IDs, evidence references, rubric versions, and confidence provenance. Enterprise scores must not be unexplained averages; aggregation must define normalization, weighting, reconciliation logic, uncertainty, and unresolved disagreement.

## Enterprise role specifications

- [ENT-SYNTH — Enterprise Synthesis Agent](enterprise-synthesis-agent.md)
- [ENT-SYSRISK — Systemic Risk Reviewer](systemic-risk-reviewer.md)
- [ENT-GOV — Enterprise Governance Reviewer](enterprise-governance-reviewer.md)
- [ENT-ARCH — Systems Architecture Reviewer](systems-architecture-reviewer.md)
- [ENT-STRAT — Strategic Scoring Agent](strategic-scoring-agent.md)
- [ENT-EVIDENCE — Evidence Validation Gate](evidence-validation-gate.md)
- [ENT-PORTFOLIO — Portfolio Analysis Agent](portfolio-analysis-agent.md)
- [ENT-ARCHSTRAT — Architecture Strategy Agent](architecture-strategy-agent.md)
- [ENT-MATURITY — Maturity Evaluator](maturity-evaluator.md)
- [ENT-TECHDEBT — Technical Debt Prioritizer](technical-debt-prioritizer.md)
- [ENT-MODERNIZE — Investment and Modernization Advisor](investment-modernization-advisor.md)
- [ENT-LEARN — Learning and Metrics Agent](learning-metrics-agent.md)

All enterprise outputs also inherit the evidence, CAPA, pattern/insight, traceability, confidence, and human-authority semantics.
