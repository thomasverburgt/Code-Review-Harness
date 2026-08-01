import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = "C:/Users/toomu/OneDrive/Documents/Code Harness";
const MODE = globalThis.CURRICULUM_MODE ?? process.env.CURRICULUM_MODE ?? "full";
const PACKAGE = path.join(
  ROOT,
  MODE === "condensed"
    ? "training/agentic-system-curriculum/condensed"
    : "training/agentic-system-curriculum/revised",
);
const OUT = path.join(PACKAGE, "slides");
const RENDERS = path.join(PACKAGE, "renders/slides");

const C = {
  ink: "#111827",
  muted: "#52606D",
  blue: "#2E74B5",
  blueDark: "#1F4D78",
  bluePale: "#EAF5FB",
  greenPale: "#EAF5EE",
  amberPale: "#FFF4D6",
  redPale: "#FBEAEC",
  gray: "#F2F2F2",
  line: "#CBD5E1",
  white: "#FFFFFF",
};

const fullSessions = [
  {
    n: 1, slug: "Why-a-Harness-Exists", title: "Why a Harness Exists",
    question: "Why is a strong model still not a trustworthy review system?",
    outcomes: ["Distinguish model, agent, workflow, and harness", "Name the harness controls that create trust", "Trace a review from evidence to human decision"],
    concepts: [["MODEL", "Generates candidate reasoning"], ["AGENT", "Role + contract + tools"], ["WORKFLOW", "States + transitions"], ["HARNESS", "Controls execution and artifacts"]],
    example: ["Repository change", "Evidence intake", "Contract selection", "Bounded review", "Human decision"],
    lab: "Mark every control point in an unconstrained code review.", labSteps: ["Find failure surfaces", "Add harness controls", "Defend each control"],
    prompt: "Rewrite “Review this code” as a bounded, evidence-aware request.", promptBlocks: ["Evidence", "Scope", "Consumer", "Output", "Authority", "Failure behavior"],
    exit: "Name four things the harness must control that a model cannot guarantee by itself.",
    source: "docs/philosophy.md; orchestration/workflow-model.md; contracts/universal-agent-contract.md",
  },
  {
    n: 2, slug: "Evidence-First-Humans-Decide", title: "Evidence First. Humans Decide.",
    question: "What should an agent be allowed to claim?",
    outcomes: ["Separate evidence, assessment, recommendation, and decision", "Detect authority leakage", "Rewrite claims with calibrated confidence"],
    concepts: [["EVIDENCE", "Observable source"], ["ASSESSMENT", "Bounded interpretation"], ["RECOMMENDATION", "Option for consideration"], ["DECISION", "Human-owned action"]],
    example: ["Observed behavior", "Evidence ID", "Assessment", "Recommendation", "Decision request"],
    lab: "Sort ten statements by epistemic type and repair the overclaims.", labSteps: ["Classify", "Cite evidence", "Restore authority"],
    prompt: "Add authority language that prevents approval, waiver, or risk acceptance.", promptBlocks: ["May observe", "May assess", "May recommend", "Must request", "Must not approve", "Must preserve uncertainty"],
    exit: "Turn an overconfident conclusion into an evidence-linked decision request.",
    source: "docs/philosophy.md; governance/human-review-and-maturity.md; contracts/evidence-contract.md",
  },
  {
    n: 3, slug: "Evidence-Provenance-and-Traceability", title: "Evidence, Provenance, and Traceability",
    question: "Can another engineer reproduce why this finding exists?",
    outcomes: ["Build a complete evidence chain", "Use provenance, coverage, and confidence correctly", "Handle missing, stale, and conflicting evidence"],
    concepts: [["PROVENANCE", "Origin + acquisition"], ["COVERAGE", "Inspected + omitted"], ["TRACEABILITY", "Stable links"], ["CONFIDENCE", "Support, not certainty"]],
    example: ["Lockfile line", "Evidence item", "Finding", "CAPA", "Decision request"],
    lab: "Build and then deliberately break a finding’s traceability chain.", labSteps: ["Map identifiers", "Remove one link", "Explain the failure"],
    prompt: "Write evidence admission and citation rules that prevent unsupported findings.", promptBlocks: ["Admissibility", "Freshness", "Evidence IDs", "Coverage", "Conflicts", "Incomplete input"],
    exit: "Show a reproducible chain and state its coverage limit.",
    source: "contracts/evidence-contract.md; contracts/evidence-flow-model.md; contracts/universal-agent-contract.md",
  },
  {
    n: 4, slug: "How-Contracts-Work", title: "How Contracts Work",
    question: "How do independent agents exchange trustworthy artifacts?",
    outcomes: ["Explain additive contract inheritance", "Map producers and consumers", "Validate the universal envelope"],
    concepts: [["UNIVERSAL", "Identity + integrity envelope"], ["LAYER", "Shared role-class rules"], ["ARTIFACT", "Typed evidence and findings"], ["ROLE", "Owned question + method"]],
    example: ["Universal contract", "Layer contract", "Artifact contract", "Role specification", "Prompt"],
    lab: "Repair a flawed artifact without changing its evidence.", labSteps: ["Find missing fields", "Find semantic violations", "Validate the repair"],
    prompt: "Translate contract obligations into explicit prompt clauses and output fields.", promptBlocks: ["Identity", "Execution", "Scope", "Evidence", "Confidence", "Consumers"],
    exit: "Explain why a role prompt cannot override the universal contract.",
    source: "contracts/contract-catalog.md; contracts/contract-dependency-graph.md; contracts/style-and-validation.md",
  },
  {
    n: 5, slug: "Agent-Identity-and-Architecture-Layers", title: "Agent Identity and Architecture Layers",
    question: "Which agent should answer which question?",
    outcomes: ["Navigate all six catalog layers", "Use canonical identity and status", "Route work to the narrowest authoritative agent"],
    concepts: [["SPECIALIST", "22 bounded reviewers"], ["PRODUCT", "4 product synthesizers"], ["CAPABILITY", "11 cross-product roles"], ["ENTERPRISE", "12 system-of-systems roles"]],
    example: ["Question", "Authoritative owner", "Layer", "Status", "Consumer"],
    lab: "Route twelve questions and name one tempting wrong agent for each.", labSteps: ["Find owner", "Check status", "Defend boundary"],
    prompt: "Draft identity and boundary blocks for a specialist and a synthesizer.", promptBlocks: ["UUID", "Designation", "Version", "Question", "Exclusions", "Consumers"],
    exit: "Route one scenario and explain the layer boundary in one sentence.",
    source: "agents/agent-registry.md; agents/agent-identities.json; agents/agent-naming-and-identity-standard.md",
  },
  {
    n: 6, slug: "State-Machines", title: "State Machines: Making Work Observable",
    question: "What exactly must be true before work advances?",
    outcomes: ["Model states, events, transitions, and guards", "Distinguish incomplete input, failure, and supersession", "Design deterministic transitions"],
    concepts: [["STATE", "Durable execution condition"], ["EVENT", "Transition request"], ["GUARD", "Required predicate"], ["TERMINAL", "Validated or stopped"]],
    example: ["registered", "ready", "running", "validated", "routed"],
    branches: ["incomplete_input", "failed", "superseded"],
    lab: "Run a tabletop execution; transition only when every guard passes.", labSteps: ["Draw event", "Evaluate guard", "Log transition"],
    prompt: "Specify safe incomplete-input behavior with no guessing.", promptBlocks: ["Ready guard", "Missing evidence", "State output", "Retry rule", "Failure reason", "Next action"],
    exit: "Explain the difference between an event and a guard, then model two failure paths.",
    source: "orchestration/workflow-model.md; contracts/universal-agent-contract.md",
  },
  {
    n: 7, slug: "Orchestration-Fan-Out-Fan-In-and-Gates", title: "Orchestration: Fan-Out, Fan-In, and Gates",
    question: "How do we coordinate many agents without hiding causality?",
    outcomes: ["Separate scheduler, fan-out, fan-in, and gate duties", "Identify safe parallelism", "Keep orchestrators from becoming reviewers"],
    concepts: [["ORCH-SCHED", "Selects roles + versions"], ["ORCH-FANOUT", "Dispatches independent work"], ["ORCH-FANIN", "Validates prerequisites"], ["ENT-EVIDENCE", "Gates enterprise fitness"]],
    example: ["Schedule", "Parallel reviews", "Track executions", "Validate join", "Route artifacts"],
    lab: "Design a release-review workflow with dependencies, retries, and a human gate.", labSteps: ["Mark parallel work", "Define join guard", "Place decision point"],
    prompt: "Draft an orchestration prompt that routes work but never creates findings.", promptBlocks: ["Select", "Dispatch", "Track", "Validate", "Route", "Never assess domain"],
    exit: "Draw a safe fan-out/fan-in graph and write its join guard.",
    source: "orchestration/workflow-model.md; contracts/orchestration-agent-contract.md; agents/enterprise/evidence-validation-gate.md",
  },
  {
    n: 8, slug: "Prompt-Implements-the-Contract", title: "The Prompt Implements the Contract",
    question: "How do we turn a specification into reliable model behavior?",
    outcomes: ["Use the universal prompt structure", "Trace every clause to a requirement", "Keep method, output, and authority consistent"],
    concepts: [["IDENTITY", "Who and which version"], ["AUTHORITY", "Allowed conclusions"], ["EXECUTION", "Inputs + method + states"], ["OUTPUT", "Exact artifact contract"]],
    example: ["Contract obligation", "Prompt clause", "Output field", "Test case", "Pass invariant"],
    lab: "Convert a specialist role specification into a prompt and trace matrix.", labSteps: ["Extract obligations", "Draft clauses", "Verify coverage"],
    prompt: "Draft a complete first-pass prompt for a baseline specialist.", promptBlocks: ["Identity", "Authority", "Inputs", "Method", "Output", "Failure behavior"],
    exit: "Defend each prompt section by citing its governing source.",
    source: "contracts/universal-agent-contract.md; contracts/specialist-agent-contract.md; agents/specialists/",
  },
  {
    n: 9, slug: "Prompt-Decomposition-and-Specialization", title: "Prompt Decomposition and Specialization",
    question: "How do we keep 55 prompts coherent without making them identical?",
    outcomes: ["Separate shared modules from specialization", "Define exclusions and consumers", "Preserve disagreement during synthesis"],
    concepts: [["SHARED MODULE", "Evidence + authority rules"], ["SPECIALIZATION", "Domain criteria + tools"], ["SYNTHESIS", "Correlation, not invention"], ["CONSUMER FIT", "Right semantics downstream"]],
    example: ["Universal module", "Layer module", "Role block", "Runtime context", "Typed output"],
    lab: "Draft one prompt per layer, then extract the genuinely reusable clauses.", labSteps: ["Compare drafts", "Extract modules", "Retest boundaries"],
    prompt: "Write a synthesis clause that preserves source IDs and conflicts.", promptBlocks: ["Source IDs", "Coverage", "Disagreement", "No overrule", "Confidence", "Decision request"],
    exit: "Move one duplicated policy clause into a shared module without erasing role boundaries.",
    source: "agents/hierarchical-agent-architecture.md; contracts/contract-dependency-graph.md; contracts/enterprise-synthesis-contract.md",
  },
  {
    n: 10, slug: "Prompt-Failure-Modes-and-Adversarial-Testing", title: "Prompt Failure Modes and Adversarial Testing",
    question: "How will this prompt fail under pressure?",
    outcomes: ["Recognize major prompt failure modes", "Design adversarial cases", "Specify safe failure behavior"],
    concepts: [["SCOPE DRIFT", "Answers adjacent questions"], ["AUTHORITY LEAK", "Recommendation becomes approval"], ["EVIDENCE LAUNDERING", "Unsupported claim gains polish"], ["INJECTION", "Input attacks instructions"]],
    example: ["Malicious input", "Instruction boundary", "Evidence filter", "Safe state", "Human request"],
    lab: "Attack another team’s prompt with eight hostile or degraded inputs.", labSteps: ["Break it", "Capture evidence", "Repair the invariant"],
    prompt: "Add failure behavior without creating an unreadable exception list.", promptBlocks: ["Missing", "Conflicting", "Malicious", "Oversized", "Tool failure", "Schema mismatch"],
    exit: "Demonstrate a fail-closed path that preserves provenance and requests human action.",
    source: "contracts/style-and-validation.md; contracts/sandboxed-contract-evolution.md; governance/integration-boundaries.md",
  },
  {
    n: 11, slug: "Evaluation-Calibration-and-Prompt-Evolution", title: "Evaluation, Calibration, and Prompt Evolution",
    question: "How do we know a prompt is improving rather than merely changing?",
    outcomes: ["Build a contract-derived rubric", "Measure calibration and boundary adherence", "Evolve prompts through controlled change"],
    concepts: [["EVAL CASE", "Input + expected invariant"], ["CALIBRATION", "Confidence matches support"], ["REGRESSION", "Lost prior invariant"], ["EVOLUTION", "Propose, test, approve, version"]],
    example: ["Baseline cases", "Candidate prompt", "Run both", "Compare scores", "Human disposition"],
    lab: "Score two prompt versions against the same corpus and explain every regression.", labSteps: ["Run cases", "Compare evidence", "Recommend disposition"],
    prompt: "Create a ten-case suite with negative and conflict cases.", promptBlocks: ["Grounding", "Completeness", "Boundaries", "Authority", "State", "Consumer fit"],
    exit: "Recommend a version change and tie it to semantic impact.",
    source: "governance/reviewer-calibration-and-evolution.md; contracts/sandboxed-contract-evolution.md; contracts/style-and-validation.md",
  },
  {
    n: 12, slug: "Prompt-Factory-Capstone", title: "Prompt Factory Capstone",
    question: "Can another team operate and audit your agent?",
    outcomes: ["Ship a complete prompt package", "Demonstrate contract compliance", "Conduct an evidence-based human review"],
    concepts: [["PROMPT", "Production candidate"], ["TRACE MATRIX", "Requirements coverage"], ["EVAL SUITE", "Repeatable invariants"], ["VERSION RECORD", "Review + disposition"]],
    example: ["Assign agents", "Draft packages", "Adversarial test", "Peer gate", "Human disposition"],
    lab: "Complete the assigned agent bundle and demonstrate success, conflict, incomplete-input, and authority paths.", labSteps: ["Build package", "Pass peer gate", "Demo evidence"],
    prompt: "Finalize the candidate and document every intentional deviation.", promptBlocks: ["Prompt", "Trace", "Examples", "Tests", "Scorecard", "Version"],
    exit: "Request one disposition: baseline, seed, return for change, or reject as duplicate.",
    source: "agents/agent-registry.md; contracts/universal-agent-contract.md; governance/human-review-and-maturity.md",
  },
];

