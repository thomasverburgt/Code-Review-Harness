# PROD-SYNTH Candidate Admission Evidence

This directory retains the deterministic reference package and complete local/GX-10 conformance evidence for the first Increment 5 slice under proposed ADR-0014.

The candidate is intentionally not scheduled in `WF-VERTICAL-RISK-001`. The accepted `PROD-SEC -> CAP-RISK` route remains the rollback path until a later decision approves promotion and scheduling.

## Results

- The complete seven-gate local suite passed.
- The complete seven-gate GX-10/DGX Spark-equivalent suite passed on `aarch64`.
- Prompt SHA-256, candidate identity, universal/product/role schemas, exact child inventory, preserved finding/evidence lineage, deterministic replay, and capability compatibility passed.
- All seven declared negative admission cases failed closed.
- `FINDING-PRODSEC-001` and `FINDING-SECRET-001` survive the `PROD-SYNTH -> CAP-RISK` handoff unchanged.
- `PROD-SYNTH` remains unscheduled and the baseline workflow remains unchanged.

Retained hashes:

- `gx10-product-synth-conformance.txt`: `d7aeaf797aa9198ddb3eef0cee0f2789dd99146defecc977ebc15dab37ee2ca2`
- `gx10-product-synth-reference.tar.gz`: `cd869005725945702d792c0fc19a99f79bb8270f4a91a06cceab1e8e184ee371`
