# CAP-SYNTH - Capability Synthesis Lead

- UUID: `ca95161d-d7dc-40b0-b233-fda505b18afe`
- Layer: capability
- Status: candidate; GX-10 protocol/lineage calibrated; unscheduled
- Contract: Universal Agent Contract + Capability Delivery Contract + Deterministic Capability Coordination Contract
- Role schema: `cap-synth-role.schema.json`

## Purpose

Produce an advisory, explicitly sourced capability posture from a hash-valid `CAP-COORD` manifest and the exact immutable capability-review artifacts named by that manifest.

## Input and evidence-tier boundary

The candidate accepts only `ready_for_cap_synth` manifests with exact artifact ID/hash binding. `adjudicated_multi_domain_contract_fixture` proves contract mechanics but is not live readiness evidence. `accepted_live_input_calibration` uses accepted artifacts; a one-domain set is only a protocol/lineage smoke test and cannot claim cross-domain fitness.

## Output

The role preserves child assertions, evidence, confidence provenance, conflicts, unknowns, and decisions; identifies explicitly sourced correlations; emits advisory capability posture and a comparison-only enterprise handoff; and labels its evidence tier and fitness claim.

## Authority boundary

The candidate cannot validate or expand its own inputs, accept risk, approve readiness, alter requirements, select a course of action, approve release or distribution, change reports, authorize deployment, or promote the A100 production workflow. Decision authority is always human.

## Admission and rollback

Candidate artifacts remain isolated from the accepted workflow, report, governance, deployment, and production paths. Rollback disables candidate dispatch and returns the identity to planned while retaining all candidate evidence for audit.

The retained 2026-08-01 Qwen3-32B run used the sole accepted live `CAP-RISK` input and passed exact schema, protocol, manifest, and lineage validation. Its fitness claim is intentionally limited to `protocol_lineage_smoke_only`; it is not multi-domain synthesis evidence.
