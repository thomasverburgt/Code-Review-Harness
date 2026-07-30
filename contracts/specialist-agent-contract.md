# Specialist Agent Contract

- **Contract designation:** `CONTRACT-AGENT-SPECIALIST`
- **Version:** `1.0.0`
- **Extends:** [Universal Agent Contract](universal-agent-contract.md)

`SPEC-*` agents assess one bounded technical concern within declared product scope.

## Required extension

Every specialist artifact adds `product_id`, `domain_scope`, `eligible_population`, `domain_observations`, `domain_assessments`, `domain_findings`, `domain_patterns`, `domain_unknowns`, `domain_coverage`, `domain_confidence`, and `product_consumers`.

## Shared responsibility and boundary

Specialists apply versioned domain criteria, distinguish facts from assessment, identify evidence gaps, publish findings/CAPAs and positive patterns through separate channels, and expose conflicts. They do not declare an entire product safe, ready, compliant, reliable, or approved; accept risk; approve release; alter requirements; rewrite evidence; or resolve another specialist's disagreement.

## Failure and partial review

A specialist reports inaccessible or ineligible assets explicitly. Missing tools, credentials, source revisions, criteria, or evidence reduce coverage and confidence; they do not become `no_findings`. Partial review follows the universal `incomplete_input` rule.

## Common consumers

`PROD-*` agents are the normal parents. Capability, enterprise, governance, or human consumers may read a specialist artifact directly but MUST preserve its product scope and MUST NOT bypass required synthesis gates.
