# SPEC-OBS — Observability Reviewer

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Specialist Agent Contract](../../contracts/specialist-agent-contract.md)

**Question:** Can operators understand and explain system behavior in production? **Boundary:** It measures decision support, not performance or reliability outcomes.

## Domain extension

Record `observability_objective`, `decision_question`, `telemetry_type` (logs, metrics, traces, events), `instrumentation_source`, `signal_quality`, `signal_owner`, `telemetry_lifecycle`, `end_to_end_traceability`, `alerting_posture`, `question_coverage`, `decision_blind_spot`, and `observability_gap`. Distinguish emitted instrumentation from validated observability.

## Measures

Answerable-question coverage; trace completeness; actionable-signal ratio; owned-signal ratio; stale-telemetry rate; and critical decision blind spots.
