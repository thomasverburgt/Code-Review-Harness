# CAP-REQ — Requirements Traceability Reviewer

**Question:** Do implementation evidence and product assessments satisfy the declared requirements, including Block 39 response commitments where applicable?

**Boundary:** Correlates requirements, evidence, findings, tests, and product assertions. It does not invent requirements, silently resolve ambiguity, or declare contractual acceptance.

## Inputs

Requirement records, Block 39 mappings, product synthesis artifacts, specialist findings, test evidence, architecture decisions, source revisions, and approved requirement changes.

## Outputs

Requirement-to-evidence graph edges, satisfaction state, coverage gaps, conflicting evidence, confidence dimensions, unsupported claims, and escalation requests.

## Required extension fields

`requirement_id`, `requirement_source`, `requirement_text_hash`, `response_commitment`, `participating_products`, `evidence_refs`, `verification_method`, `validation_method`, `satisfaction_state`, `coverage_state`, `conflict_state`, `finding_refs`, `confidence`, `rationale`, `change_history`, and `decision_owner`.

## Measures

Requirement coverage; evidence-backed satisfaction rate; unsupported-claim count; conflict count; stale-evidence rate; and confidence distribution.