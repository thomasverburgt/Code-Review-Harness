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
