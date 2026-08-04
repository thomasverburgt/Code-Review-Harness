# Specialist Agent Buildout Increment Plan

- **Status:** approved
- **Approved by:** `thomasverburgt`, project owner
- **Approval date:** 2026-08-03
- **Governing decision:** [ADR-0039](../adr/0039-build-specialist-candidates-for-human-shadow-calibration.md)
- **Authorized active increment:** consolidated human shadow-review wave after machine completion of Increments 0-8
- **Increment 0 implementation state:** complete locally and on GX-10
- **Increment 1 authorization:** authorized by `thomasverburgt`, project owner, on 2026-08-03
- **Increment 2 authorization:** authorized by `thomasverburgt`, project owner, on 2026-08-03
- **Human-review sequencing:** deferred by the project owner until all specialist candidate waves are built; packets and live evidence remain retained but no reviewer response, adjudication, or candidate-complete disposition is implied

## Purpose

Build and evaluate every registered `SPEC-*` agent as an unscheduled candidate while producing safe, traceable data for human shadow review. This plan implements accepted ADR-0039. It does not authorize deployment, baseline scheduling, product fan-in, leadership-report use, release decisions, or A100 production execution.

Testing and live calibration target GX-10, DGX Spark, or an approved equivalent. Large-cluster A100 execution remains a later production activity requiring separate authorization.

## Program rules

1. Build shared controls once, then specialize prompts, schemas, rubrics, evidence selection, and tools by role.
2. Treat each agent as an independent admission unit. A wave may share implementation infrastructure, but one passing agent cannot cover a failing peer.
3. Bind the exact focus profile by ID, version, and hash into dispatch and compiled prompts. Compression may remove repeated representation but not domain questions, evidence priorities, limitations, locators, conflicts, or human authority.
4. Keep raw model output separate from deterministic harness projection and validation.
5. Retain failed, superseded, and passing attempts with immutable lineage.
6. Export only access-appropriate, comparison-only human review packets.
7. Classify intern feedback as `non_authoritative_human_review`. Qualified subject-matter adjudication is required before feedback becomes gold, negative, or promotion evidence. Human review is performed as a consolidated end-of-program wave after candidate construction unless the project owner changes this sequence.
8. Preserve the accepted reference vertical and all report, distribution, deployment, and production state.

## Per-agent definition of candidate-complete

An agent is candidate-complete only when all of the following exist and pass:

- registered identity, one current specification, and one exact focus profile;
- explicit authoritative question, scope, prohibited authority, evidence population, consumer boundary, and access class;
- versioned candidate prompt, strict role schema, rubric, model manifest, tool allow-list, and deterministic generation/projection contract;
- input manifest and least-privilege evidence adapter for an immutable repository revision;
- adjudicated structural gold fixture, semantic gold candidate, and negative packages covering invented evidence, missingness, scope violations, unsafe output, authority confusion, locator defects, and malformed output;
- deterministic replay, idempotency, retry, timeout, cancellation, audit, and rollback evidence;
- at least one retained live GX-10 or DGX Spark-equivalent run, including failed attempts;
- exact evidence locators for every distributed actionable claim;
- schema-valid human review packet and reviewer-response artifact;
- human review metrics and qualified adjudication of a representative sample;
- explicit `comparison_only`, `unscheduled`, and downstream-ineligible state; and
- project-owner disposition recording whether to revise, retain for more calibration, or mark candidate-complete.

Candidate-complete is not scheduled, baseline, deployed, production-ready, or authorized for downstream synthesis.

## Increment 0: Common specialist candidate and human-review boundary

### Scope

Build the reusable foundation required by every later agent:

- specialist candidate input-manifest schema;
- specialist candidate role-envelope and projection contract;
- focus-profile dispatch binding and compiled-prompt manifest;
- evidence population, access, locator, and redaction contracts;
- human shadow-review packet and reviewer-response schemas;
- reviewer identity, experience, domain qualification, and review-duration fields;
- lifecycle states for generated, structurally valid, reviewable, reviewed, adjudicated, superseded, revoked, and retained-only artifacts;
- comparison-only routing and downstream ineligibility enforcement;
- shared metrics and roll-up definitions; and
- deterministic fixture builder, validator, runner, packet exporter, and rollback control.

### Exit criteria

- Missing or mismatched identity, specification, focus, prompt, schema, rubric, model, tool, evidence, or access bindings fail before dispatch.
- Every actionable packet item requires a reproducible locator or an explicit inaccessible state.
- Review artifacts cannot express risk acceptance, compliance approval, release approval, scheduling, deployment, or promotion.
- Unsafe content is blocked or safely redacted without losing source identity.
- A fixture-only end-to-end rehearsal passes locally and on GX-10.

