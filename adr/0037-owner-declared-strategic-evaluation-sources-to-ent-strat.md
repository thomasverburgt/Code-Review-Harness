# ADR-0037: Evaluate ENT-STRAT Using Owner-Declared Project Strategy Sources and Semantically Accepted CAP-SYNTH

- Status: accepted
- Date: 2026-08-02
- Decision authority: project owner
- Owners: enterprise strategy, capability synthesis, orchestration, evidence governance, and validation
- Depends on: ADR-0023, ADR-0033, ADR-0034, ADR-0035, and ADR-0036
- Supersedes: none
- Superseded by: none

## Context

ADR-0023 admitted ENT-STRAT as an isolated candidate and proved objective and scoring-method authority boundaries, exact bindings, missing-data behavior, deterministic scoring controls, and human decision authority. Its retained live run was a single-domain protocol calibration using fixture-authority sources; it was not accepted-live strategic fitness.

CAP-SYNTH is now semantically accepted and eligible for bounded enterprise candidate evaluation. ENT-ARCH and ENT-GOV have independently evaluated that same capability posture and are eligible for later ENT-SYNTH candidate evaluation. ENT-STRAT is the remaining peer enterprise domain without accepted-live evidence.

ENT-STRAT must independently evaluate the accepted capability posture against authoritative strategy inputs. ENT-ARCH and ENT-GOV outputs must not become strategy authority or be used to manufacture objectives, weights, thresholds, or scores. The ADR-0023 fixture manifests also must not be silently promoted into accepted-live authority.

The bounded evaluation concerns the Code Harness project, so the project owner may declare project-level evaluation objectives and the deterministic scoring method. This authority does not extend to an external enterprise's mission strategy, investment approval, portfolio prioritization, risk acceptance, or deployment authorization.

## Proposed decision

1. Create immutable project-strategic-objective and scoring-method manifests declared by `thomasverburgt`, bound to `HUMAN-PROJECT-OWNER-001`, the exact authority-registry version and hash, immutable repository sources, applicability, measures, directionality, weights, missingness policy, sensitivity rules, and prohibition on an aggregate composite score.
2. Version the authority registry without destroying the exact prior registry state. The new version may authorize the project owner to declare Code Harness project-evaluation objectives and methods only. Historical source manifests and packets remain verifiable against their retained registry snapshots.
3. Admit only the exact semantically accepted CAP-SYNTH artifact named by its active enterprise-evaluation eligibility record. Preserve CAP-RISK and CAP-REQ as excluded child lineage and do not count ENT-ARCH or ENT-GOV as strategic evidence inputs.
4. Construct an exact ENT-EVIDENCE gate and ENT-STRAT evaluation-input manifest binding CAP-SYNTH, its eligibility, the objective manifest, the scoring-method manifest, and field-level evidence locators.
5. Label the run `accepted_live_multi_domain_single_capability_strategy_evaluation`. This tier permits an objective-by-objective assessment of the bounded Code Harness capability posture. It does not establish enterprise strategy, portfolio priority, investment value, mission effectiveness, cross-capability strategic alignment, or production fitness.
6. Preserve every missing measure as missing. Do not impute values, normalize unavailable data to zero, invent targets, select weights, create thresholds, or calculate a composite score. Confidence must describe the bounded assessment or its insufficiency, not strategic approval.
7. Separate raw model output from harness-owned authority, manifests, deterministic scoring controls, exact bindings, prohibited fields, and downstream state. Every projected field must disclose its provenance.
8. Execute the pinned Qwen3-32B ENT-STRAT candidate on GX-10 or another approved DGX Spark equivalent. Produce deterministic comparison evidence, negative and rollback evidence, downstream compatibility, and an exact project-owner semantic-review packet.
9. Keep CAP-SYNTH, ENT-ARCH, ENT-GOV, ENT-STRAT, and ENT-SYNTH unscheduled. Do not modify the accepted report, distribution state, deployment, or A100 production baseline.

## Proposed flow

