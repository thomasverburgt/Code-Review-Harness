# CAP-REQ Candidate Admission Evidence

ADR-0019 evidence retains immutable requirement-source manifests, exact evidence locators, zero-population semantics, candidate artifacts, negative tests, GX-10 calibration, and the pending human requirements-acceptance boundary. No files in `uds-core` are modified and CAP-SYNTH remains unscheduled.

ADR-0019 passed the structural validator and all 55 then-current tests locally and on GX-10. The live Qwen3-32B result correctly makes no satisfaction claim because the bounded source manifest contains no authoritative requirement. Technical validity does not constitute human requirements acceptance.

ADR-0020 passed the expanded structural validator and all 64 tests locally and on GX-10. Its immutable external-review packet received an explicit `accept_review_as_complete` response from `thomasverburgt` as `requirements-acceptance-authority`. The response is recorded but not yet independently verified, so accepted-input eligibility remains fail-closed and CAP-SYNTH remains unscheduled.