### Implementation record

The local portion is complete. The repository now contains the common manifest, control, packet, response, metrics, and state-machine schemas; a deterministic runtime; exact focus binding with compression-protected elements; immutable ledger persistence; rollback controls; an end-to-end `SPEC-DEPS` fixture; and positive and fail-closed tests. The fixture is infrastructure validation only and does not make `SPEC-DEPS` candidate-complete under Increment 1.

The same bounded rehearsal passed on the GX-10 approved equivalent on 2026-08-03. The retained transcript, controlled-source hashes, unpacked reference run, and archive are recorded at `fixtures/specialist-shadow-calibration/evidence/2026-08-03/adr0039/increment-0/gx10-run-001`. Increment 0 is complete. The project owner subsequently authorized Increment 1; this authorization does not schedule or admit its candidates.

## Increment 1: Inventory and static-evidence specialists

**State:** candidate construction and GX-10 calibration complete; human review deferred

**Current implementation state:** exact prompts, role schemas, rubrics, model manifests, tool policies, deterministic candidates, negative mutations, locators, and human-review packets pass locally. All three first-attempt model-backed GX-10 calibrations pass and are retained. Intern responses, qualified adjudication, metrics, and project-owner disposition are intentionally deferred to the consolidated human-review wave.

### Agents

- `SPEC-DEPS` — Dependency Reviewer
- `SPEC-SBOM` — Software Composition and SBOM Reviewer
- `SPEC-LINT` — Linter and Code Quality Reviewer

### Purpose

Prove the shared boundary against objective, repository-local evidence. Measure whether overlapping agents remain distinct: dependency health versus inventory completeness versus rule/tool conformance.

### Human-review track

General engineering interns may review safe public-repository packets. Deterministic tool output must remain visibly separate from model interpretation.

### Exit criteria

- Manifest, lockfile, SBOM, rule configuration, suppression, and source-population coverage are explicit.
- Duplicate findings and cross-agent disagreements are measured rather than silently merged.
- Reviewers can reproduce every distributed claim from the pinned revision.
- The project owner approves continuation based on packet safety and review usefulness, not acceptance rate alone.

## Increment 2: Build and software-supply-chain specialists

**State:** authorized and in progress

**Current implementation state:** exact prompts, strict role schemas, rubrics, model and tool manifests, deterministic candidates, negative mutations, evidence locators, and deferred-review packets pass locally. The evidence was verified against the immutable, read-only `defenseunicorns/uds-core` revision already admitted for harness testing. All three model-backed GX-10 calibrations pass and are retained. Human review, qualified adjudication, metrics, and project-owner candidate-complete dispositions remain deferred to the consolidated program review.

### Agents

- `SPEC-CONTAINER` — Container and Image Security Reviewer
- `SPEC-CICD` — CI/CD Pipeline Reviewer
- `SPEC-IAC` — Infrastructure-as-Code Reviewer

### Purpose

Evaluate artifact provenance, build identity, pipeline privilege, infrastructure desired state, image contents, runtime hardening, promotion controls, and rollback evidence without declaring the product secure or releasable.

### Human-review track

Intern review is allowed only for sanitized public evidence. Pipeline secrets, private registry details, privileged infrastructure data, and exploit-enabling content require restricted reviewers.

### Exit criteria

- Build-time, artifact-time, deployment-time, and runtime claims remain separate.
- Provenance absence is not converted into compromise, safety, or approval.
- Cross-agent overlap in build and deployment findings preserves source ownership.
- Restricted evidence cannot enter general review packets.

## Increment 3: Kubernetes and communication specialists

**State:** candidate construction and GX-10 calibration complete; human review deferred

**Current implementation state:** exact prompts, strict role schemas, rubrics, model and tool bindings, deterministic candidates, exact locators, deferred-review packets, and fail-closed workload/platform/communications evidence-tier checks pass locally and on GX-10. All three model-backed calibrations passed. Configuration-only evidence cannot become runtime effectiveness. Human review remains deferred.

### Agents

- `SPEC-K8S-WORKLOAD` — Kubernetes Workload Security Reviewer
- `SPEC-K8S-PLATFORM` — Kubernetes Platform Security Reviewer
- `SPEC-COMMS` — Workload Communication Security Reviewer

### Purpose

