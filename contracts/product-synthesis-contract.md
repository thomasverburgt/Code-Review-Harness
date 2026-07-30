# Product Synthesis Contract

> Role extension for `PROD-SYNTH`. All product agents inherit the [Product Agent Contract](product-agent-contract.md).

The product synthesis agent consumes completed specialist artifacts for one product and answers: **What is the coherent engineering state of this product?**

Required extension fields: `product_id`, `specialist_artifact_inventory`, `input_completeness`, `cross_domain_correlations`, `unresolved_conflicts`, `product_findings`, `product_patterns`, `product_risk_posture`, `technical_confidence_score`, `coverage_score`, `evidence_quality_score`, `release_readiness_input`, and `escalation_candidates`.

The agent preserves specialist finding IDs and may create a derived assertion only when it names its contributing artifacts and correlation logic. It does not make an authorized release decision.
