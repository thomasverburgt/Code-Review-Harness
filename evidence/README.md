# Retained Evidence

This is the canonical root for future immutable execution, review, response, verification, and calibration packages.

```text
evidence/YYYY-MM-DD/adrNNNN/<scenario>/<run-id>/
```

Every package must contain or reference an evidence manifest identifying source revision, environment, artifact hashes, authority state, retention class, and supersession. Production targets the A100 large cluster; test and calibration evidence identifies DGX Spark or an approved equivalent and records its limitations.

Existing evidence remains under `fixtures/*/evidence` as an immutable legacy layout. [`legacy-catalog.json`](legacy-catalog.json) records an inventory hash for each root, and [`legacy-path-map.json`](legacy-path-map.json) records its future canonical prefix and `indexed_in_place` treatment. These catalogs do not move, rewrite, or supersede the evidence.

