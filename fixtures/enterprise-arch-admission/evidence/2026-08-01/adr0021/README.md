# ADR-0021 ENT-ARCH Candidate Admission

- Local structural validation: passed.
- Local full suite: passed, 72 tests.
- GX-10 structural validation: passed.
- GX-10 full suite: passed, 72 tests.
- Deterministic candidate artifact ID: `317c84a1-5b31-58b2-8c42-7ae55a83f62a`.
- Deterministic semantic output hash: `sha256:53db3f93acf6889f54b59dfd79047a6936be5305952d3b0cd02fe54746d85f84`.
- Deterministic candidate file SHA-256: `6a261c3068a9758b42de5c01fc7ae9080be23324b6852731baa29ea3dbb75f10`.
- Deterministic ledger object hash: `sha256:a8638f6793134dc7b22ce9c95d7b69d9e4de66dc8e46a21c36fa8aa1fb2c3cd6`.
- Live candidate artifact ID: `437695da-050f-58dc-afb3-fe791b81672b`.
- Live semantic output hash: `sha256:1eb47f0e14ebff14103f6e2af68f6e448082860dc2ae32fd95b3251a159323b1`.
- Live raw-response SHA-256: `de4cb07916dc1e21e48d75175c015c8ce1f4e218e8c3db3c96c1b8366a90a475`.
- GX conformance transcript SHA-256: `28c5a02b381b22953c90a74dca9538da91bba0d0b2b278f104c1452a7355e649`.
- GX live-calibration transcript SHA-256: `4881000cdee618cfc18528ca0dcdf61a5f0548a5672760c8c2afd4dc3266787`.
- GX reference archive SHA-256: `aed29d0384eaa58ac31913dc7259518d7de669b8f6c4ab1be6191be71ece9d12`.
- GX live archive SHA-256: `c942d8fe9a16dfbb5d5b0ee62a50a3fbd49f7ce8be345e1b23b283d744e90991`.

The deterministic two-capability package is an adjudicated synthetic contract fixture, not production fitness evidence. The live Qwen3-32B run used one accepted capability input and is explicitly limited to `protocol_lineage_smoke_only`. It consumed 3,800 input tokens and produced 842 output tokens.

ENT-ARCH remains candidate, comparison-only, and unscheduled. The accepted `ENT-EVIDENCE -> ENT-SYSRISK` workflow, immutable report package, ADR-0020 requirements gate, CAP-SYNTH schedule, and deployment state are unchanged. Production targets the A100 large cluster; all testing occurred on the GX-10 DGX Spark equivalent.
