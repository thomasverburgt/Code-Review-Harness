# Report Governance and External Decision Reconciliation

ADR-0012 places governance around the completed report while leaving substantive authority outside the harness.

```text
accepted artifact chain
  -> immutable report package
  -> leadership review export (NOT APPROVED FOR DISTRIBUTION)
  -> external leadership authorization
  -> administrator records source-backed distribution attestation
  -> different verifier confirms bindings
  -> approved controlled export
  -> experts decide outside the harness
  -> administrator records source-backed expert decision
  -> different verifier confirms bindings
  -> derived reconciliation view (record-only)
```

`tools/report_governance_runtime.py` implements the reference boundary, and `tools/run_report_governance_reference.py` materializes its retained record chain. `tools/test_report_governance_runtime.py` checks deterministic packaging, controlled-export markings, role separation, exact item/source bindings, independent verification, immutable replay, mutation rejection, report preservation, and absence of external effects.

The authority registry at `appendices/governance/decision-authorities-0.1.0.json` contains synthetic test identities. Production identity mappings require an approved deployment policy. `approved_by` and `decided_by` describe the external authorities; `recorded_by` and `verified_by` are authenticated system actors. Those fields are not interchangeable.

The state machine at `orchestration/state-machines/report-governance.state-machine.json` is descriptive of immutable record state. State is derived from retained packages, exports, attestations, and verifications; no mutable approval flag is authoritative. A rejected or incomplete verification blocks progress, and no state transition mutates an external governance or deployment system.