const condensedSessions = [
  {
    n: 1, slug: "Harness-Philosophy-and-Human-Authority", title: "Harness Philosophy and Human Authority",
    question: "What turns capable model output into a trustworthy engineering review?",
    outcomes: ["Distinguish model, agent, workflow, and harness", "Separate evidence, assessment, recommendation, and decision", "Locate the human authority boundary"],
    concepts: [["MODEL", "Generates candidate reasoning"], ["AGENT", "Role + contract + tools"], ["HARNESS", "Controls execution + artifacts"], ["HUMAN", "Owns consequential decisions"]],
    example: ["Repository change", "Evidence intake", "Bounded review", "Recommendation", "Human decision"],
    demo: "Compare an unconstrained review response with the same review executed through harness controls.",
    demoSteps: ["Expose unsupported claims", "Add evidence and scope", "Restore human authority"],
    prompt: "Convert “Review this code” into a bounded, evidence-aware instruction.",
    promptBlocks: ["Identity", "Evidence", "Scope", "Consumer", "Output", "Authority"],
    exit: "Name the controls that make the review reproducible—and the decision that must remain human.",
    source: "docs/philosophy.md; contracts/universal-agent-contract.md; governance/human-review-and-maturity.md",
    format: "condensed",
  },
  {
    n: 2, slug: "Evidence-Provenance-and-Contracts", title: "Evidence, Provenance, and Contracts",
    question: "How can another engineer reproduce and validate an agent’s result?",
    outcomes: ["Build a traceable evidence chain", "Explain additive contract inheritance", "Validate the universal artifact envelope"],
    concepts: [["PROVENANCE", "Origin + acquisition"], ["COVERAGE", "Inspected + omitted"], ["CONTRACT", "Shared obligations"], ["TRACEABILITY", "Stable links end to end"]],
    example: ["Source line", "Evidence item", "Finding", "Recommendation", "Decision request"],
    demo: "Repair a flawed artifact while preserving its underlying evidence and provenance.",
    demoSteps: ["Find missing fields", "Check semantics", "Validate consumers"],
    prompt: "Translate evidence and contract obligations into explicit prompt behavior.",
    promptBlocks: ["Admission", "Evidence IDs", "Coverage", "Confidence", "Envelope", "Incomplete input"],
    exit: "Trace one assessment to evidence, contract, consumer, and decision request.",
    source: "contracts/evidence-contract.md; contracts/contract-dependency-graph.md; contracts/style-and-validation.md",
    format: "condensed",
  },
  {
    n: 3, slug: "Agent-Catalog-and-State-Machines", title: "Agent Catalog and State Machines",
    question: "Who owns the question, and what must be true before work advances?",
    outcomes: ["Route work to the narrowest authoritative agent", "Read canonical identity, layer, version, and status", "Model states, events, guards, and failure paths"],
    concepts: [["IDENTITY", "Canonical role + version"], ["LAYER", "Scope of synthesis"], ["STATE", "Durable execution condition"], ["GUARD", "Predicate for transition"]],
    example: ["registered", "ready", "running", "validated", "routed"],
    branches: ["incomplete_input", "failed", "superseded"],
    demo: "Route a release question to the catalog, then walk its execution through guarded states.",
    demoSteps: ["Find the owner", "Evaluate readiness", "Log the transition"],
    prompt: "Specify identity, boundaries, and safe incomplete-input behavior.",
    promptBlocks: ["Designation", "Question", "Exclusions", "Ready guard", "Failure state", "Next action"],
    exit: "Route one question and explain both its agent boundary and its next legal state transition.",
    source: "agents/agent-registry.md; agents/agent-identities.json; orchestration/workflow-model.md",
    format: "condensed",
  },
  {
    n: 4, slug: "Orchestration-and-Contract-Driven-Prompts", title: "Orchestration and Contract-Driven Prompts",
    question: "How do many agents coordinate without hiding causality or inventing findings?",
    outcomes: ["Separate scheduler, fan-out, fan-in, and gate duties", "Identify safe parallelism and join guards", "Project contract obligations into prompt clauses"],
    concepts: [["SCHEDULE", "Select roles + versions"], ["FAN-OUT", "Dispatch independent work"], ["FAN-IN", "Validate prerequisites"], ["PROMPT", "Implements the contract"]],
    example: ["Select agents", "Parallel reviews", "Track executions", "Validate join", "Route artifacts"],
    demo: "Walk a release review through parallel dispatch, artifact validation, and a human decision gate.",
    demoSteps: ["Mark dependencies", "Define join guard", "Place decision point"],
    prompt: "Write orchestration behavior that schedules and validates but never performs domain review.",
    promptBlocks: ["Select", "Dispatch", "Track", "Validate", "Route", "Never assess"],
    exit: "Explain the join guard and identify what the orchestrator is prohibited from concluding.",
    source: "orchestration/workflow-model.md; contracts/orchestration-agent-contract.md; contracts/universal-agent-contract.md",
    format: "condensed",
  },
  {
    n: 5, slug: "Prompt-Engineering-Deep-Dive", title: "Prompt Engineering Deep Dive",
    question: "How do we make 55 prompts coherent, specialized, and safe under pressure?",
    outcomes: ["Separate shared modules from role specialization", "Trace each clause to a governing requirement", "Design fail-closed behavior for adversarial inputs"],
    concepts: [["SHARED MODULE", "Stable inherited behavior"], ["ROLE BLOCK", "Owned method + exclusions"], ["TRACE MATRIX", "Requirement coverage"], ["ADVERSARIAL CASE", "Invariant under pressure"]],
    example: ["Contract rule", "Prompt clause", "Output field", "Test case", "Pass invariant"],
    demo: "Decompose one specialist prompt, trace its clauses, and test it against a malicious repository instruction.",
    demoSteps: ["Extract obligations", "Draft modules", "Attack invariants"],
    prompt: "Use the platform’s six-block core to draft a bounded specialist prompt.",
    promptBlocks: ["Identity", "Authority", "Inputs", "Method", "Output", "Failure behavior"],
    exit: "Defend one prompt clause with its source and demonstrate its fail-closed behavior.",
    source: "contracts/universal-agent-contract.md; contracts/specialist-agent-contract.md; contracts/sandboxed-contract-evolution.md",
    format: "condensed",
  },
  {
    n: 6, slug: "Evaluation-Evolution-and-Agent-Prompt-Playbook", title: "Evaluation, Evolution, and the Agent Prompt Playbook",
    question: "How do teams draft and improve every catalog prompt without losing control?",
    outcomes: ["Evaluate grounding, boundaries, state, authority, and consumer fit", "Version prompt changes through controlled evidence", "Apply one repeatable drafting playbook across all agent layers"],
    concepts: [["EVAL CASE", "Input + expected invariant"], ["CALIBRATION", "Confidence matches support"], ["VERSION", "Reviewed semantic change"], ["PLAYBOOK", "Repeatable drafting sequence"]],
    example: ["Select role", "Trace contracts", "Draft prompt", "Run cases", "Human review"],
    demo: "Compare two prompt versions and show how evidence supports—or rejects—the proposed change.",
    demoSteps: ["Run same cases", "Compare regressions", "Record disposition"],
    prompt: "Apply the universal template while preserving each layer’s distinct authority and consumers.",
    promptBlocks: ["Universal", "Layer", "Role", "Runtime", "Evaluation", "Version"],
    exit: "State the evidence required before a prompt version may become the new baseline.",
    source: "governance/reviewer-calibration-and-evolution.md; contracts/style-and-validation.md; agents/hierarchical-agent-architecture.md",
    format: "condensed",
  },
];

