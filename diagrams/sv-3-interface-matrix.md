# SV-3: Interface Matrix

| Source / producer | Interface object | Consumer | Control |
|---|---|---|---|
| GitLab Platform Factory | revision, job report, artifact attestation | CI/CD, SBOM, container, product synthesis | commit SHA, pipeline ID, signature |
| Kubernetes stacks | manifest, Helm values, policy result, topology | workload/platform/comms reviewers | cluster/environment scope, evidence hash |
| ServiceNow | change, exception, approval, release record | CI/CD, governance, enterprise synthesis | record reference, access controls |
| Specialist reviewer | Markdown report + JSON contract | Product synthesis | schema validation, immutable artifact ID |
| Product synthesis | product assessment | Capability delivery | cited specialist IDs and confidence rollup |
| Capability delivery | capability assessment | Enterprise synthesis | cited product IDs and mission-thread traceability |
| Enterprise synthesis | decision brief | Human governance board | required human approval and policy routing |
