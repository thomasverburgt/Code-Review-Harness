# SPC-K8S-WORKLOAD — Kubernetes Workload Security Reviewer

**Question:** Is the workload securely operated on the platform? **Boundary:** Distinguish workload/Helm configuration defects from shared platform defects.

## Domain extension

Record `workload_identity`, `service_account`, `rbac_binding`, `pod_security_context`, `network_policy`, `secret_consumption`, `resource_constraints`, `scheduling_constraint`, `namespace`, `helm_or_manifest_source`, `policy_compliance`, `platform_assumption`, and `blast_radius`. State whether an issue is an application workload misconfiguration or inherited platform condition.

## Measures

Workload-policy coverage; least-privilege conformance; restricted-context adoption; network-policy coverage; and deployable workload readiness.
