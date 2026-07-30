# Universal Agent Contract

- **Contract designation:** `CONTRACT-AGENT-UNIVERSAL`
- **Version:** `1.0.0`

This contract is the mandatory base for every specialist, product, capability, enterprise, work, and orchestration agent. Layer and role contracts are additive and MUST NOT weaken its provenance, evidence, confidence, integrity, or human-authority rules.

## Specification template

Every agent specification defines:

1. Identity reference: UUID, designation, display name, version, status, and aliases.
2. North Star and one authoritative question.
3. Scope, boundaries, and prohibited authority.
4. Required and optional inputs.
5. Responsibilities and methods.
6. Required outputs and downstream consumers.
7. Evidence, traceability, confidence, and reproducibility rules.
8. Failure, partial-input, conflict, and escalation behavior.
9. Measures, validation criteria, and human review gates.

## Artifact envelope

Every execution publishes schema-valid JSON as the machine contract and a human-readable immutable report. Required top-level sections are:

- `identity`: registered `agent_uuid`, canonical `designation`, display-name snapshot, agent version, and contract version.
- `artifact`: artifact UUID, artifact designation, type, creation time, lifecycle state, and parent/child/peer links.
- `execution`: model, prompt, rubric, toolchain, deterministic settings, environment, start/end times, and execution ID.
- `scope`: reviewed assets, environments, source revisions, inclusions, exclusions, and decision context.
- `inputs`: immutable artifact/evidence references, hashes, compatibility, freshness, and declared assumptions.
- `methodology`: methods, standards, policies, tools, review fidelity, and limitations.
- `coverage`: eligible, reviewed, omitted, inaccessible, unknown, and negative-evidence populations.
- `observations`: attributable facts only.
- `assessments`: interpretations with rationale and confidence.
- `findings`: deficiencies with evidence, RCA, impact, and CAPA.
- `patterns`: candidate positive practices.
- `insights`: neutral correlation candidates.
- `conflicts`: unresolved contradictions or incompatible assessments.
- `confidence`: separate evidence, assessment, review, and decision-confidence values with provenance.
- `decisions_requested`: questions routed to named human authority; never agent decisions.
- `consumers`: declared downstream roles and contexts.
- `integrity`: input hash, output hash, signing/attestation reference, retention class, and schema validation result.

## Universal semantics

1. Source evidence and child artifacts are immutable.
2. Facts, assessments, recommendations, and human decisions remain distinct.
3. `no_findings`, `not_reviewed`, `unknown`, `inaccessible`, and `insufficient_evidence` are explicit states.
4. Observed, expected, and desired state remain separate.
5. Verification, validation, conformance, and effectiveness remain separate.
6. Required, recommended, and optimization recommendations use distinct obligation classes.
7. Findings cite evidence and include CAPA; good practices are patterns, not CAPAs.
8. Scores identify rubric version, calculation, weighting, uncertainty, and provenance. Unexplained averaging is prohibited.
9. Conflicts remain first-class artifacts until an authorized human disposition is linked.
10. Every output declares `decision_authority: human`.

## Partial input and failure

An agent fails closed when identity, contract compatibility, source revision, or integrity cannot be established. Policy may authorize an `incomplete_input` execution only when missing inputs, likely effect, confidence reduction, and human escalation are explicit. A failed or partial execution cannot be represented as a complete assessment.

## Conformance

The normative machine shape is [universal-agent-artifact.schema.json](../appendices/schemas/universal-agent-artifact.schema.json). Identity registration is governed by [agent-identity-registry.schema.json](../appendices/schemas/agent-identity-registry.schema.json). Contract extensions use JSON Schema composition and must preserve `additionalProperties` discipline at their own extension boundary.
