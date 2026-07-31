# Canonical PROD-SEC GX-10 Evidence

This package records the passing live PROD-SEC synthesis through the canonical analytical-payload path on the approved GX-10 DGX Spark-equivalent test platform.

The run used model `Qwen/Qwen3-32B-FP8` at revision `aa55da1ecc13d006e8b8e4f54579b1ea8c3db2df`, generation contract `canonical-product-payload-1.0.0`, assembler `deterministic-envelope-1.1.0`, projection `product-analytical-projection-1.0.0`, and the previously accepted live SPEC-SECRETS artifact as its immutable upstream input.

Result: `complete`. The model emitted 1,230 output tokens, the worker completed in 187,509 ms, the worker-derived generation limit was false, and the accepted artifact hash was `sha256:89bec57be37acf901a313aed1bea11363867d6a85180d8d237faf8195bdd62dc`. The credential was environment-injected and was not exported.

Evidence files:

- `gx10-canonical-product-conformance.txt` — all four conformance suites, exit tuple `0,0,0,0`; SHA-256 `39b743346c3343b3e25daa990cc4d97c4446589452483a276c6adc97915af29a`.
- `gx10-live-canonical-prod-sec.txt` — live calibration summary; SHA-256 `9bf8fcedd5db730923cc12a4c690c159d176ce3b7c430c6c2b79b4f01058ab03`.
- `canonical-product-live-output.tar.gz` — raw response, payload, assembly, telemetry, result, gate, artifact, and ledger records; SHA-256 `ec9734c19668090de384589b225155d902a6a307a7c49fb74046bedbdd313204`.
- `accepted-prod-sec.artifact.json` — immutable downstream input artifact; artifact ID `1e27ed34-d9a5-5309-a876-ab02af8b7d13`, declared output hash `sha256:073d9b9112933f0f482e80e9be57c34ea610759ac909260be1d176648a35c6e3`, file SHA-256 `0459a6a6f1c6e3f4df190795837599b91aaac1dc2ce8fe02359e9c85f8bcad7e`.

This result validates one declared live vertical chain segment, SPEC-SECRETS to PROD-SEC. It is not a release decision, repository-wide security conclusion, measured A100 capacity, or approval to promote CAP-RISK or enterprise roles.
