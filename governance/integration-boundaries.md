# Platform Factory, ServiceNow, Release Management, and Kubernetes Boundaries

- **GitLab Platform Factory:** supplies source revision, pipeline evidence, test/scan reports, signed artifacts, and promotion-state inputs. It remains the delivery system of record.
- **Kubernetes stacks:** supply manifests, Helm values, admission/policy results, deployment state, topology, and runtime evidence. Cluster configuration and workload configuration are reviewed separately.
- **ServiceNow governance:** supplies approved change, exception, control, and release-management records. The harness links to these records but does not bypass authorization workflows.
- **Release management:** consumes validated readiness inputs, outstanding risk, exceptions, and human decisions. A review artifact is not a release approval.

All integrations are references in immutable evidence objects with least-privilege access and retention labels.
