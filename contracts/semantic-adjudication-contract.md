# Shadow Semantic Adjudication Contract

This contract governs human review of semantic differences between an accepted baseline artifact and a comparison-only shadow artifact. It does not authorize workflow promotion.

## Request boundary

The harness may deterministically generate an immutable adjudication packet only from an exact blocked comparison and its exact baseline and shadow hashes. Every comparison dimension marked `different` must have one or more exact JSON-pointer deltas. Each delta presents both values, materiality, downstream consequence, allowed dispositions, and `block_cutover` as the unresolved default.

The request has `effect: review_request_only`. It cannot express approval, distribution authority, risk acceptance, workflow scheduling, report replacement, deployment authorization, or A100 production promotion.

## Human authority and recording

The `enterprise-risk-acceptance-authority` decides semantic meaning outside the harness. For every delta it selects exactly one disposition and supplies rationale. The response is bound to the exact packet hash and an authoritative external-source hash.

Under ADR-0012, a governance records administrator records the response and a different records verifier confirms its source, authority, packet, and delta bindings. Authentication of either administrator does not make that actor the semantic decision authority.

## Derived recommendation

The overall recommendation is deterministic:

- any `reject_semantic_drift` yields `reject_cutover`;
- otherwise any `insufficient_evidence` yields `insufficient_evidence`;
- otherwise any `require_normalization` yields `normalization_required`; and
- only accepted dispositions yield `eligible_for_cutover_review`.

Even `eligible_for_cutover_review` has `effect: record_only`. A later project-maintainer ADR, complete regression, report-impact analysis, and rollback verification are required before scheduling changes.

## Failure and rollback

Missing deltas, duplicate decisions, wrong authority, mutated hashes, inconsistent recommendations, or unverified sources fail closed. Disabling this boundary leaves ADR-0015 shadow isolation and the direct baseline unchanged. Existing packets and responses remain retained for audit.
