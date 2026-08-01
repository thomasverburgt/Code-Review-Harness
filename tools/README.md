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

Sprint 4 will move importable modules to a Python package and tests to a dedicated tree. Existing paths will remain as compatibility wrappers until local and GX-10 regression gates pass and a later sprint approves their removal.

