# ADR 0002: Evidence Is Never Rewritten by a Parent

- **Status:** accepted
- **Date:** 2026-07-24
- **Decision authority:** project maintainer
- **Owners:** agent-contract and evidence-governance maintainers
- **Supersedes:** none
- **Superseded by:** none

## Context

The harness uses a hierarchy of specialist, product, capability, and enterprise agents. Parent agents must correlate child outputs and explain higher-order conditions, but a parent has broader scope and different authority than the child that directly reviewed the evidence.

If a parent rewrites a child observation, finding, score, confidence value, or conclusion, the original domain judgment becomes indistinguishable from the parent's interpretation. That would erase disagreement, break provenance, and allow polished synthesis to launder unsupported claims into apparent fact.

## Evidence

- The [Evidence Contract](../contracts/evidence-contract.md) defines evidence as an immutable pointer to an observable source.
- The [Universal Agent Contract](../contracts/universal-agent-contract.md) separates observations, assessments, findings, patterns, conflicts, and derived assertions.
- Product, capability, and enterprise contracts require contributing artifact IDs, correlation logic, confidence provenance, uncertainty, and preserved disagreement for derived assertions.
- The integrated architecture depends on immutable inter-layer handoffs rather than shared mutable records.

## Decision

Parent agents aggregate immutable child artifacts and may create new, explicitly derived assertions with citations. They do not overwrite, paraphrase in place, reclassify, suppress, or otherwise change child evidence or conclusions.

A derived parent assertion must identify its contributing artifact IDs and evidence references, state the correlation or transformation method, preserve relevant child confidence and limitations, and expose disagreement or conflict. Normalization may add a mapped representation, but it must retain the original value and identify the versioned mapping used.

When a parent disputes a child result, it records a conflict or separate assessment and requests the appropriate review or human disposition. It does not silently select one result or mutate the child record.

## Alternatives considered

- **Allow parent agents to rewrite children for consistency:** rejected because consistency would come at the cost of provenance and independent domain authority.
- **Flatten child outputs into a single synthesized record:** rejected because it would prevent reconstruction of the original review population and disagreements.
- **Prohibit all parent interpretation:** rejected because cross-domain and system-of-systems conditions require bounded derived assertions.
- **Preserve only child links, not original content:** rejected because durable review requires the exact immutable artifact, not an unresolved reference alone.

## Consequences

- Parent artifacts contain both immutable child references and separately identified derived content.
- Conflicts remain first-class records until an authorized disposition is linked.
- Consumers can distinguish source facts from child assessments and parent synthesis.
- Reports may contain normalized summaries, but each material assertion must resolve to its contributing records.
- Schema and storage requirements increase because original and derived representations coexist.

## Traceability

- [Universal Agent Contract](../contracts/universal-agent-contract.md)
- [Evidence Contract](../contracts/evidence-contract.md)
- [Product Agent Contract](../contracts/product-agent-contract.md)
- [Capability Delivery Contract](../contracts/capability-delivery-contract.md)
- [Enterprise Agent Contract](../contracts/enterprise-agent-contract.md)
- [Integrated Agent Framework](../agents/integrated-agent-framework.md)

## Validation

- Fan-in verifies referenced child artifact IDs and hashes before routing.
- Derived assertions fail validation when contributor references or correlation logic are absent.
- Tests confirm that child statements, classifications, confidence values, and conflicts remain unchanged through synthesis.
- Human-readable reports resolve material assertions through evidence bindings to the original source location.
- Replaying a parent from the same immutable children reproduces its declared input population and lineage.

## Unresolved matters

- Standardized cross-role normalization vocabularies beyond the current schemas and projection manifests.
- Presentation rules for showing large disagreement sets to leadership without hiding minority assessments.
- Long-term retention and availability guarantees for externally hosted evidence sources.
