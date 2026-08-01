# Repository Artifact Lifecycle

This document assigns a purpose, authority, mutability rule, and retention expectation to repository artifacts. It implements ADR 0027 without changing the authority of previously accepted evidence.

| Class | Canonical purpose | Mutability | Examples |
|---|---|---|---|
| Authored source | Human- or tool-authored material from which controlled artifacts are produced | Changed through normal review | contracts, agent specifications, schemas, prompts, document builders |
| Reusable fixture | Synthetic or bounded data intentionally reused by tests | Versioned; changed only with affected tests and expectations | source manifests, gold cases, negative cases, expected outputs |
| Immutable evidence | Creation-time record of an execution, review, response, or verification | Append-only; correction creates a linked successor | reference runs, ledger objects, GX-10 archives, human responses |
| Generated deliverable | Human-consumable output built from controlled source or evidence | Rebuilt as a new version; approved distributions are retained | DOCX reports, PDFs, training decks |
| Current-state projection | Rebuildable view of the latest authoritative records | May be regenerated; never overrides source records | readiness summary, decision queue, live roadmap status |
| Temporary work | Local render, cache, scratch, or transient execution output | Disposable and ignored | `_runs`, `_docx_work`, intermediate page renders |

## Directory responsibilities

- `agents`, `contracts`, `orchestration`, `requirements`, `governance`, `adr`, and most of `docs` contain authored source.
- `fixtures` is the canonical reusable-fixture root. Existing `fixtures/*/evidence` paths are immutable legacy packages indexed under `evidence`; new retained evidence uses the top-level `evidence` root.
- `status` contains living, rebuildable projections. It must cite authoritative records and must not contain approval authority.
- `deliverables`, `session-review`, and `training` contain controlled outputs and must identify source, version, approval state, and whether an item is a final release or working artifact.
- `_runs` and `_docx_work` are temporary work and remain ignored.

## Evidence rules

Existing accepted evidence remains at its recorded path unless a separately approved migration copies it, verifies its hash, and records the mapping. A move never authorizes rewriting content. Descriptive current-state documentation may be corrected, but creation-time packets, manifests, ledgers, responses, and calibration archives remain unchanged.

## Generated-output rules

Every generated deliverable should identify, directly or through a neighboring manifest:

- source artifact IDs, paths, and hashes;
- generator and version;
- generation timestamp and environment;
- lifecycle state such as draft, leadership review, approved distribution, or superseded;
- the human authority required for state transitions.

Intermediate renders are not retained in the main source tree unless they are explicit review evidence.

## Migration and rollback

Material reorganizations use a manifest containing old path, new path, artifact class, hash, compatibility treatment, validation result, and rollback command or procedure. The initial migration commit does not delete the old copy. Legacy removal occurs only after consumers and links have been checked locally and on the approved DGX Spark-equivalent test system.
