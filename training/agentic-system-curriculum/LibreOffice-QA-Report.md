# LibreOffice QA Report

**Review date:** July 30, 2026  
**Renderer:** LibreOffice 26.2.5.2 (headless PDF export)  
**Source package:** `C:\Users\toomu\OneDrive\Desktop\agentic-system-curriculum`  
**QA output:** `C:\Users\toomu\OneDrive\Documents\Code Harness\training\agentic-system-curriculum\qa-libreoffice`

## Outcome

**Conditional pass — revisions recommended before classroom release.**

- The Word handbook opened and exported successfully in LibreOffice.
- All 12 PowerPoint decks opened and exported successfully.
- All 84 slides are present and visually legible.
- No missing fonts, missing images, clipped slide objects, overlaps, or broken diagrams were observed.
- One slide has an awkward mid-word wrap.
- The handbook has several list and page-break defects that reduce usability.
- The source DOCX and PPTX files were not changed during QA.

## Word handbook

**Artifact:** `Code-Review-Harness-Agentic-System-Curriculum.docx`  
**LibreOffice result:** 53-page PDF and 53 rendered page images

### Findings

1. **Numbered facilitation lists do not restart for each session — medium severity.**
   The “Facilitation run of show” numbering continues across session boundaries. For example, Session 1 begins with items 7–11, Session 2 with 12–16, and later sessions continue the same global sequence. Each session should restart at 1 unless the cumulative numbering is intentional.

2. **Agent matrix rows split across pages without repeated row context — medium severity.**
   Page 45 begins with the continuation text “Communication Security Reviewer,” while the associated designation and other fields remain on page 44. Page 49 similarly begins with a continuation for “Metrics Agent.” Keep each matrix row together or repeat the identifying fields on continuation pages.

3. **Capstone disposition callout splits across pages 50–51 — medium severity.**
   Page 50 ends with “return for,” and page 51 begins with “change; or reject because…”. Keep the full disposition callout on one page.

4. **Several instructional table rows split at page boundaries — low severity.**
   Examples include continuation fragments at the tops of pages 23, 26, and 29. The content remains readable, but the split weakens scanability during instruction.

5. **Cross-renderer pagination differs — informational.**
   LibreOffice produced 53 pages, compared with the previously observed 51-page Word rendering. There are no blank pages; the difference comes from reflow and the split items described above.

## PowerPoint decks

**Artifacts:** Sessions 01–12  
**LibreOffice result:** 12 PDFs, 7 slides per deck, 84 rendered slides

### Finding

1. **Session 02, slide 4: “Recommendation” breaks mid-word — low severity.**
   LibreOffice renders the label as “Recommendat” / “ion.” Widen the fourth process card, reduce the label size slightly, or insert a deliberate line break at a semantic boundary.

### Visual pass

Sessions 01 and 03–12 rendered cleanly. Titles, diagrams, process arrows, activity cards, footers, and exit-ticket slides remain within their intended bounds.

## Speaker notes

LibreOffice’s normal PDF export does not include presenter notes, so this pass confirms slide-canvas rendering rather than the visual formatting of notes pages. Notes should receive a separate presenter-view or notes-page print check if printed notes are part of the delivery package.

## Recommended release disposition

Correct the handbook numbering and page-break issues, correct Session 02 slide 4, then rerun the same LibreOffice export. The current package is usable for internal review but should not be treated as the final classroom master.
