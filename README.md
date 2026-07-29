# Code Review Harness

## Executive summary

The Code Review Harness is an evidence-driven, multi-agent engineering review system for evaluating software products, the cross-product capabilities they form, and the enterprise systems those capabilities support. It converts fragmented technical evidence into repeatable, traceable, decision-ready assessments while keeping engineering, governance, risk-acceptance, and promotion authority with designated humans.

Product specialists review bounded technical concerns. Capability reviewers determine whether products work together to satisfy requirements, execute documented mission threads, support operators with acceptable cognitive load, manage systemic risk, and converge on intended mission outcomes. Enterprise agents will synthesize capability evidence into system-of-systems, portfolio, modernization, governance, and investment perspectives.

Every assessment uses immutable evidence, stable identifiers, versioned contracts and rubrics, confidence provenance, reproducibility metadata, and bidirectional traceability. Agents may identify findings, generate risks, propose CAPAs, and compare courses of action, but they may not accept risk, approve releases, modify requirements, select alternatives, or promote changes.

Reviewer quality is also engineered through gold-standard packages, calibration testing, drift detection, reproducibility checks, and sandboxed improvement loops. Candidate prompt, contract, rubric, tool, or model changes must demonstrate measurable improvement without unacceptable regression and require human approval before production use.

This repository is the working architecture library for the Code Review Harness. Its directory structure follows the architecture’s working domains, not the eventual Volume I–IX written-package outline.

## Library map

| Area | Purpose |
|---|---|
| [agents](agents/README.md) | Agent registry, hierarchy, capability coverage, and specialist definitions |
| [contracts](contracts/README.md) | Shared machine and human artifact contracts |
| [diagrams](diagrams/README.md) | Architecture views and interface matrices |
| [governance](governance/README.md) | Decisions, maturity, review gates, and integration boundaries |
| [orchestration](orchestration/README.md) | Workflow, policy, and execution design |
| [requirements](requirements/README.md) | Requirements traceability and evidence graph design |
| [integrations](integrations/README.md) | External-system integration designs, including GitLab CI/CD |
| [deployment](deployment/README.md) | Runtime and platform deployment designs, including DGX H100 |
| [planning](planning/README.md) | Architecture-package burn-down and implementation planning |
| [appendices](appendices/README.md) | Reusable schemas, prompts, workflows, policies, and metrics |

The [architecture package roadmap](planning/architecture-package-roadmap.md) tracks the eventual written Volume I–IX package. It does not prescribe the repository’s file layout.
