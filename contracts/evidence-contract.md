# Evidence Contract

Evidence is an immutable pointer to an observable source. Required fields: `evidence_id`, `source_type`, `source_uri`, `source_revision`, `collector`, `collection_method`, `collected_at`, `excerpt_or_locator`, `integrity_hash`, `freshness`, `access_constraints`, and `reliability_rating`.

Accepted source types include source code, configuration, IaC plan, GitLab job output, SBOM, image attestation, Kubernetes manifest, runtime telemetry, test result, ServiceNow record, approved architecture decision, and human review record. Evidence is never converted into a conclusion without an explicit assessment.
