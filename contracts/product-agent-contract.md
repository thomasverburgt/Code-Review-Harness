# Product Agent Contract

- **Contract designation:** `CONTRACT-AGENT-PRODUCT`
- **Version:** `1.0.0`
- **Extends:** [Universal Agent Contract](universal-agent-contract.md)

Product agents correlate immutable `SPEC-*` artifacts within one product. Required extension fields are `product_id`, `specialist_artifact_inventory`, `input_completeness`, `cross_domain_correlations`, `unresolved_conflicts`, `product_findings`, `product_patterns`, `product_risk_posture`, `technical_confidence`, `coverage`, `evidence_quality`, `release_readiness_input`, and `escalations`.

Product agents preserve specialist IDs and meaning. They may create derived assertions only with contributing artifact IDs, correlation logic, confidence provenance, and uncertainty. They do not approve release, accept risk, rewrite specialist evidence, or bypass a required capability review.
