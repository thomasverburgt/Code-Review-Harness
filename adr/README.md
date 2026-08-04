# Architecture Decision Records

Architecture Decision Records preserve the context, authority, evidence, alternatives, and consequences behind material project decisions.

Use sequential identifiers such as `0001-short-decision-title.md`. ADRs are immutable once accepted except for clerical correction. A later ADR may supersede an earlier one and must link both directions.

Statuses:

- proposed
- accepted
- rejected
- deprecated
- superseded

Copy `template.md` when creating a new ADR. Material changes identified in `GOVERNANCE.md` require an ADR before acceptance.

## Recorded decisions

- [ADR 0001: Immutable Artifacts Are Authoritative](0001-immutable-artifacts-are-authoritative.md)
- [ADR 0002: Evidence Is Never Rewritten by a Parent](0002-evidence-is-never-rewritten-by-a-parent.md)
- [ADR 0003: Specialists Do Not Decide](0003-specialists-do-not-decide.md)
- [ADR 0004: CAPA and Positive Patterns Are Separate Channels](0004-capa-and-positive-patterns-are-separate-channels.md)
- [ADR 0005: Human Review Is Earned, Not Presumed Absent](0005-human-review-is-earned-not-presumed-absent.md)
- [ADR 0006: Universal Agent Identity and Contract Standard](0006-universal-agent-identity-and-contract-standard.md)
- [ADR 0007: Executable Extension Validation and Enterprise Evidence Gate](0007-executable-extension-validation-and-enterprise-evidence-gate.md)
- [ADR 0008: A100 Production and DGX Spark Test Baseline](0008-a100-production-dgx-spark-test-baseline.md)
- [ADR 0009: Content-Addressed Artifact and Execution Ledger](0009-content-addressed-artifact-and-execution-ledger.md)
- [ADR 0010: Contract-Gated Worker and Adapter Boundary](0010-contract-gated-worker-and-adapter-boundary.md)
- [ADR 0011: Deterministic Envelope and Role-Payload Generation](0011-deterministic-envelope-and-role-payload-generation.md)
- [ADR 0012: Immutable Report Distribution and External Decision Reconciliation](0012-immutable-human-decision-boundary.md)
- [ADR 0013: Reproducible Evidence Locators and Expert Review Packets](0013-reproducible-evidence-locators-and-expert-review-packets.md)
- [ADR 0014: Product Synthesis Candidate Admission Before Scheduling](0014-product-synthesis-candidate-admission.md)
- [ADR 0015: Shadow Product Synthesis Before Baseline Cutover](0015-shadow-product-synthesis-before-baseline-cutover.md)
- [ADR 0016: Human Semantic Adjudication Before Shadow Cutover](0016-human-semantic-adjudication-before-shadow-cutover.md)
- [ADR 0017: Separate Capability Coordination from Semantic Synthesis](0017-separate-capability-coordination-from-semantic-synthesis.md)
- [ADR 0018: Capability Synthesis Candidate Admission Requires Proven Input Tiers](0018-capability-synthesis-candidate-admission.md)
- [ADR 0019: Establish Live Capability Requirements Review Before Multi-Domain Synthesis](0019-live-capability-requirements-review-before-multi-domain-synthesis.md)
- [ADR 0020: Require Human Acceptance of the CAP-REQ Artifact Before Multi-Domain Use](0020-human-acceptance-of-capability-requirements-artifact.md)
- [ADR 0021: Align Enterprise Registry Status with Executable Reality and Admit ENT-ARCH as a Candidate](0021-enterprise-registry-truth-and-architecture-candidate-admission.md)
- [ADR 0022: Require Authoritative Governance-Source Manifests for ENT-GOV Candidate Admission](0022-authoritative-governance-source-boundary-and-ent-gov-candidate-admission.md)
- [ADR 0023: Require Human-Controlled Strategic Objectives and Scoring Methods for ENT-STRAT Candidate Admission](0023-human-controlled-strategic-objectives-and-scoring-boundary.md)
- [ADR 0024: Separate Enterprise Synthesis from Domain Authority and Report Release](0024-enterprise-synthesis-provenance-and-release-boundary.md)
- [ADR 0025: Require Accepted Multi-Domain Evidence Before Enterprise Shadow Integration](0025-require-accepted-multi-domain-evidence-before-enterprise-shadow-integration.md)
- [ADR 0026: Create an Authority-Separated Human Readiness Action Dossier](0026-authority-separated-human-readiness-action-dossier.md)
- [ADR 0027: Govern Repository Artifact Lifecycles Before Structural Migration](0027-govern-repository-artifact-lifecycles.md)
- [ADR 0028: Separate Controlled Binary Releases from Transient Render Evidence](0028-binary-release-and-transient-render-retention.md)
- [ADR 0029: Separate Reusable Fixtures from Retained Evidence](0029-separate-reusable-fixtures-from-retained-evidence.md)
- [ADR 0030: Introduce a Compatibility-First Python Package Boundary](0030-compatibility-first-python-package-boundary.md)
- [ADR 0031: Require One Specification per Agent and Generated Registry Catalogs](0031-one-agent-one-specification-and-generated-catalogs.md)
- [ADR 0032: Defer Legacy Retirement Until Observation and Archive Gates Pass](0032-defer-legacy-retirement-until-observation-and-archive-gates.md)
- [ADR 0033: Project-Owner Finalization Replaces Mandatory Second-Person Verification](0033-project-owner-finalization-without-mandatory-second-verifier.md)
- [ADR 0034: Require Accepted-Live Multi-Domain Evaluation Before CAP-SYNTH Scheduling](0034-accepted-live-multi-domain-capability-synthesis-evaluation.md)
- [ADR 0035: Evaluate ENT-ARCH Using Semantically Accepted CAP-SYNTH Without Scheduling Either Candidate](0035-semantically-accepted-cap-synth-input-to-ent-arch-evaluation.md)
- [ADR 0036: Evaluate ENT-GOV Using an Owner-Declared Governance Source and Semantically Accepted CAP-SYNTH](0036-owner-declared-governance-source-to-ent-gov-evaluation.md)
- [ADR 0037: Evaluate ENT-STRAT Using Owner-Declared Project Strategy Sources and Semantically Accepted CAP-SYNTH](0037-owner-declared-strategic-evaluation-sources-to-ent-strat.md)
- [ADR 0038: Evaluate ENT-SYNTH Using the Accepted Enterprise Domain Set Without Scheduling or Report Promotion](0038-accepted-live-enterprise-synthesis-evaluation.md)
- [ADR 0039: Build Specialist Candidates for Human Shadow Calibration Without Deployment](0039-build-specialist-candidates-for-human-shadow-calibration.md)
