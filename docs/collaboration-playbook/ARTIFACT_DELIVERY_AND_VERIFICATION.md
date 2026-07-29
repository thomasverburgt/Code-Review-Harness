# Artifact Delivery and Verification

## 1. Delivery principle

An artifact is delivered only when the recipient can locate, access, and verify the actual file. A prose statement that a file was created, an expired sandbox reference, or an untested path is not delivery.

## 2. Delivery procedure

1. Create files in the agreed repository or output directory.
2. Inspect the resulting file list and sizes.
3. Produce a package manifest containing file paths, size, and checksum where appropriate.
4. Create the ZIP from the verified package root.
5. Inspect the ZIP contents after creation.
6. Provide the recipient a stable, clickable repository/output link or an approved storage location.
7. Report the exact path, package name, and verification result.

## 3. ZIP manifest format

Include a `MANIFEST.md` in every delivered package:

| Field | Requirement |
| --- | --- |
| Package name and version | Required |
| Creation date | Required |
| Source root | Required |
| File inventory | Required |
| Integrity data | SHA-256 for the ZIP and optionally each file |
| Verification performed | Required |
| Known limitations | Required when applicable |

## 4. Verification checklist

- [ ] Required files exist at the stated paths.
- [ ] ZIP opens successfully.
- [ ] ZIP inventory matches `MANIFEST.md`.
- [ ] Markdown links are relative and resolve within the package where possible.
- [ ] No delivery link is claimed as verified unless it was opened or otherwise tested in the target interface.
- [ ] If interface limitations prevent testing, state that limitation plainly and provide a durable alternate location.

## 5. Failed delivery handling

If a recipient cannot access an artifact:

1. Do not claim it was delivered successfully.
2. Determine whether the failure is file creation, packaging, path, permission, expiration, or UI rendering.
3. Re-deliver through the agreed durable location.
4. Re-run package verification and report the corrected result.