const sessions = MODE === "condensed" ? condensedSessions : fullSessions;

function textbox(slide, text, x, y, w, h, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width: w, height: h },
    fill: style.fill ?? "none",
    line: style.line ?? { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    fontSize: style.fontSize ?? 24,
    bold: style.bold ?? false,
    color: style.color ?? C.ink,
    typeface: style.typeface ?? "Aptos",
    alignment: style.align ?? "left",
    verticalAlignment: style.valign ?? "top",
    autoFit: style.autoFit ?? "shrinkText",
    insets: style.insets ?? { left: 0, right: 0, top: 0, bottom: 0 },
  };
  return shape;
}

function rect(slide, x, y, w, h, fill, radius = "rounded-xl", lineFill = C.line) {
  const options = {
    geometry: "roundRect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: lineFill, width: 1 },
  };
  if (radius && radius !== "none") options.borderRadius = radius;
  return slide.shapes.add(options);
}

function line(slide, x, y, w, h, fill = C.line) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function flowArrow(slide, startX, endX, centerY, fill = C.blue) {
  const headWidth = 14;
  const shaftEnd = endX - headWidth;
  line(slide, startX, centerY - 2, Math.max(1, shaftEnd - startX), 4, fill);
  slide.shapes.add({
    geometry: "chevron",
    position: { left: shaftEnd, top: centerY - 9, width: headWidth, height: 18 },
    fill,
    line: { style: "solid", fill, width: 0 },
  });
}

