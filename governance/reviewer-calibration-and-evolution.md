# Reviewer Calibration and Controlled Evolution

## Purpose

Reviewer quality is a first-class system concern. Production reviewers remain deterministic and immutable within a released version. Calibration, prompt improvement, contract evolution, and candidate model changes occur only in an isolated validation environment.

## Calibration and QA service

The cross-cutting calibration service SHALL:

- test rubric adherence, inter-reviewer consistency, longitudinal stability, evidence fidelity, uncertainty handling, and output-schema conformance;
- rerun historical and gold-standard packages after prompt, contract, model, tool, or rubric changes;
- calculate reviewer health measures and expose drift without editing production artifacts;
- retain every input, output, score, diff, rationale, configuration, and benchmark result;
- route all promotion decisions to a human authority.

## Gold-package validation matrix

The benchmark suite SHALL cover combinations of:

- small and large repositories, products, capabilities, evidence graphs, and dependency graphs;
- exemplary, average, degraded, and severely deficient implementations;
- strong, weak, ambiguous, conflicting, incomplete, stale, and adversarial evidence;
- strong and weak requirements, including vague, untestable, conflicting, misallocated, and missing requirements;
- low and high integration complexity, coupling, mission criticality, HCD maturity, security posture, governance maturity, and architectural maturity;
- pathological combinations such as good implementation against bad requirements, bad implementation against good requirements, high mission value with high cost, and apparently compliant systems with poor mission effectiveness;
- controlled mutations of the same package to test whether reviewer outputs change proportionally and explainably;
- repeated execution of unchanged packages to test deterministic stability.

Gold packages SHALL include positive exemplars, severe-failure packages expected to produce many findings and CAPAs, and complex mixed-quality packages where correct uncertainty and conflict handling matter more than finding count.

## Reviewer health measures

At minimum, track:

- rubric conformance;
- schema validity;
- repeatability and variance on identical inputs;
- agreement with adjudicated gold outcomes;
- false-positive and false-negative rates;
- finding, evidence, and review confidence calibration;
- severity and priority calibration;
- CAPA appropriateness and validation completeness;
- uncertainty and insufficient-evidence detection;
- cross-version regression count and impact;
- downstream artifact compatibility;
- human-review agreement and override patterns.

No single reviewer health score may conceal the component distribution.

## Controlled evolution loop

Evolution follows `observe -> analyze -> propose -> benchmark -> regress -> human review -> promote or reject`.

Candidate prompt, contract, rubric, tool, or model variants MAY be generated iteratively inside the sandbox under a human-approved evolution budget. The budget MUST constrain:

- permitted mutation types;
- maximum iterations;
- benchmark subset and full-suite requirements;
- minimum improvement thresholds;
- maximum tolerated regressions;
- protected safety, authority, traceability, and schema invariants;
- stopping conditions.

A human may authorize a bounded sequence of loops, but production promotion remains a separate human decision after reviewing aggregate results and material diffs.

## Immutable lineage and promotion package

Every candidate and released reviewer version MUST retain:

- parent version and immutable lineage ID;
- complete prompt, contract, rubric, tool, model, and configuration versions;
- exact textual and structural diff;
- reason for each change and evidence that motivated it;
- benchmark inputs, outputs, score deltas, confidence deltas, and regression analysis;
- downstream compatibility and regression-impact assessment;
- human disposition, approver identity, timestamp, and decision record;
- release and rollback instructions.

## Non-negotiable controls

- No autonomous self-modification in production.
- No candidate may rewrite gold labels or acceptance criteria to improve its score.
- No aggregate improvement may hide a protected-invariant failure or material regression.
- No production result may be silently regenerated after a reviewer version changes.
- Historical results retain the exact reviewer lineage that produced them.
