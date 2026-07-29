# Code Review Harness

**Current architecture-library version: v0.1.0**

## Executive summary

The Code Review Harness is an evidence-driven, multi-agent engineering review system for evaluating software products, the cross-product capabilities they form, and the enterprise systems those capabilities support. It converts fragmented technical evidence into repeatable, traceable, decision-ready assessments while keeping engineering, governance, risk-acceptance, and promotion authority with designated humans.

Product specialists review bounded technical concerns. Capability reviewers determine whether products work together to satisfy requirements, execute documented mission threads, support operators with acceptable cognitive load, manage systemic risk, and converge on intended mission outcomes. Enterprise agents synthesize capability evidence into system-of-systems, portfolio, modernization, governance, and investment perspectives.

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
| [ADRs](adr/README.md) | Material architecture and governance decision records |

The [architecture package roadmap](planning/architecture-package-roadmap.md) tracks the eventual written Volume I–IX package. It does not prescribe the repository’s file layout.

## Project principles

The project's governing principles are documented in [Project Philosophy](docs/philosophy.md): evidence over opinion, immutable artifacts, human decision authority, traceability by default, explainable assessment, CAPA discipline, explicit confidence, bounded automation, and reviewability.

## Contributing and governance

Contributions are welcome under the process in [CONTRIBUTING.md](CONTRIBUTING.md). The project uses Developer Certificate of Origin sign-offs, human review of AI-assisted contributions, [CODEOWNERS](CODEOWNERS), [project governance](GOVERNANCE.md), a [Code of Conduct](CODE_OF_CONDUCT.md), and private vulnerability reporting described in [SECURITY.md](SECURITY.md).

## License

Code Review Harness is licensed under the GNU Affero General Public License, version 3 only (`AGPL-3.0-only`). See [LICENSE](LICENSE) and [LICENSING.md](LICENSING.md). Unless a file states otherwise, this applies to the repository's source code, scripts, schemas, prompts, agent contracts, architecture documents, diagrams, governance material, and examples.

Copyright © 2026 Thomas Verburgt.