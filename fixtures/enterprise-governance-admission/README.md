# ENT-GOV Candidate Admission Fixtures

This fixture set implements ADR-0022 without changing the accepted workflow. The human-authored governance-source manifest is the sole source of obligations and applicability. The deterministic two-capability fixture proves contract and matrix mechanics; the retained live single-capability GX-10 run proves source, protocol, and lineage handling only.

ADR-0036 adds an owner-declared, accepted-live, single-capability evaluation using the exact semantically accepted CAP-SYNTH artifact. Its revised GX-10 flow binds exact authority-registry identity, JSON-pointer evidence locators, eligibility, input manifests, confidence interpretation, and harness-owned projection provenance. The declared agent-authority obligation remains `insufficient_evidence` because the supplied evidence does not prove enforcement across every agent instance. The revised candidate is semantically accepted, owner-finalized, and eligible only for later ENT-SYNTH candidate evaluation; it remains unscheduled.

Production targets the A100 large cluster. Development, conformance, calibration, integration, security, rollback, and regression testing run on a DGX Spark or approved equivalent, currently GX-10.

Rollback removes the ENT-GOV candidate workflow from discovery and restores its registry state to `planned`. Prompts, schemas, manifests, fixtures, and evidence remain retained for audit. The accepted ENT-EVIDENCE to ENT-SYSRISK baseline, report package, ADR-0020 state, CAP-SYNTH schedule, ENT-ARCH schedule, and deployment state remain unchanged.
