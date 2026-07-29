# Sandboxed Contract and Prompt Evolution Contract

Agent prompts, contracts, scoring rules, schemas, and policies may evolve only inside an isolated training or evaluation sandbox. No self-learning process may directly modify production behavior, production contracts, or deployed policy.

## Controlled loop model

A human operator defines the candidate scope, objective, dataset, scoring method, maximum loop count, stop conditions, and promotion authority. The operator may authorize a bounded series of loops, for example: execute up to ten loops while the approved score improves, then stop for human review.

Each loop must:

1. Start from an immutable baseline revision.
2. Produce a candidate prompt, contract, schema, or policy diff.
3. Record the reasoning and evidence supporting every change.
4. Execute the approved evaluation suite.
5. Record score changes, regressions, confidence, and uncertainty.
6. Preserve all generated artifacts and logs.
7. Stop on regression, policy violation, evaluation failure, exhausted loop budget, or human intervention.

## Mandatory trace record

Every loop records `experiment_id`, `loop_number`, `baseline_revision`, `candidate_revision`, `changed_artifacts`, `diff_refs`, `change_rationale`, `hypothesis`, `evaluation_dataset`, `scoring_model`, `prior_scores`, `candidate_scores`, `score_delta`, `regressions`, `confidence`, `policy_checks`, `stop_condition`, `operator_authorization`, `human_disposition`, and `promotion_reference`.

## Human authority

A score improvement never constitutes production approval. After the bounded loop sequence, a designated human reviews the complete diff history, scoring trace, regressions, and rationale. Promotion requires an explicit decision record and follows normal pull-request, governance, validation, and release controls.

## Audit and reproducibility

All loop inputs, outputs, model versions, prompts, tool versions, random seeds where applicable, environment metadata, and evaluation results must be retained sufficiently to reproduce the experiment. Parent agents and later loops may cite prior artifacts but may not rewrite them.

## Production prohibition

The production environment may consume only explicitly promoted, versioned artifacts. Online self-modification, hidden prompt mutation, unlogged contract changes, and direct production learning are prohibited.