# Increment 4 Evidence Localization

This directory retains local and GX-10/DGX Spark-equivalent conformance evidence for the reproducible evidence-locator and expert-review-packet boundary proposed in ADR-0013.

The reference run is bound to report package `43ac6c58-2d9f-5465-91a5-b7ac00e75e8f` and preserves its original package hash. The generated annex identifies the exact `uds-core` repository revision, file, line, redacted context, and fingerprint without embedding the matched value.

## Results

- The complete six-gate local suite passed.
- The complete six-gate GX-10 suite passed on `aarch64` with Python 3.12.3.
- All seven actionable report items resolved to exact locators and the derived packet state was `ready_for_expert_review`.
- The original report package hash remained `sha256:430233c423d65642bdebde1d9217517d7023bc2ddcc5dbbf89ebe361d9ceeb4a`.
- `gx10-evidence-locator-conformance.txt` SHA-256: `0233e5050d0e0ec2ef9e587806b616aed0e4618016ddbc27336e35d81e813974`.
- `gx10-evidence-locator-reference.tar.gz` SHA-256: `be6df90ae6dda3f1a573c44da09f855f9d22885df4211d0b842936cd96e64481`.

`reference-run/expert-evidence-annex.md` is the human-readable reviewer view. The JSON packet, binding manifest, and locator records are the machine-verifiable source of that view.
