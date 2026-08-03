# ADR-0035 ENT-ARCH Accepted-Live Evaluation Evidence

This package evaluates the exact CAP-SYNTH artifact that the project owner accepted under ADR-0034. The enterprise input manifest admits that parent artifact once and retains CAP-RISK and CAP-REQ only as child lineage, preventing parent-child double counting.

## Results

- `reference-run/` retains the original deterministic package that preceded semantic-review corrections.
- `corrected-reference-run/` contains the corrected deterministic gate, input manifest, ENT-ARCH projection, compatibility result, semantic-review packet, and ledger replay evidence.
- `gx10-live-evaluation/first-attempt/` retains the first Qwen3-32B response. It failed closed because the initial runtime allow-list did not recognize valid evidence references preserved through CAP-SYNTH and because the model proposed architecture-debt and corrective-action content that a single-capability input cannot establish.
- `gx10-live-evaluation/successful-run/` contains the tightened GX-10 result. The harness accepts genuine preserved evidence references while owning and suppressing unsupported topology, concentration, propagation, debt, CAPA, target-state, and transition fields.
- `gx10-live-evaluation/corrected-run/` reprojects the exact retained successful model response through the corrected harness. It restores child-qualified decision identifiers and replaces the inherited CAP-RISK gate observation with an exact CAP-SYNTH admission statement. No new model inference was performed.
- `gx10-live-evaluation/gx10-conformance.txt` records the passing structural, ADR-0035, and legacy ENT-ARCH tests on the approved DGX Spark-equivalent platform.
- `gx10-live-evaluation/gx10-correction-conformance.txt` records the final correction-specific structural, nine-test ADR-0035, and eight-test legacy ENT-ARCH conformance run on GX-10.

The corrected model candidate is `00f8b5b9-19f9-5a1b-8cd1-3122333f2d55` with content hash `sha256:321186b8016dde5dee6f4948d5254397a011e6796b0c63ae5bebf49ab2d3faab`. Its corrected semantic-review packet is `09c336f5-faa1-519a-a375-b4ba18cf2384` with hash `sha256:170b55b2ff03a9e4ca034f52f3eedec3a2cb3c9d948146bb0eafb5c6db8126e5`. The unchanged raw model response hash is `a65e88e6dd8d488c83d63d681ccd4683bc2d33c33b243509640c9722c3a9796a`.

The candidate concludes that architecture coherence is `insufficient_evidence`: the accepted capability posture retains a declared-requirements traceability gap and an unresolved credential-like-value classification. It makes no cross-capability topology or system-of-systems fitness claim. Both CAP-SYNTH and ENT-ARCH remain unscheduled, and the accepted report, distribution state, deployment state, and A100 production baseline are unchanged.

## Project-owner semantic disposition

`project-owner-semantic-disposition/` binds the project owner's passing semantic disposition to the corrected candidate and packet. It contains the immutable disposition, project-owner finalization, revocable enterprise-synthesis evaluation eligibility, ledger records, and the passing GX-10 conformance transcript. ENT-ARCH becomes eligible only as an input to a later isolated ENT-SYNTH candidate evaluation; neither role is scheduled.
