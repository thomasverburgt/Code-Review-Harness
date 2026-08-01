# Accepted ADR-0012 Report Governance Evidence

This package records the accepted Increment 3 report-distribution and external-decision reconciliation boundary. All testing ran on the approved GX-10 DGX Spark-equivalent platform; the production target remains the A100 large cluster.

The complete five-gate regression passed: structural/semantic validation, vertical negative/runtime conformance, immutable artifact-ledger conformance, worker/adapter conformance, and the report-governance suite. The report-governance suite verifies deterministic self-contained packaging, review-copy markings, distribution-authority/recorder/verifier separation, exact report and item bindings, hashed external sources, independent verification, idempotency, mutation rejection, report preservation, and record-only effects.

The reference report package is `43ac6c58-2d9f-5465-91a5-b7ac00e75e8f`, with package hash `sha256:430233c423d65642bdebde1d9217517d7023bc2ddcc5dbbf89ebe361d9ceeb4a`. It contains seven stable finding, risk, CAPA, and recommendation items plus evidence statements and per-source confidence, coverage, conflicts, methodology, and limitations.

Evidence files:

- `gx10-report-governance-conformance.txt` — full five-gate GX output; SHA-256 `f17e504e0ca680484cfaf8bc5b185b047799bf12be82c3fd8d37c9af4159d574`.
- `gx10-report-governance-reference.txt` — deterministic materialization summary; SHA-256 `c32a9238833f6ac8c4208c23b75a7009dd7106a10da1ad0a07fc0263fa03f7e0`.
- `gx-reference-run.tar.gz` — GX-generated immutable ledger, exports, attestations, verifications, reconciliation, and summary; SHA-256 `7a14db2a2454baaa710f6c4c094486278acec13215f0ee1cbe45d519514c4a17`.
- `reference-run/` — locally materialized equivalent records for direct inspection.

All authorities and source hashes are synthetic test values. No production identity token, SSH credential, model credential, or live decision source is retained. Every governance effect is `record_only`.
