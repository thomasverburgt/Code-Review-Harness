COMPANION REFERENCE · 2 AUGUST 2026

# Code Review Harness

_Leadership and Technical Frequently Asked Questions_

A detailed guide to the purpose, mechanics, governance, performance, and philosophy of a human-controlled multi-agent review system.

> **How to use this document**
> Read Questions 1–7 for an executive orientation, Questions 8–15 for implementation mechanics, Questions 16–22 for governance and operations, and Questions 23–30 for the deeper ideas that shape the architecture.

| Audience | Use |
| --- | --- |
| Senior leadership | Understand what the harness can establish, what remains human, and what evidence is required before production authorization. |
| Technical leadership | Understand prompt construction, contracts, evidence flow, orchestration, token control, state, and rollback. |
| Human reviewers | Understand how to evaluate findings, limitations, disagreement, confidence, and source evidence. |

NAVIGATION

## Questions by theme

| Theme | Questions |
| --- | --- |
| Purpose and architecture | 1–7: purpose, outputs, layers, harness/agent boundary, coordinator, state machine, shadow integration |
| Prompts, focus, and context | 8–15: prompt derivation, focus profiles, compression, schemas, one-agent-per-role, model behavior, invalid output |
| Evidence, governance, and operations | 16–22: traceability, insufficient evidence, semantic review, human authority, immutability, rollback, performance |
| Philosophy and leadership | 23–30: knowledge, disagreement, intelligence versus authority, trust, automation bias, correctness, value, production readiness |

### Core vocabulary

| Term | Meaning |
| --- | --- |
| Artifact | An immutable, content-addressed input, output, decision, packet, manifest, or state record. |
| Contract | A machine-checkable statement of responsibility, evidence, authority, lifecycle, and handoff obligations. |
| Candidate | An implemented role or workflow that is being evaluated but is not part of the accepted scheduled baseline. |
| Eligible | Permitted for one exact next use; not automatically scheduled, approved, released, or deployed. |
| Shadow | Executed alongside the accepted route with no authoritative effect. |
| Semantic disposition | A human judgment about whether an exact technically valid artifact faithfully represents its evidence and role. |
| Projection | A deterministic, role-specific representation that preserves necessary meaning while removing repetition and harness-owned detail. |

> **Governing distinction**
> Technical validity is not semantic acceptance; semantic acceptance is not scheduling; scheduling is not report approval; report approval is not a technical or business decision; and none of these automatically authorizes deployment.

PART I · PURPOSE AND ARCHITECTURE

## Understanding the harness

### 1. What is the Code Review Harness?

The Code Review Harness is a governed system for turning source evidence into traceable technical findings, recommendations, decision requests, and leadership reports. It combines model-based agents with deterministic validation, immutable evidence, explicit workflows, state machines, and human authority.

It is not simply a collection of prompts. The prompts perform bounded reasoning, while the harness determines what evidence is eligible, which role may run, which versions govern the run, whether the result is structurally valid, how it is stored, and what may happen next.

Practical meaning: The value comes from the combination of reasoning and control. The model supplies analysis; the harness supplies identity, evidence, policy, lifecycle, and accountability.

### 2. What is the intended output of the entire system?

The intended product is an evidence-backed report containing findings, recommendations, uncertainty, conflicts, evidence locators, and decisions that require human attention. That report can be exported from the system for senior-leadership review.

Leadership approval for distribution occurs outside the technical analysis. Human experts then make their decisions, and an authorized administrator records those decisions in the system. Agent recommendations, leadership distribution approval, expert judgment, and administrative recording remain separate events.

Practical meaning: The harness prepares decision support. It does not become the decision-maker or treat report generation as approval.

### 3. Why are there multiple levels of agents?

Different questions require different evidence scopes and different kinds of judgment. A specialist can inspect one technical domain deeply. A product agent can correlate specialists within one product. A capability agent can examine end-to-end behavior across products. An enterprise agent can reason across capabilities and enterprise concerns. Orchestration agents control execution without making engineering conclusions.

Layering prevents a broad model from claiming knowledge it was never given. It also preserves accountability: a synthesis agent can cite and correlate a specialist conclusion without silently replacing it.

- Specialist: bounded domain observations and findings.
- Product: product-scoped correlation and engineering posture.
- Capability: cross-product and mission-level questions.
- Enterprise: system-of-systems and leadership decision support.
- Orchestration: identity, scheduling, dispatch, validation, routing, audit, and rollback.
Practical meaning: The layers create controlled abstraction. Each level may add traceable interpretation, but it must preserve the meaning and limitations of the levels below it.

