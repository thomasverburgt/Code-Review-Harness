# ADR-0039 Increment 1 Static-Evidence Specialists

This scenario builds independent comparison-only candidates for `SPEC-DEPS`, `SPEC-SBOM`, and `SPEC-LINT` against the immutable Code Harness revision `ada870cc7fc557a417f4215c8e60fbf3bee367d9`.

Each candidate has its own prompt, strict role schema, rubric, model manifest, least-privilege tool policy, focus binding, input manifest, artifact, exact locators, and human shadow-review packet. The shared source lines intentionally test semantic overlap without merging the roles:

- `SPEC-DEPS` assesses declared dependency constraint and graph-health limits;
- `SPEC-SBOM` assesses declared inventory identity and SBOM completeness limits; and
- `SPEC-LINT` assesses defined quality-rule evidence and refuses to call a gate passed without a completed execution record.

The packets are ready for non-authoritative human shadow review. They are not model-backed results or qualified adjudications yet. No candidate is admitted, scheduled, eligible for product fan-in or leadership-report use, deployed, or authorized for A100 production.

Run locally with:

```text
python tools/run_specialist_static_evidence_increment1.py
python tools/test_specialist_static_evidence_increment1.py -v
```

`negative/cases.json` records the retained fail-closed mutation classes exercised by the tests. GX-10 model calibration and human responses are later steps in the active increment.

The first passing model-backed GX-10 package and intern handoff are retained at [`evidence/2026-08-03/adr0039/gx10-live-run-001`](evidence/2026-08-03/adr0039/gx10-live-run-001/README.md). Human responses and qualified adjudication remain outstanding.
