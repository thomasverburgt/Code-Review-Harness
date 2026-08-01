# Deterministic Capability Coordination Contract

`CAP-COORD` is a deterministic capability-domain fan-in boundary. It validates and inventories immutable capability-review artifacts before any model-backed capability synthesis is dispatched.

The coordinator owns expected and received input sets, identity and schema checks, artifact-integrity verification, freshness and compatibility state, completeness, partial-input authorization records, conflict preservation, traceability indexing, input hashing, manifest hashing, and routing. It emits `capability-input-manifest.schema.json`.

The coordinator does not generate narrative, derive capability meaning, resolve a conflict, alter child confidence, recommend action, accept risk, approve readiness, change requirements, authorize release, alter reports, or authorize deployment. Its effect is `validation_and_routing_only` and its decision authority remains human.

`CAP-SYNTH` dispatch is permitted only when the expected and received designation sets match exactly, every input is complete, fresh, compatible, schema-valid, and integrity-valid, and all child conflicts and traceability records are preserved. A partial-input authorization may make incompleteness inspectable but does not permit synthesis in the initial candidate policy.

The first reference uses only `CAP-RISK` because it is the sole accepted live capability-review artifact in the vertical slice. That run is labeled `single_domain_mechanical_calibration` and establishes no multi-domain synthesis or scheduling fitness.

Rollback disables coordinator registration and CAP-SYNTH dispatch while preserving manifests for audit. Existing accepted capability artifacts, the direct enterprise path, reports, governance records, and the A100 production baseline remain unchanged.
