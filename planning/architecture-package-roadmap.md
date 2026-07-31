# Code Review Harness Architecture Package Roadmap

## Objective

Produce a complete, reviewable architecture package through discussion and iterative refinement. This document is the master burn-down for the eventual written package; the repository library is organized by working domain and is intentionally independent of the volume outline.

## Written-package burn-down

| Volume | Title | Status | Working-source areas |
|---|---|---|---|
| I | Executive Architecture Overview | Not started | Planning, governance, diagrams |
| II | Reference Architecture | In progress | Diagrams, governance, orchestration |
| III | Agent Catalog | In progress | Agents, contracts, appendices |
| IV | Orchestration Engine Design | In progress | Orchestration, contracts, governance |
| V | Risk Engine and Human Review Gates | In progress | Governance, agents, contracts, appendices |
| VI | Requirements Traceability | Not started | Requirements, contracts, appendices |
| VII | GitLab CI/CD Integration | Not started | Integrations/gitlab, orchestration, governance |
| VIII | A100 Large-Cluster Deployment Guide | In progress | Deployment/a100-large-cluster, orchestration, integrations |
| IX | Implementation Roadmap | Not started | Planning |
| Appendices | Schemas, prompts, workflows, policies, metrics | In progress | Appendices |

## Definition of done

- Volume I: Executive narrative, mission, scope, stakeholders, and architecture decisions.
- Volume II: OV-1, OV-2, OV-5, SV-1, SV-2, SV-3, and SV-4 with cross-references.
- Volume III: Every agent fully specified with responsibilities, inputs, outputs, prompt contract, JSON schema, dependencies, and examples.
- Volume IV: Temporal/Argo decision, state machines, policy engine, fan-out/fan-in, and recovery behavior.
- Volume V: Risk and confidence models, governance, promotion criteria, and human review gates.
- Volume VI: Requirements traceability, Block 39 mapping, graph model, and confidence propagation.
- Volume VII: GitLab integration, Platform Factory, ServiceNow, and release management.
- Volume VIII: A100 large-cluster production deployment; DGX Spark-equivalent test execution; Kubernetes, vLLM, scaling, storage, GPU allocation, promotion evidence, and throughput.
- Volume IX: Multi-release implementation plan with dependencies and exit criteria.
- Appendices: JSON schemas, prompt templates, naming conventions, workflows, policy examples, and metrics.

## Working method

As an architectural discussion completes a subject, place its source artifact in the appropriate working-domain directory, update this burn-down, and capture material decisions in governance. Assemble the final written volumes from these controlled source artifacts rather than using the file tree as the package outline.

## Active implementation increment

The active 2026-07-31 increment is the [Executable Agent Vertical Slice](today-executable-vertical-slice.md):

`SPEC-SECRETS -> PROD-SEC -> CAP-RISK -> ENT-SYSRISK -> human decision request`

This increment advances Volume III, Volume IV, Volume V, Volume IX, and the Appendices by converting selected prompt designs and contracts into schemas, a declarative reference workflow, minimal orchestration behavior, and adjudicated success/failure fixtures.
