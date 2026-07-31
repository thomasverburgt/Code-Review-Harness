# ADR-0008: A100 Production and DGX Spark Test Baseline

- Status: accepted
- Date: 2026-07-31
- Decision authority: project maintainer
- Owners: platform architecture and harness operations
- Supersedes: prior planning references to DGX H100 as the production deployment target
- Superseded by:

## Context

The architecture library previously named DGX H100 as the future production deployment target but did not define a separate test platform or a promotion boundary. The intended operating model is now an NVIDIA A100 large cluster for production and NVIDIA DGX Spark, or an approved equivalent, for all test execution. The repository needs one consistent rule for deployment design, test evidence, environment-specific configuration, and promotion.

## Evidence

- The harness already requires pinned prompts, contracts, schemas, policies, models, tools, immutable evidence, deterministic replay, and human promotion authority.
- Production GPU capacity should remain isolated from development and regression workloads.
- DGX Spark and equivalent systems can validate harness behavior and model quality, but hardware-sensitive capacity results do not automatically represent A100 cluster performance.
- Supported deployment models are material architecture decisions under `GOVERNANCE.md`.

## Decision

The large-cluster production target is NVIDIA A100 GPU infrastructure running the approved Kubernetes and model-serving topology.

All development, regression, calibration, integration, security, resilience, rollback, and performance test suites execute on NVIDIA DGX Spark or an approved equivalent platform. The production A100 cluster is limited to deployment smoke checks, health checks, configuration verification, and operational monitoring necessary to verify release health; it is not the general test environment.

An equivalent test platform is approved only when it supports the required CUDA and container stack, can execute the selected test model or an explicitly documented scaled configuration, preserves the same harness contracts and deterministic controls, and emits normalized telemetry and immutable test evidence.

Promotion must preserve pinned software and artifact versions, identify the test platform and workload scale, retain environment-specific configuration deltas, and record the named human authority. Hardware- or scale-sensitive results must be labeled. Scaled test results must not be described as measured A100 production capacity.

## Alternatives considered

- **Retain DGX H100 as production:** rejected because it does not match the selected large-cluster target.
- **Use the A100 production cluster for all testing:** rejected because it mixes production capacity with development workloads and weakens environment separation.
- **Permit any GPU workstation as an equivalent:** rejected because equivalence without a compatibility and evidence envelope would make results non-comparable.
- **Require identical hardware for test and production:** rejected because the chosen operating model intentionally uses DGX Spark-class systems for testing and controls the difference through pinned interfaces, explicit scaling, and promotion evidence.

## Consequences

- Deployment designs, capacity planning, Kubernetes topology, and production operations target A100 GPUs.
- Test automation, gold-package evaluation, prompt and model calibration, failure injection, and performance characterization target DGX Spark or an approved equivalent.
- Hardware-sensitive configuration becomes explicit, versioned input rather than an undocumented environmental assumption.
- Functional and quality evidence can be promoted when the compatibility envelope is preserved, while capacity claims require clear modeling and qualification.
- The platform team must maintain normalized telemetry and document scaled tests, configuration deltas, and limitations.

## Traceability

- `deployment/README.md`
- `deployment/a100-large-cluster/README.md`
- `planning/architecture-package-roadmap.md`
- `planning/today-executable-vertical-slice.md`
- `planning/post-vertical-slice-sequence.md`
- `GOVERNANCE.md`

## Validation

- Repository documentation contains no active DGX H100 deployment references.
- Every deployment plan identifies A100 as the large-cluster production target.
- Every test plan identifies DGX Spark or an approved equivalent and records the platform, configuration, and scale.
- Promotion records preserve immutable test evidence, version pins, configuration deltas, limitations, and human authorization.
- Deployment smoke and health checks verify A100 release health without converting the production cluster into the general test environment.

## Unresolved matters

- Exact A100 cluster size, GPU form factor, networking, storage, and high-availability topology.
- Approved DGX Spark-equivalent platform list and the authority that maintains it.
- Model-specific scale factors and the method used to project DGX Spark-equivalent measurements to A100 capacity plans.
- Production SLOs, workload envelope, and capacity headroom.