function footer(slide, session, num) {
  line(slide, 42, 672, 1196, 1, C.line);
  textbox(slide, `SESSION ${String(session.n).padStart(2, "0")}  •  CODE REVIEW HARNESS`, 42, 682, 500, 22, { fontSize: 12, bold: true, color: C.muted });
  textbox(slide, String(num).padStart(2, "0"), 1165, 682, 72, 22, { fontSize: 12, bold: true, color: C.muted, align: "right" });
}

function notes(slide, text, source) {
  slide.speakerNotes.textFrame.setText(`${text}\n\n[Sources]\n- Code Review Harness repository: ${source}`);
  slide.speakerNotes.setVisible(true);
}

function addTitle(slide, title, kicker) {
  textbox(slide, kicker.toUpperCase(), 42, 35, 500, 28, { fontSize: 13, bold: true, color: C.blue });
  textbox(slide, title, 42, 78, 1195, 82, { fontSize: 38, bold: true, color: C.ink });
}

function addCover(p, s) {
  const slide = p.slides.add();
  slide.background.fill = C.white;
  rect(slide, 780, 0, 500, 720, C.bluePale, "none", C.bluePale);
  line(slide, 780, 0, 12, 720, C.blue);
  textbox(slide, `SESSION ${String(s.n).padStart(2, "0")}`, 52, 52, 300, 30, { fontSize: 14, bold: true, color: C.blue });
  textbox(slide, s.title, 52, 150, 660, 220, { fontSize: 52, bold: true, color: C.ink, valign: "bottom" });
  textbox(slide, s.question, 52, 415, 620, 115, { fontSize: 25, color: C.muted });
  rect(slide, 850, 150, 330, 330, C.white, "rounded-2xl", C.line);
  textbox(slide, String(s.n).padStart(2, "0"), 885, 185, 260, 150, { fontSize: 94, bold: true, color: C.blue, align: "center", valign: "middle" });
  textbox(slide, "EVIDENCE\nCONTRACTS\nSTATE\nHUMAN AUTHORITY", 885, 352, 260, 100, { fontSize: 18, bold: true, color: C.blueDark, align: "center", valign: "middle" });
  textbox(slide, s.format === "condensed" ? "Condensed Young Engineer Training Series • 55 minutes" : "Young Engineer Training Series", 52, 640, 650, 28, { fontSize: 15, bold: true, color: C.muted });
  notes(slide,
    `Welcome learners and read the driving question aloud. Ask for a quick show of hands: who has used an AI assistant, who has relied on an automated code-review tool, and who has had to explain why an automated finding was correct? Frame this session as engineering a trustworthy system around model capability. Preview that every claim in the course will be tied to evidence, a contract, a workflow state, or a human authority boundary. Do not teach the whole session from the title slide; use it to establish the problem and invite one concrete experience from the room.`,
    s.source);
  return slide;
}

