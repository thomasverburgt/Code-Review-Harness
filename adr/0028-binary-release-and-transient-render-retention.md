# ADR-0028: Separate Controlled Binary Releases from Transient Render Evidence

- Status: accepted
- Date: 2026-08-01
- Decision authority: project maintainer
- Owners: training, documentation, release, and repository maintainers
- Supersedes: none
- Superseded by: none

## Context

The training curriculum and prompt-design deliverables contain useful authored builders and approved or candidate DOCX/PPTX outputs, but they also contain intermediate PDFs, page PNGs, contact sheets, inspection records, and repeated QA passes. Binary training artifacts account for most tracked repository bytes. The prompt-design DOCX builders existed only in ignored working storage, making their committed outputs difficult to reproduce.

Applying Git LFS attributes directly to every existing binary would rewrite hundreds of tracked files into LFS pointers in one increment. Deleting repeated renders before classifying their review and release role would risk discarding evidence.

## Evidence

- `training/agentic-system-curriculum` contains 888 tracked files, including 639 PNGs and 40 PDFs.
- Revised and condensed release reports record passing LibreOffice QA for the current candidate packages.
- Four committed prompt-design DOCX files have corresponding Python builders under the previously ignored `_docx_work` tree.
- Git LFS 3.7.1 is available in the development environment.

## Decision

1. Track reproducible deliverable builders under `document_builders` and keep temporary render output ignored.
2. Add content-hashed release manifests for the current prompt-design deliverables and the revised and condensed training candidates.
3. Use Git LFS for future approved DOCX, PPTX, and PDF files placed under explicit `releases` directories.
4. Store intermediate page renders, contact sheets, montages, inspection output, and superseded QA passes as ephemeral CI artifacts or external release-review archives rather than normal source files.
5. Treat existing tracked binaries as a legacy release layout. Do not rewrite or delete them in Sprint 2. A later retirement sprint may migrate them only with an old-to-new mapping, SHA-256 verification, reviewed archive destination, and rollback instructions.
6. Preserve final QA reports and only those render artifacts explicitly designated as human-review evidence.

## Alternatives considered

- **Convert every existing binary to Git LFS immediately:** rejected because the pointer rewrite would obscure the organization change and increase rollback risk.
- **Keep all QA renders permanently in Git:** rejected because multiple render passes dominate repository size and do not all remain authoritative.
- **Move every binary to external storage:** rejected because controlled source deliverables and compact approved releases benefit from repository traceability.
- **Delete exact duplicates immediately:** rejected because byte identity does not determine whether a self-contained evidence package has an independent retention obligation.

## Consequences

- The repository grows slightly before the later compaction sprint.
- New approved binary releases have a predictable LFS boundary.
- Release candidates become independently integrity-verifiable.
- Document-generation dependencies and invocation commands become controlled source.
- Historical QA trees remain until the retirement gate is met.

## Traceability

- [ADR 0027: Govern Repository Artifact Lifecycles](0027-govern-repository-artifact-lifecycles.md)
- [Repository Artifact Lifecycle](../docs/repository-artifact-lifecycle.md)
- [Repository Organization Sprint Plan](../planning/repository-organization-sprints.md)
- [Training Curriculum Index](../training/agentic-system-curriculum/README.md)
- [Deliverable Builders](../document_builders/README.md)

## Validation

- Every release-manifest artifact path exists and reproduces its recorded SHA-256 and byte length.
- Each prompt-design deliverable maps to a tracked builder.
- Structural CI verifies release manifests.
- No existing retained evidence hash changes in Sprint 2.
- Future binary migrations are tested locally and on DGX Spark or an approved equivalent before legacy removal.

## Unresolved matters

- The external archive service and retention period for superseded training QA packages.
- Whether final visual-review PNGs remain in Git LFS or release assets after the first migrated curriculum release.