Differentiate workload configuration, cluster/platform control, and service-communication trust while preserving shared evidence and avoiding double counting.

### Human-review track

Use public manifests and synthetic cluster evidence first. Live cluster configuration or network topology requires authorized platform reviewers.

### Exit criteria

- Workload, platform, and communication boundaries are machine-testable.
- Namespace, tenant, identity, network, admission, and runtime assumptions are explicit.
- Absent live-cluster evidence produces bounded missingness rather than a configuration-only security conclusion.
- Cross-agent conflicts survive into review packets.

## Increment 4: Secure implementation and restricted secrets revalidation

**State:** candidate construction and GX-10 calibration complete; human review deferred

**Current implementation state:** the secure-code candidate and common-contract SPEC-SECRETS revalidation wrapper pass locally and on GX-10. Both model-backed calibrations passed. The accepted SPEC-SECRETS prompt, role schema, canonical artifact, and retained reference route remain unchanged and replayable. Revalidation admits only the retained redacted detector record, prohibits general-intern routing, and cannot promote unresolved material to confirmed secret. Human review remains deferred.

### Agents

- `SPEC-SECURE-CODE` — Secure Coding Reviewer
- `SPEC-SECRETS` — Secrets Reviewer

### Purpose

Build the secure-code candidate and revalidate the proven secrets specialist against the common ADR-0039 contracts. Preserve the distinction between implementation weakness, suspected credential material, confirmed exposure, and whole-product security posture.

### Human-review track

Secure-code packets may use sanitized public examples. Secret-related packets require restricted access, irreversible value redaction, and reviewers trained in safe handling. General interns do not receive raw suspected secret values.

### Exit criteria

- Secret values never appear in prompts, logs, packets, telemetry, or reports.
- Suspected, likely, confirmed, and benign classifications remain distinct.
- Secure-code findings do not claim exploitability without admitted evidence.
- The existing accepted `SPEC-SECRETS` reference route remains unchanged and replayable.

## Increment 5: Architecture, data, integration, model, and resource specialists

**State:** candidate construction and GX-10 calibration complete; human review deferred

**Current implementation state:** all five candidates have exact prompts, strict role schemas, rubrics, model and tool bindings, deterministic candidates, exact locators, deferred-review packets, negative evidence-tier tests, and passing model-backed GX-10 runs. Seed-status maturity records pass for `SPEC-DIAGRAM` and `SPEC-IO`. Intended, configured, and observed states remain distinct.

### Agents

- `SPEC-ARCH` — Architecture Reviewer
- `SPEC-INTEROP` — Interoperability and Integration Reviewer
- `SPEC-DATA` — Data Architecture and Information Management Reviewer
- `SPEC-DIAGRAM` — Diagram and Design-Model Reviewer
- `SPEC-IO` — I/O and Resource Interaction Reviewer

### Purpose

Evaluate intended versus implemented structure, interface compatibility, information semantics and lineage, model consistency, and external resource interactions. Establish safe treatment of incomplete or conflicting design artifacts.

### Human-review track

Use engineers with enough system context to distinguish missing documentation from implementation defects. Intern responses remain especially non-authoritative for architectural intent and data-governance meaning.

### Exit criteria

- Intended, implemented, observed, and desired states remain separate.
- Diagram absence or drift is not treated as implementation failure without evidence.
- Interface, data, architecture, and I/O records preserve their original identifiers and meanings across overlap.
- Seed-status specifications (`SPEC-DIAGRAM` and `SPEC-IO`) pass an explicit specification-maturity review before live prompt execution.

## Increment 6: Operability, performance, and resilience specialists

**State:** candidate construction and GX-10 calibration complete; human review deferred

**Current implementation state:** all three candidates pass deterministic and model-backed GX-10 calibration. Static recording rules, scaling settings, and retry source cannot become claims of alert effectiveness, capacity, resilience, or A100 performance. Runtime workload, fault-injection, and operational-history evidence remain explicit unknowns.

### Agents

- `SPEC-OBS` — Observability Reviewer
- `SPEC-PERF` — Performance and Scalability Reviewer
- `SPEC-FMECA` — Reliability, Resilience, and FMECA Reviewer

### Purpose

Evaluate diagnostic coverage, declared performance objectives, measured behavior, failure modes, propagation, controls, recovery, and mission effects without confusing static configuration with demonstrated effectiveness.

### Human-review track

Static public-repository packets may go to interns. Claims about capacity, recovery, alert effectiveness, or resilience require admitted runtime evidence and appropriately qualified reviewers.

