# ADR-0013: Reproducible Evidence Locators and Expert Review Packets

- **Status:** Accepted
- **Date:** 2026-07-31
- **Accepted by:** project maintainer
- **Owners:** evidence engineering, report operations, security, records administration, and audit
- **Scope:** Increment 4 expert-review preparation

## Context

ADR-0012 freezes the technical report before controlled off-system review. The report identifies evidence references, but an evidence identifier alone does not tell a human expert which file was scanned, which immutable version was assessed, or where in that file the observed condition appeared. A reviewer cannot reasonably ascertain correctness without a reproducible route back to the source.

The maintainer confirmed on 2026-07-31 that exact source localization is required before moving to the next increment.

## Decision record

Accepted by the project maintainer on 2026-07-31 after the reference implementation preserved the ADR-0012 report hash and passed the complete six-gate local and GX-10 conformance suites.

## Decision

1. Keep the approved technical report immutable.
2. Attach a separately versioned and hashed expert-review packet to the exact report package ID and package hash.
3. Represent each evidence source with a structured locator containing the repository URI, immutable revision, repository-relative path, line range or named section, safe redacted excerpt, integrity fingerprint, collection method, access constraints, and reproduction steps.
4. Bind every actionable report item to one or more evidence references and resolved locators. Derived CAPAs and recommendations require explicit bindings; ancestry may not be guessed by the reviewer.
5. Mark the packet `ready_for_expert_review` only when every actionable item resolves to at least one `source_located` locator. Otherwise fail closed as `blocked_missing_locator` or `blocked_unverified_locator` and list the affected report items.
6. Never place raw secret values in the packet. Redaction must preserve the location and enough safe context to reproduce the observation under authorized access.
7. Persist packets and locators immutably. A changed source or locator produces a new record and hash; it cannot rewrite the report or an accepted locator.
8. Treat source access as least privilege. The packet explains how an authorized reviewer obtains the source but does not embed restricted source content.

## State model

`report_packaged -> locator_resolution -> packet_blocked | ready_for_expert_review -> controlled_export`

The packet state is derived. It does not approve distribution, decide a finding, accept a risk, or authorize a change.

## Consequences

- Human experts can navigate from a report item to the exact assessed source.
- Review packages remain usable after the working clone is removed because the source revision is immutable.
- Missing, stale, inaccessible, or ambiguous locations are visible before expert review.
- Report immutability and the external human-decision boundary from ADR-0012 remain intact.
- Locator construction and verification become explicit testable responsibilities of the harness.

## Validation required

- exact report ID and package-hash binding;
- immutable Git revision, safe relative path, valid line range, and canonical hashes;
- complete actionable-item-to-evidence-to-locator resolution;
- deterministic packet and annex generation;
- rejection of path traversal, mutable revisions, altered bindings, unsafe excerpts, and missing locators;
- unchanged report bytes and package hash; and
- full local and GX-10/DGX Spark-equivalent conformance.

## Rollback plan

Disable expert-packet generation and controlled export of packets, returning to the immutable ADR-0012 report output. Retain existing packets and locators as readable audit evidence without rewriting or deleting them. Re-enable only after corrected schemas/runtime pins pass local and GX-10 conformance. Rollback cannot make an unlocalized report item review-ready.
