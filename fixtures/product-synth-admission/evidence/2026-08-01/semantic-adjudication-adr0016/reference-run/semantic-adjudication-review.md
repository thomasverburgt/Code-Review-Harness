# PROD-SYNTH Shadow Semantic Adjudication Packet

Packet: `047813b4-5125-56f0-9e5c-81803cd078e2`
Packet hash: `sha256:3d87fb628ee30a280c60fc564ba9b365b6225a02119654c1059ef300fa5e9810`

**CUTOVER BLOCKED — HUMAN ADJUDICATION REQUIRED**

Preserved dimensions: capa_options, confidence, coverage, decisions_requested, findings
Differing dimensions: assessments, conflicts, risk_register

## 1. assessments — `/assessments/0/rationale`

Does the changed likelihood wording preserve the accepted assessment meaning?

Materiality: `potentially_substantive`

Baseline:
```json
"The presence of a redacted credential-like value in a documentation file suggests a potential exposure. The unresolved credential-like value may represent a potential exposure if it is a real secret."
```

Shadow:
```json
"The presence of a redacted credential-like value in a documentation file indicates a potential exposure. The unresolved credential-like value may represent a potential exposure if it is a real secret."
```

Downstream consequence: Changes the rationale presented to capability-risk reviewers.

Allowed dispositions: `accept_preserved_meaning`, `accept_beneficial_enrichment`, `require_normalization`, `reject_semantic_drift`, `insufficient_evidence`

If unresolved: `block_cutover`

## 2. conflicts — `/conflicts`

Should the shadow-added DC-001 question be retained as an explicit capability conflict?

Materiality: `substantive`

Baseline:
```json
[]
```

Shadow:
```json
[
  {
    "conflict_id": "DC-001",
    "evidence_refs": [],
    "statement": "Should the redacted credential-like value be classified as a confirmed secret, likely secret, or benign/nonsecret?"
  }
]
```

Downstream consequence: Changes whether downstream reports and reviewers see an unresolved conflict.

Allowed dispositions: `accept_preserved_meaning`, `accept_beneficial_enrichment`, `require_normalization`, `reject_semantic_drift`, `insufficient_evidence`

If unresolved: `block_cutover`

## 3. risk_register — `/extensions/capability/role/risk_register/0/risk_category`

Is security_exposure an acceptable replacement for secrets_exposure?

Materiality: `substantive`

Baseline:
```json
"secrets_exposure"
```

Shadow:
```json
"security_exposure"
```

Downstream consequence: Changes risk taxonomy, aggregation, filtering, and trend analysis.

Allowed dispositions: `accept_preserved_meaning`, `accept_beneficial_enrichment`, `require_normalization`, `reject_semantic_drift`, `insufficient_evidence`

If unresolved: `block_cutover`

## 4. risk_register — `/extensions/capability/role/risk_register/0/dependency_chain`

Is adding PRODUCT-ALPHA to the dependency chain supported and useful?

Materiality: `potentially_substantive`

Baseline:
```json
[]
```

Shadow:
```json
[
  "PRODUCT-ALPHA"
]
```

Downstream consequence: Changes dependency and blast-radius reasoning.

Allowed dispositions: `accept_preserved_meaning`, `accept_beneficial_enrichment`, `require_normalization`, `reject_semantic_drift`, `insufficient_evidence`

If unresolved: `block_cutover`

## 5. risk_register — `/extensions/capability/role/risk_register/0/likelihood_basis`

Does the likelihood-basis wording preserve uncertainty?

Materiality: `potentially_substantive`

Baseline:
```json
"The presence of a redacted credential-like value in a documentation file suggests a potential exposure."
```

Shadow:
```json
"The presence of a redacted credential-like value in a documentation file indicates a potential exposure."
```

Downstream consequence: May change perceived evidentiary strength.

Allowed dispositions: `accept_preserved_meaning`, `accept_beneficial_enrichment`, `require_normalization`, `reject_semantic_drift`, `insufficient_evidence`

If unresolved: `block_cutover`

## 6. risk_register — `/extensions/capability/role/risk_register/0/mission_effect`

Does the generalized sensitive-information mission effect preserve the accepted unauthorized-access meaning?

Materiality: `substantive`

Baseline:
```json
"Potential unauthorized access to the system if the redacted credential-like value is a real secret."
```

Shadow:
```json
"Potential exposure of sensitive information if the redacted value is a real secret."
```

Downstream consequence: Changes mission consequence communicated to leadership.

Allowed dispositions: `accept_preserved_meaning`, `accept_beneficial_enrichment`, `require_normalization`, `reject_semantic_drift`, `insufficient_evidence`

If unresolved: `block_cutover`

## 7. risk_register — `/extensions/capability/role/risk_register/0/treatment_options/0`

Are the shadow treatment wording, sequencing, evidence, and verification changes acceptable?

Materiality: `substantive`

Baseline:
```json
{
  "action_owner": "security_engineer",
  "contributing_causes": [
    "The presence of a redacted credential-like value in a documentation file."
  ],
  "cost_schedule_mission_tradeoffs": [],
  "decision_owner": "security_engineer",
  "dependencies": [],
  "expected_consequence_effect": "high",
  "expected_evidence": "Manual classification of the redacted credential-like value.",
  "expected_probability_effect": "medium",
  "proposed_control": "Manual classification by the security team.",
  "remaining_unknowns": [
    "The exact impact of the unresolved credential-like value is unknown without further classification."
  ],
  "sequencing": [],
  "side_effects": [],
  "target_condition": "Classify the redacted value as confirmed secret, likely secret, or benign/nonsecret.",
  "verification_method": "manual classification by security team"
}
```

Shadow:
```json
{
  "action_owner": "security_engineer",
  "contributing_causes": [
    "The presence of a redacted credential-like value in a documentation file."
  ],
  "cost_schedule_mission_tradeoffs": [],
  "decision_owner": "security_engineer",
  "dependencies": [],
  "expected_consequence_effect": "high",
  "expected_evidence": "Manual classification result.",
  "expected_probability_effect": "medium",
  "proposed_control": "Manual classification by security team.",
  "remaining_unknowns": [
    "The exact impact of the unresolved credential-like value is unknown without further classification."
  ],
  "sequencing": "immediate",
  "side_effects": [],
  "target_condition": "Classify the redacted value as confirmed secret, likely secret, or benign/nonsecret.",
  "verification_method": "Manual review and validation."
}
```

Downstream consequence: Changes the action package human experts may consider.

Allowed dispositions: `accept_preserved_meaning`, `accept_beneficial_enrichment`, `require_normalization`, `reject_semantic_drift`, `insufficient_evidence`

If unresolved: `block_cutover`

## Authority and effect

The enterprise risk acceptance authority decides semantic meaning outside the harness. Any recorded response remains record-only. A separate later ADR is required for workflow cutover.
