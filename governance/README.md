# Governance

This area contains architecture decisions, automation maturity and human-review gates, and cross-boundary governance material.

The executable Increment 3 boundary is documented in [Report Governance and External Decision Reconciliation](../orchestration/human-review-and-governance.md), with the versioned test authority registry under `appendices/governance/`.

ADR-0020 adds the [CAP-REQ Human Acceptance Contract](../contracts/requirements-acceptance-contract.md). The requirements authority decides whether the bounded review is complete, a separate governance verifier checks the immutable record, and the harness derives eligibility without asserting satisfaction, readiness, risk acceptance, scheduling, report distribution, or deployment approval.
