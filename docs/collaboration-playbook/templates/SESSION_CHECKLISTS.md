# Session Checklists

## Facilitator checklist

### Before

- [ ] Identify objective, scope, roles, authority, GitHub repository/default branch, and delivery location.
- [ ] Mark supplied conversational context as trusted, untrusted, or to-be-verified.
- [ ] Locate the current baseline, changelog, ADR index, and handoff.

### During

- [ ] Separate observations, assumptions, ideas, recommendations, decisions, and actions.
- [ ] Ask for alternatives and material trade-offs.
- [ ] Assign stable IDs and evidence references for material items.
- [ ] Do not present an intended update as a completed file change.
- [ ] Confirm explicit decision authority before labeling anything accepted.

### At commit

- [ ] Update primary artifact, changelog, indexes, handoff, and ADRs as required.
- [ ] Validate links, IDs, and cross-document consistency.
- [ ] List actual files changed and validation results.
- [ ] Open or update a pull request; do not describe the change as baselined until it is merged.

### At closeout

- [ ] Provide decisions, open questions, evidence gaps, actions, and next step.
- [ ] Verify the actual delivery artifact and path.

## Sponsor/operator checklist

- [ ] State constraints, desired outcome, and decision authority.
- [ ] Correct misunderstandings promptly; specify whether the correction changes a decision.
- [ ] Explicitly accept, reject, or defer material recommendations.
- [ ] Request a documentation commit when persistence is required.
- [ ] Confirm receipt and accessibility of final artifacts.

## Document custodian checklist

- [ ] Ensure all requested files physically exist in the designated location.
- [ ] Work from a project-specific GitHub repository and use a working branch rather than treating a local folder as authoritative.
- [ ] Update `CHANGELOG.md` and ADRs as required.
- [ ] Package only verified content and include `MANIFEST.md`.
- [ ] Inspect the package after creation.
- [ ] Report paths and VCS IDs accurately; never infer them.
- [ ] Record the merged commit SHA in release packages and session closeout.

