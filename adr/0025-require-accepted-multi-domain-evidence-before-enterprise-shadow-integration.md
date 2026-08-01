# ADR-0025: Require Accepted Multi-Domain Evidence Before Enterprise Shadow Integration

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Required external authorities: requirements authority, enterprise-risk authority, governance-source owner, enterprise-strategy authority, and domain acceptance authorities
- Depends on: ADR-0016, ADR-0020, ADR-0021, ADR-0022, ADR-0023, ADR-0024

## Context

One complete vertical remains accepted and operational. Four enterprise roles are now contract-complete candidates, but their live calibrations intentionally prove only isolated protocol and lineage handling. CAP-REQ still lacks an external acceptance disposition, the earlier product-synthesis semantic comparison still awaits authoritative adjudication, and ENT-ARCH, ENT-GOV, ENT-STRAT, and ENT-SYNTH do not have a complete independently accepted live multi-domain input set.

Connecting the candidates into a shadow enterprise chain now would be mechanically possible but semantically misleading. It could create a polished end-to-end artifact whose upstream evidence remains candidate-only, incomplete, or pending human action.

## Proposed decision

1. Do not schedule or connect the enterprise candidates into a shadow chain until a human-controlled enterprise-readiness manifest proves all required domain inputs are independently accepted, compatible, fresh, and scope-aligned.
2. Make unresolved external gates explicit prerequisites, including ADR-0016 semantic adjudication and ADR-0020 requirements acceptance where their artifacts are used.
3. Require each candidate role to receive a live multi-domain package appropriate to its authoritative question, followed by independent human semantic evaluation against its source domains.
4. Require acceptance records to bind exact artifact IDs and hashes, evidence tiers, scope, rubric, evaluator authority, disposition, limitations, and expiration or supersession state.
5. Prohibit protocol-smoke, fixture, candidate, or pending artifacts from satisfying an accepted-live readiness prerequisite.
6. After prerequisites pass, authorize only a comparison-only shadow workflow. It remains excluded from the authoritative report, leadership distribution, human decision recording, release, and deployment.
7. Define rollback before shadow execution: disable candidate workflow discovery, discard derived shadow state, retain immutable evidence, and continue the accepted `ENT-EVIDENCE -> ENT-SYSRISK` route unchanged.
8. Require differential comparison against the accepted path, domain-by-domain human adjudication, fail-closed partial execution, and a separate cutover ADR before any baseline scheduling change.
9. Keep production targeted to the A100 large cluster and conduct all readiness, shadow, rollback, integration, and regression testing on DGX Spark or an approved equivalent, currently GX-10.

## Alternatives considered

- **Connect the candidates now because all schemas and regressions pass:** rejected because contract fitness is not semantic or operational fitness.
- **Treat live protocol-smoke outputs as accepted domain evidence:** rejected because each calibration explicitly disclaims that level of fitness.
- **Use the synthetic multi-domain fixtures as readiness evidence:** rejected because fixtures prove mechanics only.
- **Continue adding downstream enterprise roles:** rejected because integration readiness is now the higher-risk architectural boundary.

## Consequences

The next work shifts from adding roles to closing evidence and human-acceptance gaps. Progress may depend on external reviewers, but the resulting shadow workflow will have a defensible provenance chain and a tested rollback path rather than merely complete wiring.

## Rollback

This ADR creates no scheduled workflow. If its readiness mechanism is removed, retain all acceptance packets and evidence for audit and leave every candidate unscheduled. The current accepted baseline, reports, governance records, and deployment state remain unchanged.

## Validation required

- exact readiness-manifest and external-acceptance bindings;
- no candidate/fixture/protocol tier promotion;
- prerequisite closure for every domain used by the shadow chain;
- independent semantic evaluation and immutable human records;
- fail-closed missing, stale, incompatible, superseded, partial, or unauthorized inputs;
- byte-identical accepted workflow, report, human-decision, and deployment state;
- tested disable/discard rollback to the accepted route; and
- local and GX-10 full regression before a separate shadow-integration authorization.

## Decision requested

Approve, reject, or amend the accepted-live multi-domain readiness gate. Approval would authorize readiness contracts, packets, and validation tooling only. It would not fabricate missing human decisions, schedule a shadow chain, promote a candidate, modify the report, or authorize A100 deployment.

## Decision

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes readiness contracts, blocked-state materialization, rollback validation, and conformance testing only. It does not satisfy an external prerequisite, promote evidence, schedule a shadow workflow, modify the report, or authorize deployment.
