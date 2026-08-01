# Canonical SPEC-SECRETS GX-10 Evidence

This package records the first passing live prompt calibration through the canonical analytical-payload path on the approved GX-10 DGX Spark-equivalent test platform.

The run used model `Qwen/Qwen3-32B-FP8` at revision `aa55da1ecc13d006e8b8e4f54579b1ea8c3db2df`, generation contract `canonical-role-payload-1.2.0`, assembler `deterministic-envelope-1.1.0`, projection `specialist-analytical-projection-1.0.0`, and a declared one-file, one-candidate redacted `uds-core` slice at revision `329ade01852f9e570d31cb7b19d9979152938c17`.

Result: `complete`. The model emitted 872 output tokens, the worker completed in 132,803 ms, the worker-derived generation limit was false, and the accepted artifact hash was `sha256:361f52f224378973b5d1764b349c812bfa2357d7bba5d7d39da252837c1ba3a8`. The credential was environment-injected and was not exported.

Evidence files:

- `gx10-canonical-v12-conformance.txt` — all four conformance suites, exit tuple `0,0,0,0`; SHA-256 `3c64af8d09de3459befb9c7860adb41706f3145ac33c5a2b4f4631ba321ccf2a`.
- `gx10-live-canonical-spec-v12.txt` — live calibration summary; SHA-256 `da226a78495d6b4c68f5f5b9f365dc49f7f12d5be77a8df24fa38422d9cc0205`.
- `canonical-live-v12-output.tar.gz` — raw response, payload, assembly, telemetry, result, gate, artifact, and ledger records; SHA-256 `225000034df33d05379d0eb9a43114a088c2bbc557daf6e3182b32309c53004d`.
- `accepted-spec-secrets.artifact.json` — extracted immutable upstream artifact for downstream one-node calibration; artifact ID `85879acf-6be4-5637-9789-5aa5670c3c33`, declared output hash `sha256:aa48e2e0f3f2603d32ce9f97c7a775b7d07d50febb9abd083bd5844b0582e9c8`, file SHA-256 `767d5137cbff0228d9b2c4c89563825cdefc5e536e252af7bd2360fed376a6d9`.

This result calibrates only the declared slice and only SPEC-SECRETS. It is not a repository-wide security conclusion, measured A100 capacity, or approval to extend canonical projection to other roles.