### 4. What is the difference between an agent and the harness?

An agent is a bounded reasoning role. It receives a signed task, exact eligible evidence, a focus area, a rubric, and an output contract. It produces observations, assessments, findings, correlations, recommendations, and decision requests within that role.

The harness is the control and evidence system around the agent. It owns immutable identity, dispatch, input eligibility, prompt and model pins, schema validation, projection, ledger publication, lifecycle state, state transitions, human records, rollback, and authorized consumers.

Practical meaning: Anything that determines authority or system state should be deterministic and outside the model wherever practical.

### 5. What does the coordinator do?

The coordinator creates the exact input set for a synthesis role. It verifies that required designations are present, rejects unexpected or duplicated inputs, binds every artifact by ID and hash, preserves conflicts and partial-input state, and determines whether dispatch is permitted.

The coordinator is not a junior synthesis agent. It does not decide which finding matters more, resolve conflicts, or infer missing content. Its job is mechanical integrity and routing.

Practical meaning: The coordinator determines what may enter the reasoning boundary; the synthesis agent determines what can be responsibly said about that admitted evidence.

### 6. What is the state machine for?

The state machine prevents conceptually different events from collapsing into one ambiguous idea of approval. A candidate may be generated, technically validated, packaged for review, semantically dispositioned, owner-finalized, made eligible, scheduled, reported, distributed, superseded, or revoked. Each transition has a different authority and effect.

This matters because a schema-valid answer can still be semantically wrong, and a semantically faithful artifact can still be inappropriate for scheduling or distribution. The state machine makes those distinctions enforceable.

Practical meaning: The state machine is the architecture's memory of what is true, who established it, and what that truth authorizes next.

### 7. What is shadow integration, and why is it the next step?

Shadow integration runs a candidate workflow alongside the accepted route using the same eligible evidence, while preventing the candidate from changing the official report, baseline, decision records, scheduling, or deployment. Its output is comparison evidence only.

Isolated evaluation proves that an agent can produce a valid and semantically faithful artifact. Shadow integration asks the harder operational question: can that agent live safely inside the real harness, preserve upstream and downstream meaning, fail without disruption, and add useful information rather than noise?

- Compare coverage, findings, conflicts, confidence, limitations, and decision requests.
- Measure end-to-end latency, token use, storage, failure isolation, and rollback.
- Require human review of material semantic differences.
- Keep the accepted ENT-EVIDENCE → ENT-SYSRISK route authoritative until a later promotion decision.
Practical meaning: Shadow integration is controlled observation before authority. Success supplies evidence for a later decision; it does not make that decision automatically.

PART II · PROMPTS, FOCUS, AND CONTEXT

## How bounded reasoning is engineered

### 8. How are the necessary prompts derived?

A prompt is derived from the agent's architectural purpose, universal contract, layer contract, role contract, focus-area definition, rubric, exact workflow position, input manifest, output schema, and state-machine authority. It is closer to a compiled role specification than to an improvised request.

The prompt defines the mission, exact inputs, required analytical work, evidence obligations, prohibited claims, required output records, confidence treatment, human decision boundaries, and lifecycle effect. The harness separately attaches identity, hashes, versions, execution state, and eligible consumers.

Practical meaning: The prompt is not the primary source of authority. It is the model-facing expression of authority and obligations already established in contracts and state.

### 9. How do we ensure that a prompt references the agent's special focus area?

The focus area must be a versioned analytical obligation, not merely a role name. A secrets specialist, for example, needs required questions about creation, storage, injection, access, transmission, logging, rotation, revocation, and disposal; relevant evidence populations; a secrets taxonomy; confidence rules; safe-handling restrictions; and required output types.

The current prompt templates, role schemas, rubrics, agent frameworks, and input selection carry much of this information. The recommended strengthening is a machine-readable focus profile bound into every dispatch by ID, version, and hash. Dispatch would fail if the profile were missing, incompatible, or not represented in the compiled prompt.

- Focus changes which evidence is selected and which tools are permitted.
- Focus defines required questions, methods, output classes, and prohibited conclusions.
- The rubric tests whether the model actually applied the domain lens rather than producing generic analysis.
- Downstream agents preserve the focus profile, source designation, and original finding identifiers.
Practical meaning: A specialist should be able to prove not only that it ran, but which professional lens governed its analysis.

### 10. What gets compressed when prompts take too long or consume too many tokens?

Compression removes repeated representation before it removes evidence. Complete child artifacts are retained in immutable storage, while the model receives a bounded projection containing the conclusions, conflicts, limitations, confidence, decision requests, evidence references, and source IDs needed for its role.

