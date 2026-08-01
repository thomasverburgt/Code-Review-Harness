# Vertical Risk Slice Fixtures

The gold package exercises:

`SPEC-SECRETS -> PROD-SEC -> CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK -> human decision request`

The live canonical chain now covers SPEC-SECRETS, PROD-SEC, CAP-RISK, a deterministic ENT-EVIDENCE gate, and ENT-SYSRISK. Each result is retained under its corresponding `evidence/canonical-*-2026-07-31/` package. The final enterprise output remains decision support. It is packaged into an immutable report; leadership authorization and expert decisions occur outside the harness and are later recorded as separate verified attestations.

The semantic review path contains the four designed review prompts. `ENT-EVIDENCE` is the mandatory enterprise input gate required by the Enterprise Agent Framework.

## Gold package

`gold/` contains five immutable agent artifacts and the final human decision request. The evidence is synthetic and includes no real credential value.

## Negative package

`negative/cases.json` defines mutations and adjudicated rejection reasons for identity, graph, dependency, artifact, lineage, schema, freshness, lifecycle, version, CAPA, authority, leakage, decision-link, and role errors.

## Validation

Run on NVIDIA DGX Spark or an approved equivalent test platform:

```powershell
python tools/validate_vertical_slice.py
python tools/test_vertical_slice.py
python tools/test_artifact_ledger.py
```

The test suite also exercises complete, authorized partial-input, retry-success, timeout-failure, and supersession-failure runtime scenarios and compares two deterministic replay outputs byte for byte.

The ledger suite persists a gold run, verifies every retained hash and audit-chain link, materializes a semantic replay, and rejects mutation, tampering, reordering, unauthorized access, and invalid supersession.

## Retained platform evidence

- [GX-10 conformance result, 2026-07-31](evidence/gx10-conformance-2026-07-31.txt) records the DGX Spark-equivalent platform identity, source hashes, suite outputs, timestamps, and zero exit status for all three gates.
- [GX-10 Increment 2 conformance result, 2026-07-31](evidence/gx10-increment2-conformance-2026-07-31.txt) records the four-suite worker/adapter gate, pinned vLLM image/model/revision, source hashes, and a live authenticated `qwen3-32b` smoke response with no credential export.
- [GX-10 live prompt calibration, 2026-07-31](evidence/live-prompt-calibration-2026-07-31/README.md) records four fail-closed live passes, redacted `uds-core` input evidence, telemetry/raw-response archives, and the deterministic-envelope recommendation.
- [ADR-0011 role-payload implementation evidence, 2026-07-31](evidence/adr11-role-payload-2026-07-31/README.md) records passing dual-mode rollback conformance and the remaining live payload-topology blocker.
- [Canonical enterprise systemic-risk evidence, 2026-07-31](evidence/canonical-ent-sysrisk-2026-07-31/README.md) records the deterministic evidence gate, passing four-suite GX conformance, live ENT-SYSRISK generation, exact two-input lineage, and human-only decision authority.
- [Pre-acceptance Increment 3 design evidence, 2026-07-31](evidence/governance-increment3-2026-07-31/README.md) records the superseded direct-decision candidate and is not evidence of the accepted ADR-0012 model.
- [Accepted ADR-0012 report-governance evidence, 2026-07-31](evidence/governance-increment3-report-reconciliation-2026-07-31/README.md) records the passing five-gate GX-10 run and deterministic report, distribution, external-decision, verification, and reconciliation records.
