# ADR-0011 Role-Payload Implementation Evidence — 2026-07-31

## Outcome

The rollback-capable deterministic envelope implementation passed the complete GX-10 conformance gate. The legacy `full_artifact` path and the new `role_payload_v1` path both replaced all four fixture nodes successfully. Deterministic assembly replay was byte-identical; attempted model control of harness-owned identity was rejected; disclosed cardinality truncation produced `incomplete_input` and published no artifact.

Live `qwen3-32b` calibration did not yet pass. The retained targeted attempts established that the current generation payload topology remains too broad:

- unbounded role payload: SPEC-SECRETS exceeded the 900-second worker timeout;
- array-bounded payload: generation was manually stopped after ten minutes without completion;
- `role-payload-1.2.0`, 2,048 tokens: completed in 327,085 ms but returned JSON truncated at the token ceiling;
- `role-payload-1.2.0`, 3,072 tokens: completed in 485,840 ms but returned JSON truncated at the token ceiling; and
- `role-payload-1.3.0`, 3,072 tokens with 256-character strings: completed in 489,497 ms but again returned JSON truncated at the ceiling.

No live payload reached deterministic assembly, and no live artifact or gate was published. The next correction is generation-payload topology reduction: eliminate duplicated analytical fields across the universal and layer representations, generate one canonical analytical form, and deterministically project it into the unchanged final schemas.

## Rollback readiness

- `full_artifact` remains the default compatibility mode when generation fields are absent from a job.
- `role_payload_v1` requires exact generation-contract and assembler version pins.
- Both modes publish the same universal artifact contract and share final semantic validation.
- Telemetry records generation mode, generation-contract version/hash, and assembler version.
- Role-payload executions retain raw payload and assembly records separately.
- The last ADR-0010 fixture path remains green on GX-10.

## Evidence integrity

- `adr11-gx10-conformance.txt`: SHA-256 `f3ae2cca65ea32a79ffe5daaf20144caca46d3e38a7f955791afe675c83bfa55`
- `adr11-live-calibration-outputs.tar.gz`: SHA-256 `2a537ed48e3d83e9fe6808d3e1e84d5b8d8b654b3473bce1b369cbc15eb255b3`

The live archive contains failed or partial worker outputs and raw model responses produced only from controlled or redacted evidence. No service credential is included.
