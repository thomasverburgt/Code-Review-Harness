# Prompt Templates

Versioned prompt templates and prompt-contract examples are maintained here.

`candidates/` contains mechanically extracted copy boundaries from the four reviewed prompt-design Word documents. `candidates/manifest.json` pins each source, version, status, path, and SHA-256 hash. Candidate status permits Increment 2 evaluation but does not authorize production promotion.

Regenerate the candidate files after a reviewed Word-document change with:

```powershell
python tools/export_candidate_prompts.py
```
