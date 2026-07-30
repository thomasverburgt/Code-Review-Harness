# SPEC-DEPS — Dependency Reviewer

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Specialist Agent Contract](../../contracts/specialist-agent-contract.md)

**Question:** Is the dependency graph healthy and sustainable? **Boundary:** Does not declare vulnerabilities or approve a release.

## Domain extension

Record `graph_node`, `graph_edge`, `dependency_intent` (core, tooling, test, temporary), `ownership_or_stewardship`, `critical_path_tags` (startup, auth, data), `coupling_type`, `circularity`, `orphan_status`, `version_drift`, `maintenance_signal`, `license_risk`, `replacement_complexity`, and `stability_trajectory`. CAPAs identify migration/API-breakage/effort implications.

## Measures

Circular and orphan counts; duplicate libraries; abandoned dependency exposure; critical-path concentration; and graph trend.