function addOutcomes(p, s) {
  const slide = p.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "By the end, learners can do three observable things", `Session ${s.n} outcomes`);
  const colors = [C.bluePale, C.greenPale, C.amberPale];
  s.outcomes.forEach((o, i) => {
    rect(slide, 42, 205 + i * 132, 690, 105, colors[i], "rounded-xl");
    textbox(slide, `0${i + 1}`, 66, 228 + i * 132, 70, 54, { fontSize: 28, bold: true, color: C.blue });
    textbox(slide, o, 150, 222 + i * 132, 545, 62, { fontSize: 23, bold: true, color: C.ink, valign: "middle" });
  });
  textbox(slide, "RUN OF SHOW", 805, 205, 330, 30, { fontSize: 14, bold: true, color: C.blue });
  const agenda = s.format === "condensed"
    ? ["Mental model", "Worked example", "Instructor demo", "Prompt walkthrough", "Knowledge check"]
    : ["Mental model", "Worked example", "Guided lab", "Prompt lab", "Exit ticket"];
  agenda.forEach((a, i) => {
    line(slide, 824, 263 + i * 72, 3, 52, i === agenda.length - 1 ? C.blue : C.line);
    slide.shapes.add({ geometry: "ellipse", position: { left: 813, top: 277 + i * 72, width: 24, height: 24 }, fill: i === 0 ? C.blue : C.white, line: { style: "solid", fill: C.blue, width: 2 } });
    textbox(slide, a, 858, 270 + i * 72, 300, 38, { fontSize: 20, bold: i === 0, color: C.ink });
  });
  footer(slide, s, 2);
  notes(slide,
    s.format === "condensed"
      ? `Walk through the outcomes as observable capabilities. Preview the 55-minute rhythm: mental model, worked example, instructor demonstration, prompt walkthrough, and knowledge check. Keep participation conversational and spend no more than four minutes here.`
      : `Walk through the outcomes as performance statements, not topics. Tell learners what evidence they will create for each outcome. Preview the rhythm: a small amount of instruction followed by a worked example, a team lab, a prompt-writing task, and a short exit ticket. Ask each learner to choose the outcome that feels least familiar and write it at the top of their notes. Revisit that choice at the end. Keep this slide under five minutes; its purpose is to make success inspectable.`,
    s.source);
}

