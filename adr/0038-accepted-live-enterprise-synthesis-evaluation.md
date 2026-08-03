# ADR-0038: Evaluate ENT-SYNTH Using the Accepted Enterprise Domain Set Without Scheduling or Report Promotion

- Status: accepted
- Date: 2026-08-02
- Decision authority: project owner
- Owners: enterprise synthesis, enterprise domains, orchestration, evidence governance, and validation
- Depends on: ADR-0024, ADR-0033, ADR-0035, ADR-0036, and ADR-0037
- Supersedes: none
- Superseded by: none

## Context

ADR-0024 admitted ENT-SYNTH as an isolated candidate and established that synthesis may reconcile domain outputs but cannot replace domain authority, decide disputes, accept risk, change policy, approve strategy, or release a report. Its retained live calibration mixed accepted and candidate protocol evidence and therefore did not establish accepted-live synthesis fitness.

The planned domain set is now available for bounded evaluation. ENT-SYSRISK remains the accepted baseline enterprise-risk artifact. ENT-ARCH and ENT-GOV are semantically accepted and owner-finalized for ENT-SYNTH candidate evaluation. The corrected ENT-STRAT candidate is semantically accepted and owner-finalized; its superseded four implementation limitations are historical and must not be injected into synthesis. Its genuine remaining boundaries and CAP-SYNTH source context must remain visible downstream. None of these agents is scheduled, and the accepted report package remains unchanged.

## Proposed decision

1. Admit only the exact accepted ENT-SYSRISK artifact and the exact active ENT-SYNTH evaluation eligibility records for ENT-ARCH, ENT-GOV, and ENT-STRAT. Bind every domain artifact, packet, disposition, finalization, eligibility, evidence tier, and carried limitation by ID and hash.
2. Construct a new content-addressed ENT-EVIDENCE gate and enterprise-synthesis input manifest. Preserve domain independence, original terminology, confidence meaning, missingness, conflicts, unresolved decisions, authority boundaries, and excluded lineage.
3. Label the run `accepted_live_bounded_enterprise_domain_synthesis_evaluation`. This tier evaluates synthesis of the available bounded Code Harness domain set. It does not establish enterprise readiness, production fitness, strategic approval, governance compliance, architecture approval, or risk acceptance.
4. Carry ENT-STRAT's active boundaries into its domain summary, contribution map, completeness statement, uncertainty, and semantic-review packet: one-capability evidence scope; missing finding-locator coverage; no authorized composite; comparison-only operation; no strategy, investment, or scheduling authority; and disclosed deterministic harness projection. Preserve its `0.50` evidence coverage and `0.85` assessment confidence as different concepts, and do not interpret the observed component value `1.0` as objective completeness or strategic approval.
5. Preserve the admitted CAP-SYNTH source context carried by ENT-STRAT eligibility: absent declared requirements, the unresolved redacted credential-like value, the human-owned later-promotion review request, and the exact evidence needed to resolve locator coverage. Treat these as source context rather than scoring inputs unless a later owner-declared method explicitly admits them.
6. Require ENT-SYNTH to distinguish domain facts, preserved domain conclusions, cross-domain observations, unresolved disagreements, missing evidence, and human decision requests. Any derived correlation must cite exact domain records and state its derivation and uncertainty.
7. Prohibit a composite enterprise score, silent confidence averaging, evidence-tier promotion, domain-authority override, conflict resolution by the model, invented CAPA, report mutation, distribution approval, and scheduling.
8. Separate raw model output from harness-owned identity, exact bindings, eligibility enforcement, limitation propagation, prohibited fields, report boundary, authority boundary, and downstream state. Disclose all projected ownership. Distinguish internal declared hashes from content-addressed artifact hashes in human-review projections.
9. Execute the pinned Qwen3-32B ENT-SYNTH candidate on GX-10 or another approved DGX Spark equivalent. Produce deterministic comparison evidence, negative and rollback evidence, downstream report compatibility, and an exact project-owner semantic-review packet.
10. Keep ENT-ARCH, ENT-GOV, ENT-STRAT, and ENT-SYNTH unscheduled. Do not modify the accepted report, distribution state, deployment, or A100 production baseline.

## Proposed flow

`accepted ENT-SYSRISK + exact owner-finalized ENT-ARCH/ENT-GOV/ENT-STRAT eligibility -> exact domain and limitation bindings -> ENT-EVIDENCE/synthesis input manifest -> retained raw GX-10 ENT-SYNTH response -> disclosed harness-owned synthesis projection -> project-owner semantic review -> later shadow-integration eligibility decision`

## Alternatives considered

