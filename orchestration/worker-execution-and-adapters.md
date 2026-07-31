# Worker Execution and Model/Tool Adapters

## Purpose

Increment 2 replaces adjudicated fixture artifacts one node at a time without allowing model output to bypass the contracts, fan-in gate, or persistent ledger. The reference implementation is `tools/worker_runtime.py`; it is a conformance boundary for later queue, worker, and serving technologies.

## Execution flow

```text
signed dispatch
  -> immutable job + idempotency binding
  -> atomic worker lease
  -> prompt/rubric/tool/model version resolution
  -> least-privilege evidence reads
  -> model adapter invocation
  -> optional deterministic envelope assembly
  -> universal + layer + role + full-chain fan-in validation
  -> accepted artifact, gate, telemetry, and result publication
  -> content-addressed ledger
```

An invalid, timed-out, exhausted, or cancelled generation may retain its result and telemetry but cannot publish an artifact or gate.

## Generation and rollback modes

The job selects one of three versioned modes:

- `full_artifact` retains the ADR-0010 behavior and is the compatibility/rollback path.
- `role_payload_v1` accepts only a compact analytical payload. The worker owns identity, artifact and execution metadata, scope, exact inputs and hashes, lineage links, consumers, human authority, lifecycle, integrity metadata, and the final envelope.
- `canonical_payload_v1` is the topology-reduced adoption path. The model emits one canonical analysis plus the irreducible role payload and, where necessary, a small irreducible layer context. A designation-specific, versioned, and hashed projection manifest derives the final layer extension without making decisions or inventing confidence. It is live-calibrated for all four review roles in the reference vertical. ENT-EVIDENCE is not model-generated; the harness builds it deterministically from the accepted CAP-RISK input before ENT-SYSRISK can run.

Both payload modes require exact generation-contract and assembler pins; canonical mode also requires the exact projection pin and hash. They retain the raw payload and an immutable assembly record separately from the final artifact. The final universal, layer, role, and semantic gates are identical in all modes. In canonical mode, the model reports omission and truncation counts while the worker derives the lifecycle limit flag, preventing a model-controlled or internally contradictory lifecycle transition.

Rollback pins new work to `full_artifact` and the last validated prompt/model manifest. Accepted history is never deleted or rewritten. New role-payload promotion pauses, leased work completes or cancels normally, and the ADR-0010 suite plus all fixture replacements must pass before dispatch resumes.

## Queue and idempotency

The filesystem queue uses immutable job files and atomic moves through `pending`, `leased`, `completed`, `failed`, and `cancelled` directories. An idempotency key is bound to one job ID and content hash. Repeating identical enqueue or processing is safe; reusing the key with changed content fails closed.

Cancellation is a separate immutable record. Retry attempts remain part of one job and one result, preventing duplicate artifact publication.

## Version resolution

Before model invocation, the worker resolves and verifies:

- registered UUID, designation, layer, and contract version;
- workflow and policy versions;
- the candidate prompt path, version, and SHA-256;
- rubric version and SHA-256;
- toolchain version and SHA-256;
- model provider, model ID, and version; and
- expected layer and role schemas.

The four candidate prompts are mechanically extracted from their reviewed Word copy boundaries and recorded in `appendices/prompt-templates/candidates/manifest.json`. Candidate status permits controlled testing, not production promotion.

## Adapter boundaries

`FixtureModelAdapter` returns adjudicated artifacts for deterministic conformance. `VLLMAdapter` implements the authenticated OpenAI-compatible `/v1/chat/completions` boundary with deterministic temperature, JSON output intent, bounded timeout, retryable HTTP/transport classification, and token telemetry.

The GX-10 test platform exposes `Qwen/Qwen3-32B-FP8` as `qwen3-32b` through a pinned NVIDIA vLLM container. The real API key remains inside the service environment. The protocol suite uses a local authenticated mock, and the platform gate separately performs a minimal live in-container inference smoke check without exporting the credential.

`LeastPrivilegeEvidenceAdapter` accepts only exact allowlisted repository paths, rejects traversal or undeclared references, and has no mutation methods. Tool availability does not expand job scope or agent authority.

## Fan-in and publication

Every candidate output is validated against:

- the universal artifact schema;
- the registered layer extension schema;
- the registered role schema;
- UUID/designation and contract pins;
- prompt, rubric, and toolchain pins; and
- the complete five-node reference artifact chain and human-decision request.

Only after those checks pass does the worker write an artifact and gate and bind them into the content-addressed ledger. This ordering makes the fan-in gate an executable publication boundary rather than advisory post-processing.

## Telemetry

Each result retains job, execution, dispatch, node, designation, worker, model, prompt, rubric, toolchain, generation mode, generation-contract hash/version, assembler lineage, and—when used—projection version/hash; attempt states; wall and CPU duration; token counts; estimated cost; and final status. Telemetry is retained for success, failure, and cancellation.

## Reference test command

Run only on NVIDIA DGX Spark or an approved equivalent:

```powershell
python tools/test_worker_runtime.py
```

The suite covers all four one-node replacement paths in both generation modes, deterministic assembly replay, harness-field override rejection, disclosed-truncation rejection, rollback compatibility, invalid-output rejection, ledger publication ordering, retry idempotency, timeout exhaustion, cancellation, least-privilege evidence access, telemetry lineage, vLLM authentication enforcement, and the OpenAI-compatible protocol.
