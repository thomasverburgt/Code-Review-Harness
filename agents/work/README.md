# Work Agents

Work agents inherit the [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Work Agent Contract](../../contracts/work-agent-contract.md).

## `WORK-REVIEW` — Evidence Review Worker

**Question:** Does the bounded input set satisfy the requesting contract's review criteria?

Applies pinned criteria to declared inputs and returns attributable observations, coverage, exceptions, and quality checks. It cannot create an authoritative layer finding unless the requesting reviewer adopts it with provenance.

Role details are defined in [evidence-review-worker.md](evidence-review-worker.md).

## `WORK-ANALYZE` — Evidence Analysis Worker

**Question:** What reproducible relationships, measures, or anomalies exist in the bounded input set?

Performs declared calculations and correlations, preserves assumptions and methods, and returns analysis results with uncertainty. It cannot choose a course of action or expand the dataset.

Role details are defined in [evidence-analysis-worker.md](evidence-analysis-worker.md).

## `WORK-SUMMARIZE` — Evidence Summarization Worker

**Question:** What faithful, loss-aware summary of the bounded inputs serves the declared consumer?

Produces a source-linked summary, omitted-detail manifest, conflicts, and compression limitations. It cannot resolve contradictions, remove material caveats, or represent a summary as the source record.

Role details are defined in [evidence-summarization-worker.md](evidence-summarization-worker.md).
