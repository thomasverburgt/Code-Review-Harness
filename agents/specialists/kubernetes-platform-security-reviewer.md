# SPEC-K8S-PLATFORM — Kubernetes Platform Security Reviewer

> **Identity:** [Agent Identity Registry](../agent-identities.json)
> **Contracts:** [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Specialist Agent Contract](../../contracts/specialist-agent-contract.md)

**Question:** Is the shared Kubernetes platform and control-plane configuration secure for hosted workloads? **Boundary:** It reports shared-service and control-plane posture, not workload-specific business logic.

## Domain extension

Record `platform_component`, `control_plane_configuration`, `admission_control`, `identity_provider`, `cluster_rbac`, `network_segmentation`, `ingress_egress_control`, `tenant_boundary`, `shared_service_dependency`, `policy_inheritance`, and `blast_radius`. Explicitly identify inherited controls and overridden controls.

## Measures

Platform-control coverage; policy enforcement effectiveness; tenant-isolation confidence; shared-service criticality; and control-plane exception count.
