#!/usr/bin/env python3
"""Build deterministic, role-specific focus profiles for every registered agent."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "agents" / "agent-identities.json"
OUTPUT = ROOT / "agents" / "focus-profiles"
PROFILE_SCHEMA = "../../appendices/schemas/agent-focus-profile.schema.json"
PROFILE_VERSION = "1.0.0"
LAYER_ORDER = ["specialist", "product", "capability", "enterprise", "work", "orchestration"]


DIMENSIONS = {
    "SPEC-SECRETS": ["secret lifecycle and approved storage", "credential exposure and leakage paths", "rotation, revocation, ownership, and blast radius"],
    "SPEC-SBOM": ["component inventory completeness", "component identity and provenance", "SBOM generation, currency, integrity, and policy conformance"],
    "SPEC-DEPS": ["dependency health and currency", "direct, transitive, and runtime coupling", "supportability, licensing, provenance, and replacement risk"],
    "SPEC-SECURE-CODE": ["implementation-level vulnerability patterns", "authentication, authorization, validation, and error handling", "secure coding controls and exploitability context"],
    "SPEC-SECURITY": ["integrated product attack surface", "security-control coverage and assumptions", "cross-specialist attack paths, conflicts, and escalation"],
    "SPEC-CONTAINER": ["image provenance and supply-chain trust", "runtime hardening and least privilege", "base-image currency, contents, signing, and vulnerability exposure"],
    "SPEC-K8S-WORKLOAD": ["workload identity, privilege, and security context", "resource, network, storage, and secret configuration", "availability, isolation, and workload-policy conformance"],
    "SPEC-K8S-PLATFORM": ["cluster control-plane and node security", "tenant isolation, admission, and policy enforcement", "platform identity, upgrades, audit, and shared-service risk"],
    "SPEC-COMMS": ["service communication boundaries and trust paths", "encryption, identity, authentication, and authorization in transit", "network policy, exposure, routing, and failure behavior"],
    "SPEC-IAC": ["desired-state correctness and reproducibility", "infrastructure security, policy, and privilege", "drift, state protection, module provenance, and change safety"],
    "SPEC-CICD": ["pipeline identity, permissions, and isolation", "build provenance, integrity, and artifact promotion", "secret handling, approvals, reproducibility, and rollback"],
    "SPEC-OBS": ["logging, metrics, tracing, and event coverage", "diagnostic quality, correlation, and alert effectiveness", "sensitive-data handling, retention, and operational usability"],
    "SPEC-PERF": ["performance objectives and workload assumptions", "latency, throughput, saturation, and scalability", "capacity evidence, bottlenecks, degradation, and efficiency"],
    "SPEC-FMECA": ["failure modes, causes, local effects, and end effects", "detection, controls, propagation, and criticality", "designed and demonstrated resilience, recovery, and mission impact"],
    "SPEC-ARCH": ["intended architecture and implemented structure", "component responsibilities, dependencies, and interfaces", "quality attributes, constraints, drift, and decision alignment"],
    "SPEC-INTEROP": ["interface contracts and compatibility", "data exchange, protocols, identity, timing, and failure semantics", "integration assumptions, versioning, and end-to-end interoperability"],
    "SPEC-DATA": ["data models, semantics, ownership, and lineage", "quality, lifecycle, protection, retention, and access", "integration, governance, residency, and recoverability"],
    "SPEC-RISK": ["product-scoped risk identification and causality", "likelihood, consequence, controls, and uncertainty", "risk dependencies, treatment options, and human escalation"],
    "SPEC-LINT": ["rule applicability and execution coverage", "code-quality, correctness, and maintainability signals", "false positives, suppressions, trends, and remediation evidence"],
    "SPEC-IO": ["external input and output boundaries", "filesystem, network, storage, device, and resource interactions", "validation, failure behavior, concurrency, and resource exhaustion"],
    "SPEC-DIAGRAM": ["model completeness and internal consistency", "diagram-to-design and design-to-implementation alignment", "interfaces, cardinality, behavior, notation, and unresolved ambiguity"],
    "SPEC-RESEARCH": ["source authority, provenance, and publication context", "claim applicability, freshness, and conflicting knowledge", "licensing, use constraints, and governed knowledge admission"],
    "PROD-SYNTH": ["complete specialist and product-domain inventory", "cross-domain product posture, conflicts, and confidence", "capability handoff, unresolved decisions, and advisory readiness"],
    "PROD-SEC": ["cross-domain product attack paths", "security-control coverage and evidence gaps", "product security findings, CAPA options, and escalation"],
    "PROD-ARCH": ["intended-versus-implemented architecture", "dependency, interface, data, reliability, and performance coherence", "architecture drift, quality attributes, and capability escalation"],
    "PROD-LINT": ["normalized rule and tool coverage", "systemic maintainability and quality trends", "false positives, technical-debt signals, and CAPA options"],
    "CAP-REQ": ["authoritative requirement population and provenance", "requirement-to-evidence traceability and satisfaction state", "coverage gaps, conflicts, change history, and acceptance requests"],
    "CAP-XPROD": ["cross-product interfaces and dependencies", "compatibility, shared assumptions, and integration contracts", "emergent gaps, ownership, and capability-level escalation"],
    "CAP-RISK": ["emergent capability risks across products", "risk aggregation without double counting", "controls, propagation, treatment options, and human risk authority"],
    "CAP-MISSION": ["end-to-end mission steps, actors, and success criteria", "product, service, data, control, and human handoffs", "breakpoints, degraded modes, failure effects, and mission evidence"],
    "CAP-HCD": ["operator and user journeys", "cognitive load, clarity, accessibility, and error recovery", "human-system handoffs, workload, resilience, and outcome evidence"],
    "CAP-ARCH": ["cross-product capability structure", "interfaces, shared services, dependencies, and architectural constraints", "mission alignment, quality attributes, drift, and architecture decisions"],
    "CAP-TRADE": ["decision alternatives and evaluation criteria", "evidence-backed benefits, costs, risks, and sensitivities", "assumptions, uncertainty, reversibility, and human selection"],
    "CAP-GOV": ["applicable obligations and authority", "cross-product controls, approvals, exceptions, and accountability", "governance gaps, conflicts, evidence, and decision requests"],
    "CAP-PROGRESS": ["declared capability outcomes and milestones", "evidence-backed convergence, blockers, and trends", "readiness limitations, dependencies, and decisions needed"],
    "CAP-COORD": ["exact expected and received input sets", "identity, schema, integrity, freshness, compatibility, and eligibility", "conflict preservation, deterministic indexing, and dispatch routing"],
    "CAP-SYNTH": ["exact coordinator-bound capability evidence", "cross-domain capability posture and sourced correlations", "conflicts, unknowns, confidence, decisions, and enterprise handoff"],
    "ENT-SYNTH": ["exact enterprise-domain set and evidence tiers", "cross-domain enterprise posture and traceable correlations", "disagreement, limitations, decisions, and leadership brief boundaries"],
    "ENT-SYSRISK": ["systemic and cross-capability risk classes", "risk propagation, concentration, common causes, and controls", "enterprise exposure, uncertainty, treatment options, and human risk decisions"],
    "ENT-GOV": ["enterprise obligations and source authority", "control applicability, coverage, exceptions, and approvals", "cross-capability governance gaps, conflicts, and human decisions"],
    "ENT-ARCH": ["system-of-systems topology and boundaries", "cross-capability dependencies, shared services, and failure propagation", "target-state coherence, architecture gaps, and decision requests"],
    "ENT-STRAT": ["owner-declared objectives and scoring method", "evidence-to-objective mapping and missingness", "confidence distribution, sensitivity, limitations, and strategic decision boundaries"],
    "ENT-EVIDENCE": ["enterprise input identity and provenance", "schema, integrity, lineage, freshness, compatibility, and tier", "completeness, conflict inventory, eligibility, and deterministic routing"],
    "ENT-PORTFOLIO": ["capability inventory and portfolio composition", "duplication, concentration, gaps, dependencies, and balance", "portfolio options, tradeoffs, uncertainty, and decision authority"],
    "ENT-ARCHSTRAT": ["current and target architecture states", "roadmap alignment, transition dependencies, and sequencing", "standards, investment constraints, uncertainty, and architecture authority"],
    "ENT-MATURITY": ["configuration-driven maturity model and scope", "evidence-backed level attainment and gaps", "confidence, comparability, improvement path, and prohibited unsupported scoring"],
    "ENT-TECHDEBT": ["enterprise technical-debt inventory and provenance", "impact, coupling, trajectory, and remediation dependencies", "priority options, uncertainty, and investment decision boundaries"],
    "ENT-MODERNIZE": ["modernization objectives and constraints", "investment options, benefits, risks, dependencies, and sequencing", "reversibility, evidence quality, uncertainty, and human selection"],
    "ENT-LEARN": ["harness quality, drift, and outcome measures", "prompt, model, rubric, and workflow performance", "feedback provenance, experiment validity, and governed improvement proposals"],
    "WORK-REVIEW": ["requesting criteria and bounded evidence set", "attributable observations, exceptions, and coverage", "quality checks, uncertainty, and return-manifest integrity"],
    "WORK-ANALYZE": ["pinned method, parameters, and assumptions", "reproducible relationships, calculations, and anomalies", "uncertainty, limitations, and method metadata"],
    "WORK-SUMMARIZE": ["declared consumer and compression constraints", "faithful source-linked summary and preserved conflicts", "omitted-detail manifest, uncertainty, and loss disclosure"],
    "ORCH-FANOUT": ["authorized schedule and independent work boundaries", "least-privilege inputs, credentials, tools, and execution envelopes", "retry, timeout, cancellation, telemetry, and immutable dispatch state"],
    "ORCH-FANIN": ["exact prerequisite artifact inventory", "identity, schema, integrity, lineage, freshness, compatibility, and completeness", "partial-input authority, conflicts, routing decisions, and audit events"],
    "ORCH-SCHED": ["trigger, policy, registry, and dependency resolution", "agent eligibility, version pins, gates, and acyclic scheduling", "resource constraints, concurrency groups, exclusions, and auditability"],
}


EVIDENCE = {
    "SPEC-SECRETS": ["source code, configuration, manifests, and examples", "secret stores, mounts, environment injection, and identity policy", "CI/CD, logs, tests, and credential-like detections"],
    "SPEC-SBOM": ["SBOMs, lockfiles, manifests, and build metadata", "artifact attestations, signatures, and provenance", "component policy, vulnerability, license, and lifecycle data"],
    "SPEC-DEPS": ["package manifests, lockfiles, module graphs, and resolved trees", "release, support, vulnerability, and license metadata", "runtime loading, vendoring, and replacement evidence"],
    "SPEC-SECURE-CODE": ["application source and generated code boundaries", "security tests, static analysis, and exploit evidence", "authentication, authorization, validation, cryptography, and error paths"],
    "SPEC-SECURITY": ["accepted security-specialist artifacts", "product architecture, threat context, and control requirements", "risk, exception, test, and unresolved-conflict records"],
    "SPEC-CONTAINER": ["Dockerfiles, image manifests, layers, and package inventories", "signatures, attestations, registries, and build provenance", "runtime configuration, vulnerability, and hardening evidence"],
    "SPEC-K8S-WORKLOAD": ["workload manifests, Helm values, and rendered resources", "RBAC, service accounts, policies, secrets, and storage", "runtime tests, events, and admission results"],
    "SPEC-K8S-PLATFORM": ["cluster configuration, node and control-plane settings", "admission, policy, RBAC, tenancy, and audit configuration", "upgrade, backup, runtime, and platform test evidence"],
    "SPEC-COMMS": ["service maps, network policies, ingress, egress, and routing", "TLS, certificate, identity, and authorization configuration", "protocol contracts, traffic tests, telemetry, and failure evidence"],
    "SPEC-IAC": ["infrastructure code, modules, plans, and state policy", "policy-as-code, identity, network, storage, and encryption controls", "drift, deployment, test, provenance, and rollback evidence"],
    "SPEC-CICD": ["pipeline definitions, runners, actions, and permissions", "build, test, sign, attest, publish, and promotion records", "secret scopes, approvals, logs, and rollback configuration"],
    "SPEC-OBS": ["logging, metric, tracing, dashboard, and alert configuration", "sample telemetry, incidents, tests, and runbooks", "retention, access, redaction, and operational objectives"],
    "SPEC-PERF": ["performance objectives, workload models, and test plans", "benchmark, profiling, saturation, and scaling results", "resource telemetry, topology, configuration, and capacity limits"],
    "SPEC-FMECA": ["functions, architecture, dependencies, and mission threads", "failure analyses, tests, incidents, and recovery exercises", "controls, monitoring, redundancy, and continuity evidence"],
    "SPEC-ARCH": ["architecture decisions, diagrams, interfaces, and constraints", "source structure, deployment topology, and dependency graphs", "quality-attribute tests, drift, and implementation evidence"],
    "SPEC-INTEROP": ["interface definitions, schemas, protocols, and versions", "integration tests, traces, errors, and compatibility matrices", "identity, timing, data, ownership, and operational agreements"],
    "SPEC-DATA": ["data models, schemas, catalogs, and lineage", "storage, access, protection, retention, and quality controls", "migration, integration, backup, recovery, and governance evidence"],
    "SPEC-RISK": ["accepted product findings and architecture context", "risk criteria, control evidence, tests, and incidents", "owners, dependencies, exceptions, decisions, and treatment records"],
    "SPEC-LINT": ["linter configuration, rule sets, outputs, and suppressions", "source population, test, defect, and change history", "quality thresholds, false-positive evidence, and remediation records"],
    "SPEC-IO": ["source paths that perform external I/O", "resource configuration, permissions, limits, and concurrency controls", "failure tests, telemetry, timeouts, retries, and cleanup behavior"],
    "SPEC-DIAGRAM": ["diagrams, models, legends, and source formats", "architecture decisions, interface contracts, and requirements", "implementation topology, tests, and model-drift evidence"],
    "SPEC-RESEARCH": ["primary publications and authoritative documentation", "publication metadata, revisions, licenses, and use constraints", "existing knowledge objects, conflicts, and applicability context"],
    "PROD-SYNTH": ["exact policy-required specialist and product-domain artifacts", "product baseline, architecture decisions, tests, and human source records", "completeness, conflict, confidence, and evidence-quality manifests"],
    "PROD-SEC": ["exact security-specialist artifact set", "product architecture, threat, control, and test context", "risk, exception, conflict, and human decision records"],
    "PROD-ARCH": ["architecture, dependency, interface, data, reliability, and performance artifacts", "approved intent, decisions, constraints, and implementation evidence", "tests, drift, conflicts, and capability assumptions"],
    "PROD-LINT": ["tool outputs, rule configurations, source coverage, and suppressions", "dependency, architecture, testing, and defect artifacts", "trend, false-positive, remediation, and debt evidence"],
    "CAP-REQ": ["authoritative requirement and response-commitment sources", "product artifacts, findings, tests, decisions, and source revisions", "requirement changes, acceptance records, conflicts, and gaps"],
    "CAP-XPROD": ["product artifacts and exact interface contracts", "dependency, compatibility, integration, and shared-service evidence", "ownership, test, conflict, and exception records"],
    "CAP-RISK": ["accepted product and capability-domain findings", "risk criteria, controls, dependencies, mission effects, and tests", "human risk decisions, exceptions, treatments, and unresolved conflicts"],
    "CAP-MISSION": ["mission scenarios, activities, actors, and success criteria", "product, interface, identity, data, control, and human-workflow artifacts", "end-to-end tests, telemetry, failure analysis, and degraded-mode evidence"],
    "CAP-HCD": ["user research, journeys, tasks, interfaces, and accessibility criteria", "training, procedures, workload, errors, and support evidence", "usability tests, telemetry, incidents, and human feedback"],
    "CAP-ARCH": ["product architecture artifacts and cross-product topology", "interfaces, shared services, constraints, decisions, and requirements", "quality-attribute, integration, failure, and drift evidence"],
    "CAP-TRADE": ["declared alternatives, criteria, weights, and authority", "cost, schedule, performance, risk, architecture, and mission evidence", "assumptions, sensitivity, uncertainty, and prior decisions"],
    "CAP-GOV": ["authoritative obligations, policies, and applicability decisions", "product controls, approvals, exceptions, and evidence locators", "ownership, conflict, audit, and decision records"],
    "CAP-PROGRESS": ["declared outcomes, milestones, plans, and acceptance criteria", "product and capability evidence, tests, blockers, and trends", "decisions, risks, dependencies, and readiness limitations"],
    "CAP-COORD": ["signed workflow, registry, expected-set policy, and dispatch", "exact capability-review artifacts and content hashes", "eligibility, freshness, compatibility, conflict, and partial-input records"],
    "CAP-SYNTH": ["hash-valid CAP-COORD manifest", "exact admitted capability-review artifacts", "evidence tiers, eligibility, conflicts, limitations, and human decisions"],
    "ENT-SYNTH": ["validated ENT-EVIDENCE synthesis manifest", "exact enterprise-domain artifacts and eligibility records", "domain limitations, source context, conflicts, and human decision requests"],
    "ENT-SYSRISK": ["validated capability-risk and enterprise evidence", "dependency, concentration, mission, control, and failure evidence", "risk criteria, human decisions, treatments, conflicts, and limitations"],
    "ENT-GOV": ["human-controlled governance-source manifest", "capability and enterprise control evidence", "applicability, approval, exception, authority, and audit records"],
    "ENT-ARCH": ["validated capability architecture and enterprise evidence", "system-of-systems topology, shared services, interfaces, and dependencies", "decisions, tests, failures, constraints, and domain limitations"],
    "ENT-STRAT": ["owner-declared objective and scoring-method manifests", "eligible capability and enterprise-domain evidence", "field locators, missingness, confidence formulas, limitations, and decisions"],
    "ENT-EVIDENCE": ["signed workflow, registry, policies, schemas, and authority context", "exact capability and enterprise input artifacts", "hashes, provenance, eligibility, freshness, compatibility, and conflicts"],
    "ENT-PORTFOLIO": ["capability catalog, costs, outcomes, risks, and dependencies", "investment, ownership, lifecycle, demand, and capacity evidence", "strategy, constraints, alternatives, and decision records"],
    "ENT-ARCHSTRAT": ["current and target architecture models", "capability roadmaps, standards, constraints, and dependencies", "investment plans, transition evidence, decisions, and risks"],
    "ENT-MATURITY": ["declared maturity model, criteria, and scope", "evidence artifacts mapped to model practices and outcomes", "assessment history, gaps, confidence, and human decisions"],
    "ENT-TECHDEBT": ["technical-debt records and source findings", "architecture, reliability, security, cost, and delivery evidence", "dependencies, trends, remediation estimates, and decisions"],
    "ENT-MODERNIZE": ["strategic objectives, current-state evidence, and constraints", "architecture, debt, portfolio, cost, risk, and capability artifacts", "alternatives, dependencies, assumptions, and investment decisions"],
    "ENT-LEARN": ["execution telemetry, quality results, and human dispositions", "prompt, model, rubric, tool, workflow, and environment versions", "outcomes, regressions, drift, incidents, and experiment records"],
    "WORK-REVIEW": ["exact work packet and requesting criteria", "bounded immutable evidence references", "scope, quality rules, exceptions, and output contract"],
    "WORK-ANALYZE": ["exact dataset and immutable references", "pinned method, parameters, assumptions, and thresholds", "calculation, anomaly, validation, and uncertainty evidence"],
    "WORK-SUMMARIZE": ["exact source artifacts and declared consumer", "compression constraints and required citations", "conflicts, limitations, omissions, and source structure"],
    "ORCH-FANOUT": ["authorized schedule and dependency state", "exact immutable input manifests and execution pins", "credential, network, filesystem, model, tool, retry, and timeout policies"],
    "ORCH-FANIN": ["exact execution results, artifacts, and manifests", "schemas, policies, gate criteria, and dependency state", "freshness, compatibility, conflicts, partial-input authority, and audit context"],
    "ORCH-SCHED": ["trigger, signed workflow, policy, and registry", "dependency, eligibility, authority, environment, and resource state", "contract, prompt, rubric, model, tool, schema, and version compatibility"],
}


LAYER_DEFAULTS = {
    "specialist": {
        "methods": ["Inspect only the declared eligible evidence population using the role's pinned domain criteria.", "Separate observations, assessments, findings, unknowns, and recommendations while preserving exact evidence locators."],
        "outputs": ["domain-specific observations and findings", "coverage, confidence, limitations, and evidence locators", "CAPA options and human decision requests"],
        "prohibitions": ["Do not declare the whole product safe, secure, compliant, reliable, ready, approved, or acceptable.", "Do not convert missing, inaccessible, or unreviewed evidence into no findings or effective controls."],
        "rubric": ["Every actionable claim is supported by an exact eligible evidence reference.", "The output applies the named domain dimensions rather than generic review language.", "Missing evidence, uncertainty, and authority boundaries remain explicit."],
    },
    "product": {
        "methods": ["Correlate only the exact specialist and product-domain artifacts named by the validated product manifest.", "Preserve child identifiers, meaning, confidence, evidence gaps, and disagreement in every derived product assertion."],
        "outputs": ["source-linked product correlations and posture", "conflicts, confidence reconciliation, limitations, and evidence gaps", "CAPA options, escalations, and capability handoff"],
        "prohibitions": ["Do not rewrite or suppress specialist conclusions or treat synthesis as new source evidence.", "Do not approve release, accept risk, grant an exception, close CAPA, or promote an artifact."],
        "rubric": ["Every derived assertion identifies its contributing immutable child records.", "Product-level conclusions remain within one declared product and preserve disagreement.", "Release-readiness content remains advisory and human controlled."],
    },
    "capability": {
        "methods": ["Evaluate only the declared capability scope and exact eligible product or capability-domain artifacts.", "Trace cross-product or cross-domain conclusions to contributors without double counting child evidence."],
        "outputs": ["source-linked capability findings, posture, or routing records", "coverage, conflicts, unknowns, confidence, and limitations", "human decisions and bounded enterprise handoff where authorized"],
        "prohibitions": ["Do not invent requirements, resolve human decisions, accept risk, approve readiness, or select a course of action.", "Do not promote incomplete, fixture-tier, stale, incompatible, or ineligible evidence."],
        "rubric": ["The output answers the role's capability-level question rather than repeating product summaries.", "Cross-product lineage and excluded evidence remain explicit.", "Missing requirements, products, domains, and mission evidence do not become positive claims."],
    },
    "enterprise": {
        "methods": ["Use the validated enterprise input manifest and preserve the independent authority of each admitted domain artifact.", "Distinguish preserved domain conclusions from traceable cross-domain observations and human-owned decisions."],
        "outputs": ["enterprise-domain or synthesis records with assertion-level provenance", "systemic conflicts, missingness, confidence, limitations, and uncertainty", "bounded leadership decision support and human decision requests"],
        "prohibitions": ["Do not accept enterprise risk, approve architecture, strategy, governance, investment, report distribution, release, or deployment.", "Do not average incompatible confidence, invent a composite, erase disagreement, or promote evidence tiers."],
        "rubric": ["Every enterprise claim is supported by exact admitted records and stays within the declared enterprise scope.", "Domain authority, evidence tiers, conflicts, and active limitations are preserved.", "Leadership support is advisory and cannot change scheduling, report, distribution, or production state."],
    },
    "work": {
        "methods": ["Execute only the requesting agent's exact work packet, pinned method, and output contract.", "Return attributable intermediate results with coverage, uncertainty, limitations, and source references."],
        "outputs": ["bounded intermediate work records", "method, coverage, uncertainty, limitations, and return manifest"],
        "prohibitions": ["Do not expand scope, acquire undeclared evidence, or alter the requesting method.", "Do not create an authoritative layer finding, choose a course of action, or imply approval."],
        "rubric": ["Every result is attributable to the requesting packet and exact source inputs.", "The worker preserves method, assumptions, omissions, and uncertainty.", "The return manifest prevents intermediate work from being mistaken for an authoritative finding."],
    },
    "orchestration": {
        "methods": ["Apply the signed workflow, registry, policy, state machine, and exact version pins deterministically.", "Emit immutable control-plane records for each validation, scheduling, dispatch, routing, retry, and failure effect."],
        "outputs": ["deterministic schedules, dispatches, gates, routing records, or audit events", "explicit rejection, retry, timeout, partial-input, and rollback state"],
        "prohibitions": ["Do not alter analytical conclusions, reconcile disagreement, waive a gate, or exercise engineering or governance authority.", "Do not broaden permissions, substitute identities, infer eligibility, or treat execution success as analytical acceptance."],
        "rubric": ["Every control action is traceable to exact signed policy, identity, input, and state.", "Least privilege, idempotency, failure isolation, and rollback behavior are explicit.", "Orchestration records no semantic conclusion beyond validation and routing authority."],
    },
}


ROLE_DEFAULTS = {
    "CAP-COORD": {
        "methods": ["Compare the declared and received input sets exactly and deterministically.", "Validate identity, schema, integrity, lineage, freshness, compatibility, eligibility, and partial-input authority without semantic synthesis."],
        "outputs": ["exact capability input manifest and indexed record inventory", "deterministic gate results, conflicts, limitations, and dispatch routing state"],
        "prohibitions": ["Do not generate a capability assessment, new risk, recommendation, or enterprise semantic handoff.", "Do not normalize disagreement, change confidence, settle a decision, or treat routing eligibility as human approval."],
        "rubric": ["Declared and received designations, artifact identifiers, and hashes agree exactly.", "Every rejection or routing result cites the exact failed or satisfied gate.", "The coordinator produces validation and routing metadata only and preserves human authority."],
    },
    "ENT-EVIDENCE": {
        "methods": ["Validate the exact enterprise input set deterministically against the signed workflow and policy.", "Check identity, schema, integrity, lineage, provenance, freshness, compatibility, tier, completeness, conflicts, and eligibility without analytical synthesis."],
        "outputs": ["validated enterprise input manifest and artifact inventory", "deterministic gate results, limitations, conflicts, eligibility, and routing state"],
        "prohibitions": ["Do not create an enterprise conclusion, risk, score, recommendation, or report narrative.", "Do not repair evidence, promote a tier, waive a human gate, or treat technical validity as semantic acceptance."],
        "rubric": ["Every admitted artifact and eligibility record matches its exact identifier and hash.", "Missing, stale, incompatible, revoked, or tier-confused inputs fail closed with explicit reasons.", "The gate emits only validation and routing facts and preserves downstream domain authority."],
    },
}


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def section(text: str, names: tuple[str, ...]) -> str | None:
    for name in names:
        match = re.search(rf"^## {re.escape(name)}\s*$\n+(.+?)(?=\n+## |\Z)", text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if match:
            for paragraph in re.split(r"\n\s*\n", match.group(1).strip()):
                cleaned = " ".join(line.strip(" -*`") for line in paragraph.splitlines() if line.strip())
                if cleaned:
                    return cleaned
    return None


def authoritative_question(text: str, display_name: str) -> str:
    match = re.search(r"\*\*Question:\*\*\s*(.+?)(?:\s*\*\*Boundary:|\n|$)", text)
    if match:
        return re.split(r"(?<=\?)\s+", match.group(1).strip())[0]
    answer = section(text, ("Authoritative question", "Authoritative Question", "Purpose", "North Star"))
    if answer:
        first = re.split(r"(?<=[.!?])\s+", answer)[0].strip()
        if first.endswith("?"):
            return first
        return f"What evidence-backed result must the {display_name} produce to satisfy this purpose: {first.rstrip('.')}?"
    return f"What bounded result must the {display_name} produce from its exact eligible inputs?"


def mission(question: str, display_name: str) -> str:
    stem = question.rstrip(".?")
    return f"Apply the {display_name} focus to determine: {stem}, using only exact eligible evidence and preserving uncertainty and human authority."


def profile(agent: dict, registry_version: str) -> dict:
    designation = agent["designation"]
    spec = ROOT / "agents" / agent["specification"]
    text = spec.read_text(encoding="utf-8")
    question = authoritative_question(text, agent["display_name"])
    defaults = ROLE_DEFAULTS.get(designation, LAYER_DEFAULTS[agent["layer"]])
    dimensions = DIMENSIONS[designation]
    evidence = EVIDENCE[designation]
    return {
        "$schema": PROFILE_SCHEMA,
        "schema_version": "1.0.0",
        "profile_id": f"FOCUS-{designation}",
        "profile_version": PROFILE_VERSION,
        "agent": {
            "agent_uuid": agent["agent_uuid"],
            "designation": designation,
            "display_name": agent["display_name"],
            "layer": agent["layer"],
            "contract_version": agent["contract_version"],
        },
        "source": {
            "identity_registry": "agents/agent-identities.json",
            "identity_registry_version": registry_version,
            "specification": f"agents/{agent['specification']}",
            "specification_sha256": sha256(spec),
        },
        "focus": {
            "mission": mission(question, agent["display_name"]),
            "authoritative_questions": [question],
            "dimensions": dimensions,
            "evidence_priorities": evidence,
            "required_methods": defaults["methods"] + [f"Apply the role-specific dimensions: {', '.join(dimensions)}."],
            "required_outputs": defaults["outputs"] + [f"role-specific coverage of {', '.join(dimensions)}"],
            "prohibited_conclusions": defaults["prohibitions"],
            "rubric_checks": defaults["rubric"] + [f"The result materially addresses {', '.join(dimensions)}."],
        },
        "prompt_binding": {
            "required_sections": ["mission", "authoritative_questions", "dimensions", "evidence_priorities", "required_methods", "required_outputs", "prohibited_conclusions", "rubric_checks"],
            "compression_protected_elements": ["authoritative_questions", "dimensions", "evidence_priorities", "prohibited_conclusions", "rubric_checks", "evidence locators", "active limitations", "human authority boundaries"],
            "missing_profile_effect": "fail_closed_before_dispatch",
            "hash_mismatch_effect": "fail_closed_before_dispatch",
        },
        "handoff": {
            "preserve": ["profile_id and version", "source designation", "source record identifiers", "evidence locators", "confidence meaning", "conflicts and unknowns", "active limitations", "human decision requests"],
            "consumer_rule": "A consumer may summarize this role's output only when the focus identity, source meaning, evidence, disagreement, limitations, and authority boundary remain traceable.",
        },
        "lifecycle": {
            "agent_status": agent["status"],
            "dispatch_requirement": "exact_profile_id_version_and_sha256_required",
            "change_control": "new_profile_version_and_regression_evidence_required",
        },
    }


def canonical(data: dict) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def render_outputs() -> dict[Path, str]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    agents = registry["agents"]
    expected = {agent["designation"] for agent in agents}
    if set(DIMENSIONS) != expected:
        raise ValueError(f"dimension map mismatch: missing={sorted(expected - set(DIMENSIONS))}, extra={sorted(set(DIMENSIONS) - expected)}")
    if set(EVIDENCE) != expected:
        raise ValueError(f"evidence map mismatch: missing={sorted(expected - set(EVIDENCE))}, extra={sorted(set(EVIDENCE) - expected)}")
    outputs: dict[Path, str] = {}
    entries = []
    ordered = sorted(agents, key=lambda item: (LAYER_ORDER.index(item["layer"]), item["designation"]))
    for agent in ordered:
        data = profile(agent, registry["registry_version"])
        rendered = canonical(data)
        path = OUTPUT / f"{agent['designation'].lower()}.json"
        outputs[path] = rendered
        entries.append({
            "agent_uuid": agent["agent_uuid"],
            "designation": agent["designation"],
            "layer": agent["layer"],
            "profile_id": data["profile_id"],
            "profile_version": PROFILE_VERSION,
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": "sha256:" + hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
        })
    catalog = {
        "schema_version": "1.0.0",
        "catalog_version": PROFILE_VERSION,
        "generated_from": ["agents/agent-identities.json", "agents/focus-profiles"],
        "profiles": entries,
    }
    outputs[OUTPUT / "catalog.json"] = canonical(catalog)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = render_outputs()
    stale = []
    for path, rendered in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered, encoding="utf-8", newline="\n")
    if stale:
        print("Stale focus profiles:")
        for path in stale:
            print(f"- {path}")
        return 1
    print(f"Agent focus profiles {'verified' if args.check else 'written'}: {len(outputs) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
