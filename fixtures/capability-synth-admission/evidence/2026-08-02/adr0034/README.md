# ADR-0034 Accepted-Live CAP-SYNTH Evidence

`reference-run/` is the deterministic comparison package. It binds the exact accepted CAP-RISK artifact, live CAP-REQ artifact, owner-finalized CAP-REQ eligibility, CAP-COORD manifest, deterministic CAP-SYNTH candidate, enterprise compatibility record, semantic-review packet, and immutable ledger references.

`gx10-live-evaluation/first-attempt/` is a failed-closed credential-discovery attempt. It produced no candidate.

`gx10-live-evaluation/pre-lineage-tightening-attempt/` is a schema-valid model attempt retained because review exposed a stale deterministic derived-assertion ID in the harness-owned enterprise handoff. It is not the authoritative review candidate.

`gx10-live-evaluation/successful-run/` is the tightened Qwen3-32B result. Candidate artifact `0cbe961f-82da-5cf5-92bd-2674c07459ef`, output hash `sha256:32af60e0eb9ab3f397496abc4a55876ce4e7d8c97354c568841ac9f714fbe269`, and semantic-review packet hash `sha256:49b85c84b96ca7d148c067ddaf39cda7970c8008b2656a394b8af4e400d7447f` are the exact records awaiting project-owner semantic review.

`project-owner-semantic-disposition/` records the project owner's `accept_semantically_faithful` disposition, same-owner finalization under ADR-0033, and revocable eligibility for enterprise candidate evaluation. It does not create scheduling authority.

All material remains comparison-only. CAP-SYNTH and every enterprise candidate remain unscheduled. Reports, distribution, deployment, and the A100 production baseline are unchanged. Rollback revokes CAP-REQ or CAP-SYNTH evaluation eligibility or disables this candidate workflow while preserving all evidence and continuing `CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK`.
