# ADR-0011: Deterministic Envelope and Role-Payload Generation

- **Status:** Accepted
- **Date:** 2026-07-31
- **Decision authority:** project maintainer
- **Owners:** harness orchestration, agent contracts, and model platform
- **Scope:** Increment 2 prompt-calibration completion

## Decision record

Accepted by the project maintainer on 2026-07-31 with an explicit requirement that the change remain safely reversible.

## Context

ADR-0010 prevents model output from bypassing validation and publication controls, but live calibration showed that asking the model to generate the entire universal artifact is unreliable and inefficient. Unconstrained generation produced malformed JSON, missing fields, and incorrect immutable lineage. Full universal-schema constrained decoding exceeded the GX-10 worker timeout and exposed grammar incompatibilities.

Most failed fields are not analytical judgments. Identity, dispatch bindings, artifact identifiers, execution metadata, version pins, input IDs and hashes, lineage, lifecycle, routing, consumers, decision authority, access classification, timestamps, and integrity attestations are already known to the harness.

## Proposed decision

Split generation from assembly:

1. Define a compact, versioned generation contract for each role. The model returns only the bounded analytical payload requiring model judgment.
2. Have the worker deterministically assemble the universal artifact, layer envelope, exact upstream references, identity, execution pins, lifecycle, routing, consumers, authority boundary, and integrity metadata from the signed job and resolved versions.
3. Embed the generated role payload without rewriting its analytical meaning.
4. Validate the assembled artifact against the unchanged universal, layer, and role schemas and complete semantic fan-in checks before publication.
5. Retain the raw role payload, assembly record, validation result, telemetry, generation-contract version/hash, and final artifact hash.
6. Permit calibration cardinality caps only when truncation and coverage limits remain explicit; capped output must never be represented as complete.

## Consequences

- The model cannot invent or mutate deterministic identity, lineage, authority, or integrity fields.
- Prompt and output token load decreases materially.
- Structured decoding operates on smaller role schemas instead of the universal artifact grammar.
- The worker gains an explicit deterministic assembly responsibility with its own schema, tests, and replay evidence.
- Analytical omissions still fail the authoritative role and semantic gates.

## Alternatives considered

- Unconstrained full-artifact generation is rejected by the malformed, incomplete, and lineage-invalid live results.
- Full universal-schema constrained decoding is rejected for the current GX-10 baseline because it exceeded the worker timeout after array bounding.
- Arbitrary JSON repair is rejected because repair could silently change analytical meaning or authority.
- Adjudicated gold artifacts as generation templates are rejected because they contaminate prompt-quality evaluation.

## Validation required

- deterministic assembly replay produces byte-identical envelopes for identical jobs and role payloads;
- model output cannot set or override harness-owned fields;
- all four live prompts produce role payloads that assemble into contract-valid artifacts one node at a time;
- exact input IDs and hashes survive assembly and semantic fan-in;
- capped output records coverage and truncation explicitly; and
- accepted artifacts publish once, while invalid, timed-out, or cancelled payloads publish none.

## Rollback plan

The worker must retain two explicit, versioned generation modes during adoption:

- `full_artifact`: the ADR-0010 behavior in which an adapter returns a complete candidate artifact. This remains the compatibility and rollback path.
- `role_payload_v1`: the ADR-0011 behavior in which an adapter returns a bounded analytical payload and the worker creates the deterministic envelope.
- `canonical_payload_v1`: the topology-reduced adoption mode in which the model returns one canonical analysis and irreducible role payload, while a pinned deterministic projection creates the layer extension. Its first approved scope is SPEC-SECRETS only.

Rollback is performed by pinning affected workflows and jobs back to `full_artifact`, restoring the last validated prompt/model manifest, and replaying from immutable input references. No accepted artifact, assembly record, telemetry record, or audit event is deleted or rewritten. Artifacts produced through `role_payload_v1` remain readable and valid because both modes publish the same universal artifact contract.

The following rollback assets must be retained until a later ADR removes the compatibility path:

- the full-artifact adapter and validation path;
- the last passing ADR-0010 conformance fixtures and GX-10 evidence;
- generation-mode, generation-contract, prompt, model, assembler, and schema version/hash pins in every job and telemetry record;
- raw model payloads and deterministic assembly records for role-payload executions; and
- replay tests proving that the same retained payload and job reproduce the same assembled envelope.

Rollback triggers include an increased invalid-artifact rate, loss of analytical content during assembly, lineage or authority regressions, unacceptable latency or resource use, non-deterministic replay, downstream incompatibility, or inability to reconstruct an accepted artifact from retained records.

Before rollback, pause new payload-mode promotion, allow already leased work to complete or cancel under normal controls, and record the operator decision. Pin new work directly to `full_artifact`; do not fall back from canonical mode to the earlier payload topology unless that exact contract remains independently validated. After rollback, run the complete ADR-0010 conformance suite and one-node fixture replacements before resuming dispatch. Re-enabling a withdrawn payload or projection version requires correction evidence and a new validated pin; it must not silently reuse the withdrawn version.