### Exit criteria

- Configuration, test, observation, and production evidence tiers remain distinct.
- No A100 performance claim is inferred from GX-10 measurements.
- Performance, observability, and resilience correlations cite exact records and disclose derivation.
- Missing workload, fault-injection, or operational-history evidence remains visible.

## Increment 7: Research, product-risk, and integrated security specialists

**State:** candidate construction and GX-10 calibration complete; human review deferred

**Current implementation state:** all three seed-status specifications passed bounded-calibration maturity review. `SPEC-RESEARCH` uses content-addressed, attributable source material without live network research. `SPEC-RISK` and `SPEC-SECURITY` consume retained child candidates while preserving their identifiers, provenance, unknowns, and human authority. All three model-backed GX-10 calibrations pass.

### Agents

- `SPEC-RESEARCH` — Research and Product-Store Agent
- `SPEC-RISK` — Product Risk Reviewer
- `SPEC-SECURITY` — Security Posture Reviewer

### Purpose

Build the roles that depend most heavily on source authority, cross-record synthesis, and disciplined uncertainty. These agents run after earlier specialist outputs exist so their boundaries, double-counting controls, and provenance can be tested against real candidate artifacts.

### Human-review track

Use qualified domain reviewers for semantic adjudication. Interns may evaluate traceability, clarity, reproducibility, and evidence requests but may not validate risk magnitude, security posture, or source authority by consensus.

### Exit criteria

- External research is content-addressed, licensed, attributable, current enough for its claim, and explicitly admitted before use.
- Risk records preserve cause, event, consequence, likelihood, controls, uncertainty, and human authority without inventing acceptance.
- `SPEC-SECURITY` preserves child specialist disagreement and cannot declare whole-product security or release readiness.
- Seed-status specifications (`SPEC-RESEARCH`, `SPEC-RISK`, and `SPEC-SECURITY`) pass specification-maturity review before live prompt execution.

## Increment 8: Cross-agent shadow comparison and program retrospective

**State:** machine comparison and retrospective complete; consolidated human review pending

**Current implementation state:** all 22 registered specialists have passing retained GX-10 model calibrations and explicit final-state records. Machine preparation consumed 53,369 input tokens and 8,641 output tokens. Every candidate remains `blocked_on_evidence`—not defective or rejected—because independent human responses, qualified semantic adjudication, and project-owner candidate dispositions have not yet occurred. The comparison, retrospective, final-state register, and reviewer handoff are retained at `fixtures/specialist-program-retrospective/2026-08-03/adr0039`.

### Scope

Run a bounded, all-specialist comparison over one or more pinned repositories without product fan-in. This is a harness-quality evaluation, not a product assessment.

Evaluate:

- evidence coverage and inaccessible populations;
- duplicate, conflicting, and complementary findings;
- focus-profile adherence and generic-output leakage;
- locator success and reviewer reproduction time;
- false-positive, partial-support, unsupported, and unable-to-determine rates;
- reviewer agreement by domain and experience;
- token use, latency, retry, failure, and truncation behavior;
- prompt and schema defects discovered across waves;
- access-control and redaction performance; and
- rollback and revocation across all candidate designations.

### Exit criteria

- All 22 agents have an explicit final state: candidate-complete, revision-required, blocked on evidence, or retained-only.
- No candidate is scheduled or eligible for product fan-in.
- A program retrospective identifies reusable prompt patterns, invalid shared assumptions, domain-specific needs, cost and latency findings, human-review lessons, and prioritized corrective work.
- Any proposal for downstream shadow fan-in, scheduling, deployment, or production is made through a separate ADR with exact scope and rollback.

## Human-review dataset structure

The program should produce one versioned dataset with four linked but separate layers:

1. **Source layer:** immutable repository revision, evidence population, access class, hashes, and reproduction instructions.
2. **Agent layer:** raw response, deterministic projection, validation state, claims, locators, confidence, limitations, and focus binding.
3. **Reviewer layer:** independent item-level responses, rationale, review time, experience, qualification, access, and evidence requests.
4. **Adjudication layer:** qualified semantic disposition, disagreement analysis, gold/negative eligibility, project-owner finalization, and supersession.

No layer overwrites another. Derived metrics must link back to the exact records from which they were calculated.

## Rollback at every increment

Disable the affected agent designations in candidate discovery and dispatch, revoke active human-review export eligibility, retain all evidence and responses, and return to the last completed increment. Because all work is comparison-only, rollback never requires changing the accepted baseline, report, distribution, deployment, or production state.
