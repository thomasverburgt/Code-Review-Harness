# ADR-0015: Shadow Product Synthesis Before Baseline Cutover

- **Status:** Accepted
- **Date:** 2026-07-31
- **Owners:** product engineering, orchestration, capability risk, report operations, and governance
- **Scope:** Increment 5 `PROD-SYNTH` integration and promotion decision

## Context

ADR-0014 admitted `PROD-SYNTH` as an unscheduled candidate. Its identity, prompt, executable schema, deterministic projection, negative cases, capability handoff, local regressions, GX-10 regressions, and live `qwen3-32b` calibration now pass. The first live response failed closed because it treated a role-internal correlation ID as a universal child record; the corrected runtime exposed an explicit universal-record allow-list and the second response passed without weakening exact-lineage validation.

The accepted baseline routes `PROD-SEC` directly to `CAP-RISK`. Replacing that route immediately would change artifact lineage, downstream artifact IDs, the immutable report package, report-item bindings, and reviewer evidence packets simultaneously. A passing single live calibration is not sufficient evidence for that cutover.

## Decision record

Accepted by the project maintainer on 2026-07-31. Acceptance authorizes an isolated comparison-only shadow workflow and GX-10 testing. It does not authorize baseline cutover, report publication, governance reconciliation, or deployment effects from shadow artifacts.

## Decision

1. Introduce `PROD-SYNTH` in an isolated shadow workflow after the accepted `PROD-SEC` artifact.
2. Feed its capability handoff to a shadow `CAP-RISK` execution while the baseline `PROD-SEC -> CAP-RISK` route remains authoritative.
3. Keep shadow artifacts in a separate ledger namespace and prohibit them from report packaging, distribution approval, external decision reconciliation, deployment authorization, or baseline fan-in.
4. Compare baseline and shadow paths for preserved findings/evidence, added derived meaning, conflicts, CAPA semantics, risk statements, confidence provenance, coverage, report-item impact, determinism, latency, and resource cost.
5. Fail closed on any dropped or invented lineage, authority change, unresolved semantic divergence, or attempted shadow publication.
6. Require a later explicit cutover ADR before changing `WF-VERTICAL-RISK-001` or its report package.

## Shadow state model

`accepted_prod_sec -> baseline_cap_risk`

`accepted_prod_sec -> prod_synth_shadow -> cap_risk_shadow -> comparison_only`

Only the first path remains authoritative during this increment.

## Exit criteria

- exact preservation of all baseline product findings and evidence references;
- deterministic `PROD-SYNTH` and shadow `CAP-RISK` replay;
- no unauthorized report, governance, or deployment effect;
- explained and human-reviewed semantic differences between baseline and shadow capability risk;
- complete local and GX-10/DGX Spark-equivalent regression, failure, and rollback tests;
- measured latency/resource deltas with no claim that GX-10 capacity equals A100 production capacity; and
- a cutover recommendation that names remaining uncertainty and rollback triggers.

## Rollback plan

Disable and remove the shadow workflow registration. Retain its immutable artifacts, comparisons, telemetry, and failures for audit. The accepted baseline route and report package remain unchanged throughout, so rollback requires no artifact rewrite, report retraction, or decision-record migration.

## Implementation evidence and cutover recommendation

Implemented on 2026-07-31 as `WF-PROD-SYNTH-CAP-RISK-SHADOW-001` with a separate `shadow/adr-0015` comparison ledger, a schema-validated comparison record, deterministic replay, model-backed GX-10 execution, publication denial, semantic divergence blocking, and rollback tests.

The deterministic local and GX-10 reference paths were equivalent. All 24 repository regression tests passed locally and on the DGX Spark-equivalent GX-10. The model-backed `qwen3-32b` shadow CAP-RISK artifact also passed its schemas, exact child binding, human-authority, routing, and immutable-ledger gates in 258,695 ms. Its comparison correctly remained blocked because assessments, conflicts, and the risk register differed from the accepted baseline. The live path preserved findings, evidence, CAPA options, confidence, coverage, decisions requested, and exact PROD-SYNTH lineage.

Do not cut over the baseline yet. Human risk reviewers must adjudicate whether the added `DC-001` conflict, changed risk category (`secrets_exposure` to `security_exposure`), added `PRODUCT-ALPHA` dependency, and altered mission-effect and treatment language are acceptable derived meaning or semantic drift. A later cutover ADR must record that decision. Until then, shadow output remains comparison-only and cannot affect reports, governance, deployment, or the A100 production baseline.