## Implementation and validation record

The accepted dual-mode boundary is implemented. GX-10 conformance passes both `full_artifact` and `role_payload_v1` one-node replacements for all four roles, deterministic assembly replay, harness-owned-field override rejection, disclosed-truncation fail-closed behavior, ledger publication ordering, and the prior ADR-0010 controls.

Live SPEC-SECRETS calibration has not passed. Unbounded payloads timed out; bounded payload versions completed faster but exhausted their token ceilings and returned truncated JSON. No live payload reached assembly and no live artifact was published. Evidence is retained under `fixtures/vertical-risk-slice/evidence/adr11-role-payload-2026-07-31/`.

The first topology-reduction increment is implemented and live-calibrated for SPEC-SECRETS. The initial `canonical-role-payload-1.0.0` removed the layer duplicate but still exhausted the 3,072-token live ceiling. Version 1.1.0 reduced the single review form to methodology, review counts, findings/CAPA, tagged secondary records, confidence, decision requests, and the irreducible secrets role payload; it completed live generation and assembly in 135 seconds and 893 output tokens. The model nevertheless returned a contradictory disclosure (`limit_applied=true` with zero omitted and zero truncated items), so no artifact was published. Version `canonical-role-payload-1.2.0` removes model control of lifecycle: the model reports only nonnegative omission/truncation counts and the worker deterministically derives `limit_applied`. Assembler `deterministic-envelope-1.1.0` and projection `specialist-analytical-projection-1.0.0` derive universal observations and assessments from classified secret observations, project tagged secondary channels, and construct the specialist extension. Replay is byte-identical, positive disclosed counts fail closed, and the unchanged universal, specialist, role, semantic, ledger, and authority gates pass. The targeted live GX-10 run completed in 132,803 ms with 872 output tokens and published artifact `sha256:361f52f224378973b5d1764b349c812bfa2357d7bba5d7d39da252837c1ba3a8`. Evidence is retained under `fixtures/vertical-risk-slice/evidence/canonical-spec-secrets-2026-07-31/`. Other roles require their own topology design and calibration before promotion.

The second topology-reduction increment is implemented and live-calibrated for PROD-SEC as `canonical-product-payload-1.0.0` with projection `product-analytical-projection-1.0.0`. The worker derives immutable specialist inventory and completeness from actual inputs, universal observations from security-domain correlations, assessments from attack-path hypotheses, product-layer references and confidence from the canonical synthesis, and an advisory readiness state that can never become a release decision. The targeted GX-10 run consumed the accepted live SPEC-SECRETS artifact, completed in 187,509 ms with 1,230 output tokens, preserved its exact artifact ID and output hash, and published artifact `sha256:89bec57be37acf901a313aed1bea11363867d6a85180d8d237faf8195bdd62dc`. Evidence is retained under `fixtures/vertical-risk-slice/evidence/canonical-prod-sec-2026-07-31/`.

The third topology-reduction increment is implemented and live-calibrated for CAP-RISK as `canonical-capability-risk-payload-1.0.0` with projection `capability-risk-analytical-projection-1.0.0`. Irreducible mission-thread and operational context remains model-generated; the worker projects universal risk observations/assessments, participating products, upstream confidence rollup, capability risk references, conflicts, and enterprise escalations without making a risk disposition. Accepted external input artifacts act as validated boundary nodes during one-node fan-in, while the candidate's direct inbound edge still requires the exact upstream artifact ID and output hash. The targeted GX-10 run consumed the accepted live PROD-SEC artifact, completed in 272,544 ms with 1,790 output tokens, and published artifact `sha256:d691b498eb96556d2c5d3a68f675eaa814b425fa8c1e73e91b6cf5eede475dd5`. Evidence is retained under `fixtures/vertical-risk-slice/evidence/canonical-cap-risk-2026-07-31/`.

The fourth topology-reduction increment is implemented and live-calibrated for ENT-SYSRISK as `canonical-enterprise-systemic-risk-payload-1.0.0` with projection `enterprise-systemic-risk-analytical-projection-1.0.0`. The harness first creates a deterministic ENT-EVIDENCE gate bound to the accepted CAP-RISK artifact ID and output hash; the model cannot generate, alter, or bypass that gate. The worker derives the enterprise capability manifest, exact two-input traceability, upstream confidence preservation, risk/unknown references, and human decision-request routing while the model supplies the irreducible systemic-risk analysis. The targeted GX-10 run completed in 256,569 ms with 1,633 output tokens and published artifact `sha256:06cabaf4305f6b281b0be78a9878c52bcee9bfa25a3f62048750e1c1d2520824`. Both universal and role authority remain `human`. Evidence is retained under `fixtures/vertical-risk-slice/evidence/canonical-ent-sysrisk-2026-07-31/`.
