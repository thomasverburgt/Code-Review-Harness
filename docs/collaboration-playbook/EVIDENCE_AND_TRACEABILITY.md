# Evidence and Traceability

## 1. Evidence model

Every material claim, recommendation, finding, and decision SHOULD be traceable through the chain below:

`source -> observation -> assessment -> recommendation -> decision -> action -> validation`

Observations are factual statements tied to source material. Assessments interpret observations. Recommendations propose action. Decisions are made only by an authorized decision authority.

## 2. Evidence record

Use stable IDs such as `EVD-0001`, `REC-0001`, `DEC-0001`, and `ACT-0001`. An evidence record MUST include:

| Field | Description |
| --- | --- |
| `evidence_id` | Stable, unique identifier. |
| `claim_supported` | Exact claim or finding it supports. |
| `source_type` | Repository file, test result, interview, standard, design artifact, or external source. |
| `source_locator` | Immutable locator: path and revision, URL, report ID, or interview record. |
| `collection_method` | How it was obtained or derived. |
| `captured_at` | Date/time collected or source version date. |
| `provenance` | Origin and transformations, if any. |
| `freshness` | Current, aging, stale, or unknown. |
| `confidence` | Evidence confidence with short rationale. |
| `limitations` | Coverage gaps, ambiguity, or conditions. |

## 3. Traceability requirements

- A recommendation MUST reference the evidence and assumptions on which it relies.
- An accepted decision MUST reference its recommendation(s), alternatives, and the ADR when required.
- An action MUST reference the accepted decision or an approved corrective/preventive action.
- Validation MUST link back to the relevant acceptance criteria.
- Agents or tools MUST preserve child evidence identifiers when aggregating or summarizing; they may add derived evidence but MUST NOT rewrite provenance.

## 4. Handling untrusted or incomplete context

Conversation transcripts, recalled statements, and generated summaries are useful context but are not automatically authoritative evidence. Mark them as `untrusted_context` until verified against a primary source or explicitly accepted as an operating assumption.

When evidence conflicts, retain both references, describe the conflict, assign an owner, and do not silently select one. The decision record MUST state how the conflict was resolved or why it remains open.

## 5. Context preservation

At each commit or shutdown, create or update a concise context handoff containing:

- scope and current design version;
- accepted decisions and ADR IDs;
- open questions and decision triggers;
- assumptions and evidence gaps;
- exact repository paths and artifact versions;
- next recommended work item.

The handoff is an index, not a substitute for authoritative source artifacts.


