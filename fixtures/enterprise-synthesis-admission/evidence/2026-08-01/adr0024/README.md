# ADR-0024 ENT-SYNTH Admission Evidence

Status: passed on 2026-08-01.

- Local and GX-10 structural validation: passed.
- Local and GX-10 regression: 102 tests passed.
- Deterministic artifact: `sha256:a4e16571a301637bcf3b090c20867fe319a629701c19c91dadfdd4031558d29f` locally and on GX-10.
- Live Qwen3-32B artifact: `sha256:08ce796d4bb85058dbbaff83c31785173258d613abc8bd358c70273e2d79385f`.
- Live raw response: `sha256:0bca7b3814655d5fd758e491df15fa1e842b63cc91dca5df658f5574628b8b91`.
- Live usage: 4,824 input tokens and 3,197 output tokens.
- GX reference archive SHA-256: `3c0358de21bc8789556bd18406987afc2b00a6a0ac983f1f221c049b8ecef1fc`.
- GX live archive SHA-256: `3b5c579221ada5939558456844d8c23530edf97d2e332313b4ce38725169532b`.

The live result claims only `mixed_tier_protocol_lineage_smoke_only`. ENT-SYNTH remains candidate, comparison-only, and unscheduled. The authoritative report and distribution state machine are unchanged.
