# Orchestration and Policy Model

The workflow engine schedules declared contracts; the policy engine decides depth, gates, and escalation. vLLM or another model-serving layer provides inference only and is not the orchestration system.

The control roles are `ORCH-SCHED`, `ORCH-FANOUT`, and `ORCH-FANIN`. They implement the [Orchestration Agent Contract](../contracts/orchestration-agent-contract.md) and never alter review conclusions or waive human authority.

## Lifecycle

1. Ingest source revision and immutable evidence.
2. Calculate review-risk signals: changed critical paths, authentication/control-plane changes, dependency/SBOM deltas, complexity, historical defects, and mission criticality.
3. `ORCH-SCHED` resolves registered UUID/designation pairs, pins effective contract versions, and selects required agents through versioned policy.
4. `ORCH-FANOUT` dispatches independent bounded work with immutable, least-privilege inputs.
5. `ORCH-FANIN` validates identity, schema, integrity, provenance, freshness, confidence, conflict objects, and CAPA completeness.
6. Fan in through product and capability; run `ENT-EVIDENCE` before the remaining enterprise framework.
7. Permit partial review only through explicit policy authorization and an `incomplete_input` lifecycle state.
8. Route all decision requests to the named human gate and ServiceNow/release-management controls.

## Identity and version pinning

Schedules store `agent_uuid`, canonical `designation`, agent version, contract version, prompt version, rubric version, policy version, and registry version. Legacy aliases may be resolved at ingestion but are normalized before dispatch. An unregistered identity, alias collision, version incompatibility, or UUID/designation mismatch fails closed.

## Enterprise fan-in

`ENT-EVIDENCE` produces the validated enterprise input manifest. Domain enterprise roles run according to the dependency graph in the [Enterprise Agent Framework](../agents/enterprise/enterprise-agent-framework.md). `ENT-SYNTH` consumes immutable role outputs and preserves disagreement; it is not an approval gate.

## Example policy

```yaml
rule: control-plane-change
when:
  changed_paths_match: ["helm/**", "k8s/**", "platform/**"]
then:
  require_agents: [SPEC-K8S-WORKLOAD, SPEC-K8S-PLATFORM, SPEC-COMMS, SPEC-IAC, SPEC-CICD]
  minimum_review_fidelity: deep
  human_gate: platform-security-approver
```
