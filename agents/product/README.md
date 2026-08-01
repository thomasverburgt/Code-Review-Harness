# Product Agents

Product agents inherit the [Universal Agent Contract](../../contracts/universal-agent-contract.md) and [Product Agent Contract](../../contracts/product-agent-contract.md). They correlate specialist outputs within one product and preserve all child evidence and disagreement.

The layer topology, workflow, role status, and shared gates are defined in the [Product Agent Framework](product-agent-framework.md).

## `PROD-SYNTH` — Product Synthesis Lead

**Question:** What coherent engineering state follows from all required product specialist reviews?

Produces the authoritative product input manifest, cross-domain correlations, product posture, unresolved conflicts, confidence reconciliation, and capability handoff. It cannot approve release or override a specialist.

Executable candidate details are defined in [product-synthesis-lead.md](product-synthesis-lead.md). Candidate status does not authorize baseline workflow scheduling.

## `PROD-SEC` — Product Security Synthesizer

**Question:** What integrated product security posture follows from secure-code, secrets, composition, dependency, image, workload, platform, communications, IaC, pipeline, and risk evidence?

Produces security-domain correlations, attack-path hypotheses, control coverage, evidence gaps, product security findings, CAPA options, and escalation requests. It cannot declare a product secure or accept cyber risk.

Role details are defined in [product-security-synthesizer.md](product-security-synthesizer.md).

## `PROD-ARCH` — Product Architecture Synthesizer

**Question:** Does the product's implemented structure coherently realize its approved architecture and operational intent?

Produces intended/implemented comparisons, dependency and interface correlations, quality-attribute posture, architecture drift, product architecture findings, cost drivers, and capability escalations. It cannot approve architecture or substitute preference for criteria.

Role details are defined in [product-architecture-synthesizer.md](product-architecture-synthesizer.md).

## `PROD-LINT` — Product Quality Synthesizer

**Question:** What product-level maintainability and code-quality posture follows from lint, dependency, architecture, testing, and defect evidence?

Produces normalized quality-rule coverage, maintainability trends, systemic code-quality findings, false-positive analysis, debt signals, and CAPA options. It cannot turn tool output directly into an authoritative finding without assessment.

Role details are defined in [product-quality-synthesizer.md](product-quality-synthesizer.md).
