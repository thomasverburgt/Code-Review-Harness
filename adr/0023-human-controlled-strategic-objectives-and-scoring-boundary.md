# ADR-0023: Require Human-Controlled Strategic Objectives and Scoring Methods for ENT-STRAT Candidate Admission

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Required external authorities: enterprise-strategy authority and scoring-method owner
- Depends on: ADR-0006, ADR-0007, ADR-0012, ADR-0013, ADR-0020, ADR-0021, ADR-0022

## Context

ADR-0021 and ADR-0022 established isolated candidates for enterprise architecture and governance while preserving the accepted `ENT-EVIDENCE -> ENT-SYSRISK` baseline. The accepted sequence calls next for strategic scoring. `ENT-STRAT` must make evidence-supported alignment, readiness, resilience, and mission confidence transparent without allowing a model-selected formula or a visually persuasive score to become a decision.

The repository does not yet contain an authoritative strategic-objective and scoring-method input contract. Objectives, measure direction, normalization, weighting, missing-data treatment, aggregation, threshold context, and materiality are policy choices. Letting a model infer them would silently create strategy and could average away weak evidence, disagreement, or candidate-only inputs. Candidate `ENT-ARCH` and `ENT-GOV` artifacts also cannot be represented as accepted enterprise posture merely because their contract mechanics passed.

The current live vertical contains an accepted evidence gate and one accepted live capability-risk artifact. That is adequate for protocol and lineage calibration only. It is not enough to establish enterprise strategic-scoring fitness or produce a leadership-grade strategic confidence score.

## Proposed decision

1. Change `ENT-STRAT` from `planned` to `candidate` only after its full admission package passes.
2. Require every run to consume:
   - an exact validated `ENT-EVIDENCE` manifest;
   - the exact accepted or explicitly tiered enterprise posture artifacts named by that manifest;
   - a human-authored, content-addressed strategic-objective manifest; and
   - a human-authored, content-addressed scoring-method manifest.
3. Make the strategic-objective manifest the sole admission point for objectives, outcomes, measures, ownership, scope, applicability, approved directionality, and traceability to human strategy authority. The model cannot invent or revise an objective.
4. Make the scoring-method manifest the sole admission point for normalization, weights, aggregation, confidence treatment, missingness, uncertainty, sensitivity parameters, threshold context, and materiality. The model cannot choose weights, impute missing values, set thresholds, or silently reconcile disagreement.
5. Require explicit input-evidence tiers for every contributing posture: `accepted_live`, `candidate_live_protocol_only`, `adjudicated_fixture`, or `unavailable`. Candidate and fixture data must remain visibly separate and cannot contribute to an accepted-live strategic score.
6. Require objective-level scorecards, component distributions, sensitivity analysis, missing-data effects, disagreement records, provenance, and counterfactuals. A composite score may be emitted only when the authoritative scoring-method manifest defines it; otherwise the result remains multidimensional.
7. Prohibit false precision. Results must preserve uncertainty intervals and show whether rankings or conclusions change under authorized sensitivity ranges. Insufficient evidence remains missing or unknown and is never silently treated as zero, neutral, or compliant.
8. Require every score, distribution, and derived assertion to bind the exact objective, method, posture artifact, source evidence, confidence provenance, and unresolved disagreement. Missing, extra, stale, mutated, unauthorized, or mixed-tier inputs fail closed.
9. Separate evidence tiers:
   - a human-adjudicated synthetic multi-domain package proves scoring-contract, missingness, sensitivity, and traceability mechanics only;
   - the accepted live risk artifact plus authoritative objective and method manifests prove protocol and lineage handling only;
   - live enterprise strategic-scoring fitness requires a later accepted multi-domain enterprise posture set and independent human validation against real decision outcomes.
10. Keep all output advisory and comparison-only. `ENT-STRAT` cannot establish strategy, approve thresholds or weights, convert a score into a decision, accept risk, approve investment or modernization, authorize report distribution, schedule agents, authorize release, or authorize deployment.
11. Keep the accepted workflow, report package, ADR-0020 eligibility state, CAP-SYNTH schedule, ENT-ARCH schedule, ENT-GOV schedule, governance records, and deployment state unchanged.
12. Target production deployment to the A100 large cluster. Run all development, conformance, calibration, integration, security, rollback, and regression testing on a DGX Spark or approved equivalent, currently GX-10.

## Alternatives considered

- **Let the model derive weights and thresholds from the supplied artifacts:** rejected because that creates strategy and obscures the accountable human policy choice.
- **Publish one overall strategic score by default:** rejected because a scalar can conceal missingness, disagreement, sensitivity, and incomparable evidence tiers.
- **Treat candidate ENT-ARCH and ENT-GOV artifacts as accepted inputs:** rejected because candidate admission demonstrates bounded mechanics, not production or leadership-use fitness.
- **Train against prior human decisions immediately:** rejected because the current repository lacks a governed, representative, outcome-labeled calibration set and a leakage review.
- **Proceed directly to ENT-SYNTH:** rejected because synthesis should consume transparent domain postures and must not absorb scoring-policy authority.

## Consequences

The increment adds explicit strategy-authority and scoring-method preparation responsibilities. This is intentional: strategic scoring becomes reproducible and reviewable, while the model performs bounded mapping, calculation, explanation, and sensitivity analysis. Leadership receives distributions, missingness, and decision context rather than an unexplained recommendation disguised as a number.

## Rollback

Remove the ENT-STRAT candidate workflow from discovery, restore its registry status to `planned`, and retain prompts, schemas, manifests, fixtures, and calibration evidence for audit. The accepted `ENT-EVIDENCE -> ENT-SYSRISK` workflow, ENT-ARCH and ENT-GOV candidates, reports, governance records, CAP-REQ state, and deployment configuration remain unchanged. No A100 production migration is required.

## Validation required

- exact evidence-gate, enterprise-posture, objective-manifest, scoring-method, authority, and human-record bindings;
- strict universal, enterprise, and ENT-STRAT role schemas;
- deterministic projection, immutable ledger, and replay;
- complete objective-to-measure coverage with explicit evidence tiers and missingness;
- reproducible normalization, weighting, aggregation, confidence, sensitivity, and counterfactual calculations;
- fail-closed missing, extra, stale, mutated, unauthorized, mixed-tier, silently imputed, or invented inputs;
- no invented objectives, weights, thresholds, strategy, approvals, decisions, risk acceptance, report distribution, scheduling, release, or deployment authority;
- accepted baseline, report package, ADR-0020 state, ENT-ARCH schedule, and ENT-GOV schedule remain byte-identical; and
- full local and GX-10 regression plus isolated Qwen3-32B protocol calibration.

## Decision requested

Approve, reject, or amend the human-controlled strategic-objective and scoring-method boundary and isolated `ENT-STRAT` candidate admission. Approval would authorize implementation and testing only; it would not approve an objective, weight, threshold, strategic score, enterprise decision, report distribution, A100 deployment, or candidate scheduling.

## Decision

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes the bounded candidate implementation and isolated conformance testing only. It does not approve strategy, objectives, scoring policy, weights, thresholds, enterprise decisions, report distribution, scheduling, release, or deployment.
