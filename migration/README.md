# Repository Migration and Retirement

This directory records reversible organization migrations and the evidence required before legacy removal.

[`retirement-readiness.json`](retirement-readiness.json) is generated from repository state and explicit governance gates. `removal_authorized: false` means no listed compatibility, evidence, or training path may be deleted merely to simplify the tree.

The retirement sequence is:

1. observe one release using the new canonical path;
2. select and verify any required external archive;
3. run complete local and GX-10 regression and replay;
4. record old-to-new paths, hashes, and rollback;
5. obtain human approval for the removal commit;
6. retain the pre-migration tag and archive evidence.

