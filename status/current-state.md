# Current Harness State

**As of:** 2026-08-02
**Projection authority:** derived only  
**Enterprise shadow state:** `blocked_as_designed`

The accepted baseline route remains `ENT-EVIDENCE -> ENT-SYSRISK`. No enterprise shadow candidate is scheduled and no deployment or A100 production state has changed.

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
