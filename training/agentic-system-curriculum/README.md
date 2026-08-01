# Agentic System Curriculum

This curriculum currently contains full and condensed course variants, generated decks and handouts, LibreOffice review output, and several retained QA render passes.

- `revised` contains the full revised curriculum package.
- `condensed` contains the six-session condensed package.
- `qa-libreoffice` contains LibreOffice-based review material.
- `LibreOffice-QA-Report.md` records the suite-level QA result.

The revised and condensed packages now have content-hashed `release-manifest.json` files. Their DOCX/PPTX outputs and final QA reports are release candidates. Multiple render passes, page images, contact sheets, inspection NDJSON, and superseded QA directories are migration candidates for CI artifacts or external review archives.

ADR 0028 selects Git LFS for future approved binaries placed under explicit `releases` directories. Existing binaries remain in their legacy paths until a verified migration records old and new paths, hashes, archive treatment, and rollback. Do not delete or consolidate binary artifacts solely because their hashes match.
