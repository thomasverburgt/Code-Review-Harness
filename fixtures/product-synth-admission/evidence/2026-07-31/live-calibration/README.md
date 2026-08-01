# PROD-SYNTH Live Candidate Calibration

ADR-0014 authorizes candidate calibration but not baseline workflow scheduling. This package records two targeted `qwen3-32b` attempts on the GX-10/DGX Spark-equivalent test platform against the immutable accepted `PROD-SEC` artifact.

## Attempt 1 — failed closed

The model correctly copied the child artifact, finding, insight, and evidence identifiers, but also represented role-internal `CORRELATION-001` as a universal child conflict. The child contained no such conflict record. Exact lineage validation rejected the response, published no artifact, and returned the failure recorded in `failed-attempt-1-summary.json`.

The bounded correction added an explicit runtime allow-list of universal child records and instructed the model that role-internal correlation and hypothesis IDs are not preservable child records. No invalid response was rewritten or grandfathered.

## Attempt 2 — passed

- Status: `complete`
- Artifact hash: `sha256:bbb642801216bc347892d212440e5b23ec36a3863c83dea8e91a359e62693196`
- Model input/output: 8,642 / 1,754 tokens
- Wall duration: 264,198 ms
- Child artifact: `1e27ed34-d9a5-5309-a876-ab02af8b7d13`
- Preserved finding: `FINDING-001`
- Handoff state: `ready_for_capability_fan_in`
- Authority: human
- Consumer: `CAP-RISK`
- Candidate scheduled: no
- Baseline workflow changed: no

The full eight-gate GX-10 regression passed before the successful live request. `accepted-prod-synth.artifact.json` and `summary.json` are extracted review copies; the compressed output retains payload, assembly, gate, telemetry, result, raw response, queue, and ledger records.

## Retained file hashes

- `gx10-prod-synth-live-conformance.txt`: `e28c0a46669be861ae981223e707a6bef20e2d8c00200117b4b4754c596251f8`
- `gx10-prod-synth-live-output.tar.gz`: `a569ca54957460840e87b323f7e3bc0120cb344a8f749ad23dac0cde35041f8d`
- `accepted-prod-synth.artifact.json`: `684e1f742e8e75396fcd660500d804c805e96989b694343bce4a52c26c25d625`
