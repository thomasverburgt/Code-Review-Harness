# ADR-0021: Align Enterprise Registry Status with Executable Reality and Admit ENT-ARCH as a Candidate

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Depends on: ADR-0006, ADR-0007, ADR-0017, ADR-0018, ADR-0020

## Context

The enterprise registry currently labels twelve enterprise roles as `baseline`, but the accepted executable vertical contains only `ENT-EVIDENCE` and `ENT-SYSRISK`. The other roles have design specifications but lack the complete prompt, role schema, rubric, deterministic projection, gold and negative packages, workflow node, downstream compatibility evidence, and GX-10 calibration required by the harness's own admission standard.

Treating prose-only roles as baseline weakens registry meaning and could allow an orchestrator or operator to mistake intended architecture for scheduled capability. The accepted Increment 5 sequence calls next for enterprise architecture, governance, strategic scoring, and synthesis workflows. `ENT-ARCH` is the best first addition because it establishes the system-of-systems dependency and interface posture later consumed by architecture strategy, technical-debt, modernization, and enterprise synthesis roles.

The live CAP-REQ artifact remains blocked pending an external requirements-authority disposition under ADR-0020. That gate must not be bypassed. Candidate enterprise contract work may proceed using explicitly marked fixtures and accepted existing inputs, but it must not characterize single-capability evidence as multi-capability architectural fitness or modify the accepted enterprise/report path.

## Proposed decision

1. Reserve `baseline` status for roles that are present in an accepted executable workflow and have passed the complete conformance gate.
2. Keep `ENT-EVIDENCE` and `ENT-SYSRISK` at `baseline`. Change the remaining prose-only enterprise roles to `planned` until each completes candidate admission and a separate scheduling decision.
3. Admit `ENT-ARCH` as the first enterprise candidate by defining its versioned prompt, strict role schema, rubric, deterministic projection, candidate workflow, gold package, negative cases, and immutable evidence.
4. Require `ENT-ARCH` to consume an exact `ENT-EVIDENCE` validated input manifest plus the capability artifacts named by that manifest. Missing, extra, stale, mutated, incompatible, candidate-only, or ineligible inputs fail closed.
5. Separate bounded candidate evidence from live fitness:
   - adjudicated synthetic multi-capability fixtures may prove contract and correlation behavior;
   - accepted live single-capability input may prove only protocol, lineage, and source-location handling;
   - system-of-systems fitness requires an accepted live multi-capability input set in a later increment.
6. Keep all model-generated architecture assertions explicitly sourced and advisory. `ENT-ARCH` cannot approve architecture, establish a target state, select a design, resolve conflicts, accept risk, alter requirements, authorize report distribution, schedule another agent, or authorize deployment.
7. Keep the accepted workflow, immutable report package, governance records, CAP-REQ eligibility state, and CAP-SYNTH scheduling state unchanged.
8. Target production deployment to the A100 large cluster and perform all conformance, calibration, integration, rollback, and regression testing on a DGX Spark or approved equivalent, currently GX-10.

## Alternatives considered

- **Implement `ENT-SYNTH` next:** rejected because synthesis should consume proven architecture, governance, strategic, and risk inputs rather than absorb their responsibilities into one prompt.
- **Implement `ENT-GOV` first:** viable, but architecture establishes reusable dependency and interface topology for more downstream enterprise roles and exposes cross-capability input limitations earlier.
- **Leave all enterprise roles marked baseline:** rejected because registry status would continue to overstate executable capability.
- **Wait for the external CAP-REQ disposition before any enterprise work:** rejected because isolated candidate admission does not consume CAP-REQ as an accepted input or change operational state.

## Consequences

The registry becomes a truthful scheduling and discovery control instead of a catalog of aspirations. `ENT-ARCH` gains a testable, narrow admission path. Some documentation will show fewer baseline enterprise roles, which is intentional and reversible. The increment does not increase accepted production scope.

## Rollback

Remove the `ENT-ARCH` candidate workflow from discovery, restore its status to `planned`, and retain candidate prompts, schemas, fixtures, and evidence for audit. The accepted `ENT-EVIDENCE -> ENT-SYSRISK` workflow and direct report path remain unchanged, so rollback requires no report, governance, deployment, or A100 production migration.

## Validation required

- registry statuses agree across machine-readable and human-readable registries;
- the accepted workflow contains only executable baseline roles;
- exact ENT-EVIDENCE manifest and capability-artifact binding;
- strict universal, enterprise, and ENT-ARCH role validation;
- deterministic projection, immutable ledger, and replay;
- source-located, assertion-level traceability and explicit uncertainty;
- fail-closed missing, extra, stale, mutated, incompatible, unauthorized, and ineligible inputs;
- no architecture approval, risk acceptance, requirements change, scheduling, report, governance, or deployment authority;
- accepted baseline, report package, and ADR-0020 packet remain byte-identical; and
- full local and GX-10 regression plus isolated Qwen3-32B candidate calibration.

## Decision requested

Approve, reject, or amend the enterprise registry correction and isolated `ENT-ARCH` candidate-admission increment. Approval authorizes implementation and testing only; it does not schedule `ENT-ARCH`, accept CAP-REQ, schedule CAP-SYNTH, or promote any A100 production workflow.

## Decision

Accepted by the project maintainer on 2026-08-01. Acceptance authorizes registry correction, isolated candidate implementation, and conformance testing only. It does not schedule `ENT-ARCH` or alter any external human gate.
