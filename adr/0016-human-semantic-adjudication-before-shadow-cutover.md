# ADR-0016: Human Semantic Adjudication Before Shadow Cutover

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: capability risk, product engineering, orchestration, report operations, and governance
- Supersedes: none
- Superseded by: none

## Context

ADR-0015 introduced the comparison-only `PROD-SYNTH -> CAP-RISK` shadow path. Its deterministic replay is equivalent to the accepted baseline, but its model-backed GX-10 run produced a schema-valid and exactly bound CAP-RISK artifact with unresolved semantic differences in assessments, conflicts, and the risk register. The harness must not silently decide whether those changes are useful synthesis, acceptable normalization, or semantic drift.

## Evidence

- accepted baseline CAP-RISK artifact `a5ada795-db2f-5625-aed9-1b619411be17`;
- accepted shadow PROD-SYNTH artifact `089b3a2a-cf18-52c3-afc1-545feab8e03d`;
- live shadow CAP-RISK artifact `2cd0b5e6-0f65-521a-93bf-c813f3b85ab8`;
- blocked comparison `571e8285-7051-51ab-a53e-ad8de1ea7832`;
- 31/31 local and GX-10 regression tests, including the dedicated record-only state machine; and
- unchanged authoritative workflow and report package.

## Decision record

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes the immutable, record-only semantic adjudication boundary. It does not adjudicate any delta, authorize baseline cutover, change a report, approve deployment, or promote the A100 production workflow.

## Decision

1. Generate an immutable semantic-adjudication packet from exact baseline, shadow, and comparison hashes.
2. Present every material delta with its JSON location, both values, downstream consequence, and allowed human dispositions.
3. Require the `enterprise-risk-acceptance-authority` to adjudicate semantic meaning outside the harness.
4. Require an authenticated administrator and independent verifier to record that external decision under ADR-0012 controls.
5. Keep every request and response `record_only`; neither may schedule `PROD-SYNTH`, replace CAP-RISK, alter a report, authorize deployment, or approve A100 production promotion.
6. Allow a later cutover ADR only when every delta is accepted, normalized and retested, or explicitly waived by the named authorities with evidence.

## Alternatives considered

- Treat schema validity as semantic equivalence: rejected because structural validity does not establish risk meaning.
- Automatically normalize the live artifact to the baseline: rejected because it would conceal model behavior and erase review evidence.
- Promote and rely on rollback: rejected because report lineage and leadership decision support would change before semantic review.
- Reject `PROD-SYNTH` immediately: premature because preserved lineage and several semantic dimensions already pass.

## Consequences

Cutover remains slower but auditable. Reviewers receive precise differences instead of comparing full artifacts manually. A record-only adjudication can support a later maintainer decision but cannot become operational authority. Unresolved or missing decisions keep the shadow path blocked.

## Rollback

Disable semantic-packet generation and retain existing request records. ADR-0015 shadow isolation and the direct `PROD-SEC -> CAP-RISK` baseline remain unchanged; no report, decision, or artifact migration is required.

## Validation

- deterministic packet and response-template generation;
- exact source hashes and JSON-pointer resolution;
- complete coverage of every comparison dimension marked different;
- rejection of invented, omitted, mutated, or unauthorized decisions;
- byte-for-byte baseline and report preservation; and
- full local and DGX Spark-equivalent conformance before ADR acceptance.

## Unresolved matters

The human authority has not yet classified the live semantic deltas. Acceptance of this ADR is not a substitute for that adjudication and does not recommend cutover.

## Proposal validation evidence

The deterministic reference packet contains seven exact deltas covering all three differing dimensions and has hash `sha256:3d87fb628ee30a280c60fc564ba9b365b6225a02119654c1059ef300fa5e9810`. The expanded local and DGX Spark-equivalent GX-10 suites each pass 31/31 tests. Baseline workflow, report package, deployment state, and A100 production configuration remain unchanged.
