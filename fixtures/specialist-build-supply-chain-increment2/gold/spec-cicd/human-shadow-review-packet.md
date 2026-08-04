# SPEC-CICD Deferred Human Shadow Review Packet

Reviewability: **ready_for_human_shadow_review**

Retained for consolidated end-of-program human review. Comparison-only; no admission, scheduling, report, deployment, or A100 authority.

## ITEM-0001 - observation

The release workflow pins release-please to an immutable commit while its tag job declares write-all permissions; the called publish workflow defines job-scoped permissions.

- `.github/workflows/tag-and-release.yaml` line 21: `    permissions: write-all`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/publish.yaml` line 30: `    permissions:`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/tag-and-release.yaml` line 30: `        uses: googleapis/release-please-action@45996ed1f6d02564a971a2fa1b5860e934307cf7 # v5.0.0`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0002 - finding

No completed pipeline run, produced artifact identity, attestation, promotion decision, failure recovery, or rollback event is admitted for this calibration slice.

- `.github/workflows/tag-and-release.yaml` line 21: `    permissions: write-all`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/publish.yaml` line 30: `    permissions:`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/tag-and-release.yaml` line 30: `        uses: googleapis/release-please-action@45996ed1f6d02564a971a2fa1b5860e934307cf7 # v5.0.0`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0003 - recommendation

Review and narrow the tag job permissions, then retain linked run, artifact, provenance, gate, promotion, and rollback evidence.

- `.github/workflows/tag-and-release.yaml` line 21: `    permissions: write-all`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/publish.yaml` line 30: `    permissions:`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/tag-and-release.yaml` line 30: `        uses: googleapis/release-please-action@45996ed1f6d02564a971a2fa1b5860e934307cf7 # v5.0.0`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0004 - unknown

Secret scope, runner isolation, actual permission use, repeatability, gate effectiveness, artifact provenance, promotion governance, and recovery behavior remain unknown without execution records.

- `.github/workflows/tag-and-release.yaml` line 21: `    permissions: write-all`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/publish.yaml` line 30: `    permissions:`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `.github/workflows/tag-and-release.yaml` line 30: `        uses: googleapis/release-please-action@45996ed1f6d02564a971a2fa1b5860e934307cf7 # v5.0.0`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

