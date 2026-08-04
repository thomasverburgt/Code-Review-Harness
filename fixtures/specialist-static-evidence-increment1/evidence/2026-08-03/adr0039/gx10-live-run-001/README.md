# ADR-0039 Increment 1 GX-10 Live Calibration

- **Result:** all three candidates passed structural, focus, role-schema, projection, locator, packet, and comparison-only authority gates
- **Platform:** GX-10 / approved DGX Spark-equivalent, NVIDIA GB10
- **Model:** `qwen3-32b` (`Qwen/Qwen3-32B-FP8`)
- **Archive SHA-256:** `3dc42ec18f05aeede33385c413261f8bf99aa14053e9dd45d2a2a1f309dfa7ed`
- **Semantic state:** awaiting human review

| Candidate | Input tokens | Output tokens | Result |
|---|---:|---:|---|
| `SPEC-DEPS` | 3,131 | 624 | passed |
| `SPEC-SBOM` | 3,521 | 761 | passed |
| `SPEC-LINT` | 3,269 | 383 | passed |
| **Total** | **9,921** | **1,768** | **passed** |

The model emitted only the strict role payload. The harness separately produced the universal artifact envelope, integrity and lifecycle fields, locators, and human-review packet. Raw responses remain retained beside—not substituted for—the deterministic projection.

The results preserve the intended distinctions: dependency graph measures remain unmeasurable without a resolved graph; manifest declarations remain a partial inventory rather than a complete SBOM; and the lint quality gate remains `not_executed` without an admitted run result.

The temporary remote API-key copy was deleted before this package was created. Credentials are not present in the archive, logs, prompts, responses, or summaries.

No result is semantically accepted or candidate-complete. All candidates remain unscheduled, downstream-ineligible, report-ineligible, undeployed, and unauthorized for A100 production.

See [human-review-handoff.md](human-review-handoff.md) for reviewer instructions.
