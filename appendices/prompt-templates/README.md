# Prompt Templates

Versioned prompt templates and prompt-contract examples are maintained here.

`candidates/` contains versioned prompt candidates. The original four are mechanically extracted copy boundaries from reviewed prompt-design Word documents. `PROD-SYNTH`, `CAP-SYNTH`, `CAP-REQ`, `ENT-ARCH`, `ENT-GOV`, `ENT-STRAT`, and `ENT-SYNTH` are contract-derived admission candidates whose sources are their registered agent specifications. `candidates/manifest.json` pins each source, version, status, path, and SHA-256 hash. Candidate status permits evaluation but does not authorize baseline scheduling or production promotion.

Regenerate the document-derived candidate files after a reviewed Word-document change with:

```powershell
python tools/export_candidate_prompts.py
```
