# ADR-0012: Immutable Report Distribution and External Decision Reconciliation

- **Status:** Accepted
- **Date:** 2026-07-31
- **Accepted by:** project maintainer
- **Owners:** governance, report operations, identity, records administration, and audit
- **Scope:** Increment 3 report distribution and post-review reconciliation

## Decision record

Accepted by the project maintainer on 2026-07-31 after clarification of the operating model. The harness does not serve as the forum in which senior leaders and subject-matter experts exercise their decision authority.

## Context

The output of the code review harness is a report containing findings, recommendations, risks, CAPAs, evidence, confidence, coverage, conflicts, and uncertainty. A controlled review copy is taken off the system and presented to senior leadership. Once leadership approves the report for distribution, human experts review it and make decisions outside the harness. An administrator subsequently records those externally made decisions in the system.

The earlier candidate assumed decision authorities would submit dispositions directly through an in-system inbox. That does not match the approved workflow and conflates decision authority with administrative data entry.

## Decision

1. Freeze each completed review as an immutable report package bound to the exact source artifacts, report items, evidence references, version pins, and package hash.
2. Produce a controlled leadership-review export explicitly marked `not_approved_for_distribution`.
3. Record leadership's external distribution authorization as a source-backed attestation that distinguishes `approved_by` from `recorded_by`.
4. Generate an approved distribution export only after the distribution attestation passes authority, source, report-hash, and recorder checks.
5. Treat expert decisions as external decisions. An administrative record must distinguish the external `decided_by` authority or body from the authenticated `recorded_by` administrator.
6. Bind every recorded disposition to the exact report package and stable finding, recommendation, risk, or CAPA identifiers presented to the experts.
7. Require a decision-source reference and hash. Consequential records remain `recorded_pending_verification` until a different authorized records verifier confirms the source and binding in a separate immutable verification record.
8. Derive report, distribution, reconciliation, and verification status from immutable records. Never rewrite the original report or agent artifacts.
9. Keep all effects record-only. Downstream risk, exception, CAPA, release, promotion, or deployment state changes require separately authorized consumers.

## Authority separation

- Senior leadership or its named body approves distribution.
- Human experts or named decision bodies make substantive decisions outside the harness.
- A records administrator transcribes the external authorization or decision and attests that the entry reflects the cited source.
- A records verifier confirms consequential entries and must be a different subject from the recorder.
- Agents and orchestration components may generate, validate, package, route, age, and report; they cannot approve distribution, make expert decisions, or impersonate administrators.

## Consequences

- The system accurately represents the actual off-system leadership and expert workflow.
- An administrator's authentication proves who recorded the entry, not who made the substantive decision.
- Reports and decisions remain replayable and mutation-resistant.
- Draft review exports cannot be mistaken for distributable reports.
- Missing or unverifiable external source evidence remains visibly pending or rejected.
- Downstream systems must consume verified linked attestations rather than infer approval from report prose or administrative status.

## Validation required

- report packages reproduce byte-for-byte from pinned inputs;
- review exports remain marked not approved until a valid distribution attestation exists;
- distribution approver and administrative recorder identities remain distinct fields;
- expert authority and administrative recorder roles cannot substitute for one another;
- records without exact report/item bindings or source hashes fail closed;
- consequential entries require independent verification;
- identical entries are idempotent and changed entries cannot mutate accepted records;
- the report, findings, recommendations, evidence, confidence, coverage, conflicts, and uncertainty remain unchanged; and
- no record automatically changes an external governance or deployment system.

## Rollback plan

The boundary is additive and record-only. Rollback disables creation of new review exports, distribution attestations, external-decision attestations, and verification records. The harness returns to producing the immutable technical report and decision-support package from Increment 2. Existing packages and governance records remain retained and readable; none are deleted, rewritten, or converted into agent artifacts.

Rollback triggers include incorrect report contents or hashes, distribution of an unapproved export, conflation of decision-maker and recorder identity, unverifiable source evidence, mutable attestations, incorrect reconciliation status, or any unintended external effect. Re-enablement requires corrected schema/runtime pins, complete local and GX conformance, and a new maintainer decision if the authority model changes.

## Superseded pre-acceptance candidate

The direct in-system decision candidate and its initial GX evidence were produced before this ADR was accepted. They are retained only as design evidence and are not an approved operating model. The accepted implementation must replace that candidate with report packaging, external authorization attestation, administrative recording, and independent verification.
