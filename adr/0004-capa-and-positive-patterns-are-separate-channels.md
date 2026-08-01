# ADR 0004: CAPA and Positive Patterns Are Separate Channels

- **Status:** accepted
- **Date:** 2026-07-24
- **Decision authority:** project maintainer
- **Owners:** quality, risk, and learning-governance maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

The harness must represent both deficiencies that require treatment and beneficial practices that may be repeated or promoted. These records have different meanings, evidence requirements, owners, lifecycles, and governance effects.

Using CAPA to record a good practice would imply a deficiency and corrective obligation where none exists. Using a positive pattern to represent remediation would obscure accountability, validation, residual risk, and closure.

## Evidence

- The [CAPA Contract](../contracts/capa-contract.md) requires root cause, corrective action, preventive action, owner role, target horizon, implementation level, and validation method for every finding.
- The [Pattern and Insight Contract](../contracts/pattern-and-insight-contract.md) treats beneficial practices and neutral correlations as candidates requiring evidence and promotion controls.
- The [Universal Agent Contract](../contracts/universal-agent-contract.md) provides separate `findings`, `patterns`, and `insights` channels.
- Agent frameworks preserve recommendation, approval, implementation, validation, residual-risk decision, and closure as distinct states.

## Decision

CAPA and positive-pattern records remain separate channels.

CAPA remedies a demonstrated deficiency. It links to a finding and records root cause, corrective action for the present instance, preventive action against recurrence, accountable owner role, target horizon, implementation level, and validation method.

A pattern candidate documents a demonstrably beneficial practice. It records supporting evidence, applicable context, boundaries, expected benefit, confidence, possible adverse effects, and a separate promotion or reuse path. A pattern is not mandatory remediation and does not become a standard merely because an agent observed it.

Neutral relationships that are neither deficiencies nor established beneficial practices remain insights until sufficient evidence supports reclassification through an authorized process.

## Alternatives considered

- **Use one recommendation list for deficiencies and strengths:** rejected because consumers could not distinguish mandatory treatment from optional reuse.
- **Represent good practices as preventive actions:** rejected because preventive action belongs to the recurrence control for a specific deficiency.
- **Automatically promote repeated patterns into policy:** rejected because frequency alone does not establish applicability, safety, or governance authority.
- **Omit positive patterns from the harness:** rejected because validated strengths support learning, consistency, and investment decisions.

## Consequences

- Schemas, reports, metrics, backlogs, and user interfaces must preserve separate CAPA, pattern, and insight types.
- CAPA closure does not promote a pattern, and pattern promotion does not close a finding.
- Positive practices require evidence and applicability limits rather than celebratory assertions.
- Quality metrics can distinguish deficiency treatment from learning and reuse.
- Human authorities retain separate control over remediation approval, closure, standardization, and pattern promotion.

## Traceability

- [CAPA Contract](../contracts/capa-contract.md)
- [Pattern and Insight Contract](../contracts/pattern-and-insight-contract.md)
- [Universal Agent Contract](../contracts/universal-agent-contract.md)
- `appendices/schemas/capa.schema.json`
- `appendices/schemas/pattern.schema.json`
- `appendices/schemas/insight.schema.json`

## Validation

- Every finding includes a schema-valid CAPA chain.
- CAPA records fail validation when they do not reference a deficiency or omit required ownership and validation fields.
- Pattern records fail validation when evidence, applicability, limitations, or confidence are absent.
- Reports and downstream routing preserve CAPAs, patterns, and insights as different collections and lifecycle states.
- Tests prevent pattern promotion or CAPA closure from being inferred from an agent recommendation alone.

## Unresolved matters

- Program-specific pattern promotion authorities and review cadence.
- Metrics for measuring realized benefit after a pattern is adopted.
- Rules for identifying when a preventive action is sufficiently reusable to become a separate pattern candidate.
