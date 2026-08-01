# ADR-0022: Require Authoritative Governance-Source Manifests for ENT-GOV Candidate Admission

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Required external authorities: governance-source-owner and applicable decision authority named by each source
- Depends on: ADR-0006, ADR-0007, ADR-0012, ADR-0013, ADR-0020, ADR-0021

## Context

ADR-0021 established truthful enterprise registry states and admitted `ENT-ARCH` as an isolated candidate. The accepted sequence calls next for enterprise governance. `ENT-GOV` must correlate obligations, applicability, evidence, exceptions, approvals, conflicts, and cross-capability consistency without creating policy or granting authority.

The repository contains governance documents, policy examples, contracts, findings, and decision records, but their presence alone does not make every statement an authoritative governance obligation for every reviewed capability. A model must not promote advisory prose, examples, evidence, findings, or inferred expectations into policy. Applicability is also a governed determination, not a similarity judgment.

The current executable vertical has an accepted `ENT-EVIDENCE` gate and one accepted live capability-risk artifact. This is sufficient for protocol and lineage calibration but not for a live cross-capability compliance conclusion. Synthetic multi-capability fixtures may exercise contract mechanics only.

## Proposed decision

1. Change `ENT-GOV` from `planned` to `candidate` only after its complete admission package passes.
2. Require every run to consume:
   - an exact validated `ENT-EVIDENCE` manifest;
   - the exact capability artifacts named by that manifest;
   - a human-authored, content-addressed governance-source manifest; and
   - any exception, waiver, approval, or prior human-decision records explicitly declared by that source manifest.
3. Make the governance-source manifest the sole admission point for obligations. Each entry must identify source ID, source type, authority, immutable version or revision, exact locator and content hash, effective date, lifecycle state, scope, applicability determination and authority, obligation class, required evidence, required approvals, exception process, retention rule, and conflicts or precedence that are already authoritative.
4. Classify supplied material as `authoritative`, `advisory`, `example`, or `evidence_only`. Only `authoritative` entries with an explicit applicable determination may generate compliance-matrix rows. The model cannot change classification or applicability.
5. Require `ENT-GOV` to distinguish `compliant`, `noncompliant`, `approved_exception`, `expired_exception`, `pending_approval`, `insufficient_evidence`, `conflicting_obligation`, and `not_applicable`. Missing evidence is not automatically noncompliance, and an exception is never inferred from silence.
6. Keep approvals and exceptions as immutable referenced human records. `ENT-GOV` may report their verified state and expiration but cannot grant, renew, revoke, or interpret them beyond the supplied authoritative record.
7. Require assertion-level traceability to governance source, obligation, applicability record, capability artifact, and exact evidence locator. Unsupported legal conclusions, implied policy, silent conflict resolution, and invented obligation or approval records fail closed.
8. Separate evidence tiers:
   - a human-adjudicated synthetic multi-capability governance package proves contract and matrix mechanics only;
   - the harness's own immutable governance sources plus one accepted live capability artifact prove source, protocol, and lineage handling only;
   - live cross-capability governance fitness requires a later accepted multi-capability set and independently accepted applicability determinations.
9. Keep output advisory and comparison-only. `ENT-GOV` cannot create policy, make legal determinations beyond supplied sources, approve compliance, grant waivers, accept risk, authorize release or report distribution, schedule agents, or authorize deployment.
10. Keep the accepted workflow, report package, ADR-0020 eligibility state, CAP-SYNTH schedule, ENT-ARCH schedule, governance records, and deployment state unchanged.
11. Target production deployment to the A100 large cluster. Run all development, conformance, calibration, integration, security, rollback, and regression testing on a DGX Spark or approved equivalent, currently GX-10.

## Alternatives considered

- **Let ENT-GOV extract obligations directly from arbitrary documents:** rejected because extraction would silently combine source discovery, authority classification, applicability, and assessment.
- **Treat repository governance prose as universally applicable:** rejected because repository scope does not establish applicability to every capability or external organization.
- **Use findings and recommendations as governance sources:** rejected because evidence and recommendations do not become obligations without an authoritative human-controlled source.
- **Proceed directly to ENT-STRAT:** rejected because strategic scoring should consume proven governance and architecture postures and must not absorb their source-boundary responsibilities.
- **Schedule ENT-GOV immediately after candidate validation:** rejected because candidate admission proves isolation and contract fitness, not production scheduling fitness.

## Consequences

The increment adds an explicit governance-source preparation responsibility for humans or trusted source-system integrations. This is deliberate: it makes authority and applicability visible and testable. The model receives a smaller, safer task—assess supplied obligations against supplied evidence—and downstream strategic and synthesis roles receive traceable governance states rather than ungrounded policy interpretations.

## Rollback

Remove the ENT-GOV candidate workflow from discovery, restore its registry status to `planned`, and retain prompts, schemas, source manifests, fixtures, and calibration evidence for audit. The accepted `ENT-EVIDENCE -> ENT-SYSRISK` workflow, ENT-ARCH candidate, reports, governance records, CAP-REQ state, and deployment configuration remain unchanged. No A100 production migration is required.

## Validation required

- exact ENT-EVIDENCE, capability-artifact, governance-source, applicability, exception, approval, and human-record bindings;
- strict universal, enterprise, and ENT-GOV role schemas;
- deterministic projection, immutable ledger, and replay;
- authoritative/advisory/example/evidence-only separation;
- complete obligation-to-capability matrix with explicit missingness semantics;
- source-located assertion, exception, approval, and conflict traceability;
- fail-closed missing, extra, stale, mutated, inapplicable, unauthorized, unverified, expired, or invented records;
- no policy creation, legal overreach, compliance approval, exception grant, risk acceptance, scheduling, report-distribution, release, or deployment authority;
- accepted baseline, report package, ADR-0020 packet, and ENT-ARCH scheduling state remain byte-identical; and
- full local and GX-10 regression plus isolated Qwen3-32B protocol calibration.

## Decision requested

Approve, reject, or amend the authoritative governance-source boundary and isolated `ENT-GOV` candidate admission. Approval authorizes implementation and testing only; it does not supply an external applicability determination, schedule ENT-GOV, approve compliance, grant an exception, or promote an A100 production workflow.

## Decision

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes the source-boundary implementation and isolated conformance testing only. It does not schedule ENT-GOV or constitute a compliance, exception, release, report-distribution, or deployment decision.