function addConcepts(p, s) {
  const slide = p.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "One system, four distinct ideas", "Mental model");
  const positions = [[42, 205], [648, 205], [42, 420], [648, 420]];
  const colors = [C.bluePale, C.greenPale, C.amberPale, C.redPale];
  s.concepts.forEach(([name, desc], i) => {
    const [x, y] = positions[i];
    rect(slide, x, y, 565, 165, colors[i], "rounded-2xl");
    textbox(slide, name, x + 28, y + 28, 235, 38, { fontSize: 17, bold: true, color: C.blueDark });
    textbox(slide, desc, x + 28, y + 78, 500, 54, { fontSize: 23, bold: true, color: C.ink, valign: "middle" });
  });
  line(slide, 615, 268, 25, 4, C.blue);
  line(slide, 615, 483, 25, 4, C.blue);
  line(slide, 315, 378, 4, 34, C.blue);
  line(slide, 921, 378, 4, 34, C.blue);
  footer(slide, s, 3);
  notes(slide,
    `Teach the four terms by asking learners to compare responsibilities, not definitions. For each card, ask: what can this thing guarantee, and what can it only attempt? Use the connecting marks to emphasize that the concepts cooperate but are not interchangeable. Invite learners to supply an example from familiar CI/CD tooling. Correct any answer that treats fluent language as proof of evidence, treats a workflow as a simple checklist, or treats the harness as merely a place to store prompts. End by having pairs explain the full mental model in sixty seconds without using the word “AI.”`,
    s.source);
}

