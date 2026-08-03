# ADR-0037 Evidence

- `reference-run/` contains the deterministic owner-source, exact-evidence, input, candidate, semantic-review, and ledger package.
- `gx10-live-evaluation/` contains the pinned Qwen3-32B response and the disclosed harness-owned projection generated on GX-10.

The live candidate is `9a0edab2-f80a-5179-a311-1975988ad252` with hash `sha256:ab5e620ffbab8ce32ec90687ecdb76e6f85af9735dade36fc037646a93ed7450`. Its semantic-review packet is `0a6862f2-ab8d-5c46-b41d-3315ec61c7ea` with hash `sha256:03d61c101eb4fa1b10d07e8a293c755e05313a9a47317ae0e93ad6acf84b7fdf`. Raw-response hash is `9e8bca069c37664cf7e8396e779263a29e6878551e4397aa36e370de213213ec`.

The raw response reproduced the bounded role projection: human authority is observed from two exact locators, finding-locator coverage remains missing, strategic confidence remains `insufficient_evidence`, and no composite, threshold, scheduling, report, deployment, or production authority is created.

- `project-owner-semantic-disposition/` records acceptance as-is, preserves the four semantic-review limitations, finalizes the owner record, and derives revocable ENT-SYNTH evaluation eligibility without scheduling either candidate.
- `corrected-reference-run/` and `corrected-gx10-live-evaluation/` correct all four limitations under authority registry `0.9.0` and project scope `CODE-HARNESS-PROJECT-001`.
- `corrected-candidate-supersession.json` preserves the prior accepted candidate as immutable history but prevents ADR-0038 from admitting it as the current ENT-STRAT input. The corrected candidate requires its own semantic disposition.

The corrected GX-10 candidate is `dd5598c9-628a-5f24-b974-9f2a53512119` with hash `sha256:e9a673ad1e126ccb19d75ee8c73bb142be82370505d0c5ce4cea3bf80190a8e2`. Its semantic-review packet is `a640de06-f9e1-5263-b928-d453ef860957` with hash `sha256:90d7dd3bc3f464b46f5d7550dc65f126147838c170272e86c16de7524d9b3a95`. The raw-response hash is `31dce99c237ae0ff40c49b94b36cb6ed4c0be91b845cf8182afdc0fc4d49cf87`.
