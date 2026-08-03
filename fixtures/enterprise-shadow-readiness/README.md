# Enterprise Shadow Readiness

ADR-0025 implements a fail-closed readiness gate before any enterprise candidate shadow integration. The manifest binds every prerequisite to an exact retained packet or evidence archive and rejects missing, duplicate, mutated, promoted, or partially satisfied prerequisites.

Current state: `blocked`. ADR-0016 semantic adjudication awaits an external human decision and project-owner finalization. The ADR-0020 requirements response is owner-finalized under ADR-0033, and its exact CAP-REQ artifact is eligible for accepted capability input. ENT-ARCH, ENT-GOV, ENT-STRAT, and ENT-SYNTH have protocol calibration evidence but not accepted-live multi-domain semantic evaluations. No candidate is scheduled. See the living [`current-state` projection](../../status/current-state.md); retained readiness manifests remain creation-time snapshots.

Rollback disables candidate discovery, discards derived shadow state, retains immutable evidence, and continues the accepted `ENT-EVIDENCE -> ENT-SYSRISK` route. Production targets the A100 large cluster; tests run on DGX Spark or an approved equivalent.