function addExample(p, s) {
  const slide = p.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "A trustworthy result is a chain—not a clever paragraph", "Worked example");
  const x0 = 42, y = 260, w = 208, gap = 39;
  s.example.forEach((item, i) => {
    const x = x0 + i * (w + gap);
    rect(slide, x, y, w, 165, i === 4 ? C.amberPale : C.gray, "rounded-xl");
    textbox(slide, String(i + 1), x + 18, y + 18, 38, 32, { fontSize: 16, bold: true, color: C.blue });
    const itemFontSize = item === "Recommendation" ? 16 : (item.length > 13 ? 19 : 21);
    textbox(slide, item, x + 20, y + 68, w - 40, 70, { fontSize: itemFontSize, bold: true, color: C.ink, align: "center", valign: "middle" });
    if (i < 4) {
      flowArrow(slide, x + w + 6, x + w + gap, y + 82);
    }
  });
  if (s.branches) {
    textbox(slide, `Failure branches: ${s.branches.join("  •  ")}`, 140, 470, 1000, 70, { fontSize: 22, bold: true, color: C.blueDark, align: "center", fill: C.redPale, insets: { left: 16, right: 16, top: 16, bottom: 12 } });
  } else {
    textbox(slide, "At every handoff: preserve identity, provenance, coverage, confidence, and consumer intent.", 100, 486, 1080, 64, { fontSize: 21, bold: true, color: C.blueDark, align: "center" });
  }
  footer(slide, s, 4);
  notes(slide,
    `Walk the example from left to right. At each handoff ask the room to name the producer, artifact, contract, validation condition, and consumer. Pause before the final box and ask who has authority to act. If the session includes failure branches, show that a safe system records why progress stopped instead of hiding the gap or guessing. Use one concrete repository example—such as a dependency, a secret, or a release artifact—but keep the technical details secondary to the control flow. The goal is for learners to see causality and traceability, not memorize labels.`,
    s.source);
}

function addLab(p, s) {
  const slide = p.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, s.format === "condensed" ? "See the control in action" : "Build an artifact the room can inspect", s.format === "condensed" ? "Instructor demonstration" : "Guided team lab");
  rect(slide, 42, 190, 1196, 180, C.bluePale, "rounded-2xl");
  textbox(slide, s.format === "condensed" ? "LIVE WALKTHROUGH" : "TEAM TASK", 76, 220, 220, 28, { fontSize: 14, bold: true, color: C.blue });
  textbox(slide, s.format === "condensed" ? s.demo : s.lab, 76, 265, 1110, 76, { fontSize: 27, bold: true, color: C.ink, valign: "middle" });
  const colors = [C.gray, C.greenPale, C.amberPale];
  (s.format === "condensed" ? s.demoSteps : s.labSteps).forEach((step, i) => {
    const x = 42 + i * 411;
    rect(slide, x, 410, 374, 165, colors[i], "rounded-xl");
    textbox(slide, `${i + 1}`, x + 24, 434, 45, 34, { fontSize: 20, bold: true, color: C.blue });
    textbox(slide, step, x + 24, 486, 320, 55, { fontSize: 22, bold: true, color: C.ink, valign: "middle" });
  });
  textbox(slide, s.format === "condensed" ? "Suggested timing: 2 min setup • 7 min walkthrough • 3 min questions" : "Suggested timing: 5 min brief • 20 min work • 10 min critique • 5 min repair", 42, 616, 1000, 28, { fontSize: 15, bold: true, color: C.muted });
  footer(slide, s, 5);
  notes(slide,
    s.format === "condensed"
      ? `Run this as a live instructor demonstration, not a learner exercise. Use one prepared repository example and narrate each decision shown on screen. Pause after each step for one evidence question from the room. Keep the demonstration to twelve minutes and preserve the before-and-after artifact for reference.`
      : `Form teams of three or four and assign one recorder. Read the task exactly once, then ask teams to restate the acceptance condition in their own words. During work time, circulate and ask evidence questions rather than supplying answers. At the critique, require another team to identify one strength, one contract gap, and one unsafe assumption. Give teams five minutes to repair the artifact before debrief. Collect the final artifact as course evidence; it will become input to the capstone. If time compresses, protect the critique and repair steps—the learning comes from validation, not only drafting.`,
    s.source);
}

