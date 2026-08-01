# Superseded Pre-Acceptance Increment 3 Design Evidence

> **Not an accepted operating model.** This package predates acceptance of ADR-0012 and tests a direct in-system human-decision inbox. It is retained for audit and design history only. The accepted model uses immutable report exports, off-system leadership and expert action, administrative recording, and independent verification.

This package records the technically passing pre-acceptance candidate run on the approved GX-10 DGX Spark-equivalent test platform. Passing tests do not confer architectural approval. The production deployment target remains the A100 large cluster.

All five suites passed with exit tuple `0,0,0,0,0`: structural/semantic validation, vertical negative/runtime tests, artifact-ledger tests, worker/rollback tests, and governance-runtime tests. The governance suite validates immutable human dispositions, exact source/request/gate binding, role-based authority, authenticated human-only submission, option binding, expiry, aging, partial-input visibility, confidence/coverage/conflict presentation, source-artifact immutability, and deterministic replay.

The synthetic gold request produced decision record `fecefd65-8152-541e-b851-ef5c54281bb0`, with canonical content hash `sha256:1ba3eb2f3624de68df5763ac2e21cbe7438ac502e2512e2a60a54f7a59d2d7a6`. The accepted live ENT-SYSRISK request produced inbox item `4c7a6c19-46be-5be3-8d64-88f566afb279` in `blocked_authority_mismatch`; no decision was permitted for that route.

Evidence files:

- `gx10-governance-conformance.txt` — five-suite output; SHA-256 `b65500ad174e194397096764162321be33c59f7965c43cb85a94897b38cc058a`.
- `gx10-governance-reference.txt` — reference-run summary; SHA-256 `f4282f0f0b41fab78c13231aab8d0e567b3861c78b20e97edaa94a54bc92ba69`.
- `gx10-governance-reference.tar.gz` — complete reference run and immutable ledger; SHA-256 `a71ecb8c4990a61a17177b19b50ae7a2bcc931005d9313a2a1c13784ecf11935`.
- `human-decision-record.json` — separate human disposition; SHA-256 `17d5bf57ffa3475acde1dddc708a1fa3ce759d06575f80e894588ebd6065a52f`.
- `blocked-live-inbox-item.json` — retained live authority mismatch; SHA-256 `a1633c5d9accb635d03251bd64b69c2375a00241b0e2779320ca88c657972b8f`.
- `decided-evidence-view.json` — decision-linked evidence presentation; SHA-256 `e9c30f49f5ffab244a27e00fa1b91febe2f2baee0748d88b967932bb493e35b9`.
- `final-inbox-view.json` — derived decided and blocked states; SHA-256 `8172dcfd8f535a68cf7483b7ddb4c8c01ddc7ba4a890ea1ddd4a0f0fe43bcbe6`.
- `summary.json` — retained identifiers and authority/effect assertions; SHA-256 `f3225d540cde603b313f619dbe976e7186f89e04cdf19c51501b8126d68b35c9`.

The test authority subjects are synthetic. No production account, identity token, SSH credential, or model credential is retained. Decision effects remain `record_only`; this increment performs no risk-system, exception, CAPA, release, promotion, or deployment mutation.
