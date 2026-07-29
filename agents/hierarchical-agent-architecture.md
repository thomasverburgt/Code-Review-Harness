# Hierarchical Agent Architecture

## Product ecosystem

Specialists collect and assess evidence within a product boundary. Product synthesis integrates their results without overwriting them. The baseline specialists are listed in the registry and cover secrets, composition, dependencies, secure coding, containers, Kubernetes workload/platform/communications, IaC, pipelines, observability, performance, FMECA, architecture, interoperability, information management, risk, linting, I/O, diagrams, and research.

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

Initial baseline enterprise agents:

- **`ENT-SYNTH` Enterprise Synthesis Agent:** produces a coherent, traceable enterprise posture and decision-ready handoff across capabilities.
- **`ENT-SYSRISK` Systemic Risk Reviewer:** identifies cross-capability concentration, common-mode, cascading, and systemic mission risks.
- **`ENT-GOV` Enterprise Governance Reviewer:** assesses governance consistency, obligations, approvals, exceptions, conflicts, and traceability.

Planned enterprise agents:

- **Systems architecture reviewer** — system-of-systems architecture coherence.
- **Strategic scoring agent** — strategic confidence, target-state alignment, and readiness.
- **Evidence validation gate** — provenance, completeness, conflict handling, and traceability validation.
- **Portfolio analysis agent** — duplication, consolidation, and dependency concentration.
- **Architecture strategy agent** — roadmap and target-state alignment with trajectory forecasting.
- **Maturity evaluator** — configuration-driven product, capability, and enterprise maturity measures.
- **Technical debt prioritizer** — enterprise debt trajectory and investment options.
- **Investment and modernization advisor** — options, tradeoffs, and modernization sequencing.
- **Learning and metrics agent** — human/AI agreement, false positives, cycle time, and feedback-loop measurements.

Enterprise agents do not approve capabilities, accept risk, establish strategy, grant exceptions, approve investments or releases, rewrite capability findings, or silently settle conflicts. Derived assertions cite contributing capability artifact IDs, evidence references, rubric versions, and confidence provenance. Scores require explicit normalization, weighting, reconciliation logic, uncertainty, and unresolved disagreement.

Enterprise-level UX is not rescored; the layer consumes capability-level human-centered systems trends as workforce-experience and mission-effectiveness signals.