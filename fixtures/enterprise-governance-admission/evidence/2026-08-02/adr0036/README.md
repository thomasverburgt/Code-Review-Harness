# ADR-0036 ENT-GOV Accepted-Live Evaluation Evidence

This package evaluates the exact owner-finalized CAP-SYNTH artifact against a governance-source manifest declared by `thomasverburgt` in the registered governance-source-owner capacity. The manifest binds `GOVERNANCE.md` line 13 at revision `ab84b15d3c6bd6ba2c594c9a01457df8474d623e` and declares the automated-agent authority boundary as obligation `GOV-AGENT-AUTH-001`.

## Results

- `reference-run/` retains the initial deterministic package.
- `corrected-reference-run/` contains the revised deterministic authority, evidence-binding, input, candidate, review, and ledger flow.
- `gx10-live-evaluation/first-attempt/` retains the original Qwen3-32B projection. It passed structural checks, but semantic inspection rejected its compliance-row rationale because it repeated requirements and credential uncertainty rather than evaluating the governance obligation.
- `gx10-live-evaluation/successful-run/` retains the first harness-owned row correction. A subsequent human semantic review identified that its `DERIVED-001` evidence reference was unrelated, its authority declaration was not independently registry-bound, and its model-versus-harness provenance was insufficiently explicit.
- `gx10-live-evaluation/revised-flow-run/` implements the accepted semantic-review recommendations. It binds the declarer to `HUMAN-PROJECT-OWNER-001` and the exact authority registry, introduces four exact JSON-pointer evidence locators, removes `DERIVED-001`, binds eligibility and evaluation manifests into the candidate, defines confidence as confidence in bounded evidence insufficiency rather than compliance, and discloses every harness-owned field plus the retained raw-response hash. No new model inference was performed.
- `gx10-live-evaluation/gx10-conformance.txt` records passing structural, seven-test ADR-0036, and legacy ENT-GOV conformance on GX-10.

The revised-flow candidate is `86456e45-010b-571a-97fb-f78a275320a9` with hash `sha256:ee04f21b04d026cecfc6040568812b32a39c833f8d2b4910ff91e6844aa6d370`. Its semantic-review packet is `2310362f-43a1-55d0-8243-fa739d01b3b4` with hash `sha256:869f86a26c52085e3b8ad7df6e04519499cc984a61eed046ac92b635d1d3cc07`. The retained raw-response hash remains `58c56cfd650f34dba9acc4440f1d5f8b803ef13d1d6aa8e28d8afffcaed39d64`.

- `project-owner-semantic-disposition/` binds the project owner's acceptance to the exact revised packet and candidate, finalizes the governance record, and derives revocable ENT-SYNTH evaluation eligibility without scheduling either agent.

The candidate records `insufficient_evidence`: CAP-SYNTH demonstrates human decision authority, advisory-only posture, and an unscheduled comparison handoff, but the bounded artifact does not prove enforcement of every repository-wide agent prohibition. It creates no exception, approval, maturity assessment, CAPA, compliance approval, or schedule. The accepted report, distribution state, deployment, and A100 production baseline remain unchanged.
