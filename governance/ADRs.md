# Architecture Decision Records

## ADR-001 — Immutable artifacts are authoritative

Git-versioned Markdown/JSON artifacts are the record of review. Indexes may accelerate query and correlation but cannot become the source of truth.

## ADR-002 — Evidence is never rewritten by a parent

Parent agents aggregate and create derived assertions with citations. They do not overwrite child evidence or conclusions.

## ADR-003 — Specialists do not decide

Specialists observe and assess. Decisions are reserved for designated synthesis and human governance roles.

## ADR-004 — CAPA and positive patterns are separate channels

CAPA remedies deficiencies. Pattern candidates document demonstrably beneficial practices and follow a separate promotion path.

## ADR-005 — Human review is earned, not presumed absent

Automation maturity is measured using agreement, false-positive rates, reviewability, confidence, and risk. Policy controls may reduce—but never silently remove—human gates.
