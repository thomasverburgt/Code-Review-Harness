# Fixtures and Retained Evidence

This directory currently contains both reusable test fixtures and legacy retained evidence packages. ADR 0027 governs their gradual separation.

- A reusable fixture is versioned test input or an expected result that may be used by more than one deterministic test.
- Retained evidence is an immutable creation-time record such as a reference run, ledger object, review packet, human response, or GX-10 calibration archive.
- A domain README describes scenario scope, accepted limitations, test counts, and the authority gates that remain.
- Evidence under a dated `evidence` path is not edited to reflect later state. Consult [`status/current-state.md`](../status/current-state.md) for the living projection.

New evidence should use `evidence/YYYY-MM-DD/adrNNNN/<scenario-or-run>` until Sprint 3 approves a final canonical evidence root. Any intentionally shared fixture must preserve exact hashes and scenario traceability.

