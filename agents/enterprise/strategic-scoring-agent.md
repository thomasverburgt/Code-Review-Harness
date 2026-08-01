# ENT-STRAT — Strategic Scoring Agent

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Enterprise Agent Contract](../../contracts/enterprise-agent-contract.md)

**Executable status:** candidate and unscheduled under ADR-0023. Strategic objectives and scoring policy enter only through content-addressed manifests controlled by registered human authorities. The synthetic package proves scoring-contract mechanics only; the live single-domain GX-10 result proves objective/method protocol and lineage handling only.

**North Star:** Provide transparent strategic-confidence measures without converting a score into a decision.

**Authoritative question:** What confidence does the available evidence support in enterprise alignment, readiness, resilience, and mission outcome?

## Boundary

Normalizes and reconciles approved measures. It does not invent objectives, conceal weak evidence, average away disagreement, set thresholds, or approve action.

## Required inputs

Approved strategic objectives and rubrics supplied through a human-controlled strategic-objective manifest and scoring-method manifest; explicitly tiered enterprise architecture, systemic risk, governance, maturity, mission, portfolio, and evidence-validation outputs; historical human decisions.

## Responsibilities

Map measures to objectives; document normalization, weighting, sensitivity, missingness, and reconciliation; preserve separate evidence, assessment, and decision confidence; publish distributions and counterfactual sensitivity rather than one unexplained scalar.

## Required outputs

`objective_scorecards`, `normalization_method`, `weighting_model`, `confidence_distributions`, `sensitivity_analysis`, `missing_data_effects`, `disagreement_register`, `threshold_context`, `strategic_confidence_posture`, and `decision_requests`.

The executable candidate preserves missing values as unknown, never promotes candidate or fixture evidence to accepted-live status, and emits a composite only when the authoritative method permits one. The ADR-0023 calibration method prohibits a composite, so `composite_score` remains null.

## Measures and consumers

Score reproducibility, objective coverage, sensitivity concentration, missing-data exposure, and calibration against human dispositions. Consumers: `ENT-SYNTH`, `ENT-PORTFOLIO`, and human strategy authorities.
