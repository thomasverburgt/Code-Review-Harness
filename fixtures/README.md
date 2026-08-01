# Fixtures and Retained Evidence

This directory currently contains both reusable test fixtures and legacy retained evidence packages. ADRs 0027 and 0029 govern their gradual separation.

- A reusable fixture is versioned test input or an expected result that may be used by more than one deterministic test.
- Retained evidence is an immutable creation-time record such as a reference run, ledger object, review packet, human response, or GX-10 calibration archive.
- A domain README describes scenario scope, accepted limitations, test counts, and the authority gates that remain.
- Evidence under a dated `evidence` path is not edited to reflect later state. Consult [`status/current-state.md`](../status/current-state.md) for the living projection.

New evidence uses the top-level `evidence/YYYY-MM-DD/adrNNNN/<scenario>/<run-id>` layout. Existing evidence remains immutable and indexed in place.

[`catalog.json`](catalog.json) classifies the scenario roots. [`shared/content-addressed-index.json`](shared/content-addressed-index.json) maps exact duplicate bytes to materialized content-addressed objects and identifies matching reusable or immutable-evidence copies without deleting or rewriting them.
