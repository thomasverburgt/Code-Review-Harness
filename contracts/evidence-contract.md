# Evidence Contract

Evidence is an immutable pointer to an observable source. Required fields: `evidence_id`, `source_type`, `source_uri`, `source_revision`, `collector`, `collection_method`, `collected_at`, `excerpt_or_locator`, `integrity_hash`, `freshness`, `access_constraints`, and `reliability_rating`.

Accepted source types include source code, configuration, IaC plan, GitLab job output, SBOM, image attestation, Kubernetes manifest, runtime telemetry, test result, ServiceNow record, approved architecture decision, and human review record. Evidence is never converted into a conclusion without an explicit assessment.

## Expert-review localization

An evidence reference used by an actionable report item must resolve through `evidence-locator.schema.json`. For Git evidence, `source_uri` and `source_revision` become an exact repository URI and 40-character commit; `excerpt_or_locator` becomes a safe repository-relative path plus line range or named section; and the locator retains a redacted excerpt and integrity fingerprint. Raw secret values are prohibited.

The separately hashed binding manifest maps every finding, risk, CAPA, and recommendation to its evidence references. Direct report references cannot be replaced. Derived items require an explicit binding rather than reviewer inference. The expert-review packet is ready only when every binding resolves to a `source_located` locator. Missing, inaccessible, stale, partially located, or unverified evidence fails closed and names the blocked report items.

The packet is review support only. It does not change the report, approve distribution, decide a finding, accept risk, or authorize remediation.
