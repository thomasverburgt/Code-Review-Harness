# ADR-0039 Increment 2 GX-10 Live Calibration

- Local date: 2026-08-03
- Remote start: 2026-08-04T00:40:55Z
- Host class: GX-10 / approved DGX Spark-equivalent
- Host architecture: aarch64
- GPU: NVIDIA GB10
- Driver: 580.173.02
- Python: 3.12.3
- Model: qwen3-32b
- Source: `defenseunicorns/uds-core` at `329ade01852f9e570d31cb7b19d9979152938c17`
- Result: pass for `SPEC-CONTAINER`, `SPEC-CICD`, and `SPEC-IAC`
- Human review: deferred by project-owner direction
- Archive SHA-256: `63ebb593d1552c16969168dd9982247704968c6498ed63a4fddc6e61bcde3e24`

All nine Increment 2 fail-closed tests passed on the GX-10. Each model response passed its strict role schema, admitted-evidence check, deterministic universal projection, evidence-locator packaging, and comparison-only lifecycle controls. No candidate is scheduled, product-fan-in eligible, report eligible, deployed, or authorized for A100 production execution.

The first transport attempt failed before inference because a Windows carriage return entered the authorization header. The failed temporary run and package were purged and were not retained because the underlying library error included credential material. The adapter now strips surrounding transport whitespace, rejects remaining control characters, and the calibration scripts redact credential and bearer material from retained diagnostics. The successful retained package has zero matches for credential-marker patterns.

The cloned UDS Core worktree was read-only and remained unmodified. No branch, commit, push, issue, or pull request was created in that repository. Remote run directories, input packages, output packages, and streamed credential state were removed after result retrieval.
