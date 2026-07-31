# JSON Schemas

Normative schemas:

- [Agent identity registry](agent-identity-registry.schema.json)
- [Universal agent artifact](universal-agent-artifact.schema.json)
- [Sandbox evolution loop](sandbox-evolution-loop.schema.json)
- [Specialist extension](specialist-extension.schema.json)
- [Product extension](product-extension.schema.json)
- [Capability extension](capability-extension.schema.json)
- [Enterprise extension](enterprise-extension.schema.json)
- [SPEC-SECRETS role extension](spec-secrets-role.schema.json)
- [PROD-SEC role extension](prod-sec-role.schema.json)
- [CAP-RISK role extension](cap-risk-role.schema.json)
- [ENT-EVIDENCE role extension](ent-evidence-role.schema.json)
- [ENT-SYSRISK role extension](ent-sysrisk-role.schema.json)
- [Workflow definition](workflow-definition.schema.json)
- [Dispatch envelope](dispatch-envelope.schema.json)
- [Fan-in gate result](gate-result.schema.json)
- [Orchestration audit event](audit-event.schema.json)
- [Human decision request](human-decision-request.schema.json)
- [Orchestration state machine](orchestration-state-machine.schema.json)
- [Execution ledger manifest](execution-ledger-manifest.schema.json)
- [Artifact supersession record](supersession-record.schema.json)
- [Worker execution job](worker-job.schema.json)
- [Worker execution result](worker-result.schema.json)
- [Worker execution telemetry](execution-telemetry.schema.json)
- [Deterministic assembly record](assembly-record.schema.json)

Generation contracts are runtime-composed from these final schemas. Canonical analytical payloads additionally pin a deterministic projection manifest under `appendices/projection-manifests/`; the projection does not replace the universal, layer, or role validation gates.

Future evidence, finding, CAPA, risk, traceability, and layer-extension schemas compose with the universal artifact rather than redefining its identity, authority, provenance, confidence, or integrity fields.

Executable validation first applies the universal schema, then the registered producer's layer schema to `extensions.<layer>`, and finally the producer's role schema to `extensions.<layer>.role`. See [ADR 0007](../../adr/0007-executable-extension-validation-and-enterprise-evidence-gate.md).
