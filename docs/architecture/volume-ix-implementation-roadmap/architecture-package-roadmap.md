# Code Review Harness Architecture Package Roadmap

## Objective

Produce a complete, reviewable architecture package that evolves through discussion and iterative refinement. The package is organized in [the architecture library](../README.md); this document is its authoritative master burn-down.

## Burn-down status

| Volume | Title | Status | Baseline location |
|---|---|---|---|
| I | Executive Architecture Overview | Not started | [Volume I](../volume-i-executive-architecture-overview/README.md) |
| II | Reference Architecture | In progress | [Volume II](../volume-ii-reference-architecture/README.md) |
| III | Agent Catalog | In progress | [Volume III](../volume-iii-agent-catalog/README.md) |
| IV | Orchestration Engine Design | In progress | [Volume IV](../volume-iv-orchestration-engine/README.md) |
| V | Risk Engine and Human Review Gates | In progress | [Volume V](../volume-v-risk-engine-human-review/README.md) |
| VI | Requirements Traceability | Not started | [Volume VI](../volume-vi-requirements-traceability/README.md) |
| VII | GitLab CI/CD Integration | Not started | [Volume VII](../volume-vii-gitlab-cicd-integration/README.md) |
| VIII | DGX H100 Deployment Guide | Not started | [Volume VIII](../volume-viii-dgx-h100-deployment/README.md) |
| IX | Implementation Roadmap | In progress | [Volume IX](README.md) |
| A | Appendices | In progress | [Appendices](../appendices/README.md) |

## Definition of done

- Volume I: Executive narrative, mission, scope, stakeholders, and architecture decisions.
- Volume II: OV-1, OV-2, OV-5, SV-1, SV-2, SV-3, and SV-4 with cross-references.
- Volume III: Every agent fully specified with responsibilities, inputs, outputs, prompt contract, JSON schema, dependencies, and examples.
- Volume IV: Temporal/Argo decision, state machines, policy engine, fan-out/fan-in, and recovery behavior.
- Volume V: Risk and confidence models, governance, promotion criteria, and human review gates.
- Volume VI: Requirements traceability, Block 39 mapping, graph model, and confidence propagation.
- Volume VII: GitLab integration, Platform Factory, ServiceNow, and release management.
- Volume VIII: DGX H100 deployment, Kubernetes, vLLM, scaling, storage, GPU allocation, and throughput.
- Volume IX: Multi-release implementation plan with dependencies and exit criteria.
- Appendices: JSON schemas, prompt templates, naming conventions, workflows, policy examples, and metrics.

## Working method

When an architectural conversation completes a section, update the status, link the completed artifact from its volume index, and record decisions in the relevant governance material. Keep this roadmap focused on package-level progress; keep detailed rationale in the owning volume.
