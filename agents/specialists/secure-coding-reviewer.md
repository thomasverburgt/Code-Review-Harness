# SPEC-SECURE-CODE — Secure Coding Reviewer

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Specialist Agent Contract](../../contracts/specialist-agent-contract.md)

**Question:** Does code implement secure coding practices? **Boundary:** It assesses implementation quality, not supply-chain health or architectural approval.

## Domain extension

Record `control_area` (authentication, authorization, input validation, cryptography, secret use, error handling, secure defaults), `rule_provenance`, `code_pattern_classification`, `attack_precondition`, `exploitability_context`, and `positive_pattern_candidate`. Good and bad patterns use evidence-backed examples and explicit applicability conditions.

## Measures

Eligible code coverage; rule coverage; confirmed vs. likely finding ratio; control-area distribution; and reusable-pattern candidates.
