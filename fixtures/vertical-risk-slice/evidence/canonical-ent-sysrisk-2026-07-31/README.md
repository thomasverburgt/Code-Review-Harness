# Canonical ENT-SYSRISK GX-10 Evidence

This package records the passing enterprise systemic-risk increment on the approved GX-10 DGX Spark-equivalent test platform. The production deployment target remains the A100 large cluster.

The run used model `Qwen/Qwen3-32B-FP8` at revision `aa55da1ecc13d006e8b8e4f54579b1ea8c3db2df`, generation contract `canonical-enterprise-systemic-risk-payload-1.0.0`, assembler `deterministic-envelope-1.1.0`, and projection `enterprise-systemic-risk-analytical-projection-1.0.0`. Its immutable inputs were accepted CAP-RISK artifact `a5ada795-db2f-5625-aed9-1b619411be17` and deterministic ENT-EVIDENCE gate `e18bbf4d-0308-5975-973e-4c731f4105cb`.

Result: `complete`. The model emitted 1,633 output tokens, the worker completed in 256,569 ms, and the worker-derived generation limit was false. The accepted content artifact hash was `sha256:06cabaf4305f6b281b0be78a9878c52bcee9bfa25a3f62048750e1c1d2520824`. The credential was injected ephemerally and was not written to retained evidence.

Evidence files:

- `gx10-canonical-ent-sysrisk-conformance.txt` — all four conformance suites, exit tuple `0,0,0,0`; SHA-256 `d6173d7afad6db758eb17047db26dc8d5b633269e983de28e61fec83b6101af5`.
- `gx10-live-canonical-ent-sysrisk.txt` — live calibration summary; SHA-256 `c3ed1045c65d656153202fb3e707ac19082807f1e76636a445f55b343102d9e8`.
- `canonical-ent-sysrisk-live-output.tar.gz` — raw response, canonical payload, assembly, telemetry, result, gate, artifact, and ledger records; SHA-256 `69b7e8e22c06b4c2be08d3304e26e2f1b8b49182becd87e7a5518564620bccd4`.
- `accepted-ent-sysrisk.artifact.json` — accepted enterprise artifact; artifact ID `7d9999b9-4188-592b-a3ca-1d939dbe2fa1`, declared output hash `sha256:5aded426e5604ea65a3622d0e92f5eecf134a3fb479631fa3daae3e3e56f20c5`, file SHA-256 `7a57525b1c79ac374e5cac9f0f5e8bc1fc5bd1e25a5d8bfda51a9a6ae3efb72b`.

The accepted artifact passed the unchanged universal, enterprise-layer, ENT-SYSRISK role, lineage, lifecycle, integrity-reference, and human-authority gates locally after retrieval. It preserves both input artifact IDs and hashes. Its systemic-risk register, escalation flags, treatments, and CAPAs are advisory; risk acceptance and treatment authorization remain separate human decisions.
