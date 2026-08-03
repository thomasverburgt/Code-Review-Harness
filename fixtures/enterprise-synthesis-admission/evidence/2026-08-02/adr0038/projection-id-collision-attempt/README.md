# Projection identifier collision evidence

This retained development attempt demonstrates the immutable ledger rejecting a changed ENT-SYNTH projection that reused the earlier candidate identifier. The mixed top-level files and immutable ledger index are intentionally retained as failure evidence and must not be consumed as a valid candidate package. The corrected runtime derives candidate identity from the input-manifest hash, exact role hash, and projection version.
