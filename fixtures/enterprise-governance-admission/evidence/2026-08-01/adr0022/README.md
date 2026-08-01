# ADR-0022 ENT-GOV Admission Evidence

Status: passed on 2026-08-01.

- Local structural validation: passed.
- Local regression: 82 tests passed.
- GX-10 structural validation: passed.
- GX-10 regression: 82 tests passed.
- Deterministic fixture artifact: `sha256:36ba30c3a2ceb9fec5e84d1464f0165e12ec832655dc252516366ecb0c7e9f70` locally and on GX-10.
- Live Qwen3-32B protocol artifact: `sha256:71a20fc981654501e240838c9c59b43cfdad943fdc519e61477c7f11222e9a4b`.
- Live raw response: `sha256:0cf55f0c4cbdb1e5a46659f38fb617c91faaf55138f4aaf9077bac7dc2592887`.
- Live usage: 4,167 input tokens and 900 output tokens.
- GX reference archive: `gx10-reference.tar.gz`, SHA-256 `e12aeae19a864a5365578251776304e79285950658ba1a45d61bc4310064773a`.
- GX live archive: `gx10-live-calibration.tar.gz`, SHA-256 `80157a7b4b68e3e469f7250d25fea94bfe368b1bf835f4f5b4f1a1ee2407a7b8`.

The live result is `accepted_live_single_capability_source_protocol_smoke` and claims only `source_protocol_lineage_smoke_only`. ENT-GOV remains candidate, comparison-only, and unscheduled. It does not approve compliance, grant exceptions, accept risk, authorize report distribution, release, deployment, or change the accepted baseline.
