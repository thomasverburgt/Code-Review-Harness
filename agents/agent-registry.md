# Agent Registry

Each ID is stable. `baseline` means the contract was fully discussed; `seed` means it was named but needs a later domain-design increment.

| Agent ID | Agent | Status | Authoritative question |
|---|---|---|---|
| `SPC-SECRETS` | Secrets reviewer | baseline | Are secrets managed securely? |
| `SPC-SBOM` | Software composition and SBOM reviewer | baseline | Is inventory trustworthy and complete? |
| `SPC-DEPS` | Dependency reviewer | baseline | Is the dependency graph healthy and sustainable? |
| `SPC-SECURE-CODE` | Secure coding reviewer | baseline | Does code implement secure coding practices? |
| `SPC-SECURITY` | Security posture reviewer | seed | What is the integrated product security posture? |
| `SPC-CONTAINER` | Container/image security reviewer | baseline | Is the deployable image trustworthy and hardened? |
| `SPC-K8S-WORKLOAD` | Kubernetes workload security reviewer | baseline | Is the workload securely operated? |
| `SPC-K8S-PLATFORM` | Kubernetes platform security reviewer | baseline | Is shared platform/control-plane configuration secure? |
| `SPC-COMMS` | Workload communication security reviewer | baseline | Are service-to-service boundaries protected? |
| `SPC-IAC` | Infrastructure-as-code reviewer | baseline | Is desired infrastructure correctly and securely defined? |
| `SPC-CICD` | CI/CD pipeline reviewer | baseline | Does delivery produce trustworthy, repeatable, governable releases? |
| `SPC-OBS` | Observability reviewer | baseline | Can production behavior be understood? |
| `SPC-PERF` | Performance and scalability reviewer | baseline | Can objectives be met under expected load? |
| `SPC-FMECA` | Reliability, resilience, and FMECA reviewer | baseline | Can the system continue through failure? |
| `SPC-ARCH` | Architecture reviewer | baseline | Does implementation realize intended architecture? |
| `SPC-INTEROP` | Interoperability and integration reviewer | baseline | Can information and behavior exchange reliably? |
| `SPC-DATA` | Data architecture and information management reviewer | baseline | Is information governed and fit for mission? |
| `SPC-RISK` | Product risk reviewer | seed | What product-level risks require escalation? |
| `SPC-LINT` | Linter/code quality reviewer | seed | Does implementation meet defined quality rules? |
| `SPC-IO` | I/O and resource interaction reviewer | seed | Are storage and external I/O interactions safe and efficient? |
| `SPC-DIAGRAM` | Diagram and design-model reviewer | seed | Do diagrams faithfully represent implemented structure? |
| `SPC-RESEARCH` | Research/product-store updater | seed | What vetted external knowledge should enter the product store? |
| `PRD-SYNTH` | Product synthesis lead | planned | What is the coherent engineering state of this product? |
| `CAP-SYNTH` | Capability synthesis lead | planned | Do products collectively deliver the intended capability? |
| `ENT-SYNTH` | Enterprise synthesis lead | planned | What strategic posture and decisions follow from capability evidence? |
