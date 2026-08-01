# ADR-0015 Shadow Comparison Evidence

This directory retains comparison-only evidence for the isolated `PROD-SYNTH -> CAP-RISK` shadow path. Shadow artifacts have no report, governance, deployment, or baseline authority. The accepted baseline and immutable report package remained byte-for-byte unchanged; disabling this path is the rollback operation.

## Result

- Deterministic local and GX-10 paths are semantically equivalent to the accepted CAP-RISK baseline.
- The final local regression passed 24/24 tests.
- The final DGX Spark-equivalent GX-10 regression passed 24/24 tests.
- The model-backed `qwen3-32b` CAP-RISK shadow artifact passed contract and exact-lineage gates with artifact hash `sha256:7a656f870ac89abe53ecfd9e25082ea5e7d633a646922e96745ea3da706f2e63` in 258,695 ms.
- Its comparison is blocked for human review because `assessments`, `conflicts`, and `risk_register` differ. Findings, CAPA options, confidence, coverage, decisions requested, preserved evidence, and exact child binding remain intact.
- The failed first live attempt is retained: the runtime expected a nonexistent plural provenance key and accepted no artifact. The correction uses the registered singular `source_artifact_id`; no schema or lineage gate was weakened.

## Retained files

- `reference-run/` — corrected deterministic local artifact, comparison, summary, and isolated ledger.
- `gx10-shadow-final-conformance.txt` — final 24-test GX-10 log; SHA-256 `259ee9054e31ad24452ee15da5f311aaed25430c0c0e5388c15ba09da3868d36`.
- `gx10-shadow-evidence-final.tar.gz` — corrected deterministic GX-10 shadow output; SHA-256 `a749818908058943dae3365aeea8994fe8fd624926065975c141dafd09748068`.
- `gx10-live-shadow-attempt1-failed.tar.gz` — fail-closed first live attempt; SHA-256 `2cdafd3a81606a07283813025a4002a150217a6527c82d0cad1453c3318596b7`.
- `gx10-live-shadow-success.tar.gz` — accepted live artifact, payload, telemetry, gates, separate ledger, and blocked comparison; SHA-256 `05f6ffd17fb8e63d99000056b41ea579f72ce7a2ab6594b65041e83c4d63fdc3`.

GX-10 results demonstrate DGX Spark-equivalent test behavior only. They do not claim measured capacity for the A100 large-cluster production target.
