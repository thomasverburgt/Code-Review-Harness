# ADR-0024: Separate Enterprise Synthesis from Domain Authority and Report Release

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Required external authorities: authorities attached to each accepted domain artifact; senior-leadership distribution authority remains external
- Depends on: ADR-0012, ADR-0013, ADR-0020, ADR-0021, ADR-0022, ADR-0023

## Context

The enterprise layer now has two accepted baseline roles (`ENT-EVIDENCE`, `ENT-SYSRISK`) and three isolated candidates (`ENT-ARCH`, `ENT-GOV`, `ENT-STRAT`). The next role in the accepted sequence is `ENT-SYNTH`. Synthesis is the first place where several domain narratives could be combined into a leadership-facing posture, so it creates a material risk of laundering candidate evidence into an authoritative conclusion, overriding a domain owner through prose, or bypassing the existing report-governance and distribution-approval state machine.

The harness output is ultimately exported for senior leadership, then returned to human experts and administrators for external decisions and recorded dispositions. `ENT-SYNTH` is therefore an analytical producer, not the report, publication, approval, or decision authority.

## Proposed decision

1. Admit `ENT-SYNTH` only as an isolated, unscheduled candidate after its full admission package passes.
2. Require an exact content-addressed synthesis-input manifest listing every domain artifact, content hash, designation, schema/version, freshness, compatibility, evidence tier, authority owner, unresolved conflicts, and permitted synthesis use.
3. Preserve input tiers without promotion: `accepted_live`, `candidate_live_protocol_only`, `adjudicated_fixture`, and `unavailable`. Candidate and fixture material may appear only in visibly labeled comparison sections and cannot support an accepted enterprise conclusion.
4. Preserve domain authority. ENT-SYNTH may correlate and summarize but cannot rewrite, downgrade, close, resolve, or supersede ENT-SYSRISK, ENT-ARCH, ENT-GOV, ENT-STRAT, capability findings, human decisions, or their missingness and disagreement states.
5. Require assertion-level contribution maps. Every synthesized statement must identify exact source artifacts, source assertions, evidence tiers, evidence references, confidence provenance, transformations, uncertainty, and unresolved disagreement.
6. Separate direct quotation/normalization from derived correlation. Terminology normalization must retain the source term and cannot change meaning. Cross-domain correlations must be marked derived and cannot create a new obligation, objective, score, risk disposition, architecture approval, or decision.
7. Require explicit completeness and compatibility states. Missing required domains, mixed scopes, stale inputs, incompatible versions, duplicate artifacts, or unresolved manifest mismatches fail closed or produce an explicitly incomplete candidate artifact; they never disappear into narrative.
8. Keep report packaging and distribution outside ENT-SYNTH. Candidate output cannot enter the authoritative review report, replace its findings, mark it ready for leadership, record an expert decision, record an administrative disposition, or approve distribution.
9. Separate evidence tiers:
   - an adjudicated synthetic multi-domain package proves synthesis, conflict, tier, and traceability mechanics only;
   - the accepted live systemic-risk artifact plus candidate protocol artifacts prove mixed-tier protocol handling only;
   - live enterprise-synthesis fitness requires a later complete set of independently accepted domain artifacts and human semantic evaluation against the source domains.
10. Keep output advisory and comparison-only. ENT-SYNTH cannot accept risk, establish strategy, approve compliance, architecture, investment, modernization, release, report distribution, agent scheduling, or deployment.
11. Preserve the accepted workflow, report package, ADR-0020 state, candidate schedules, governance records, and deployment state.
12. Target production deployment to the A100 large cluster; run all testing on DGX Spark or an approved equivalent, currently GX-10.

## Alternatives considered

- **Let ENT-SYNTH consume every available enterprise artifact without tiers:** rejected because availability does not establish authority or fitness.
- **Make ENT-SYNTH the report generator:** rejected because analytical synthesis and governed publication have different contracts and human gates.
- **Allow narrative resolution of disagreements:** rejected because fluency is not decision authority.
- **Schedule candidates together as a complete enterprise workflow:** rejected because isolated admission does not establish end-to-end semantic fitness.
- **Proceed to portfolio or modernization roles first:** rejected because those roles should consume a proven, provenance-preserving enterprise synthesis boundary.

## Consequences

Enterprise synthesis gains a strict manifest and contribution graph. Leadership-facing prose remains downstream of the existing report package and human distribution gate. This adds visible tier and conflict metadata, but prevents a polished summary from silently changing the authority of its sources.

## Rollback

Remove the ENT-SYNTH candidate workflow from discovery, restore its registry state to `planned`, and retain prompts, schemas, manifests, fixtures, and evidence for audit. All baseline roles, candidate roles, reports, governance records, human-decision states, and deployment configuration remain unchanged. No A100 migration is required.

## Validation required

- exact gate, input-manifest, domain-artifact, authority, tier, scope, version, freshness, and conflict bindings;
- strict universal, enterprise, and ENT-SYNTH schemas plus deterministic projection and immutable replay;
- complete assertion-level contribution maps and source-term-preserving normalization;
- fail-closed missing, extra, duplicate, stale, mutated, incompatible, mixed-scope, tier-promoted, or invented inputs;
- domain findings, confidence, disagreement, missingness, and human records remain unchanged;
- no report publication, distribution approval, expert decision, administrative disposition, risk acceptance, strategy, compliance, architecture, investment, scheduling, release, or deployment authority;
- accepted baseline, report, ADR-0020 state, and all candidate schedules remain byte-identical; and
- full local and GX-10 regression plus isolated Qwen3-32B mixed-tier protocol calibration.

## Decision requested

Approve, reject, or amend the provenance-preserving enterprise-synthesis and report-release boundary. Approval would authorize isolated candidate implementation and testing only; it would not schedule ENT-SYNTH, accept any candidate domain posture, alter the leadership report, approve distribution, record a human decision, or authorize A100 deployment.

## Decision

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes isolated candidate implementation and testing only. It does not schedule ENT-SYNTH, promote any input tier, modify or publish a report, approve distribution, record a human disposition, or authorize deployment.
