# Agent Catalog

The machine-authoritative identity registry is [agent-identities.json](agent-identities.json). It owns immutable UUIDs, canonical designations, legacy aliases, contract versions, layer, status, and specification paths. The [naming and identity standard](agent-naming-and-identity-standard.md) governs changes.

`baseline` means the role contract is specified; `seed` needs a domain-design increment; `planned` is architecturally reserved but not ready for production scheduling.

## Specialist layer

| Designation | Agent | Status | Authoritative question |
|---|---|---|---|
| `SPEC-SECRETS` | Secrets Reviewer | baseline | Are secrets managed securely? |
| `SPEC-SBOM` | Software Composition and SBOM Reviewer | baseline | Is inventory trustworthy and complete? |
| `SPEC-DEPS` | Dependency Reviewer | baseline | Is the dependency graph healthy and sustainable? |
| `SPEC-SECURE-CODE` | Secure Coding Reviewer | baseline | Does code implement secure coding practices? |
| `SPEC-SECURITY` | Security Posture Reviewer | seed | What is the integrated product security posture? |
| `SPEC-CONTAINER` | Container and Image Security Reviewer | baseline | Is the deployable image trustworthy and hardened? |
| `SPEC-K8S-WORKLOAD` | Kubernetes Workload Security Reviewer | baseline | Is the workload securely operated? |
| `SPEC-K8S-PLATFORM` | Kubernetes Platform Security Reviewer | baseline | Is shared platform configuration secure? |
| `SPEC-COMMS` | Workload Communication Security Reviewer | baseline | Are service-to-service boundaries protected? |
| `SPEC-IAC` | Infrastructure-as-Code Reviewer | baseline | Is desired infrastructure correctly and securely defined? |
| `SPEC-CICD` | CI/CD Pipeline Reviewer | baseline | Does delivery produce trustworthy, repeatable, governable releases? |
| `SPEC-OBS` | Observability Reviewer | baseline | Can production behavior be understood? |
| `SPEC-PERF` | Performance and Scalability Reviewer | baseline | Can objectives be met under expected load? |
| `SPEC-FMECA` | Reliability, Resilience, and FMECA Reviewer | baseline | Can the system continue through failure? |
| `SPEC-ARCH` | Architecture Reviewer | baseline | Does implementation realize intended architecture? |
| `SPEC-INTEROP` | Interoperability and Integration Reviewer | baseline | Can information and behavior exchange reliably? |
| `SPEC-DATA` | Data Architecture and Information Management Reviewer | baseline | Is information governed and fit for mission? |
| `SPEC-RISK` | Product Risk Reviewer | seed | What product-level risks require escalation? |
| `SPEC-LINT` | Linter and Code Quality Reviewer | seed | Does implementation meet defined quality rules? |
| `SPEC-IO` | I/O and Resource Interaction Reviewer | seed | Are storage and external I/O interactions safe and efficient? |
| `SPEC-DIAGRAM` | Diagram and Design-Model Reviewer | seed | Do diagrams faithfully represent implemented structure? |
| `SPEC-RESEARCH` | Research and Product-Store Agent | seed | What vetted external knowledge should enter the product store? |

## Product layer

| Designation | Agent | Status | Authoritative question |
|---|---|---|---|
| `PROD-SYNTH` | Product Synthesis Lead | planned | What coherent engineering state follows from product specialist reviews? |
| `PROD-SEC` | Product Security Synthesizer | planned | What integrated product security posture follows from specialist evidence? |
| `PROD-ARCH` | Product Architecture Synthesizer | planned | Does the product coherently realize approved architecture and intent? |
| `PROD-LINT` | Product Quality Synthesizer | planned | What maintainability and code-quality posture follows from product evidence? |

## Capability layer

