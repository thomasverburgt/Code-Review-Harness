# Tool Manifests

The ADR-0039 Increment 1 static-evidence manifests grant each specialist only its declared read-only evidence readers and locator tool. Network, secret, mutation, and autofix access remain denied unless an exact later manifest separately admits them.

Tool manifests identify the bounded toolchain available to an execution. They record versions and allowed capabilities so retained results can be interpreted and replayed without assuming an unconstrained environment.
ADR-0039 Increment 2 adds non-mutating, no-cloud, no-registry, no-pipeline-execution tool policies for `SPEC-CONTAINER`, `SPEC-CICD`, and `SPEC-IAC` candidate calibration.
