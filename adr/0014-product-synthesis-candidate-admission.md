# ADR-0014: Product Synthesis Candidate Admission Before Scheduling

- **Status:** Accepted
- **Date:** 2026-07-31
- **Owners:** product engineering, orchestration, contract governance, and validation
- **Scope:** Increment 5, first agent-expansion slice

## Context

The reference vertical currently routes `PROD-SEC` directly to `CAP-RISK`. The architecture defines `PROD-SYNTH` as the product fan-in authority for coherent engineering state, but the role has no executable role schema, candidate prompt, independent gold package, or negative admission suite. Scheduling it before those controls exist would insert an unvalidated semantic transformation into a proven vertical.

## Decision record

Accepted by the project maintainer on 2026-07-31. Acceptance authorizes candidate contract validation and live-model calibration on GX-10/DGX Spark-equivalent infrastructure. It does not promote or schedule `PROD-SYNTH` in a baseline workflow.

## Decision

1. Admit `PROD-SYNTH` as a registered candidate with a dedicated specification, executable role schema, pinned candidate prompt, gold artifact, and negative cases.
2. Require complete declared child inventory, exact immutable lineage, preserved child findings and evidence references, explicit cross-domain derivation, unresolved-conflict preservation, and a capability handoff.
3. Keep release, risk, exception, CAPA closure, and promotion authority human. Product posture and readiness content remain advisory inputs.
4. Keep the candidate unscheduled in `WF-VERTICAL-RISK-001` until compatibility tests prove that capability consumers can receive its artifact without loss of product-security meaning or evidence lineage.
5. Promote or schedule the candidate only through a later explicit decision after live-model calibration and downstream fan-in validation.

## Consequences

- Product synthesis gains an executable admission boundary without destabilizing the accepted vertical.
- Capability agents receive a normalized product handoff instead of needing to infer relationships among product-domain outputs.
- The direct `PROD-SEC -> CAP-RISK` route remains the rollback path until scheduling is separately approved.

## Validation required

- candidate identity and prompt hash match their registries;
- gold artifact passes universal, product, and `PROD-SYNTH` role schemas;
- declared inputs, child inventory, preserved assertions, correlations, and capability handoff have exact lineage;
- missing children, invented lineage, authority claims, mutable prompt content, and premature scheduling fail closed; and
- an adapted capability handoff retains the existing product-security finding and evidence meaning.

## Rollback plan

Revert the candidate identity to `planned` and stop producing new `PROD-SYNTH` candidate artifacts. Because the role is not scheduled, the accepted vertical continues through `PROD-SEC -> CAP-RISK` unchanged. Retain candidate artifacts and test evidence for audit; do not rewrite them or delete evidence.
