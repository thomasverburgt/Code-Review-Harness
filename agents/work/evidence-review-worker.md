# WORK-REVIEW: Evidence Review Worker

- UUID: `bd6f200e-e01e-4025-8ef3-be63c511f54e`
- Layer: work
- Status: planned
- Contract: [Work Agent Contract](../../contracts/work-agent-contract.md)

## Purpose

Apply a requesting agent's pinned criteria to a bounded immutable input set.

## Inputs and outputs

Consumes an exact work packet, criteria, evidence references, scope, and output contract. Produces attributable observations, coverage, exceptions, quality checks, uncertainty, and a return manifest for the requesting agent.

## Boundaries

Do not expand scope, acquire additional evidence, create an authoritative layer finding, approve a result, or retain undeclared credentials. The requesting reviewer must adopt any result with provenance.

