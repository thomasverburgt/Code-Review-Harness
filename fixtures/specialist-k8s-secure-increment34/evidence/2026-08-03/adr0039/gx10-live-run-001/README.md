# ADR-0039 Increments 3 and 4 GX-10 live calibration

- Local date: 2026-08-03
- Host class: GX-10 / approved DGX Spark-equivalent
- Host architecture: aarch64
- GPU: NVIDIA GB10
- Driver: 580.173.02
- Python: 3.12.3
- Model: qwen3-32b
- Source: `defenseunicorns/uds-core` at `329ade01852f9e570d31cb7b19d9979152938c17`
- Result: pass for `SPEC-K8S-WORKLOAD`, `SPEC-K8S-PLATFORM`, `SPEC-COMMS`, `SPEC-SECURE-CODE`, and `SPEC-SECRETS` revalidation
- Prior regression: Increment 1 (8 tests) and Increment 2 (9 tests) passed on GX-10 before inference
- Human review: deferred by project-owner direction
- Tokens: 13,530 input; 1,765 output
- Model phase: approximately 3 minutes 36 seconds from first completed role to final completed role
- Archive SHA-256: `4733af6737c6639d4e61bd3d7ea100552b76e29ad7376379a1421786b695c645`

Each response passed its strict role schema, admitted-evidence check, deterministic universal projection, locator packaging, role-specific evidence-tier controls, and comparison-only lifecycle controls. No candidate is scheduled, product-fan-in eligible, report eligible, deployed, or authorized for A100 production execution.

The `SPEC-SECRETS` run used only the accepted route's retained redacted detector record. No raw matched value was admitted. The retrieved and normalized evidence contains zero matches for the rotated key and zero restricted credential markers. The accepted SPEC-SECRETS prompt, role schema, canonical artifact, and retained reference evidence were not changed.

The source repository remained read-only. No branch, commit, push, issue, or pull request was created there. The strict raw role payloads were retained unchanged. They were deterministically re-enveloped after the reused calibration helper's legacy Increment 2 provenance labels were corrected; the resulting manifests, candidates, locators, packets, and hashes were revalidated and resealed by `reproject_specialist_increment34_evidence.py`.
