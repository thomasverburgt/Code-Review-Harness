# Hierarchical Agent Architecture

## Product ecosystem

`SPEC-*` agents collect and assess evidence within a bounded product domain. `PROD-*` agents integrate their immutable results without overwriting them. The catalog covers secrets, composition, dependencies, secure coding, containers, Kubernetes workload/platform/communications, IaC, pipelines, observability, performance, FMECA, architecture, interoperability, information management, risk, linting, I/O, diagrams, research, and product-level security, architecture, quality, and synthesis.

Product-level UI/UX evaluation belongs here: workflow quality, accessibility, consistency, error handling, and application usability.

## Capability delivery layer

This layer answers end-to-end questions across products:

- **Requirements traceability reviewer:** maps harvested evidence to requirements and response narratives, including Block 39-style technical responses where applicable.
- **Cross-product integration reviewer:** correlates product interface evidence and compatibility outcomes.
- **Capability risk reviewer:** assesses capability-level technical confidence and residual risk.
- **Capability architecture reviewer:** determines whether participating products implement the intended capability.
- **Mission-thread reviewer:** evaluates whether the end-to-end mission executes across identity, gateways, services, data, events, and audit trails.
- **Data architecture reviewer:** assesses cross-product information lifecycles and semantics.
- **Operational readiness reviewer:** evaluates deployability, supportability, rollback, and cross-product operability.
- **Decision-conflict reviewer:** exposes incompatible assumptions, decisions, or recommendations.
- **Confidence scoring agent:** produces traceable technical-confidence rollups.
- **Human-centered systems evaluator:** evaluates the end-to-end operator journey, handoffs, reauthentication, errors, effort, and workflow friction.
- **Mission-effectiveness reviewer:** evaluates whether the capability delivers its intended mission outcome.

## Enterprise ecosystem

Enterprise agents consume immutable capability assessments and produce strategic decision support, not code-level verdicts or approvals. They preserve capability evidence and findings, expose disagreement, and declare `decision_authority: human` on every output.

The baseline framework contains:

- **`ENT-EVIDENCE`** for input fitness and reproducibility;
- **`ENT-ARCH`** for system-of-systems architecture;
- **`ENT-SYSRISK`** for cascading, common-mode, concentration, and systemic risk;
- **`ENT-GOV`** for obligations, approvals, exceptions, and governance consistency;
- **`ENT-STRAT`** for transparent strategic confidence;
- **`ENT-PORTFOLIO`** for duplication, gaps, and dependency concentration;
- **`ENT-ARCHSTRAT`** for target-state and trajectory alignment;
- **`ENT-MATURITY`** for evidence-supported maturity;
- **`ENT-TECHDEBT`** for debt trajectory and prioritization;
- **`ENT-MODERNIZE`** for investment and modernization options;
- **`ENT-LEARN`** for calibration, drift, reproducibility, and outcome metrics; and
- **`ENT-SYNTH`** for coherent posture and human decision handoff.

The [Enterprise Agent Framework](enterprise/enterprise-agent-framework.md) defines their dependency and fan-in model.

Enterprise agents do not approve capabilities, accept risk, establish strategy, grant exceptions, approve investments or releases, rewrite capability findings, or silently settle conflicts. Derived assertions cite contributing capability artifact IDs, evidence references, rubric versions, and confidence provenance. Scores require explicit normalization, weighting, reconciliation logic, uncertainty, and unresolved disagreement.

Enterprise-level UX is not rescored; the layer consumes capability-level human-centered systems trends as workforce-experience and mission-effectiveness signals.

## Work and orchestration

`WORK-*` roles provide bounded review, analysis, and summarization services without becoming authoritative reviewers. `ORCH-*` roles schedule, dispatch, validate, aggregate, and route immutable artifacts without altering their meaning or waiving gates.