Repeated harness envelopes, ledger indexes, telemetry, administrative metadata, schema boilerplate, and full child-object copies are replaced with exact IDs, hashes, versions, and relevant record extracts. Output repetition is reduced by referencing authoritative records rather than restating them.

- Compress first: duplicate metadata, repeated prose, complete copied child objects, and harness-owned state.
- Preserve always: finding meaning, evidence locators, conflicts, missing evidence, evidence tiers, confidence meaning, limitations, source IDs, decision requests, authority, eligibility, and rollback state.
- If required meaning cannot fit, split the task or declare incomplete input; do not silently discard evidence.
Practical meaning: The governing rule is: compress representation, not meaning.

### 11. When does compression become distortion?

Compression becomes distortion when a reviewer can no longer reconstruct why a conclusion was made, when disagreement disappears, when confidence loses its original meaning, when an omitted limitation changes the apparent result, or when multiple distinct source records collapse into an ambiguous summary.

The harness detects this through exact source bindings, coverage checks, limitation propagation, child-qualified identifiers, semantic-review packets, and comparisons between retained source artifacts and projected output. A projection is acceptable only if the full source remains available and the compact representation preserves every fact needed by the consumer's role.

Practical meaning: Token efficiency is subordinate to semantic fidelity. A cheaper answer that changes what the evidence means is a failed answer.

### 12. Why not give every agent the whole repository and one very large prompt?

A large undifferentiated context increases cost, latency, distraction, prompt-injection exposure, and the chance that the model will cross authority boundaries. It also makes it difficult to prove which evidence supported which conclusion.

Bounded evidence populations let each agent receive only what it needs, document what it could not inspect, and make claims proportionate to coverage. Broader synthesis occurs later through immutable artifacts rather than one model carrying the entire system in transient context.

Practical meaning: The architecture favors composable, inspectable judgments over one impressive but unverifiable monologue.

### 13. How do prompt, rubric, and schema work together?

The prompt describes the work and boundaries in language the model can follow. The rubric defines what good performance means and which semantic failures matter. The schema defines the records and data shapes the harness can validate and route.

These three must be co-designed. A prompt that requires uncertainty but a schema with no uncertainty field will lose meaning. A schema that requires a confidence number without a declared rubric or derivation will encourage invented precision. A rubric that is not reflected in the prompt or output cannot be evaluated reliably.

Practical meaning: Prompt, rubric, and schema form one executable specification viewed from three different angles.

### 14. Why use one agent per specification instead of one adaptable agent?

A stable agent specification makes identity, scope, evidence permissions, focus, output meaning, and test history auditable. A highly adaptable agent may be capable, but its behavior becomes harder to compare across runs and easier to accidentally broaden.

Reusable model infrastructure is still shared. The distinction is at the governed role level: each designation binds a known prompt family, contract, schema, rubric, focus profile, consumers, and lifecycle. New versions can evolve, but they do so explicitly.

Practical meaning: The system reuses intelligence while versioning responsibility.

### 15. What happens when the model returns an invalid or suspicious output?

The output does not become an artifact eligible for downstream use. Structural errors, invented sources, invalid identities, duplicate IDs, changed limitations, unauthorized effects, or incompatible evidence cause the run to fail closed. The raw response and error may be retained as development evidence.

Harness-owned corrections may be applied through a disclosed deterministic reprojection when they do not change model meaning. Semantic changes require a new model run or a human decision; the system does not silently patch the model into apparent correctness.

Practical meaning: Failure is evidence. Retaining failed attempts turns defects into regression controls without laundering them into accepted results.

PART III · EVIDENCE, GOVERNANCE, AND OPERATIONS

## How trust is established and limited

### 16. How can a human reviewer verify a finding?

Every actionable item should resolve to an evidence locator containing the repository, immutable revision, file path, line or section, fingerprint, access classification, and reproduction instructions. The reviewer can move from the report item to the exact source without relying on the model's prose alone.

Redaction may hide sensitive content, but it must not destroy location or identity. If evidence cannot be reproduced, the item is marked accordingly and cannot be presented with the same reviewability as source-located evidence.

Practical meaning: Traceability is not a citation decoration. It is the mechanism by which a human can challenge and confirm the machine's claim.

### 17. What does insufficient evidence mean?

It means the admitted evidence cannot support the requested conclusion. It does not mean failure, safety, noncompliance, compliance, satisfaction, or absence of findings. It is a bounded statement about knowledge.

The artifact should identify the missing population, why it matters, what was reviewed, what remains unknown, and which evidence would change the state. This is more useful than forcing a binary answer because it creates a concrete collection or decision request.

