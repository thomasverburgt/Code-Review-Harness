# ADR-0039 Increment 0 GX-10 Conformance

- **Result:** pass
- **Execution window:** 2026-08-03T16:02:39Z to 2026-08-03T16:02:40Z
- **Test platform:** GX-10, approved DGX Spark-equivalent
- **Architecture:** `aarch64`
- **GPU:** NVIDIA GB10
- **Python:** 3.12.3
- **Source base:** `ada870cc7fc557a417f4215c8e60fbf3bee367d9` plus the recorded ADR-0039 Increment 0 working-tree overlay
- **Reference archive SHA-256:** `f3c4458c9c7bb40a77594878ee65b731dae7c219da56d62e38528b397d81e1ee`

## Passed gates

- deterministic reference generation and project-owner revoke control;
- all 11 specialist human-shadow calibration positive and fail-closed tests;
- all 22 registered specialist focus profiles and source specifications exactly resolved;
- repository structural validation;
- vertical workflow and state-machine validation;
- package-boundary tests; and
- artifact-catalog verification.

The complete command output and controlled-source hashes are in `gx10-conformance.txt`. `reference-run/` is the unpacked GX-10 output, and `reference-run.tar.gz` is its retained transport archive.

## Authority and limitations

This evidence closes the platform-conformance criterion for ADR-0039 Increment 0 only. The included human review response is synthetic fixture data used to prove schema and metric behavior. It is not qualified semantic adjudication, does not establish candidate correctness, and does not make `SPEC-DEPS` candidate-complete.

The final control state is revoked. No specialist is scheduled, no artifact is eligible for product fan-in or a leadership report, and no deployment or A100 production authority is created.