- Omit ENT-STRAT because it has acknowledged limitations: rejected because the owner accepted it and required continuation; the limitations must be propagated, not hidden.
- Treat ENT-STRAT's observed component value `1.0` as objective completeness or strategic approval: rejected because the corrected method explicitly reports `0.50` evidence coverage, preserves missingness, and prohibits a composite.
- Feed CAP-SYNTH or its children directly into ENT-SYNTH: rejected because ENT-SYNTH consumes enterprise-domain outputs and direct capability ingestion would bypass domain boundaries and double count lineage.
- Modify the leadership report during synthesis: rejected because synthesis evidence and report distribution are separate governed state machines.
- Schedule the enterprise candidates after a successful run: rejected because semantic acceptance, shadow integration, scheduling, deployment, and production promotion require later explicit decisions.

## Rollback

Revoke any domain eligibility, disable the ADR-0038 workflow, retain all evidence, and return ENT-SYNTH to its ADR-0024 protocol-only posture. The accepted `ENT-EVIDENCE -> ENT-SYSRISK` baseline, domain semantic records, report package, distribution state, deployment, and A100 production baseline remain unchanged.

## Validation required

- exact ENT-SYSRISK and domain artifact, disposition, finalization, eligibility, and limitation bindings;
- complete domain set without capability or child double counting;
- explicit exclusion of ENT-STRAT's superseded four implementation limitations and preservation of its active boundaries and carried CAP-SYNTH source context;
- fail-closed mutation, substitution, revocation, stale input, missing domain, tier promotion, confidence flattening, limitation removal, conflict suppression, invented correlation, invented decision, report mutation, and authority-confusion cases;
- deterministic replay and pinned GX-10 model execution;
- raw-model versus harness-projection provenance;
- exact semantic-review packet and project-owner authority;
- tested rollback; and
- unchanged scheduling, reports, distribution, deployment, and A100 production baseline.

## Decision requested

Approve, reject, or amend the isolated ENT-SYNTH accepted-live bounded-domain evaluation. Approval authorizes implementation, exact domain and limitation bindings, negative and rollback controls, deterministic evidence, GX-10 evaluation, and a semantic-review packet. It does not authorize domain decisions, risk acceptance, strategic or governance approval, report changes, shadow scheduling, deployment, or A100 production promotion.

## Decision

Accepted by `thomasverburgt`, project owner, on 2026-08-02, with direction to correct the identified ENT-STRAT limitations first if feasible. The corrected ENT-STRAT artifact was subsequently accepted as semantically faithful and owner-finalized. ADR-0038 execution may consume only that corrected active eligibility, never the superseded accept-as-is eligibility. This authorizes the bounded implementation described above; it does not authorize scheduling, report changes, distribution, deployment, or A100 production promotion.

## Implementation results

The deterministic implementation admits exactly ENT-SYSRISK, ENT-ARCH, ENT-GOV, and corrected ENT-STRAT. It binds all three candidate-domain eligibility records, excludes direct capability and child lineage, preserves active limitations and CAP-SYNTH source context, carries distinct child-qualified human decision identifiers, prohibits domain rewrite and confidence averaging, and leaves report, distribution, scheduling, deployment, and A100 production state unchanged.

The first live attempt failed closed at the 900-second transport timeout because the required response embedded complete child role objects. The projection was compacted to exact artifact hashes, role hashes, and preserved source record IDs while retaining the immutable source artifacts separately. The immutable ledger then detected that projection changes could reuse an artifact ID; the ID derivation was corrected to include the exact role hash and projection version. Semantic review of the next passing attempt detected duplicate unqualified synthesized decision IDs. Those IDs were corrected to include the ENT-ARCH artifact and original child-qualified record ID, and the model was rerun rather than silently patched.

Semantic review of that run also found that ENT-ARCH and ENT-GOV limitations were exact-hash-bound but absent from the human-readable domain summaries. The manifest was corrected to combine artifact-declared and eligibility-carried limitations without replacement or duplication, and the model was rerun.

The final Qwen3-32B GX-10 run passed after 775 seconds with 7,696 input tokens and 5,104 output tokens. Candidate `ca22ea90-b911-565a-931f-9a6f39ca265c` has hash `sha256:ea730d2b8cea2978c38d99d3702c1d5cbb6cd01c461ac1a5286e0a1eed47b964`. Semantic-review packet `622d3763-f624-5264-8465-7ae347e6af6c` has hash `sha256:af22b414a826d87466216b9a518e311b4c78dfddbd82709b96169301291b0ed5`. The raw response exactly equals the projected role and has SHA-256 `33d537c3305d7d95068c0ba7a3cd71e7910c1a41bc0bb7ec87e8fc85b0c2433e`. Project-owner semantic disposition is the remaining gate.

The project owner approved the final candidate as semantically faithful. Registry `0.10.0` explicitly grants the project owner `accept_enterprise_synthesis_semantics`; exact registry `0.9.0` is retained as immutable historical input for ADR-0037. Disposition `ab66b8e5-373c-58cb-80b1-ec42681fe84d`, finalization `36f3d8dd-eaba-5330-b09e-0552974d831e`, and active eligibility `9962a86c-2a44-5d8d-b13c-65e3c1428096` authorize only a later bounded enterprise shadow-integration evaluation. They do not schedule ENT-SYNTH or modify reports, distribution, deployment, or production.
