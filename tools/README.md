# Harness Tools

This directory contains the current executable reference implementation and its tests.

| Kind | Naming | Purpose |
|---|---|---|
| Runtime | `*_runtime.py` | Deterministic contract and workflow behavior |
| Reference runner | `run_*_reference.py` | Produce bounded reference artifacts |
| Calibration | `calibrate_*.py` | Exercise controlled prompt/model boundaries |
| Validation and build | `validate_*`, `build_*`, `export_*` | Check or derive controlled repository artifacts |
| Tests | `test_*.py` | Standard-library unit and regression tests |

Run the current local gates from the repository root:

```text
python tools/check_repository_structure.py
python tools/validate_vertical_slice.py
python -m unittest discover -s tools -p "test_*.py"
```

The supported package boundary now lives under [`src/code_harness`](../src/code_harness/README.md), with package-boundary tests under [`tests`](../tests/README.md). For this compatibility release, package modules delegate to the unchanged implementations here. Existing commands and evidence paths therefore remain valid while consumers migrate.

## Specialist human-shadow calibration

ADR-0039 Increment 0 is implemented by:

- `specialist_shadow_calibration_runtime.py` — exact bindings, comparison-only validation, packet/response/metrics construction, and immutable persistence;
- `run_specialist_shadow_calibration_reference.py` — deterministic `SPEC-DEPS` fixture rehearsal and rollback demonstration; and
- `run_specialist_shadow_gx10_conformance.sh` — GX-10/DGX Spark-equivalent platform transcript and retained reference archive; and
- `test_specialist_shadow_calibration.py` — positive and fail-closed coverage, including all 22 registered specialist focus sources.

Run the bounded reference path with:

```text
python tools/run_specialist_shadow_calibration_reference.py
python tools/test_specialist_shadow_calibration.py -v
```

These tools do not invoke a model, schedule a specialist, admit a candidate, change product fan-in, or authorize deployment. A live GX-10 conformance run remains an Increment 0 exit criterion.

ADR-0039 Increment 1 adds `run_specialist_static_evidence_increment1.py` and `test_specialist_static_evidence_increment1.py`. They build and test independent deterministic `SPEC-DEPS`, `SPEC-SBOM`, and `SPEC-LINT` candidates and review packets. Model-backed GX-10 calibration remains a separate retained-evidence step.
`run_specialist_build_supply_chain_increment2.py`, `calibrate_specialist_build_supply_chain_increment2.py`, and `test_specialist_build_supply_chain_increment2.py` implement ADR-0039 Increment 2 for `SPEC-CONTAINER`, `SPEC-CICD`, and `SPEC-IAC`. They retain structurally reviewable packets while human review is deferred; no source repository mutation, deployment, or A100 authority is permitted.

`run_specialist_k8s_secure_increment34.py`, `calibrate_specialist_k8s_secure_increment34.py`, and `test_specialist_k8s_secure_increment34.py` implement ADR-0039 Increments 3 and 4 for the Kubernetes workload, Kubernetes platform, communications, secure-code, and redacted secrets-revalidation candidates. Role-specific fail-closed checks prevent static configuration from becoming runtime or exploitability claims, preserve the accepted SPEC-SECRETS route, and defer all human review.

`run_specialist_increment567.py`, `calibrate_specialist_increment567.py`, and `test_specialist_increment567.py` implement Increments 5-7 for the remaining 11 architecture, integration, data, model, resource, operability, performance, resilience, research, risk, and integrated-security candidates. `build_specialist_increment8_retrospective.py` and its test produce the all-22 comparison, explicit final-state register, retrospective, and consolidated human-review handoff without fabricating reviewer or adjudication results.
