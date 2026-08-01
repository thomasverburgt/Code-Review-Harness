# CAP-COORD — Deterministic Capability Coordinator

> **Identity:** `38d55885-5785-4da7-b4a7-94ca65e652e5`
> **Contract:** [Deterministic Capability Coordination Contract](../../contracts/capability-coordination-contract.md)
> **Implementation:** deterministic; no model prompt

## Authoritative question

Is the declared capability-review input set exact, valid, complete, traceable, and eligible to be dispatched to `CAP-SYNTH`?

## Responsibilities

Inventory expected inputs; verify identity, schemas, integrity, lifecycle, freshness, compatibility, versions, completeness, and partial-input authority; preserve conflicts; index findings, risks, conflicts, decision requests, and evidence; compute deterministic hashes; and emit routing state.

## Prohibited behavior

Do not generate a capability assessment or narrative, normalize away disagreement, change confidence, derive new risks, recommend a course of action, settle a decision, or produce an enterprise semantic handoff. Every output is validation and routing metadata with human decision authority preserved.
