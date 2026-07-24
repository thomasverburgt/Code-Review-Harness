# Session Templates

## Startup record

```markdown
# Session: <title>

- Date/time:
- Sponsor/operator:
- Facilitator/design partner:
- Decision authority:
- Document custodian:
- Objective:
- In scope:
- Out of scope:
- Definition of done:
- Authoritative repository and branch/version:
- GitHub repository URL and default branch:
- Working branch and pull request (when created):
- Documentation root:
- Delivery/output location:
- Source material and trust status:
- Known assumptions:
- Required decisions:
```

## Recommendation record

```markdown
### REC-<id>: <short title>

- Decision question:
- Proposal:
- Evidence: [EVD-...]
- Assumptions:
- Alternatives considered:
- Trade-offs and risks:
- Impact scope:
- Reversibility:
- Acceptance criteria:
- Validation method:
- Owner:
- Decision authority:
- Status: proposed | accepted | rejected | deferred
```

## Commit record

```markdown
### DOC-<id>: Documentation commit

- Triggering decision(s):
- Files created/updated:
- ADR(s) created/updated:
- Changelog entry:
- Version change:
- Validation performed:
- Delivery artifact and manifest:
- VCS commit ID (only if actually created):
- Pull request URL/status and merged commit SHA (when merged):
- Verified by:
- Status: complete | blocked
```

## Session closeout / handoff

```markdown
# Session Closeout: <title>

## Accepted decisions
- DEC-...:

## Deferred or open questions
- Q-... | owner | trigger/date:

## Assumptions and evidence gaps
- ASM-/EVD-...:

## Documentation and delivery
- Version:
- Files updated:
- ADRs:
- Package/location:
- Verification result:

## Next session
- Starting point:
- Required source material:
- Recommended first action:
```

