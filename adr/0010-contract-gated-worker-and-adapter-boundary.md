# ADR-0010: Contract-Gated Worker and Adapter Boundary

- **Status:** Accepted
- **Date:** 2026-07-31
- **Decision authority:** project maintainer
- **Owners:** harness orchestration and model platform
- **Scope:** Increment 2 reference implementation

## Decision record

Accepted by the project maintainer on 2026-07-31. The accepted boundary requires model and tool outputs to remain unpublished candidates until contract, semantic, authority, and fan-in validation pass.

## Context

The accepted persistent ledger can retain deterministic runs, but model and tool execution require queueing, version resolution, timeouts, retries, cancellation, least-privilege evidence access, telemetry, and an unambiguous publication boundary. Directly trusting model output would allow inference to bypass the schemas and human-authority invariants already proven by the vertical slice.

## Decision

Place every model or tool invocation behind an immutable worker job and signed dispatch. Resolve and hash all prompt, rubric, toolchain, schema, model, workflow, and identity versions before invocation. Bind idempotency at enqueue, lease atomically, classify retryable failures, and represent cancellation separately.

Treat every adapter output as an untrusted candidate. Validate the universal, layer, and role schemas, identity/version pins, and complete reference-chain semantics before publishing an artifact or gate. Persist accepted artifacts, gates, results, and all telemetry through the content-addressed ledger. Failed and cancelled executions retain telemetry but publish no artifact.

Use an authenticated OpenAI-compatible vLLM adapter as the production-facing model boundary and a deterministic fixture adapter as the conformance baseline. Use exact-path allowlists for the reference evidence adapter; later tool adapters must preserve the same least-privilege behavior.

## Alternatives considered

- Allowing model workers to publish directly was rejected because schema validation after publication is too late.
- Treating retries as new jobs was rejected because it risks duplicate artifacts and fragmented lineage.
- Embedding prompts in worker code was rejected because it breaks independent versioning and review.
- Sharing unrestricted repository access with every agent was rejected because tool availability would silently expand authority and evidence scope.
- Coupling the harness to one vLLM deployment was rejected; the adapter contract is stable while endpoint, model, container, and credentials remain environment configuration.

## Consequences

- Models and tools can evolve without changing orchestration or artifact semantics.
- Candidate prompts become executable, hash-pinned inputs while remaining unpromoted.
- A model response cannot become an accepted artifact without passing the existing contracts.
- Retry, timeout, cancellation, resource, token, and cost evidence remains tied to execution lineage.
- Production implementations must add durable queue leases, heartbeats, concurrency control, secret injection, and service authentication while matching this reference behavior.

## Validation

`tools/test_worker_runtime.py` exercises the four designed prompt roles one at a time, fan-in bypass rejection, ledger publication, retry/idempotency, timeout, cancellation, least-privilege evidence access, telemetry lineage, vLLM credential enforcement, and authenticated protocol behavior. The GX-10 platform also performs a minimal live `qwen3-32b` inference smoke check without exporting the service credential.

The 2026-07-31 GX-10 gate passed all four conformance suites and the live inference smoke check. Evidence is retained at `fixtures/vertical-risk-slice/evidence/gx10-increment2-conformance-2026-07-31.txt` with SHA-256 `17aa5a9bc90e4a7e8fc586e9af30d6f3092f529a3af5e03b6b12890fdcbfdef3`.

Four live prompt-calibration passes then confirmed that every malformed, schema-invalid, lineage-invalid, timed-out, or cancelled candidate failed closed and published no artifact. They also showed that full universal-artifact generation is not ready for promotion. Evidence is retained under `fixtures/vertical-risk-slice/evidence/live-prompt-calibration-2026-07-31/` and motivates proposed ADR-0011.

## Unresolved matters

- Production queue, lease, heartbeat, and worker autoscaling technologies.
- API-key or workload-identity integration for the A100 vLLM service.
- Model-specific generation-contract and deterministic assembly boundary; proposed in ADR-0011. Invalid output continues to fail closed.
- Token pricing and GPU resource-cost allocation.
- Successful live role-payload generation and assembled-artifact calibration before candidate prompt promotion.
