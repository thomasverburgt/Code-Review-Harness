# Contract Style and Validation Rules

- Use stable IDs; never reuse an ID for a different issue.
- Resolve every agent through `agents/agent-identities.json`; UUID and canonical designation must match and legacy aliases are input-only.
- Validate every output against `universal-agent-artifact.schema.json` and each applicable extension before fan-in.
- Facts belong in observations; reasoning belongs in assessments; authority belongs in human or designated decision records.
- Cite evidence at the smallest practical locator (file/line, manifest path, test ID, dashboard query, or record ID).
- Score ranges are `0.00`–`1.00`; explain all scores below `0.80`.
- Every report declares scope, exclusions, coverage, reviewability, fidelity, freshness, and explicit no-findings/unknowns.
- A contract validator rejects unregistered identities, UUID/designation mismatch, missing evidence on a finding, CAPA without validation, a decision issued by an agent, or an assessment that conflates observed and desired state.
