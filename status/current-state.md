# Current Harness State

**As of:** 2026-08-03
**Projection authority:** derived only  
**Enterprise shadow state:** `blocked_as_designed`

The accepted baseline route remains `ENT-EVIDENCE -> ENT-SYSRISK`. No enterprise shadow candidate is scheduled and no deployment or A100 production state has changed.

## Specialist candidate program

ADR-0039 and the linked all-specialist increment plan are accepted. Machine construction, GX-10 calibration, and the Increment 8 comparison are complete for all 22 registered `SPEC-*` agents. Increment 0 established the common boundary; Increments 1-7 built every registered specialist; Increment 8 produced the all-agent comparison, retrospective, final-state register, and consolidated human-review handoff. The project owner directed that all human review be held until the specialist candidate waves were built, so the consolidated review is now the next program gate. This does not admit or schedule any agent. No specialist candidate is deployed, eligible for product fan-in or leadership-report use, or authorized for A100 production execution.

All 22 exact prompts, role schemas, rubrics, model and tool manifests, deterministic candidates, negative mutations, evidence locators, and review packets pass locally and in retained GX-10 live calibrations. The program used 53,369 input tokens and 8,641 output tokens. The latest GX-10 run re-ran prior deterministic suites before inference, then passed all 11 remaining roles; the retrieved evidence contained zero exact rotated-key or restricted credential-marker matches. The final-state register records all 22 as `blocked_on_evidence` because human responses, qualified adjudications, and owner candidate dispositions remain absent—not because construction failed. Role-specific contracts keep intended, configured, desired, test, runtime, exploitability, secret classification, risk, and whole-product posture distinct. No GX-10 result is treated as A100 performance evidence. The accepted SPEC-SECRETS route is unchanged and replayable. The existing ZIP handoff artifact is intentionally not refreshed during incremental work.

| Prerequisite | Current state | Remaining gate |
|---|---|---|
| ADR 0016 semantic adjudication | Pending external decision | Enterprise-risk acceptance response and project-owner finalization |
| ADR 0020 requirements acceptance | Owner-finalized; CAP-REQ eligible | No remaining acceptance gate; eligibility is revocable and does not schedule CAP-SYNTH |
| CAP-SYNTH accepted-live evaluation | Semantically accepted and owner-finalized; eligible for enterprise candidate evaluation | Any scheduling still requires a separate ADR |
| ENT-ARCH | Semantically accepted and owner-finalized; eligible for ENT-SYNTH candidate evaluation | Any scheduling remains a separate ADR |
| ENT-GOV | Semantically accepted and owner-finalized; eligible for ENT-SYNTH candidate evaluation | Any scheduling remains a separate ADR |
| ENT-STRAT | Corrected candidate semantically accepted and owner-finalized; active eligibility issued | No remaining ADR-0038 admission gate; scheduling remains separately prohibited |
| ENT-SYNTH | Final GX-10 candidate semantically accepted and owner-finalized; active bounded shadow-integration eligibility issued | A separate integration design/decision is next; scheduling remains unauthorized |

The machine-readable source for this view is [`current-state.json`](current-state.json). Creation-time readiness manifests remain immutable snapshots and may show the state that existed before later human responses were recorded.
