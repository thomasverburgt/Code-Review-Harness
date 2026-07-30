# SPEC-SECRETS — Secrets Reviewer

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Specialist Agent Contract](../../contracts/specialist-agent-contract.md)

**Question:** Are secrets managed securely? **Boundary:** This agent reports secrets posture; it does not declare the application secure.

## Domain extension

Each secret observation records `secret_type`, `exposure_location`, `owner_role`, `rotation_policy`, `age_or_expiry`, `approved_storage_reference`, `blast_radius`, and `regulatory_or_policy_impact`. Findings must include `exposure_root_cause` and whether the evidence is a confirmed secret, likely secret, or unresolved credential-like value. Expected consumers: secure coding, Kubernetes, CI/CD, risk, and governance.

## Measures

Coverage of eligible repositories/manifests; confirmed exposure count; managed-secret adoption; rotation compliance; and unresolved detection rate.
