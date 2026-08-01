# ENT-GOV Candidate Admission Fixtures

This fixture set implements ADR-0022 without changing the accepted workflow. The human-authored governance-source manifest is the sole source of obligations and applicability. The deterministic two-capability fixture proves contract and matrix mechanics; the retained live single-capability GX-10 run proves source, protocol, and lineage handling only.

Production targets the A100 large cluster. Development, conformance, calibration, integration, security, rollback, and regression testing run on a DGX Spark or approved equivalent, currently GX-10.

Rollback removes the ENT-GOV candidate workflow from discovery and restores its registry state to `planned`. Prompts, schemas, manifests, fixtures, and evidence remain retained for audit. The accepted ENT-EVIDENCE to ENT-SYSRISK baseline, report package, ADR-0020 state, CAP-SYNTH schedule, ENT-ARCH schedule, and deployment state remain unchanged.
