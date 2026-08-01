# Architecture Decision Records

This register preserves the original concise governance decisions. The normative formal records are maintained in the [`adr`](../adr/README.md) directory.

## ADR-001 — Immutable artifacts are authoritative

Git-versioned Markdown/JSON artifacts are the record of review. Indexes may accelerate query and correlation but cannot become the source of truth. See the normative [ADR 0001](../adr/0001-immutable-artifacts-are-authoritative.md).

## ADR-002 — Evidence is never rewritten by a parent

Parent agents aggregate and create derived assertions with citations. They do not overwrite child evidence or conclusions. See the normative [ADR 0002](../adr/0002-evidence-is-never-rewritten-by-a-parent.md).

## ADR-003 — Specialists do not decide

Specialists observe and assess. Decisions are reserved for designated synthesis and human governance roles. See the normative [ADR 0003](../adr/0003-specialists-do-not-decide.md).

## ADR-004 — CAPA and positive patterns are separate channels

CAPA remedies deficiencies. Pattern candidates document demonstrably beneficial practices and follow a separate promotion path. See the normative [ADR 0004](../adr/0004-capa-and-positive-patterns-are-separate-channels.md).

## ADR-005 — Human review is earned, not presumed absent

Automation maturity is measured using agreement, false-positive rates, reviewability, confidence, and risk. Policy controls may reduce—but never silently remove—human gates. See the normative [ADR 0005](../adr/0005-human-review-is-earned-not-presumed-absent.md).

## ADR-006 — Universal agent identity and contract standard

Every agent has an immutable UUID and canonical designation, all outputs inherit one universal contract, and legacy designations remain non-reusable aliases. See the normative [ADR 0006](../adr/0006-universal-agent-identity-and-contract-standard.md).
