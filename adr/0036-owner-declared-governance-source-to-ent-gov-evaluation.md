# ADR-0036: Evaluate ENT-GOV Using an Owner-Declared Governance Source and Semantically Accepted CAP-SYNTH

- Status: accepted
- Date: 2026-08-02
- Decision authority: project owner
- Owners: enterprise governance, capability synthesis, orchestration, evidence governance, and validation
- Depends on: ADR-0022, ADR-0033, ADR-0034, and ADR-0035
- Supersedes: none
- Superseded by: none

## Context

ADR-0022 admitted ENT-GOV as an isolated candidate and proved governance-source protocol, matrix mechanics, exact bindings, missing-evidence behavior, and human authority. Its retained live run was explicitly a single-capability source/protocol smoke test, not accepted-live governance fitness.

ADR-0034 now supplies an exact, semantically accepted CAP-SYNTH artifact representing the bounded identity-and-access capability. ADR-0035 supplies a separately accepted ENT-ARCH peer-domain result, but ENT-ARCH must not become an input authority for ENT-GOV. Enterprise domain reviewers should independently evaluate the same accepted capability posture against their own authoritative sources before later synthesis.

The existing ADR-0022 governance manifest is a fixture declaration by `Project Maintainer Fixture Authority`. It is useful historical contract evidence but cannot be silently promoted into an accepted-live owner declaration. A new content-addressed governance-source declaration is required.

## Proposed decision

1. Create an immutable governance-source manifest declared by `thomasverburgt` in the registered governance-source-owner capacity. Bind each source to an immutable revision, exact path and lines, content hash, applicability determination, obligation text, required evidence, approval dependency, exception process, lifecycle state, and retention rule.
2. Admit only the exact owner-finalized CAP-SYNTH artifact named by its active enterprise-evaluation eligibility record. Retain CAP-RISK and CAP-REQ as lineage and do not count them as independent capability inputs.
3. Construct a new exact ENT-EVIDENCE gate and ENT-GOV evaluation manifest binding the CAP-SYNTH artifact, its eligibility, and the owner-declared governance-source manifest.
4. Label the run `accepted_live_multi_domain_single_capability_governance_evaluation`. This tier permits obligation-by-obligation evidence assessment for the bounded capability. It does not prove cross-capability governance consistency, enterprise governance maturity, legal compliance, approval, exception, or policy authority.
5. Require every compliance-matrix row to preserve the exact obligation, applicability, required evidence, supplied evidence, missingness, confidence, and uncertainty. Missing evidence must remain `insufficient_evidence`, never noncompliance or compliance by inference.
6. Preserve exception and approval records without model-authored creation or modification. The model may identify missing records or request human decisions but cannot grant an exception, approve compliance, interpret law authoritatively, or change policy.
7. Execute the pinned ENT-GOV Qwen3-32B candidate on GX-10 or another approved DGX Spark equivalent. Produce deterministic comparison evidence, negative and rollback evidence, downstream compatibility, and an exact project-owner semantic-review packet.
8. Keep CAP-SYNTH, ENT-GOV, ENT-ARCH, and ENT-SYNTH unscheduled. Do not modify the accepted report, distribution state, deployment, or A100 production baseline.

## Proposed flow

`owner-declared governance sources + owner-finalized CAP-SYNTH eligibility -> exact ENT-EVIDENCE/governance input manifest -> isolated GX-10 ENT-GOV evaluation -> project-owner semantic review -> later ENT-SYNTH evaluation eligibility decision`

The accepted implementation refines that flow as follows:

`authority-registry-bound owner declaration + exact CAP-SYNTH artifact and eligibility -> JSON-pointer governance evidence-binding manifest -> exact ENT-EVIDENCE/governance evaluation manifest -> retained raw GX-10 model response -> disclosed harness-owned governance projection -> project-owner semantic review -> later ENT-SYNTH evaluation eligibility decision`

## Alternatives considered

- Promote the ADR-0022 fixture manifest: rejected because fixture authority and accepted-live authority are not interchangeable.
- Feed ENT-ARCH into ENT-GOV: rejected because peer enterprise domains must preserve independent authority and evidence boundaries.
- Evaluate CAP-RISK and CAP-REQ separately alongside CAP-SYNTH: rejected because that double-counts parent and child evidence.
- Proceed directly to ENT-SYNTH: rejected because accepted-live ENT-GOV and ENT-STRAT domain evidence is still missing.
- Schedule ENT-GOV after a passing model run: rejected because semantic acceptance and scheduling are distinct project-owner decisions.

## Rollback

Revoke the governance-source declaration or CAP-SYNTH evaluation eligibility, disable the ADR-0036 candidate workflow, retain all evidence, and return ENT-GOV to its ADR-0022 protocol-only posture. ENT-ARCH semantic acceptance and the accepted direct `CAP-RISK -> ENT-EVIDENCE -> ENT-SYSRISK` route remain unchanged.

## Validation required

