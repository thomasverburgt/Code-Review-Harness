# Canonical CAP-RISK GX-10 Evidence

This package records the passing live CAP-RISK review through the canonical analytical-payload path on the approved GX-10 DGX Spark-equivalent test platform.

The run used model `Qwen/Qwen3-32B-FP8` at revision `aa55da1ecc13d006e8b8e4f54579b1ea8c3db2df`, generation contract `canonical-capability-risk-payload-1.0.0`, assembler `deterministic-envelope-1.1.0`, projection `capability-risk-analytical-projection-1.0.0`, and the previously accepted live PROD-SEC artifact as its immutable upstream input.

Result: `complete`. The model emitted 1,790 output tokens, the worker completed in 272,544 ms, the worker-derived generation limit was false, and the accepted artifact hash was `sha256:d691b498eb96556d2c5d3a68f675eaa814b425fa8c1e73e91b6cf5eede475dd5`. The credential was environment-injected and was not exported.

Evidence files:

- `gx10-canonical-cap-risk-conformance.txt` — all four conformance suites, exit tuple `0,0,0,0`; SHA-256 `4c7eedce01c1e4163343eeb5157267939bc4e5bd91211494551e86eaf4bf7ae3`.
- `gx10-live-canonical-cap-risk.txt` — live calibration summary; SHA-256 `c3389de741e5d3f7b376d873a8e17e0160917eeb5c05ae5bfd98b5913603cc3f`.
- `canonical-cap-risk-live-output.tar.gz` — raw response, payload, assembly, telemetry, result, gate, artifact, and ledger records; SHA-256 `4743ab6787015f5b6bb788139b41ab34acbd47a964426304b21cbb441d2b678a`.
- `accepted-cap-risk.artifact.json` — immutable enterprise input artifact; artifact ID `a5ada795-db2f-5625-aed9-1b619411be17`, declared output hash `sha256:b56be7afa96e29b2106b8faad851688844b1bcfdbb9b706c3d1ffcbfd57ed783`, file SHA-256 `6e7381d2dad28eea4cce10f607e12f929e53e9d173a039284284d1953ed2603a`.

The deterministic follow-on gate is retained as `accepted-ent-evidence.artifact.json`: artifact ID `e18bbf4d-0308-5975-973e-4c731f4105cb`, declared output hash `sha256:85037cc5398e9c6ccef05474fe855e7a557c45437b7e4adb5c1f8ef1f472b124`, and file SHA-256 `b17bfd4b3b76627311c283616e496f9d8db5e8caad213f351eb48e16d323123d`. It is deterministically bound to the accepted CAP-RISK artifact ID and output hash.

This result validates the live chain through `SPEC-SECRETS -> PROD-SEC -> CAP-RISK`. Risk records, priorities, treatment options, and escalation flags remain decision support; no risk was accepted or disposed. This is not measured A100 capacity or approval to promote enterprise roles.