| Designation | Agent | Status | Authoritative question |
|---|---|---|---|
| `CAP-XPROD` | Cross-Product Reviewer | baseline | Do products interact coherently across interfaces and assumptions? |
| `CAP-MISSION` | Mission Thread Analysis Agent | baseline | Can the documented mission thread execute end to end? |
| `CAP-HCD` | Human-Centered Design Evaluator | baseline | Can intended users execute the mission effectively and safely? |
| `CAP-RISK` | Capability Risk Reviewer | baseline | What emergent risks exist because products operate together? |
| `CAP-REQ` | Requirements Traceability Reviewer | baseline | Is each requirement supported by objective, traceable evidence? |
| `CAP-ARCH` | Capability Architecture Reviewer | baseline | Is the capability a coherent, resilient, mission-aligned solution? |
| `CAP-TRADE` | Capability Trade-Study Reviewer | baseline | What tradeoffs and uncertainty distinguish the alternatives? |
| `CAP-GOV` | Capability Governance Reviewer | baseline | What obligations, exceptions, and approval gaps require human action? |
| `CAP-PROGRESS` | Capability Progress and Readiness Reviewer | baseline | Is capability readiness converging on intended mission value? |
| `CAP-COORD` | Capability Coordinator | baseline | What traceable capability assessment follows from all reviews? |
| `CAP-SYNTH` | Capability Synthesis Lead | planned | Do products collectively deliver the intended capability? |

## Enterprise layer

| Designation | Agent | Status | Authoritative question |
|---|---|---|---|
| `ENT-EVIDENCE` | Evidence Validation Gate | baseline | Is the enterprise input set fit for the requested review? |
| `ENT-ARCH` | Systems Architecture Reviewer | baseline | Do capabilities form a coherent enterprise architecture? |
| `ENT-SYSRISK` | Systemic Risk Reviewer | baseline | What risks emerge across capabilities? |
| `ENT-GOV` | Enterprise Governance Reviewer | baseline | Are governance obligations consistently satisfied? |
| `ENT-STRAT` | Strategic Scoring Agent | baseline | What strategic confidence does the evidence support? |
| `ENT-PORTFOLIO` | Portfolio Analysis Agent | baseline | Where are portfolio duplication, concentration, and gaps? |
| `ENT-ARCHSTRAT` | Architecture Strategy Agent | baseline | Does architecture trajectory converge on approved target states? |
| `ENT-MATURITY` | Maturity Evaluator | baseline | What maturity is demonstrated, and where does it constrain outcomes? |
| `ENT-TECHDEBT` | Technical Debt Prioritizer | baseline | Which debt conditions most threaten enterprise outcomes? |
| `ENT-MODERNIZE` | Investment and Modernization Advisor | baseline | What modernization options and tradeoffs are evidence-supported? |
| `ENT-LEARN` | Learning and Metrics Agent | baseline | What do outcomes show about agent quality and drift? |
| `ENT-SYNTH` | Enterprise Synthesis Agent | baseline | What coherent enterprise posture follows from all assessments? |

## Work and orchestration layers

| Designation | Agent | Status | Authoritative question |
|---|---|---|---|
| `WORK-REVIEW` | Evidence Review Worker | planned | Does a bounded input set satisfy declared review criteria? |
| `WORK-ANALYZE` | Evidence Analysis Worker | planned | What reproducible relationships or anomalies exist in the inputs? |
| `WORK-SUMMARIZE` | Evidence Summarization Worker | planned | What faithful, loss-aware summary serves the declared consumer? |
| `ORCH-SCHED` | Contract Scheduler | planned | Which registered agents and contracts must execute? |
| `ORCH-FANOUT` | Parallel Dispatch Controller | planned | Which work can safely execute in parallel? |
| `ORCH-FANIN` | Artifact Aggregation Controller | planned | Are prerequisite artifacts valid and ready for routing? |

## Legacy aliases

The original `SPC-*` and `PRD-SYNTH` designations and the isolated `CAP-MTHREAD` spelling remain immutable aliases in the identity registry. They are accepted for historical resolution only and MUST NOT be emitted by new artifacts.
