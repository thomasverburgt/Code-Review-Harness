# A100 Large-Cluster Deployment

This area defines the vLLM-on-Kubernetes production deployment for NVIDIA A100 GPU capacity: GPU allocation, model placement and parallelism, queues, storage, networking, scaling, observability, resilience, and throughput estimates.

## Environment separation

The large A100 cluster is the production serving target. All development, regression, calibration, integration, security, resilience, rollback, and performance test suites execute on NVIDIA DGX Spark or an approved equivalent platform. The production cluster is limited to deployment smoke checks, health checks, configuration verification, and operational monitoring needed to establish that the deployed release is healthy.

Test and production environments must use the same versioned harness interfaces: agent identities, prompts, contracts, schemas, rubrics, policies, tool adapters, container images, model configuration, and audit formats. Hardware-sensitive settings may vary only through explicit environment configuration that is retained with each run.

## Equivalent test-platform criteria

An approved DGX Spark equivalent must:

- support the required CUDA, container, orchestration, model-serving, and tool-adapter stack;
- provide enough accelerator memory for the selected test model or use an explicitly documented scaled model or workload;
- preserve contract validation, orchestration state transitions, evidence handling, security boundaries, and deterministic replay behavior;
- expose execution, memory, latency, throughput, error, and resource telemetry in the same normalized evidence format; and
- identify every hardware- or scale-dependent limitation in the test report.

Functional and quality results may transfer when the pinned software and configuration envelope is unchanged. Capacity projections must account for the hardware difference, and scaled DGX Spark-equivalent results must never be labeled as measured A100 production capacity.

## Promotion evidence

Every promoted release must retain:

- the test-platform identity and configuration;
- test model and workload scale;
- immutable test results and adjudicated exceptions;
- the exact production image and version pins;
- the environment-specific configuration delta; and
- the named human promotion authority and decision record.

See [ADR 0008](../../adr/0008-a100-production-dgx-spark-test-baseline.md) for the governing decision.
