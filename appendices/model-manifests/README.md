# Model Manifests

The `gx10-qwen3-32b-spec-*-calibration-0.1.0.json` manifests pin the isolated ADR-0039 Increment 1 model boundary for `SPEC-DEPS`, `SPEC-SBOM`, and `SPEC-LINT`. They are GX-10/DGX Spark-equivalent comparison evidence only and carry no A100 production authority.

Model manifests pin the model identity, runtime, environment, limitations, and calibration context used by retained executions. Production targets the A100 large cluster; testing and calibration target DGX Spark or an approved equivalent.
ADR-0039 Increment 2 pins isolated GX-10 Qwen3-32B manifests for `SPEC-CONTAINER`, `SPEC-CICD`, and `SPEC-IAC`; these are comparison-only test bindings and do not authorize A100 production execution.
