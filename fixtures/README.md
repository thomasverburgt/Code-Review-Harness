# Fixtures and Retained Evidence

This directory currently contains both reusable test fixtures and legacy retained evidence packages. ADRs 0027 and 0029 govern their gradual separation.

- A reusable fixture is versioned test input or an expected result that may be used by more than one deterministic test.
- Retained evidence is an immutable creation-time record such as a reference run, ledger object, review packet, human response, or GX-10 calibration archive.
- A domain README describes scenario scope, accepted limitations, test counts, and the authority gates that remain.
- Evidence under a dated `evidence` path is not edited to reflect later state. Consult [`status/current-state.md`](../status/current-state.md) for the living projection.

New evidence uses the top-level `evidence/YYYY-MM-DD/adrNNNN/<scenario>/<run-id>` layout. Existing evidence remains immutable and indexed in place.

[`catalog.json`](catalog.json) classifies the scenario roots. [`shared/content-addressed-index.json`](shared/content-addressed-index.json) maps exact duplicate bytes to materialized content-addressed objects and identifies matching reusable or immutable-evidence copies without deleting or rewriting them.

The [`specialist-shadow-calibration`](specialist-shadow-calibration/README.md) scenario is the deterministic ADR-0039 Increment 0 rehearsal. Its human response is synthetic contract-test data and carries no adjudicative or admission authority.

The [`specialist-static-evidence-increment1`](specialist-static-evidence-increment1/README.md) scenario contains the independent `SPEC-DEPS`, `SPEC-SBOM`, and `SPEC-LINT` deterministic candidates, negative mutation classes, and human-review packets for active ADR-0039 Increment 1.
- `specialist-build-supply-chain-increment2/` contains deterministic and live-calibration evidence for the comparison-only `SPEC-CONTAINER`, `SPEC-CICD`, and `SPEC-IAC` candidates. Human review is deferred to the consolidated program review.
- `specialist-k8s-secure-increment34/` contains deterministic and GX-10 evidence for the five Increment 3/4 candidates, including the redacted `SPEC-SECRETS` revalidation.
- `specialist-increment567/` contains deterministic and GX-10 evidence for the remaining 11 specialist candidates.
- `specialist-program-retrospective/` contains the Increment 8 all-agent comparison, explicit final-state register, program retrospective, and consolidated human-review handoff. It contains no fabricated reviewer response or adjudication.
