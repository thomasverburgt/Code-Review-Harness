# ADR-0017 CAP-COORD Conformance

- Local structural validation and full suite: passed, 39 tests.
- GX-10/DGX Spark-equivalent structural validation and full suite: passed, 39 tests.
- Reference manifest file SHA-256: `b258935593be8c5e1ce8d6016719c0e0302f5f0d3e1a9821c4853c99881ebe30` (byte-identical locally and on GX-10).
- GX-10 transcript SHA-256: `7e8fb46668766f1fa2e8f881329d56b0dcfa848a7d42a8d9a3b40525e64a0bb6`.
- GX-generated reference archive SHA-256: `848a510c6d620f67dc0c89c10429722d763314593937736a045c2368318c325c`.
- Manifest semantic hash: `sha256:f3b575341961036adfebe25e8467ab0053ef916005e9516277846e9922e7a263`.

The reference is a `CAP-RISK`-only `single_domain_mechanical_calibration`. It proves deterministic coordination mechanics and exact dispatch binding; it does not prove multi-domain `CAP-SYNTH` quality or authorize scheduling, report changes, deployment, or A100 production promotion.
