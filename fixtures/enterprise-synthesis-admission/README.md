# ENT-SYNTH Candidate Admission Fixtures

ADR-0024 admits ENT-SYNTH as an isolated, comparison-only candidate. The synthesis-input manifest binds exact domain artifacts, hashes, tiers, compatibility, freshness, authority ownership, and permitted use. Source-role hashes and contribution maps prevent synthesis prose from changing domain authority.

The live GX-10 package intentionally mixes one accepted-live ENT-SYSRISK artifact with candidate-protocol ENT-ARCH, ENT-GOV, and ENT-STRAT artifacts. It proves mixed-tier handling only, not authoritative enterprise synthesis fitness. Production targets the A100 large cluster; testing runs on DGX Spark or an approved equivalent.

Rollback restores ENT-SYNTH to `planned` and removes candidate discovery while retaining all evidence. It does not change baseline roles, candidate roles, reports, human records, or deployment state.
