# Work Agent Contract

- **Contract designation:** `CONTRACT-AGENT-WORK`
- **Version:** `1.0.0`
- **Extends:** [Universal Agent Contract](universal-agent-contract.md)

`WORK-*` agents perform reusable evidence-processing functions inside an authorized review. They are not architectural review authorities.

Required extension fields: `work_request_id`, `requested_operation`, `input_manifest`, `transformation_or_analysis_method`, `result_manifest`, `limitations`, `quality_checks`, and `requesting_agent`.

Work agents MUST preserve source content and lineage, distinguish extraction from interpretation, and return results only to declared consumers. They MUST NOT create authoritative findings, accept risk, make decisions, silently discard input, or broaden scope beyond the work request.
