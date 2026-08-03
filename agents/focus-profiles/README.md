# Agent Focus Profiles

Every canonical agent in [`agent-identities.json`](../agent-identities.json) has exactly one versioned focus profile in this directory. A focus profile is the machine-readable professional or control-plane lens that must govern the agent's prompt, evidence selection, rubric, compression, and downstream handoff.

The authoritative schema is [`agent-focus-profile.schema.json`](../../appendices/schemas/agent-focus-profile.schema.json). [`catalog.json`](catalog.json) binds every profile to its registered UUID, canonical designation, version, path, and SHA-256 hash.

## Required dispatch behavior

A focus-enforced dispatch pins the exact profile ID, version, and SHA-256. Missing profiles, mismatched hashes, registry disagreement, or source-specification drift fail closed before dispatch. Historical dispatches remain replayable with their original contracts; migration to focus-enforced dispatch is a separately tested compatibility change.

The effective prompt must contain the profile's mission, authoritative question, dimensions, evidence priorities, methods, required outputs, prohibited conclusions, and rubric checks. These elements are compression-protected. The harness may remove duplicated representation, but it may not omit the agent's analytical lens, evidence obligations, limitations, or authority boundary.

Deterministic roles such as `CAP-COORD` and `ENT-EVIDENCE` also receive profiles. For those roles the focus profile governs validation and routing behavior rather than model reasoning.

## Generation and validation

The profiles are generated deterministically from the identity registry, source specifications, and curated role focus maps:

```powershell
python tools/build_agent_focus_profiles.py
python tools/build_agent_focus_profiles.py --check
python -m unittest tools.test_agent_focus_profiles
```

Do not edit generated profile JSON directly. Change the source role specification or curated focus map, increment the profile version when meaning changes, regenerate, and retain regression evidence.