Practical meaning: Unknown is a first-class result. The harness is designed to resist the organizational pressure to turn missing evidence into reassuring certainty.

### 18. What is the difference between technical validation and semantic faithfulness?

Technical validation answers whether the artifact conforms to schema, identity, lineage, integrity, policy, required fields, and prohibited effects. Semantic review asks whether it accurately represents the source evidence, preserves limitations and disagreement, uses identifiers meaningfully, and makes only supported claims.

The project has already observed technically valid artifacts with semantic defects, including flattened decision identifiers and limitations that were bound in machine records but absent from human-readable summaries. Human review caught what structural validation could not.

Practical meaning: A valid container can still carry the wrong meaning. Both forms of review are necessary.

### 19. Who is allowed to make decisions?

Agents may recommend, request, and explain decisions. Named human authorities make the decisions. Authorized administrators may record them. The project owner finalizes the bounded system effect. The harness then derives eligibility or other permitted state from those exact records.

No model response is treated as leadership approval, requirements acceptance, risk acceptance, compliance determination, strategy approval, report-distribution approval, release authorization, or deployment authority unless an explicit contract and human state transition establish that effect.

Practical meaning: Intelligence may inform authority, but it does not create authority.

### 20. Why are artifacts and human records immutable?

Immutability ensures that the evidence reviewed by a human is the same evidence later used to justify a transition. Corrections produce new artifacts, dispositions, or supersession records rather than rewriting history.

This protects replay, audit, rollback, and institutional memory. It also allows the project to retain failed and superseded approaches without confusing them with current authority.

Practical meaning: Immutability makes disagreement with the past possible without making the past disappear.

### 21. How does rollback work?

Rollback disables eligibility, discovery, scheduling, or the candidate workflow while retaining all source artifacts, decisions, evidence, and audit history. The accepted baseline continues to operate. A risky increment should identify its tested rollback route before it is promoted.

Rollback is not deletion and not history rewriting. It is a controlled change in what may be used going forward. This distinction lets the project learn from a candidate without becoming trapped by it.

Practical meaning: A reversible architecture can move faster because experimentation does not require irreversible trust.

### 22. How do tokens, latency, and hardware affect the design?

Model inference dominates runtime. The demonstrated four-stage reference vertical consumed 37,245 input and 5,525 output tokens and took about 14.2 minutes serially on GX-10. Final ENT-SYNTH consumed 7,696 input and 5,104 output tokens and took 775 seconds. Deterministic validation is comparatively fast.

Independent domain agents can run in parallel, and compact projections can reduce repeated output. Production targets an A100 large cluster, but no A100 timing has been measured. Current planning ranges must remain estimates until the exact accepted workload is benchmarked.

Practical meaning: Performance optimization should target output topology, parallelism, serving configuration, and evidence selection without weakening semantics or authority boundaries.

PART IV · PHILOSOPHY AND LEADERSHIP

## The deeper questions behind the architecture

### 23. What does it mean for the harness to know something?

The harness does not treat fluent text as knowledge. A claim becomes usable knowledge only when its source population is declared, the evidence is immutable and locatable, the transformation is traceable, limitations and conflicts are preserved, the responsible role is identified, and the claim has reached the state required for its intended use.

Knowledge in this system is therefore relational: it connects a proposition to evidence, method, scope, confidence, authority, time, and permitted consequence. Remove those relationships and the statement may still sound true, but it is no longer governable.

Practical meaning: The harness is designed to know not only a conclusion, but why it may believe it and what that belief is allowed to change.

### 24. Why preserve disagreement instead of producing one answer?

Disagreement often contains the most important information. Different agents may examine different evidence, use different methods, or carry different authorities. Averaging their conclusions can erase a real risk, conceal a missing dependency, or create false consensus.

The synthesis role may explain the disagreement, identify its source, and request the evidence or decision needed to resolve it. It may not simply choose the most confident voice or manufacture a compromise.

Practical meaning: A leadership report should reveal the decision landscape, not make uncertainty visually disappear.

### 25. Why is intelligence different from authority?

A model may identify patterns faster than a human and may articulate sophisticated recommendations. Authority, however, is an institutional relationship involving accountability, mandate, consequence, and often law or policy. Predictive ability does not supply those things.

The architecture therefore permits the model to become more capable without automatically becoming more powerful. Expanded reasoning must still pass through contracts and named human transitions.

Practical meaning: The harness is designed so that improved models increase the quality of advice, not silently expand the machine's jurisdiction.

### 26. What does it mean to trust the harness?