`registry-bound project-owner objective and method declarations + exact accepted CAP-SYNTH eligibility -> field-level strategy evidence bindings -> exact ENT-EVIDENCE/ENT-STRAT input manifest -> retained raw GX-10 model response -> disclosed harness-owned strategic projection -> project-owner semantic review -> later ENT-SYNTH evaluation eligibility decision`

## Alternatives considered

- Promote ADR-0023 fixture manifests: rejected because fixture authority is not accepted-live authority.
- Feed ENT-ARCH or ENT-GOV into ENT-STRAT: rejected because peer enterprise domains must preserve independent source and authority boundaries.
- Require an external enterprise-strategy authority for this project-scoped evaluation: deferred because the current subject is the Code Harness project, for which the project owner is the authoritative source. External-enterprise claims remain prohibited.
- Allow the model to select weights or calculate a composite: rejected because those are human-controlled method decisions and would create false precision from sparse evidence.
- Proceed directly to ENT-SYNTH without ENT-STRAT: rejected because the planned synthesis completeness set includes ENT-STRAT.

## Rollback

Revoke either strategy-source declaration or CAP-SYNTH evaluation eligibility, disable the ADR-0037 candidate workflow, retain all evidence and registry snapshots, and return ENT-STRAT to its ADR-0023 protocol-only posture. ENT-ARCH and ENT-GOV semantic acceptance and the accepted direct `ENT-EVIDENCE -> ENT-SYSRISK` route remain unchanged.

## Validation required

- exact project-owner subject, scope, registry-version, and registry-hash authority;
- retained historical authority-registry snapshot verification;
- immutable objectives, measures, method, CAP-SYNTH, eligibility, gate, evidence-locator, and input-manifest bindings;
- no CAP-SYNTH child or enterprise-peer double counting;
- no fixture-tier promotion or external-enterprise strategy claim;
- complete objective-by-capability matrix with explicit missingness;
- fail-closed mutation, substitution, revocation, stale source, invented objective, invented measure, invented weight, silent imputation, unauthorized threshold, composite-score, and authority-confusion cases;
- raw-model versus harness-projection provenance;
- deterministic replay and pinned GX-10 execution;
- exact semantic-review packet and project-owner authority;
- tested rollback; and
- unchanged scheduling, reports, distribution, deployment, and A100 production baseline.

## Decision requested

Approve, reject, or amend the isolated ENT-STRAT accepted-live single-capability strategy evaluation. Approval authorizes the bounded authority-registry versioning, project-owner source declarations, implementation, negative and rollback controls, deterministic evidence, GX-10 evaluation, and semantic-review packet. It does not authorize strategic approval, portfolio or investment decisions, scheduling, report changes, deployment, or A100 production promotion.

## Decision

Accepted by `thomasverburgt`, project owner, on 2026-08-02. Acceptance authorizes the bounded registry versioning, project strategy-source declarations, implementation, fail-closed controls, deterministic evidence, GX-10 evaluation, and semantic-review packet described above. It creates no strategy, investment, portfolio, scheduling, report, distribution, deployment, or A100 production authority.

## Implementation results

The accepted increment is implemented. Authority registry `0.8.0` grants the project owner only the bounded Code Harness evaluation-source actions. The exact canonical `0.7.0` registry snapshot remains retained with hash `sha256:eb503882b2886f2966c80cfa30914b1b616bfba6ca96baf417962f0f1e28cc72`, preserving verification of ADR-0036's accepted source declaration.

The project objective is to preserve traceable, human-controlled review outputs for leadership and expert decisions. Its method assigns equal declared weights to human-authority preservation and exact finding-locator coverage, prohibits a composite, preserves missingness without imputation, and interprets confidence as confidence in bounded insufficiency rather than strategic approval. CAP-SYNTH is the only admitted capability input; CAP-RISK and CAP-REQ remain excluded lineage, while ENT-ARCH and ENT-GOV remain independent peer-domain outputs.

