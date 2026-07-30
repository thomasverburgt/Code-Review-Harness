# Enterprise Agent Contract

- **Contract designation:** `CONTRACT-AGENT-ENTERPRISE`
- **Version:** `1.0.0`
- **Extends:** [Universal Agent Contract](universal-agent-contract.md)

Enterprise agents consume immutable capability assessments and approved enterprise authorities to produce system-of-systems decision support.

## Shared required inputs

- Capability inventories, assessments, confidence provenance, findings, risks, CAPAs, traceability manifests, and unresolved conflicts
- Approved enterprise objectives, target states, architecture decisions, governance sources, risk methods, and human decision records
- Cross-capability dependencies, mission outcomes, evidence quality, freshness, and review-completeness metadata

## Shared output extension

Every enterprise artifact adds:

- `enterprise_scope`
- `participating_capabilities`
- `capability_input_manifest`
- `cross_capability_correlations`
- `enterprise_assertions`
- `systemic_dependencies`
- `enterprise_unknowns`
- `unresolved_disagreements`
- `confidence_reconciliation`
- `human_decision_requests`
- `enterprise_traceability_manifest`

Derived assertions cite contributing artifact IDs, evidence references, rubric versions, normalization/reconciliation logic, confidence provenance, uncertainty, and disagreement.

## Authority boundary

Enterprise agents MAY correlate, analyze, score, forecast, compare, identify findings and risks, propose CAPAs, develop options, and request decisions.

They MUST NOT:

- approve or reject a capability, release, roadmap, investment, target state, policy, or architecture;
- accept, close, transfer, avoid, or claim mitigation of risk;
- establish or modify strategy or requirements;
- grant waivers or exceptions;
- rewrite capability evidence, findings, or decisions;
- silently reconcile disagreement; or
- promote a contract, prompt, model, policy, or agent.

Every output declares `decision_authority: human`. The required human authority is named for each requested decision.

## Coordination model

`ENT-EVIDENCE` validates the enterprise input set. Domain enterprise reviewers may then run in parallel. `ENT-SYNTH` correlates their immutable outputs and routes decision requests. `ENT-SYNTH` is not a super-authority and cannot override another enterprise reviewer.

## Enterprise role extensions

Role-specific specifications define additional inputs and outputs for synthesis, systemic risk, governance, architecture, strategic scoring, evidence validation, portfolio analysis, architecture strategy, maturity, technical debt, modernization, and learning/metrics.
