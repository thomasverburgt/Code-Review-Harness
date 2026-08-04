# ADR-0039: Build Specialist Candidates for Human Shadow Calibration Without Deployment

- Status: accepted
- Date: 2026-08-03
- Decision authority: project owner
- Owners: specialist agents, orchestration, evidence governance, human review, and validation
- Depends on: ADR-0003, ADR-0005, ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, ADR-0013, ADR-0031, and ADR-0033
- Supersedes: none
- Superseded by: none

## Context

The harness has proven one complete specialist-to-enterprise vertical using `SPEC-SECRETS`, including contract-gated execution, immutable lineage, deterministic projection, exact evidence locators, report separation, human-only authority, and GX-10 calibration. The repository now also contains one specification and one compression-protected focus profile for every registered agent.

Most specialist roles have not yet demonstrated prompt quality, evidence-selection quality, semantic faithfulness, or human review utility through live candidate execution. Their registry status describes the governed role and specification; it must not be interpreted as live-model fitness or production readiness.

The project owner wants to begin building specialist agents and provide their outputs to intern engineers for structured human review. This can produce valuable calibration evidence if the runs remain comparison-only, source evidence is safe and reproducible, intern feedback is not treated as professional authority, and no candidate output enters the accepted report, governance, scheduling, deployment, or production state.

This decision covers every registered `SPEC-*` role: `SPEC-ARCH`, `SPEC-CICD`, `SPEC-COMMS`, `SPEC-CONTAINER`, `SPEC-DATA`, `SPEC-DEPS`, `SPEC-DIAGRAM`, `SPEC-FMECA`, `SPEC-IAC`, `SPEC-INTEROP`, `SPEC-IO`, `SPEC-K8S-PLATFORM`, `SPEC-K8S-WORKLOAD`, `SPEC-LINT`, `SPEC-OBS`, `SPEC-PERF`, `SPEC-RESEARCH`, `SPEC-RISK`, `SPEC-SBOM`, `SPEC-SECRETS`, `SPEC-SECURE-CODE`, and `SPEC-SECURITY`. Inclusion authorizes phased candidate construction and evaluation only; it does not assert equal maturity, shared evidence access, or readiness for the same human-review population.

`SPEC-DEPS`, `SPEC-SBOM`, and `SPEC-LINT` are suitable first-wave candidates because they operate on evidence-rich, comparatively reproducible populations. `SPEC-DEPS` and `SPEC-SBOM` intentionally overlap around manifests, lockfiles, component identity, provenance, inventory completeness, and dependency health. Their overlap permits measurement of duplicate findings, conflicting classifications, missing evidence, scope discipline, and whether each focus profile produces a genuinely distinct professional lens. Higher-risk, platform-dependent, behavioral, research, risk, and cross-domain security roles follow only after the common calibration and human-review boundary is proven.

The authoritative phased sequence and per-agent completion definition are maintained in [`planning/specialist-agent-buildout-increments.md`](../planning/specialist-agent-buildout-increments.md).

## Proposed decision

1. Admit all 22 registered `SPEC-*` agents only for phased, unscheduled candidate construction, deterministic evaluation, live GX-10 or DGX Spark-equivalent calibration, and bounded human shadow review. Do not deploy any specialist candidate and do not authorize A100 production execution.
2. Bind each dispatch to the exact agent identity, specification, universal and specialist contracts, role schema, prompt, rubric, focus-profile ID/version/hash, model manifest, tool permissions, evidence manifest, and source revision. Missing or mismatched bindings fail closed before dispatch.
3. Use a read-only, immutable repository revision and declared evidence population. The initial target may be the previously authorized public `defenseunicorns/uds-core` repository or an equivalently safe public fixture. The harness and its operators must not commit, push, open pull requests, or otherwise modify the target repository.
4. Produce separate retained records for input selection, raw model response, harness-owned projection, structural validation, evidence locators, limitations, execution telemetry, and rollback. Do not silently repair semantic meaning. Invalid or suspicious output remains failed calibration evidence.
5. Label every candidate artifact and export `specialist_human_shadow_calibration`, `comparison_only`, `unscheduled`, and `non_authoritative`. Candidate artifacts are ineligible for product fan-in, capability synthesis, enterprise synthesis, leadership reporting, distribution, governance decisions, release decisions, deployment, or production promotion.
6. Generate a separately hashed human review packet for each candidate run. For every observation, finding, recommendation, and claimed unknown, the packet must provide the exact repository, immutable revision, path, line or section, fingerprint, access classification, reproduction instructions, confidence meaning, source record ID, active limitations, and specialist focus question.
7. Give intern engineers a structured response contract with at least: `supported`, `partially_supported`, `unsupported`, `duplicate`, `outside_specialist_scope`, and `unable_to_determine`; evidence-locator correctness; severity and recommendation reasonableness; missing evidence; reviewer rationale; review duration; and declared reviewer experience.
8. Classify intern responses as `non_authoritative_human_review`. Intern review may measure reviewability, locator accuracy, clarity, apparent false positives, apparent omissions, scope adherence, duplication, disagreement, and verification effort. It may not establish a gold answer, accept risk, determine compliance, approve a specialist, authorize a change, or alter harness state.
9. Require later appropriately qualified subject-matter adjudication before any intern-reviewed item becomes gold, negative, or promotion evidence. Reviewer qualifications and access must match the specialist domain. Project-owner finalization remains the only project-state authority under ADR-0033; subject-matter adjudication supplies semantic expertise and is not a mandatory second project verifier.
10. Exclude confirmed or suspected secret values, controlled data, exploit-enabling sensitive content, and evidence above the reviewers' authorized access. Redaction must preserve source identity and location. If safe reproducibility cannot be preserved, mark the item inaccessible and do not distribute it.
11. Measure at least locator success, claim support rate, partial-support rate, apparent false-positive rate, duplicate rate, scope-violation rate, unresolved rate, reviewer agreement, median verification time, evidence requests, and qualitative usability. Do not treat agreement or acceptance rate alone as correctness.
12. Keep the accepted `SPEC-SECRETS -> PROD-SEC -> CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK` reference route and all accepted report, distribution, deployment, and A100 production state unchanged. `SPEC-SECRETS` candidate work under this ADR is revalidation and hardening of the proven specialist template, not replacement or automatic promotion of that route. Any later scheduling, product fan-in, baseline promotion, broader human distribution, or deployment requires a separate decision.
13. Execute the work only through the scoped increments in the specialist buildout plan. Each increment must close its structural, semantic, evidence, safety, human-review, and rollback gates before the project owner authorizes the next increment. A passing agent does not automatically authorize another agent, its wave peers, or any downstream consumer.

