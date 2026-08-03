# ADR-0035: Evaluate ENT-ARCH Using Semantically Accepted CAP-SYNTH Without Scheduling Either Candidate

- Status: accepted
- Date: 2026-08-02
- Decision authority: project owner
- Owners: enterprise architecture, capability synthesis, orchestration, evidence governance, and validation
- Depends on: ADR-0021, ADR-0025, ADR-0033, and ADR-0034
- Supersedes: none
- Superseded by: none

## Context

ADR-0021 admitted `ENT-ARCH` as an isolated candidate. Its adjudicated two-capability fixture proved contract mechanics, while its accepted-live `CAP-RISK`-only run proved protocol and lineage for one capability artifact. Neither established accepted-live multi-domain enterprise-architecture fitness.

ADR-0034 now provides an exact CAP-SYNTH candidate whose CAP-RISK and CAP-REQ synthesis was accepted by the project owner as semantically faithful and made revocably eligible for enterprise candidate evaluation. The candidate represents one bounded capability informed by two review domains. It does not represent multiple operational capabilities and cannot support claims about cross-capability dependency topology, shared-service concentration, or failure propagation.

Passing CAP-SYNTH together with its CAP-RISK and CAP-REQ children as three independent enterprise inputs would double-count the same evidence. The enterprise boundary therefore needs an exact, lineage-aware rule before ENT-ARCH evaluation.

## Proposed decision

1. Admit only the exact owner-finalized CAP-SYNTH artifact named by the ADR-0034 enterprise-evaluation eligibility record. Reject missing, mutated, revoked, substituted, fixture-tier, or merely schema-valid candidates.
2. Construct an `ENT-EVIDENCE` manifest that names CAP-SYNTH as one capability artifact and retains its complete child lineage. Do not also present the CAP-RISK and CAP-REQ children as independent enterprise capability inputs.
3. Label the run `accepted_live_multi_domain_single_capability_evaluation`. This tier permits evaluation of architecture evidence coherence within the bounded capability; it does not prove multi-capability or system-of-systems architecture fitness.
4. Permit sourced observations about the capability's declared architecture posture, unresolved evidence, traceability, and transition unknowns. Require `insufficient_evidence` or `not_assessed` for any topology, concentration, propagation, target-state, or transition claim unsupported by the source artifacts.
5. Execute the pinned ENT-ARCH Qwen3-32B candidate on GX-10 or another approved DGX Spark equivalent. Preserve exact evidence references, source-record lineage, uncertainty, confidence provenance, and human authority.
6. Produce a deterministic comparison, an anti-double-counting record, an enterprise-consumer compatibility record, and an exact semantic-review packet for project-owner disposition.
7. Keep ENT-ARCH and CAP-SYNTH unscheduled. Do not modify reports, distribution state, deployment, or the A100 production baseline.
8. Preserve `CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK` as the accepted rollback route. Revoking CAP-SYNTH evaluation eligibility must fail closed without deleting retained evidence.

## Proposed flow

`owner-finalized CAP-SYNTH semantic eligibility -> exact CAP-SYNTH artifact -> lineage-aware ENT-EVIDENCE manifest -> isolated GX-10 ENT-ARCH evaluation -> project-owner semantic review -> later scheduling decision`

## Alternatives considered

- Pass CAP-RISK, CAP-REQ, and CAP-SYNTH independently: rejected because it double-counts parent and child evidence.
- Claim accepted-live multi-capability fitness: rejected because the bounded slice contains one capability.
- Schedule CAP-SYNTH before evaluating ENT-ARCH: rejected because explicit immutable candidate eligibility is sufficient for isolated evaluation and keeps rollback smaller.
- Skip ENT-ARCH and proceed directly to ENT-SYNTH: rejected because ENT-SYNTH consumes enterprise domain artifacts, not capability artifacts directly.

## Rollback

Revoke CAP-SYNTH enterprise-evaluation eligibility, disable the ADR-0035 candidate workflow, retain all evidence, and continue the accepted direct enterprise route. No report, distribution, deployment, or production migration is required.

## Validation required

- exact CAP-SYNTH disposition, finalization, eligibility, artifact ID, and artifact hash;
- no parent-child double counting;
- exact ENT-EVIDENCE gate and input-manifest binding;
- fail-closed mutation, substitution, revocation, missingness, tier-confusion, and invented-lineage cases;
- honest single-capability scope and unsupported-claim suppression;
- deterministic replay and pinned GX-10 model execution;
- exact semantic-review packet and project-owner authority;
- comparison-only downstream compatibility;
- tested rollback; and
- unchanged scheduling, reports, distribution, deployment, and A100 production baseline.