Trust should not mean believing that the model is usually right. It should mean confidence that the system will expose what it used, constrain what it may claim, retain what happened, fail visibly, preserve uncertainty, route decisions to the correct humans, and permit independent verification and rollback.

Model accuracy remains important, but trustworthy operation also depends on predictable failure. A system that sometimes refuses to conclude is often more trustworthy than one optimized to answer every question.

Practical meaning: Trust is earned through inspectability, boundedness, and recoverability—not through confident language.

### 27. Is having a human in the loop enough?

No. A nominal human approval can become ceremonial when the report is too dense, the evidence is inaccessible, the interface encourages acceptance, or the machine's recommendation appears inevitable. Human involvement is meaningful only when the person has authority, time, context, alternatives, source access, and the ability to reject or request more evidence.

The harness supports substantive review through exact packets, evidence locators, visible limitations, conflicts, decision-specific authority, immutable responses, and separation between the decision-maker and the machine recommendation.

Practical meaning: The goal is not a human somewhere in the workflow; it is a human who can exercise informed and consequential judgment.

### 28. How do we prevent automation bias?

Automation bias occurs when people defer to a system because it is systematic, fast, or presented with apparent precision. Controls include showing source evidence, displaying missingness and dissent, avoiding unjustified composite scores, separating confidence types, requiring explicit reasons for consequential decisions, and comparing model output with deterministic or baseline paths.

Training and report design also matter. Reviewers should be encouraged to challenge the model, not merely confirm it. The system should measure reversals, rejected findings, disputed classifications, and evidence requests rather than treating acceptance rate as quality.

Practical meaning: A successful harness should make critical review easier, not make agreement easier.

### 29. What does correctness mean for this system?

Correctness has several layers: structural correctness, evidentiary correctness, semantic faithfulness, methodological correctness, authority correctness, and operational correctness. A result may pass one and fail another.

For example, a JSON artifact may be structurally valid but cite the wrong record; it may cite the right record but overstate its meaning; it may be semantically faithful but not authorized for report distribution; or it may be authorized but too slow and fragile for production operation.

Practical meaning: Production readiness requires a portfolio of proofs, not a single passing test or expert impression.

### 30. How will we know whether the harness is worth continuing and eventually producing?

The harness should earn continuation by improving decision quality, traceability, coverage, review speed, consistency, and recoverability without increasing unsupported certainty or administrative burden. Measures should include confirmed and rejected findings, evidence-locator success, unresolved conflicts, semantic defect rates, human review time, decision reversals, token and latency cost, failure isolation, and rollback performance.

Production authorization should require bounded shadow integration, multi-repository expert-adjudicated evidence, measured A100 performance, operational orchestration, security and resilience testing, report/distribution pilots, and a new ADR that states scope, service objectives, authority, residual risks, and rollback.

- The system should find useful things humans can verify.
- It should make uncertainty and evidence gaps more visible, not less.
- It should reduce the cost of assembling and tracing a review without transferring human authority to the model.
- It should fail in ways that are contained, explainable, and recoverable.
Practical meaning: The ultimate test is not whether the agents sound intelligent. It is whether the organization makes better, more transparent, and more defensible decisions because the harness exists.

CLOSING PERSPECTIVE

## The architectural thesis

The Code Review Harness rests on a simple thesis: model reasoning becomes organizationally useful when it is bounded by evidence, made traceable through contracts, preserved through immutable state, and connected to human authority without impersonating it.

The project has already demonstrated that this thesis can be implemented through one complete vertical and an accepted-live enterprise candidate path. The next phase must establish whether the same discipline survives integration, broader evidence, sustained operation, and production hardware.

> **Leadership takeaway**
> The harness should be judged neither as an autonomous decision-maker nor as a collection of clever prompts. It is an evidence and governance architecture that uses models as bounded analytical components. Its credibility depends on preserving the difference between what the machine can infer, what the evidence can support, and what humans are authorized to decide.

### Recommended companion reading

- Leadership Progress Report: progress, maturity, measured GX-10 performance, A100 estimates, risks, and authorization request.
- Integrated Agent Framework: cross-layer responsibilities, inputs, outputs, handoffs, and authority boundaries.
- Post-Vertical-Slice Sequence: increment history, exit criteria, evidence, and current next step.
- ADR-0034 through ADR-0038: accepted-live capability and enterprise evaluations, corrections, semantic dispositions, and rollback.
> **Current boundary**
> ENT-SYNTH is semantically accepted and owner-finalized only for a later bounded shadow-integration evaluation. It remains unscheduled and has not changed the accepted report, distribution, deployment, or A100 production state.
