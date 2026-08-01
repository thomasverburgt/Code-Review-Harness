# Report Distribution and External Decision Reconciliation Contract

The harness produces immutable decision-support reports. It does not approve those reports for distribution, host the substantive expert decision, or execute a recorded decision.

## Report package

A report package binds the complete accepted artifact chain, stable report-item identifiers, evidence references, findings, recommendations, risks, CAPAs, confidence, coverage, conflicts, uncertainty, versions, and a canonical package hash. Every source must be complete and schema-valid. Packaging must not rewrite an agent artifact.

## Controlled distribution

The first export is a leadership review copy and must be visibly marked `not_approved_for_distribution`. A distributable copy may be generated only after an administrator records leadership's off-system authorization and a separate records verifier confirms the authority, source, review-export, and report-hash bindings.

The distribution record keeps these roles distinct:

- `approved_by`: senior leadership or its named distribution authority;
- `recorded_by`: the authenticated records administrator who transcribed the approval; and
- `verified_by`: a different authenticated records verifier.

Authentication of the recorder proves who entered the record. It does not prove that the recorder made the substantive authorization.

## External expert decisions

Human experts receive the approved report and decide outside the harness. The administrative attestation must bind `decided_by`, the authenticated `recorded_by` administrator, a hashed authoritative source, the exact report package, and the exact finding, recommendation, risk, or CAPA identifiers considered.

The record remains `recorded_pending_verification` until a different authorized verifier confirms its source and authority bindings. Missing, ambiguous, out-of-scope, or unverifiable bindings fail closed.

## Immutability and effects

Reports, agent artifacts, attestations, and verification records are immutable. Exact replay is idempotent; changed content under the same identity is rejected. Reconciliation is a derived view that links records without modifying report items.

Every attestation and verification has `effect: record_only`. Risk, exception, CAPA, release, promotion, deployment, or other operational changes require separately authorized downstream consumers. Report prose, recommendations, administrative entry, and verified reconciliation are never themselves execution authority.

## Rollback

The boundary can be disabled without changing the Increment 2 technical report. Existing records remain retained and readable. Re-enablement requires corrected contracts, full local and DGX Spark-equivalent conformance, and a new maintainer decision if authority semantics change.
