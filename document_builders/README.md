# Controlled Document Builders

These tracked Python modules generate the four prompt-design DOCX deliverables. They require Python 3 and the pinned dependency in [`requirements-docs.txt`](../requirements-docs.txt).

Run from the repository root:

```text
python -m document_builders.build_spec_secrets_prompt_design
python -m document_builders.build_prod_sec_prompt_design
python -m document_builders.build_cap_risk_prompt_design
python -m document_builders.build_ent_sysrisk_prompt_design
```

The builders write to `deliverables`. Generation does not approve a document for leadership review or distribution. After generation, render and visually inspect the DOCX, update its release manifest, and obtain the applicable human lifecycle decision.

`python tools/verify_document_builders.py` rebuilds all four files under ignored `_runs` storage and compares their normalized DOCX package contents to the controlled deliverables.
