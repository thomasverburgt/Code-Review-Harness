# GX-10 Live Prompt Calibration — 2026-07-31

## Scope

This package records live `qwen3-32b` calibration of SPEC-SECRETS, PROD-SEC, CAP-RISK, and ENT-SYSRISK through the accepted worker boundary. SPEC-SECRETS used a read-only shallow clone of `defenseunicorns/uds-core` at revision `329ade01852f9e570d31cb7b19d9979152938c17`. The clone remained clean and received no branch, commit, push, issue, or pull-request operation.

The evidence builder inspected 1,172 tracked files, scanned 1,168 text files offline, and retained 44 locator-only heuristic findings. Matched values and source-line content were not retained. No candidate artifact passed fan-in or entered the ledger. No model credential was exported into evidence.

## Results

### Pass 1 — unconstrained baseline

- SPEC-SECRETS: vLLM rejected the oversized request envelope with HTTP 400.
- PROD-SEC: failed immutable upstream lineage/hash validation.
- CAP-RISK: failed because required CAP-RISK role fields were absent.
- ENT-SYSRISK: placed validation/gate fields in the role payload and failed its role schema.

### Pass 2 — reduced evidence and explicit bindings

- SPEC-SECRETS: reached the 4,096-token cap and returned truncated JSON.
- PROD-SEC: exact bindings corrected lineage; the product extension then omitted required `coverage`.
- CAP-RISK: repeated the missing role-payload fields despite explicit placement guidance.
- ENT-SYSRISK: omitted required universal fields.

### Pass 3 — composed strict JSON Schema

- SPEC-SECRETS: exceeded the 900-second worker timeout.
- The other roles were rejected because the vLLM grammar engine does not implement `uniqueItems`.

### Pass 4 — grammar-compatible schema with bounded arrays

- SPEC-SECRETS: again exceeded the 900-second worker timeout.
- Remaining roles were cancelled after the repeated timeout established that full universal-schema constrained generation was not viable for routine GX-10 calibration.

## Conclusion

The worker, validation, telemetry, failure, and publication controls operated correctly: every invalid, malformed, rejected, timed-out, or cancelled candidate failed closed and published no artifact.

The prompts are not ready for promotion. The primary design problem is asking the model to generate the complete universal envelope. The worker should deterministically assemble identity, version pins, input hashes, lineage, lifecycle, routing, consumers, authority, timestamps, and integrity metadata. Model generation should be limited to a compact, versioned, role-specific analytical payload that is embedded and then evaluated by the unchanged authoritative schemas and semantic fan-in gate.

## Evidence integrity

- `pass1-output.tar.gz`: SHA-256 `096486f0262f3decc311ded952b2bbbe5fc278fbeb76e1e6bf7edb5f5eb68c21`
- `pass2-output.tar.gz`: SHA-256 `f88323bc60fd1e0704111827662d18970d5c16b16af351b07e4ca3a1ba98d36a`
- `pass3-output.tar.gz`: SHA-256 `782135cf56bb1eed4379814f4d70051353e2f3e06cfef4802647c109d4627763`
- `pass4-output-partial.tar.gz`: SHA-256 `8388660580689cc3c62f9c176805e686b18bef7c03d174746fb3946052f8fb87`

The archives contain worker results, telemetry, raw responses where received, and ledger state. Raw responses were produced only from controlled or redacted test evidence.
