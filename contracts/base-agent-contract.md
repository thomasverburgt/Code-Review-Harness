# Base Agent Contract

> Compatibility name: superseded by the [Universal Agent Contract](universal-agent-contract.md) at version `1.0.0`. Existing references to “base agent contract” resolve to that normative contract.

All agents publish a human-readable Markdown report and a schema-valid JSON payload. The JSON is the machine contract; Markdown is the immutable review record. A parent may aggregate or correlate a child artifact but may not edit its evidence, observations, or assessment.

## Required envelope

| Field | Meaning |
|---|---|
| `contract_version` | Semantic version of the contract. |
| `artifact_id` | Stable, globally unique artifact identifier. |
| `agent_uuid` / `designation` / `agent_version` | Registered producer identity and implementation version. |
| `review_scope` | Repositories, paths, services, environments, and exclusions. |
| `source_revision` | Git commit SHA, pipeline ID, image digest, and relevant configuration revision. |
| `created_at` / `evidence_freshness` | UTC creation time and age classification of the evidence. |
| `inputs` | Immutable source references and declared assumptions. |
| `methodology` | Rules, tools, standards, prompts, and analysis fidelity actually used. |
| `coverage` | Reviewed vs. eligible population, known gaps, and negative evidence. |
| `observations` | Facts with evidence references; no recommendation language. |
| `assessments` | Derived interpretation, rationale, and confidence dimensions. |
| `findings` | Traceable issues, including RCA and CAPA. |
| `patterns` | Candidate positive practices; separate from findings and CAPA. |
| `insights` | Neutral observations that may become valuable after correlation. |
| `conflicts` | Contradictory evidence or assessments; never silently resolved. |
| `consumers` | Declared downstream agents and decision contexts. |
| `integrity` | Content hash, signature/attestation reference, and retention class. |

## Mandatory global semantics

1. **No silent absence.** The agent must report `no_findings`, `not_reviewed`, or `unknown`; “not found” does not prove “does not exist.”
2. **Confidence has three dimensions.** `finding_confidence` rates the conclusion; `evidence_confidence` rates source reliability; `review_confidence` rates the overall completed review.
3. **Reviewability and fidelity are explicit.** `reviewability` records whether the asset could be examined; `review_fidelity` records the depth actually achieved.
4. **Observed, desired, and expected state remain separate.** A mismatch is not assumed to be a defect until assessed.
5. **Context accompanies every assessment.** Record `intent_classification`, `lifecycle_phase`, `change_driver`, and `decision_context` (`implementation`, `architecture`, `governance`, or `investment`).
6. **Verification differs from validation.** Verification checks conformance to specified criteria; validation tests whether the solution serves the intended operational need.
7. **Conformance differs from effectiveness.** A design can comply with its stated architecture yet no longer be effective.
8. **Required, recommended, and optimization recommendations are distinct obligation classes.**

## Finding object

```json
{
  "finding_id": "FND-SEC-000123",
  "title": "Secret committed in deployment values",
  "classification": "required",
  "criticality": "high",
  "affected_assets": ["repo/path/values.yaml"],
  "observed_state": "Plaintext credential detected",
  "desired_state": "Reference to approved secret manager",
  "evidence_refs": ["EVD-00091"],
  "root_cause": {
    "type": "implementation_defect",
    "narrative": "Template bypassed the approved deployment pattern"
  },
  "impact": {"technical": "credential exposure", "mission": "unauthorized access risk"},
  "capa": {
    "corrective_action": "Revoke credential and remove plaintext value",
    "preventive_action": "Enforce secret scanning and approved chart policy",
    "owner_role": "product delivery lead",
    "implementation_level": "product",
    "target_horizon": "immediate",
    "validation_method": "pipeline scan and deployment policy test"
  },
  "confidence": {"finding": 0.95, "evidence": 0.98, "review": 0.88}
}
```

## Parent aggregation rule

Parents may create `derived_assertions` that cite child artifact IDs and describe correlation logic. A parent’s strategic or capability score must preserve the contributing evidence and confidence distribution; it must never replace a child score with an unexplained average.
