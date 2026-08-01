# ADR 0003: Specialists Do Not Decide

- **Status:** accepted
- **Date:** 2026-07-24
- **Decision authority:** project maintainer
- **Owners:** agent-contract and human-governance maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

Specialist agents have narrow technical expertise and direct access to bounded evidence. That makes them well suited to observe, assess, identify findings and patterns, propose CAPAs, and request decisions. It does not give them authority to make product, capability, enterprise, release, risk, exception, investment, or deployment decisions.

Conflating technical analysis with decision authority would allow a narrow reviewer to approve a broader system, obscure accountable human ownership, and turn model confidence into governance authority.

## Evidence

- The [Specialist Agent Contract](../contracts/specialist-agent-contract.md) limits `SPEC-*` agents to one bounded technical concern.
- The [Universal Agent Contract](../contracts/universal-agent-contract.md) requires every output to declare human decision authority and keep observations, assessments, recommendations, and decisions distinct.
- Product, capability, and enterprise synthesis roles correlate evidence within their declared scope but do not grant human approvals or accept risk.
- The [Human Decision Contract](../contracts/human-decision-contract.md) requires exact authority, scope, evidence, and immutable record bindings for decisions.

## Decision

Specialist agents observe and assess. They may publish evidence-backed findings, patterns, confidence, CAPA proposals, escalation requests, and questions for named authorities. They do not make or imply approval, acceptance, waiver, prioritization, release, risk, compliance, readiness, investment, deployment, or closure decisions.

Designated synthesis roles may create contract-authorized derived assertions, reconcile terminology through declared mappings, and produce decision support within their layer. They may not convert those functions into human governance authority.

Substantive decisions remain with the human role named by the applicable contract, policy, and state machine. Administrative recording and independent verification preserve the decision but do not replace the deciding authority.

## Alternatives considered

- **Allow specialists to approve within their domain:** rejected because domain approval could be mistaken for product or operational approval and would blur accountability.
- **Use confidence thresholds as automatic decisions:** rejected because confidence measures epistemic support, not delegated authority.
- **Let synthesis agents settle every specialist disagreement:** rejected because synthesis cannot overrule independent domain authority without an explicit human decision.
- **Prohibit specialists from recommending action:** rejected because evidence-backed recommendations and CAPAs are useful decision support when clearly bounded.

## Consequences

- Specialist prompts and schemas require explicit prohibited-authority language and named decision requests.
- Human gates remain visible even when technical confidence is high.
- Synthesis artifacts must distinguish derived posture from approval or acceptance.
- Administrative actions require authority checks and cannot fabricate an absent expert decision.
- Automation may route or record results only within separately approved policy boundaries.

## Traceability

- [Universal Agent Contract](../contracts/universal-agent-contract.md)
- [Specialist Agent Contract](../contracts/specialist-agent-contract.md)
- [Human Decision Contract](../contracts/human-decision-contract.md)
- [Specialist Agent Framework](../agents/specialists/specialist-agent-framework.md)
- [Integrated Agent Framework](../agents/integrated-agent-framework.md)
- [ADR 0012: Immutable Report Distribution and External Decision Reconciliation](0012-immutable-human-decision-boundary.md)

## Validation

- Prompt and artifact tests reject statements that grant prohibited approval or decision authority.
- Every decision request names the required human authority and exact decision context.
- Synthesis tests preserve source disagreements rather than silently resolving them.
- Decision state advances only from a schema-valid, authority-valid human record and required independent verification.
- Missing decisions remain pending, blocked, unknown, or not eligible rather than inferred.

## Unresolved matters

- Future delegation policies for narrowly defined, low-risk automated actions at higher maturity levels.
- Program-specific authority registries and assurance requirements outside the current fixture scope.
- User-interface conventions that make advisory language and authoritative decisions unmistakably different.
