# GitHub Document Control

## 1. Repository model

Each architecture or design project MUST have a dedicated GitHub repository. The repository stores and tracks the project’s Markdown documentation, ADRs, evidence indexes, templates, diagrams, generated review artifacts, and release packages just as a software project stores code.

The repository is the authoritative source of truth. Chat sessions, local copies, and downloadable packages are supporting working or delivery artifacts only.

Recommended layout:

```text
<project-repository>/
  README.md
  CHANGELOG.md
  docs/
    collaboration-playbook/
    design/
    evidence/
    adr/
    templates/
  artifacts/
    releases/
```

## 2. Branching and change model

- The default branch (normally `main`) represents the approved project baseline.
- Direct pushes to the default branch SHOULD be blocked with branch protection.
- Every material documentation change MUST begin on a named working branch.
- Use clear branch names, for example `docs/adr-004-agent-contracts` or `design/capability-model`.
- Commits MUST be small enough to review, use meaningful messages, and contain only related changes.
- A commit is not a baseline change until its pull request is merged.

Suggested commit-message prefixes:

| Prefix | Use |
| --- | --- |
| `docs:` | Documentation content or structure. |
| `adr:` | Architecture decision record. |
| `evidence:` | Evidence index or traceability update. |
| `governance:` | Process, controls, templates, or policy. |
| `release:` | Version, manifest, or packaged artifact. |

## 3. Pull request requirements

Each pull request for a material change MUST include:

- purpose and scope;
- linked recommendation and decision/ADR IDs;
- files changed and expected baseline impact;
- evidence and assumptions;
- validation performed;
- delivery artifact information, if a package is produced;
- reviewer(s) and required approver(s).

At least one qualified reviewer SHOULD approve material architecture, governance, or interface changes. The designated decision authority MUST approve decisions within their scope. GitHub review is evidence of review; it does not substitute for the decision authority recorded in the ADR.

## 4. Merge gate

Before merging, verify:

- [ ] Pull request description contains required decision and evidence references.
- [ ] Markdown links and document indexes are valid.
- [ ] `CHANGELOG.md` and ADR status are updated.
- [ ] Required review approvals are recorded.
- [ ] Required automated checks have passed, if configured.
- [ ] No unresolved material comments remain.
- [ ] Generated artifacts identify the source commit SHA.

After merge, record the merged commit SHA in the session closeout and, where relevant, in the package manifest.

## 5. ADR and issue linkage

- Give each material decision an ADR under `docs/adr/`.
- Use GitHub Issues for open questions, follow-up actions, acceptance criteria, and reviewable work when the project uses issue tracking.
- Link pull requests to affected ADRs and issues.
- When an ADR is superseded, retain the original and add the successor reference; never delete decision history simply because the decision changed.

## 6. Release artifacts and retention

Release packages, such as ZIP files or rendered PDFs, SHOULD be generated from a clean checkout of the merged default branch. Each package MUST contain a manifest with:

- project/repository name;
- documentation version;
- source commit SHA;
- package file inventory;
- creation date;
- integrity checksum;
- verification result.

Store released packages under a versioned location such as `artifacts/releases/v<version>/`, attach them to a GitHub Release, or use another approved durable project storage location. A temporary chat attachment is never the sole delivery location.

## 7. Emergency changes

If an emergency requires bypassing normal review, the responsible authority MUST document the reason, risk, and follow-up review requirement in the pull request or ADR. The change MUST be reconciled into the normal review trail as soon as practical.


