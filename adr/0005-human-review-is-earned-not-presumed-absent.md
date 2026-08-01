# ADR 0005: Human Review Is Earned, Not Presumed Absent

- **Status:** accepted
- **Date:** 2026-07-24
- **Decision authority:** project maintainer
- **Owners:** governance, assurance, and harness-operations maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

The harness is intended to increase review scale and consistency without transferring accountable authority to automation by default. Early agent behavior may be useful but insufficiently calibrated, and aggregate accuracy can conceal severe errors in high-risk or low-frequency cases.

Removing human review merely because automation exists would make absence of oversight an implicit architecture decision. Any reduction in review must instead be supported by representative measurements, bounded policy, continued monitoring, explicit authority, and rollback.

## Evidence

- [Human Review Gates and Automation Maturity](../governance/human-review-and-maturity.md) defines progressive levels from observation through limited auto-promotion.
- Relevant quality measures include agreement with designated human reviewers, false-positive and false-negative rates, reviewability, evidence coverage, confidence calibration, severity, and risk.
- The [Universal Agent Contract](../contracts/universal-agent-contract.md) requires explicit human decision authority, uncertainty, partial-input state, and named decision requests.
- Existing governance state machines separate technical validation, human response, administrative recording, independent verification, eligibility, scheduling, distribution, deployment, and revocation.

## Decision

Human review is the default for all material recommendations and decisions. Reduced oversight must be earned through measured performance and granted through explicit, versioned, reversible policy. Human gates may be narrowed for a declared low-risk population, but they are never silently removed.

Automation maturity is evaluated using representative agreement, false-positive and false-negative behavior, evidence coverage and reviewability, confidence calibration, impact and risk, drift, reproducibility, and rollback readiness. Thresholds are program-specific decision inputs rather than universal guarantees.

Any policy that reduces human review must identify the eligible population, prohibited cases, evidence window, metrics and thresholds, decision authority, monitoring cadence, escalation triggers, expiration or reauthorization conditions, audit requirements, and rollback path. Material, ambiguous, high-risk, incomplete, conflicting, or out-of-distribution cases continue to require human review.

## Alternatives considered

- **Remove human review whenever confidence exceeds a fixed threshold:** rejected because confidence is not authority and may be miscalibrated or insensitive to impact.
- **Require identical human review forever:** rejected because sustained evidence may justify bounded efficiency improvements without weakening accountability.
- **Let each agent decide when review is unnecessary:** rejected because agents cannot grant themselves authority or modify governance policy.
- **Use aggregate agreement as the only promotion measure:** rejected because averages can conceal severe or systematically missed cases.

## Consequences

- Initial operation emphasizes human disposition, measurement, and calibration rather than autonomous promotion.
- Review reduction requires a formal policy and decision record, not an implementation shortcut.
- Monitoring and periodic audit continue after promotion, and drift can restore stricter gates.
- Low-risk automation can mature incrementally while material authority remains accountable and traceable.
- The harness must retain sufficient evidence to reproduce both the automated result and the policy decision that allowed its treatment.

## Traceability

- [Human Review Gates and Automation Maturity](../governance/human-review-and-maturity.md)
- [Universal Agent Contract](../contracts/universal-agent-contract.md)
- [Human Decision Contract](../contracts/human-decision-contract.md)
- [Sandboxed Contract Evolution](../contracts/sandboxed-contract-evolution.md)
- [Report Governance State Machine](../orchestration/state-machines/report-governance.state-machine.json)
- [Integrated Agent Framework](../agents/integrated-agent-framework.md)

## Validation

- Every workflow identifies applicable human gates and the policy version controlling them.
- A missing approval, verification, or eligibility record fails closed rather than advancing state.
- Any reduced-review policy is schema-valid, scoped, time-bounded or reauthorized, monitored, and rollback-capable.
- Calibration reports include representative populations, error rates, confidence behavior, limitations, and disagreement.
- Drift, scope mismatch, integrity failure, policy ambiguity, or threshold regression restores the stricter human-review path.

## Unresolved matters

- Program-specific maturity thresholds, representative sample definitions, and minimum observation windows.
- Which low-risk finding classes may eventually qualify for guarded routing or limited backlog promotion.
- Independent audit frequency and the authority responsible for reauthorization or rollback.
