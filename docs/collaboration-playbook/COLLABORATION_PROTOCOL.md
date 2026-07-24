# Collaboration Protocol

## 1. Purpose and operating principles

This protocol governs a human-led, AI-assisted architecture and design session. It turns exploratory discussion into traceable documentation without treating informal conversation as implementation.

Principles:

- **Human authority:** the human participant owns priorities, acceptance, risk tolerance, and final decisions.
- **Evidence before assertion:** recommendations identify facts, assumptions, inferences, and unknowns.
- **Constructive challenge:** alternatives and material trade-offs are surfaced before a decision is accepted.
- **No implied persistence:** a design is not committed until required files are updated and verified.
- **Traceability:** findings, recommendations, decisions, and artifacts retain stable identifiers and links to their basis.
- **Progressive precision:** brainstorming may be broad; commitments become increasingly specific and testable.

## 2. Participant roles

| Role | Primary responsibilities | Authority |
| --- | --- | --- |
| Sponsor / operator | States mission, constraints, priorities, and acceptance criteria; accepts decisions and commits. | Final decision authority. |
| Facilitator / design partner | Structures discussion, clarifies terms, summarizes, challenges gaps, drafts recommendations and documentation. | Recommends; does not make binding decisions. |
| Domain subject-matter expert | Supplies domain facts, constraints, standards, and review of technical claims. | Advises within domain. |
| Evidence steward | Maintains source references, provenance, confidence, and traceability links. | Validates evidence hygiene. |
| Document custodian | Maintains repository structure, document consistency, versioning, and release artifacts. | Executes and verifies written updates when authorized. |
| Decision authority | Named individual or board that accepts decisions where sponsor authority is delegated. | Final decision for delegated scope. |

One person may hold multiple roles. The session MUST identify the sponsor/operator and the document custodian before substantive work begins.

## 3. Session lifecycle

### 3.1 Startup

At startup, record:

- objective, scope, out-of-scope items, and expected deliverables;
- participants and roles;
- authoritative repository, branch or version, documentation root, and artifact destination;
- known source material and its trust status;
- decision authority and commit authority;
- definition of done for the session.

The authoritative repository MUST be the project's dedicated GitHub repository. A local working folder, chat transcript, exported ZIP, or temporary attachment is a working copy or delivery artifactâ€”not the source of truth.

Use the startup template in [Session Templates](templates/SESSION_TEMPLATES.md).

### 3.2 Brainstorming and exploration

The facilitator MUST distinguish these statement types:

| Type | Meaning | Treatment |
| --- | --- | --- |
| Observation | Directly supported fact or source excerpt. | Capture with evidence reference. |
| Assumption | Working condition not yet verified. | Label and assign validation path. |
| Idea | Candidate approach. | Explore; do not treat as a decision. |
| Recommendation | Supported proposal with rationale and trade-offs. | Challenge and prepare for acceptance. |
| Decision | Accepted direction by the decision authority. | Record and commit when authorized. |
| Action | Work to perform. | Assign owner and completion evidence. |

Brainstorming SHOULD use bounded questions: the problem being solved, constraints, options, consequences, and evidence needed. The facilitator should periodically summarize: â€œwhat we know,â€ â€œwhat we are assuming,â€ â€œwhat remains open,â€ and â€œwhat is ready for a decision.â€

### 3.3 Forming and challenging recommendations

Each material recommendation MUST include:

- a stable recommendation ID;
- problem or decision question;
- proposed approach;
- supporting evidence and assumptions;
- at least one viable alternative, or an explanation why none exists;
- benefits, costs, risks, dependencies, and reversibility;
- impact scope: product, capability, enterprise, or equivalent;
- acceptance criteria and validation method;
- recommendation owner and intended decision authority.

The facilitator MUST challenge recommendations proportionate to risk. Minimum challenge questions are:

1. What evidence supports this claim, and how current is it?
2. What assumption would most change the outcome?
3. What option was rejected, and why?
4. What could fail operationally, organizationally, or at an integration boundary?
5. How will success or harm be detected after implementation?

### 3.4 Decision acceptance

A decision is accepted only when the decision authority explicitly states acceptance or provides an equivalent written approval. Acceptance MUST identify the decision ID, scope, and any conditions.

Accepted decisions are classified as:

- **Operational:** local implementation choice; document in the relevant design artifact and changelog.
- **Architectural:** affects interfaces, quality attributes, standards, dependencies, or future options; create an ADR.
- **Governance / policy:** changes controls, approvals, retention, or compliance obligations; create an ADR and update governing policy.
- **Deferred:** intentionally not decided; record the trigger and owner for reconsideration.

The facilitator may recommend a decision but MUST NOT represent a proposal as accepted without explicit authority.

### 3.5 Commit execution

â€œCommitâ€ has two separate meanings and MUST be stated precisely:

| Term | Definition |
| --- | --- |
| **Decision commit** | The decision authority has accepted a direction. |
| **Documentation commit** | The authorized files have been updated, reviewed for consistency, and verified in the designated repository or deliverable package. |

A conversational agreement alone is neither a documentation commit nor a source-control commit. A valid documentation commit requires all of the following:

1. Identify documents, versions, and change IDs affected.
2. Apply the actual file edits.
3. Update `CHANGELOG.md`; create or update an ADR when required.
4. Validate cross-references, templates, and artifact contents.
5. Report exact created/updated files and validation results.
6. If source control is in scope, make or prepare the actual VCS commit with its identifier. Do not claim a VCS commit unless it exists.

For project documentation, source control is always in scope. The documentation commit MUST be pushed to a non-protected working branch and merged to the default branch through the project's configured pull-request process, except where a documented emergency procedure authorizes otherwise. See [GitHub Document Control](GITHUB_DOCUMENT_CONTROL.md).

### 3.6 Corrections and reversals

Corrections are normal and MUST preserveâ€”not eraseâ€”decision history. When a participant corrects a statement:

- acknowledge the correction plainly;
- classify the affected item: observation, assumption, recommendation, decision, or artifact;
- update the authoritative document(s) when a commit is requested;
- supersede rather than silently overwrite a material ADR decision;
- add a changelog entry when the correction changes published meaning or behavior.

Use â€œsuperseded,â€ â€œwithdrawn,â€ â€œclarified,â€ or â€œcorrectedâ€ rather than rewriting history without a trace.

### 3.7 Shutdown and handoff

Close the session with:

- decisions accepted, deferred, rejected, and still open;
- files updated, versions, and delivery location;
- evidence gaps and assumptions needing validation;
- assigned follow-up actions and owners;
- the next-session starting point and required context.

No session may claim completion until the deliverable verification in [Artifact Delivery and Verification](ARTIFACT_DELIVERY_AND_VERIFICATION.md) is complete.