- exact project-owner/governance-source-owner authority;
- immutable source, applicability, obligation, CAP-SYNTH, eligibility, gate, and manifest bindings;
- no CAP-SYNTH child double counting;
- no fixture-tier promotion;
- complete obligation-by-capability matrix;
- fail-closed mutation, substitution, revocation, missingness, stale source, invented evidence, invented exception, invented approval, and authority-confusion cases;
- honest single-capability scope and missing-evidence semantics;
- deterministic replay and pinned GX-10 model execution;
- exact semantic-review packet and project-owner authority;
- tested rollback; and
- unchanged scheduling, reports, distribution, deployment, and A100 production baseline.

## Decision requested

Approve, reject, or amend the isolated ENT-GOV accepted-live single-capability governance evaluation. Approval authorizes the exact source declaration, bounded implementation, negative and rollback controls, deterministic evidence, GX-10 evaluation, and semantic-review packet. It does not authorize governance approval, compliance determination, exceptions, scheduling, report changes, deployment, or A100 production promotion.

## Decision

Accepted by `thomasverburgt`, project owner, on 2026-08-02. Acceptance authorizes the bounded source declaration, implementation, fail-closed controls, deterministic evidence, GX-10 evaluation, and semantic-review packet described above. It creates no compliance, exception, scheduling, report, distribution, deployment, or A100 production authority.

## Implementation results

The accepted increment is implemented. The owner declaration binds `GOVERNANCE.md` line 13 at immutable revision `ab84b15d3c6bd6ba2c594c9a01457df8474d623e`, declares exact applicability to the bounded capability, and preserves obligation `GOV-AGENT-AUTH-001`. The enterprise gate admits only the exact owner-finalized CAP-SYNTH artifact; CAP-RISK and CAP-REQ remain excluded child lineage.

The first Qwen3-32B projection passed structural validation but was rejected during semantic inspection because its compliance-row rationale repeated requirements and credential uncertainty instead of evaluating the declared agent-authority obligation. That attempt remains retained. The tightened harness makes the obligation row policy-owned at this single-capability tier, preventing unrelated evidence, inferred compliance, noncompliance, exceptions, approvals, maturity, or CAPA from entering the candidate. The exact raw response was reprojected on GX-10 without new inference.

The corrected candidate has artifact ID `efc768dc-b057-530e-9270-bafb88551b29` and hash `sha256:d3cf61bd18259951db9c7ec2ffe185707750dcbf1f5f5d552a809758cd2bc031`. Its semantic-review packet has ID `8548f24f-4de0-51f9-974e-3967e68dd3b8` and hash `sha256:c9a89097923a1a932ba567b75182c4467adc3d971ef69002239e7e52d9460b68`.

The candidate concludes `insufficient_evidence`: CAP-SYNTH preserves human authority, advisory-only posture, and an unscheduled comparison handoff, but does not prove enforcement of every repository agent prohibition. The initial inference consumed 6,299 input tokens and 1,011 output tokens. Scoped GX-10 conformance passes. Project-owner semantic disposition remains the only open gate; CAP-SYNTH, ENT-GOV, ENT-ARCH, and ENT-SYNTH remain unscheduled.

Human semantic review required a further flow correction before disposition. The project owner accepted the recommendations to remove the unrelated `DERIVED-001` reference, add exact field-level evidence locators, bind the source declaration to `HUMAN-PROJECT-OWNER-001` and authority-registry version `0.7.0`, clarify confidence, and distinguish raw model output from harness-owned projection.

The revised flow now binds four exact JSON pointers covering human decision authority, advisory-only posture, comparison-only handoff, and unscheduled eligibility. The candidate inputs and traceability manifest explicitly include CAP-SYNTH eligibility, the governance evidence-binding manifest, and the evaluation input manifest. Its execution record identifies `model_response_with_harness_owned_governance_projection`, retains raw response hash `58c56cfd650f34dba9acc4440f1d5f8b803ef13d1d6aa8e28d8afffcaed39d64`, and enumerates every harness-owned field. Confidence `0.85` is explicitly confidence in bounded evidence insufficiency, not compliance.

The revised candidate has ID `86456e45-010b-571a-97fb-f78a275320a9` and hash `sha256:ee04f21b04d026cecfc6040568812b32a39c833f8d2b4910ff91e6844aa6d370`. Its revised semantic-review packet has ID `2310362f-43a1-55d0-8243-fa739d01b3b4` and hash `sha256:869f86a26c52085e3b8ad7df6e04519499cc984a61eed046ac92b635d1d3cc07`. Revised-flow conformance passes on GX-10; scheduling and authority effects remain unchanged.

The project owner subsequently determined that the revised packet checks out. The immutable semantic disposition has ID `94161331-c940-51bc-ad08-d7f7e1af1243` and hash `sha256:1b465d9f7cc884dfa5365665512cab54653c67e2f85c82ac1d2a20e93fbf7b97`. Project-owner finalization has ID `16b27673-e2c2-55d0-9c85-72de72ef25b6` and hash `sha256:8439d5498def6ebf5c6b7cc373dc4ddea86c82ec3ed1f9db6e968a455c42332e`. The derived, revocable ENT-SYNTH evaluation eligibility has ID `eb7281e3-f6f0-5603-9f65-ee4c9d7d08cc` and hash `sha256:1b5be2941ae9ee981a378600305f340545a44e3e8fd07d9de27b828245d5dbd9`. This acceptance does not schedule ENT-GOV or ENT-SYNTH and creates no compliance determination, exception, approval, policy, report, distribution, deployment, or production authority.
