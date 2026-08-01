# Deployment

Runtime and platform deployment architecture is maintained here, including Kubernetes topology, serving infrastructure, storage, networking, capacity, operations, and environment promotion.

## Environment baseline

- **Large-cluster production deployment:** NVIDIA A100 GPU infrastructure.
- **Test execution:** NVIDIA DGX Spark or an approved equivalent platform.
- **Promotion boundary:** test artifacts may be promoted from DGX Spark-equivalent environments to the A100 cluster only when model, prompt, contract, schema, policy, tool, container, and configuration versions remain pinned and traceable.
- **Production verification:** the A100 environment receives deployment smoke checks, health checks, configuration verification, and operational monitoring. Development, regression, calibration, resilience, security, rollback, and performance test suites execute on DGX Spark or an approved equivalent rather than consuming the production cluster.

An equivalent test platform must support the required CUDA and container runtime, execute the selected test model or an explicitly documented scaled test configuration, preserve the same harness interfaces and deterministic controls, and emit comparable execution and resource telemetry. Results derived from a scaled configuration must be labeled and must not be represented as A100 capacity evidence.

- [A100 Large-Cluster Deployment](a100-large-cluster/README.md)
- [ADR 0008: A100 Production and DGX Spark Test Baseline](../adr/0008-a100-production-dgx-spark-test-baseline.md)
