# ENT-STRAT Candidate Admission Fixtures

This fixture set implements ADR-0023 without changing the accepted workflow. Human-controlled manifests are the sole sources of strategic objectives and scoring policy. The deterministic package proves scoring-contract, evidence-tier, missingness, sensitivity, and traceability mechanics; the live single-domain GX-10 run proves protocol and lineage handling only.

The method intentionally prohibits a composite score. Missing measures remain unknown and no threshold, weight, or strategy is inferred. ENT-STRAT remains comparison-only and unscheduled.

Production targets the A100 large cluster. All testing runs on DGX Spark or an approved equivalent, currently GX-10. Rollback removes candidate discovery, restores ENT-STRAT to `planned`, and retains all evidence for audit without changing the accepted baseline, reports, ENT-ARCH, ENT-GOV, or deployment state.
