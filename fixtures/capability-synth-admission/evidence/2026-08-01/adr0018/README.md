# ADR-0018 CAP-SYNTH Candidate Conformance

- Local structural validation and full suite: passed, 47 tests.
- GX-10/DGX Spark-equivalent structural validation and full suite: passed, 47 tests.
- Deterministic candidate file SHA-256: `19c1148b74cbb4d64d4c8fd401c741bb75bb806b3118c1849a8a2edfbb061f6f` (byte-identical locally and on GX-10).
- GX-10 conformance transcript SHA-256: `a43be4fcd02cee6cfe2478f558d1dd3d6181d4059d45767047a74a244615a0f5`.
- GX deterministic reference archive SHA-256: `321ae4279ddc61f01db3a3c2b459b1dfc9fed5cf0a3097c3f98c8fd67246dffe`.
- GX live-calibration summary SHA-256: `63ca45f9d5aa40922f7f519eb371f3de9cba3228db9cf8fc3daf406681587791`.
- GX live-calibration archive SHA-256: `8b67c30143db2e55b04dbe88e093877e69298a93746f23477d403929c1c4f343`.

The adjudicated multi-domain output is `contract_fixture_only`. The live accepted `CAP-RISK`-only output is `protocol_lineage_smoke_only`. Neither evidence tier schedules CAP-SYNTH or authorizes report, governance, deployment, or A100 production changes.