## Decision requested

Approve, reject, or amend the isolated ENT-ARCH accepted-live multi-domain single-capability evaluation. Approval authorizes bounded implementation and GX-10 evaluation only; it does not authorize CAP-SYNTH scheduling, ENT-ARCH scheduling, enterprise shadow integration, report changes, deployment, or A100 production promotion.

## Decision

Accepted by `thomasverburgt`, project owner, on 2026-08-02. Acceptance authorizes the exact bounded implementation, negative and rollback controls, deterministic evidence, GX-10 model evaluation, and human semantic-review packet described above. It creates no scheduling, report, distribution, deployment, risk-acceptance, requirements-satisfaction, or A100 production authority.

## Implementation results

The bounded increment is implemented. The exact ADR-0034 CAP-SYNTH eligibility record produces a lineage-aware ENT-EVIDENCE gate and input manifest that admits only CAP-SYNTH as the capability input while retaining its CAP-RISK and CAP-REQ children as excluded lineage. Mutation, substitution, revocation, missing eligibility, tier confusion, parent-child double counting, and unsupported single-capability architecture claims fail closed.

The first GX-10 Qwen3-32B attempt was retained as failed-closed evidence. It preserved genuine source evidence references that the initial runtime allow-list did not recognize and proposed architecture-debt and corrective-action content unsupported at this tier. The tightened projection now distinguishes valid preserved evidence references from independent inputs and makes topology, concentration, propagation, debt, CAPA, target-state, and transition fields harness-owned safety controls.

The successful GX-10 candidate was subsequently corrected before semantic disposition. The projection now restores the child-qualified decision IDs `6beec632-8baf-5a58-a4ce-fa14784d8435:DC-001` and `a5ada795-db2f-5625-aed9-1b619411be17:DC-001`, rejects bare or duplicate child decision IDs, and describes the gate input as CAP-SYNTH rather than the inherited CAP-RISK wording. The prior successful package remains retained as historical evidence.

The corrected candidate has artifact ID `00f8b5b9-19f9-5a1b-8cd1-3122333f2d55` and hash `sha256:321186b8016dde5dee6f4948d5254397a011e6796b0c63ae5bebf49ab2d3faab`. Its corrected semantic-review packet has ID `09c336f5-faa1-519a-a375-b4ba18cf2384` and hash `sha256:170b55b2ff03a9e4ca034f52f3eedec3a2cb3c9d948146bb0eafb5c6db8126e5`. The exact retained model response was reprojected on GX-10 without new inference; its raw-response hash remains `a65e88e6dd8d488c83d63d681ccd4683bc2d33c33b243509640c9722c3a9796a`.

The candidate preserves the accepted CAP-SYNTH posture and rates architecture coherence `insufficient_evidence`. It retains the requirements-traceability gap and unresolved credential-like-value classification while making no unsupported topology, shared-service concentration, failure-propagation, architecture-debt, CAPA, target-state, or transition claim. The run consumed 4,986 input tokens and 1,522 output tokens. Local regression and scoped GX-10 conformance pass. Project-owner semantic disposition remains the only open gate for this evaluation; CAP-SYNTH and ENT-ARCH remain unscheduled.

The project owner subsequently determined that the corrected candidate passes semantic disposition. The immutable disposition has ID `68e9d697-10b5-5ff4-860e-3717ddfbebbd` and hash `sha256:ce17eb5e49c93e60ac04e2955299cb2a1c13b43bfdc02bbe4da3c5f3fe638eea`. Project-owner finalization has ID `5039e427-7250-544a-92d9-69c793aa4300` and hash `sha256:4669e14c291cd4fc8e5fcc42ef3209f3f078c5b41566cda715bd0311d8c27e01`. The derived, revocable ENT-SYNTH evaluation eligibility has ID `a06c4519-d7c0-5816-9e02-bb7967558c24` and hash `sha256:463251fb7f60afea8e21eb30884dd8ee0e5fc7b6ba25ffd9992348a717c81c31`. This disposition does not schedule ENT-ARCH or ENT-SYNTH and creates no architecture approval, report, distribution, deployment, or production authority.