function addPromptLab(p, s) {
  const slide = p.slides.add();
  slide.background.fill = C.white;
  addTitle(slide, "Turn the contract into executable prompt behavior", s.format === "condensed" ? "Prompt design walkthrough" : "Prompt engineering lab");
  textbox(slide, s.prompt, 42, 175, 1196, 64, { fontSize: 25, bold: true, color: C.ink });
  const colors = [C.bluePale, C.gray, C.greenPale, C.amberPale, C.redPale, C.gray];
  s.promptBlocks.forEach((block, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 42 + col * 411, y = 280 + row * 145;
    rect(slide, x, y, 374, 115, colors[i], "rounded-xl");
    textbox(slide, `0${i + 1}`, x + 22, y + 20, 44, 28, { fontSize: 15, bold: true, color: C.blue });
    textbox(slide, block, x + 74, y + 19, 270, 70, { fontSize: 21, bold: true, color: C.ink, valign: "middle" });
  });
  footer(slide, s, 6);
  notes(slide,
    s.format === "condensed"
      ? `Walk through the six blocks using a prepared prompt fragment. For each block, cite the contract or role specification that justifies it, then show one unsafe omission and its smallest repair. Invite verbal predictions before revealing the corrected clause. Keep this instructor-led and finish in ten minutes.`
      : `Require learners to draft in the six visible blocks rather than writing a long narrative prompt. For each block, they must cite the contract or role specification that justifies it. Pair reviewers should look for contradictions across blocks: a scope that exceeds the authoritative question, a method that admits evidence the input rules reject, or an output that implies decision authority. Ask reviewers to propose the smallest repair that restores the invariant. End by selecting one clause and testing it verbally with a hostile input. Remind the class that prompt quality is demonstrated by behavior across cases, not by how polished the wording sounds.`,
    s.source);
}

function addClose(p, s) {
  const slide = p.slides.add();
  slide.background.fill = C.ink;
  textbox(slide, `SESSION ${String(s.n).padStart(2, "0")}  •  EXIT TICKET`, 52, 50, 600, 30, { fontSize: 14, bold: true, color: "#8EC5E5" });
  textbox(slide, s.exit, 52, 160, 1070, 245, { fontSize: 43, bold: true, color: C.white, valign: "middle" });
  line(slide, 52, 460, 1120, 3, C.blue);
  textbox(slide, "Answer with evidence. Name the contract, state, or authority boundary you used.", 52, 500, 1040, 74, { fontSize: 23, color: "#D8E2EC" });
  const closingLabel = s.format === "condensed" && s.n === 6
    ? "CONDENSED SERIES COMPLETE • CONTINUE WITH REPOSITORY PRACTICE"
    : s.n === 12
      ? "CAPSTONE COMPLETE  •  HUMAN REVIEW REQUIRED"
      : `NEXT: SESSION ${String(s.n + 1).padStart(2, "0")}`;
  textbox(slide, closingLabel, 52, 640, 760, 28, { fontSize: 14, bold: true, color: "#8EC5E5" });
  notes(slide,
    s.format === "condensed"
      ? `Use this as a two-minute knowledge check. Ask for one evidence-backed answer and one correction or refinement from the room. Close by connecting the session to the next topic. Do not assign a graded deliverable.`
      : `Give learners two quiet minutes to answer the exit ticket individually. Require an evidence-backed response, not a slogan. Invite two contrasting answers and ask the group which is more reproducible and why. Collect responses or have learners commit them to the course workspace. Close by connecting today’s artifact to the next session and by restating the invariant: evidence is observable, assessment is bounded, recommendations inform, and humans decide. If misconceptions remain, record them as input to the next session rather than extending the lecture.`,
    s.source);
}

async function writeBlob(file, blob) {
  await fs.writeFile(file, new Uint8Array(await blob.arrayBuffer()));
}

async function buildDeck(s) {
  const p = Presentation.create({ slideSize: { width: 1280, height: 720 } });
  addCover(p, s);
  addOutcomes(p, s);
  addConcepts(p, s);
  addExample(p, s);
  addLab(p, s);
  addPromptLab(p, s);
  addClose(p, s);

  const deckName = `Session-${String(s.n).padStart(2, "0")}-${s.slug}`;
  const renderDir = path.join(RENDERS, deckName);
  await fs.mkdir(renderDir, { recursive: true });
  for (const [i, slide] of p.slides.items.entries()) {
    const stem = `slide-${String(i + 1).padStart(2, "0")}`;
    await writeBlob(path.join(renderDir, `${stem}.png`), await p.export({ slide, format: "png", scale: 1 }));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(renderDir, `${stem}.layout.json`), await layout.text());
  }
  await writeBlob(path.join(renderDir, "montage.webp"), await p.export({ format: "webp", montage: true, scale: 0.5 }));
  const pptx = await PresentationFile.exportPptx(p);
  await pptx.save(path.join(OUT, `${deckName}.pptx`));
  console.log(`${deckName}.pptx`);
}

await fs.mkdir(OUT, { recursive: true });
await fs.mkdir(RENDERS, { recursive: true });
for (const s of sessions) {
  await buildDeck(s);
}
