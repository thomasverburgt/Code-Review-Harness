# Contract Catalog

| Contract class | Purpose | Producer | Primary consumers |
|---|---|---|---|
| Universal agent | Identity, provenance, review, confidence, authority, and integrity envelope | Every agent | Validators and every downstream consumer |
| Specialist agent | Bounded product-domain assessment | `SPEC-*` | Product agents |
| Product agent | Product-level correlation and synthesis | `PROD-*` | Capability agents |
| Capability agent | Cross-product mission and readiness assessment | `CAP-*` | Enterprise agents |
| Enterprise agent | System-of-systems decision support | `ENT-*` | Human decision authorities |
| Work agent | Reusable bounded evidence processing | `WORK-*` | Requesting review agents |
| Orchestration agent | Scheduling, dispatch, aggregation, and routing | `ORCH-*` | Workflow engine and audit |
| Evidence | Immutable observable source | Collectors and every reviewer | All agents |
| Finding/CAPA | Deficiency, RCA, remediation, validation | Every reviewer | Product/capability risk and governance |
| Pattern/Insight | Good practice and neutral learning | Every reviewer | Architecture, maturity, learning agents |

Contract extensions are additive. A breaking semantic change requires a major version and an ADR.
