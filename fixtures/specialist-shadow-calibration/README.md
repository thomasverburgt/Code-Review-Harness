# Specialist Human Shadow Calibration Fixture

This scenario is the deterministic ADR-0039 Increment 0 reference rehearsal. It exercises the common specialist candidate and human-review boundary with `SPEC-DEPS` against the repository's pinned `pyproject.toml` evidence.

The fixture demonstrates:

- exact identity, contract, focus-profile, compiled-focus, prompt, schema, rubric, model, tool, repository, evidence, and access bindings;
- one comparison-only specialist candidate with observations, a finding, CAPA recommendation, positive pattern, and explicit unknown;
- exact immutable file, line, excerpt, and fingerprint locators for every review item;
- a schema-valid non-authoritative intern review response and mechanically derived metrics;
- immutable content-addressed persistence; and
- project-owner enable and revoke controls as the rollback path.

The human response is synthetic fixture data. It tests the response contract and metric derivation; it is not expert adjudication and does not establish correctness.

## Authority boundary

Everything in `gold/` is retained for specialist calibration only. Nothing here schedules an agent, changes the accepted vertical, enters product fan-in, contributes to a leadership report, approves distribution, authorizes deployment, or authorizes A100 production execution.

## Rebuild and test

From the repository root:

```text
python tools/run_specialist_shadow_calibration_reference.py
python tools/test_specialist_shadow_calibration.py -v
```

The reference output finishes in the revoked state. Delete-and-regenerate of this derived fixture is safe during development; retained live GX-10 evidence will use the governed evidence layout and will not be rewritten.

## Retained platform evidence

The passing Increment 0 GX-10 package is retained at [`evidence/2026-08-03/adr0039/increment-0/gx10-run-001`](evidence/2026-08-03/adr0039/increment-0/gx10-run-001/README.md). It reproduces the deterministic package on NVIDIA GB10 and closes the platform-conformance exit criterion without admitting or scheduling an agent.