## Proposed flow

`common candidate and review boundary -> phased agent-specific specification/prompt/schema/rubric/tool implementation -> pinned read-only evidence manifests -> focus-bound specialist candidate runs -> retained raw responses -> deterministic projections and validation -> exact evidence locators -> access-appropriate comparison-only human review packets -> measured disagreement and reviewability -> qualified semantic adjudication -> project-owner decision on the next increment`

## Alternatives considered

- Build all specialist agents in one concurrent wave: rejected because failures in the shared prompt, evidence, packet, or review method would be multiplied before the calibration loop is understood. All agents remain in scope, but construction is phased.
- Begin general intern distribution with `SPEC-SECRETS`: rejected because secret-related evidence requires stricter access and safe-handling controls. Its proven runtime remains the implementation template and is revalidated in a restricted review wave.
- Exclude seed-status agents until an unspecified later phase: rejected because the project owner directed a complete `SPEC-*` buildout. Seed roles remain in scope but must pass specification-maturity checks before prompt implementation.
- Treat intern consensus as expert truth: rejected because agreement does not establish domain authority or semantic correctness.
- Feed successful candidate outputs directly into product synthesis: rejected because candidate calibration and downstream admission are separate governed decisions.
- Run the candidates on A100 production infrastructure: rejected because development, calibration, regression, and shadow testing belong on GX-10, DGX Spark, or an approved equivalent under ADR-0008.

## Rollback

Disable candidate discovery and dispatch for `SPEC-DEPS` and `SPEC-SBOM`, revoke any active shadow-review eligibility, stop packet export, and retain all prompts, manifests, raw responses, projections, reviews, metrics, and audit history as immutable development evidence. No accepted baseline route or authoritative state requires restoration because this ADR creates no scheduling, report, deployment, or production effect.

## Validation required

- exact identity, specification, contract, schema, prompt, rubric, focus-profile, model, tool, and evidence bindings for every `SPEC-*` agent;
- deterministic input selection and replay from a pinned read-only repository revision;
- role-specific differentiation within every overlapping specialist cluster, beginning with dependency health, SBOM inventory, and lint/tool evidence;
- source-located evidence for every actionable claim;
- fail-closed missing, mutable, inaccessible, unsafe, fabricated, duplicate, out-of-scope, and altered-evidence cases;
- raw-response versus harness-projection provenance;
- comparison-only lifecycle and downstream ineligibility enforcement;
- intern-review schema validation and immutable review attribution;
- safe redaction and access-control tests;
- measured human reviewability and disagreement without converting feedback into authority;
- tested rollback; and
- unchanged baseline, report, distribution, deployment, and A100 production state.

## Decision requested

Approve, reject, or amend the phased all-specialist human-shadow-calibration program. Approval authorizes the scoped increments for all 22 registered `SPEC-*` agents: common candidate and review-packet contracts; agent-specific prompt, schema, rubric, focus, and tool bindings; deterministic fixtures and negative cases; GX-10 or DGX Spark-equivalent live calibration; and access-appropriate comparison-only human review packets. Work remains subject to per-increment project-owner continuation. Approval does not authorize deployment, scheduling, product fan-in, authoritative findings, gold-standard admission without qualified semantic adjudication, leadership-report changes, distribution approval, release decisions, or A100 production execution.

## Decision

Accepted by `thomasverburgt`, project owner, on 2026-08-03. The project owner also approved the linked specialist-agent buildout increment plan. This acceptance authorizes construction and validation of Increment 0, the common specialist candidate and human-review boundary. Later increments remain sequenced under this ADR and require explicit project-owner continuation after the preceding increment's evidence is reviewed. No specialist is deployed, scheduled, admitted to product fan-in, represented as authoritative, or authorized for A100 production execution by this decision.
