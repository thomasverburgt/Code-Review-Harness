# Repository Migration and Retirement

This directory records reversible organization migrations and the evidence required before legacy removal.

[`retirement-readiness.json`](retirement-readiness.json) is generated from repository state and explicit governance gates. `removal_authorized: false` means no listed compatibility path may be deleted merely to simplify the tree. Training and QA paths are retained repository content, not retirement candidates; changing that decision requires a separate ADR and explicit maintainer approval.

The retirement sequence is:

1. observe one release using the new canonical path;
2. run complete local and GX-10 regression and replay;
3. record old-to-new paths, hashes, and rollback;
4. obtain human approval for the removal commit;
5. retain the pre-migration tag and archive evidence.