The pinned Qwen3-32B run on GX-10 reproduced the bounded role record. Two exact CAP-SYNTH locators support human decision authority and advisory-only operation. No supplied evidence establishes exact finding-locator coverage, so that measure remains missing and the objective remains `insufficient_evidence`. No score, threshold, strategic approval, portfolio decision, scheduling, report, deployment, or production authority is produced.

The live candidate has ID `9a0edab2-f80a-5179-a311-1975988ad252` and hash `sha256:ab5e620ffbab8ce32ec90687ecdb76e6f85af9735dade36fc037646a93ed7450`. Its semantic-review packet has ID `0a6862f2-ab8d-5c46-b41d-3315ec61c7ea` and hash `sha256:03d61c101eb4fa1b10d07e8a293c755e05313a9a47317ae0e93ad6acf84b7fdf`. The raw-response hash is `9e8bca069c37664cf7e8396e779263a29e6878551e4397aa36e370de213213ec`; the run consumed 5,632 input tokens and 1,674 output tokens. Project-owner semantic disposition is the remaining gate.

Semantic review identified four limitations: the categorical human-authority evidence is projected to numeric `1.0` without an explicit manifest mapping rule; numeric confidence fields lack a complete declared derivation formula; the observed-only `1.0–1.0` distribution requires context to avoid appearing complete; and the accepted-live project evaluation retains the legacy `ENTERPRISE-FIXTURE-001` scope identifier. The project owner accepted the packet as-is and directed continuation. These limitations are preserved rather than erased.

The immutable accept-as-is disposition has ID `5e03ee9f-d4be-5661-952e-360a734bfab3` and hash `sha256:2112f3259e6c92c014e8c44a379a52c0fe957f43cce231df53560875ed7e6cc6`. Project-owner finalization has ID `2c891750-d1a3-562a-ba3d-75900626a740` and hash `sha256:55c86f8589300918c4b9207544575240f685948ee7c0afe382b17e79c92e9357`. The derived, revocable ENT-SYNTH evaluation eligibility has ID `c5097c20-071f-57ad-8a83-8a3f03f9fa2d` and hash `sha256:e85844b4bf432c66c50b53948f4e9f3998119455ac63748361bc9bd74068fc3f`. It carries all four limitations forward and does not schedule ENT-STRAT or ENT-SYNTH.

The project owner subsequently directed correction of the limitations if feasible. All four were corrected: registry `0.8.0` is retained by exact snapshot and `0.9.0` adds `CODE-HARNESS-PROJECT-001`; `MAP-HUMAN-AUTHORITY-001` explicitly authorizes the categorical-to-`1.0` transformation; evidence coverage, component confidence, assessment confidence, and reconciliation now have declared formulas; and the component range is labeled `observed_components_only_not_objective_completeness` with one observed of two eligible components.

The corrected GX-10 candidate has ID `dd5598c9-628a-5f24-b974-9f2a53512119` and hash `sha256:e9a673ad1e126ccb19d75ee8c73bb142be82370505d0c5ce4cea3bf80190a8e2`. Its new packet has ID `a640de06-f9e1-5263-b928-d453ef860957` and hash `sha256:90d7dd3bc3f464b46f5d7550dc65f126147838c170272e86c16de7524d9b3a95`. The raw response exactly matches the corrected projected role. Supersession record `a98e0a1a-b689-509c-ae39-9049c0d60dc6` makes the earlier accepted candidate historical for ADR-0038 input selection.

The project owner accepted the corrected candidate as semantically faithful. Corrected disposition `024269c8-38c2-5779-9c5d-6e35d03c48a5`, project-owner finalization `d7de6aa7-58d1-5ceb-8b0e-25e7595e3d77`, and active eligibility `be1d1e86-78e7-5c68-94e6-88c570ba526f` bind the exact corrected candidate and packet. The eligibility carries the genuine remaining evidence boundaries, CAP-SYNTH source context, human-owned promotion request, and locator-evidence remediation requirement. It authorizes only the bounded ADR-0038 ENT-SYNTH candidate evaluation and schedules neither agent.
