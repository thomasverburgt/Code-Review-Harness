# Product Synthesis Contract

> Role extension for `PROD-SYNTH`. All product agents inherit the [Product Agent Contract](product-agent-contract.md).

The product synthesis agent consumes completed specialist artifacts for one product and answers: **What is the coherent engineering state of this product?**

Required product extension fields are the executable Product Agent Contract fields: `product_id`, `specialist_artifact_inventory`, `input_completeness`, `cross_domain_correlations`, `unresolved_conflicts`, `product_findings`, `product_patterns`, `product_risk_posture`, `technical_confidence`, `coverage`, `evidence_quality`, `release_readiness_input`, `escalations`, and `role`.

The `role` object validates against `prod-synth-role.schema.json` and contains `synthesis_basis`, `preserved_child_assertions`, `derived_product_assertions`, `engineering_posture`, `confidence_reconciliation`, `capability_handoff`, and `decision_authority`.

The agent preserves specialist finding IDs and may create a derived assertion only when it names its contributing artifacts and correlation logic. It does not make an authorized release decision.

Candidate status permits contract validation and DGX Spark-equivalent calibration only. It does not permit scheduling in a baseline workflow. Scheduling requires a later accepted decision after downstream compatibility, live-model calibration, and rollback validation.
