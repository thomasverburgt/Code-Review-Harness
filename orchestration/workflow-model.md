# Orchestration and Policy Model

The workflow engine schedules declared contracts; the policy engine decides depth, gates, and escalation. vLLM or another model-serving layer provides inference only and is not the orchestration system.

## Lifecycle

1. Ingest source revision and immutable evidence.
2. Calculate review-risk signals: changed critical paths, authentication/control-plane changes, dependency/SBOM deltas, complexity, historical defects, and mission criticality.
3. Select specialist contracts through a versioned policy.
4. Fan out independent work; enforce declared contract dependencies for dependent work.
5. Validate contract shape, provenance, evidence freshness, confidence, conflict objects, and CAPA completeness.
6. Fan in to product, then capability, then enterprise synthesis as inputs become complete or policy permits an explicit partial review.
7. Route all decision requests to the required human gate and ServiceNow/release-management controls.

## Example policy

```yaml
rule: control-plane-change
when:
  changed_paths_match: ["helm/**", "k8s/**", "platform/**"]
then:
  require_agents: [SPC-K8S-WORKLOAD, SPC-K8S-PLATFORM, SPC-COMMS, SPC-IAC, SPC-CICD]
  minimum_review_fidelity: deep
  human_gate: platform-security-approver
```
