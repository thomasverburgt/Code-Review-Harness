from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUT_DIR = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
ASSET_DIR = OUT_DIR / "build" / "assets"
OUTPUT = OUT_DIR / "Code-Review-Harness-Agentic-System-Curriculum.docx"
ASSET_DIR.mkdir(parents=True, exist_ok=True)

BLUE = "2E74B5"
DARK_BLUE = "1F4D78"
INK = "17212B"
MID = "52606D"
LIGHT = "E8EEF5"
PALE_BLUE = "EAF5FB"
PALE_GREEN = "EAF5EE"
PALE_AMBER = "FFF4D6"
PALE_RED = "FBEAEC"
WHITE = "FFFFFF"


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def rounded(draw, xy, fill, outline="#B8C2CC", radius=18, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, box, text, fnt, fill="#17212B", line_gap=5):
    x0, y0, x1, y1 = box
    words = text.split()
    lines, line = [], ""
    max_w = x1 - x0 - 24
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_w:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    heights = [draw.textbbox((0, 0), s, font=fnt)[3] for s in lines]
    total = sum(heights) + max(0, len(lines) - 1) * line_gap
    y = y0 + ((y1 - y0) - total) / 2
    for s, h in zip(lines, heights):
        w = draw.textbbox((0, 0), s, font=fnt)[2]
        draw.text((x0 + ((x1 - x0) - w) / 2, y), s, font=fnt, fill=fill)
        y += h + line_gap


def arrow(draw, p1, p2, color="#2E74B5", width=6):
    draw.line([p1, p2], fill=color, width=width)
    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    length = 18
    for delta in (2.55, -2.55):
        end = (
            p2[0] + length * math.cos(angle + delta),
            p2[1] + length * math.sin(angle + delta),
        )
        draw.line([p2, end], fill=color, width=width)


def make_diagrams():
    paths = {}

    # Harness loop
    img = Image.new("RGB", (1600, 760), "white")
    d = ImageDraw.Draw(img)
    title = font(38, True)
    body = font(28, True)
    d.text((60, 40), "The harness turns review into a controlled evidence flow", font=title, fill=f"#{INK}")
    labels = ["Evidence", "Select contracts", "Run agents", "Validate artifacts", "Route to humans"]
    colors = [PALE_BLUE, LIGHT, PALE_GREEN, PALE_AMBER, PALE_RED]
    boxes = []
    x = 55
    for label, color in zip(labels, colors):
        box = (x, 260, x + 260, 440)
        rounded(d, box, f"#{color}")
        center_text(d, box, label, body)
        boxes.append(box)
        x += 305
    for a, b in zip(boxes, boxes[1:]):
        arrow(d, (a[2] + 5, 350), (b[0] - 10, 350))
    d.text((60, 570), "Control plane: identity • scope • provenance • confidence • authority • integrity", font=font(26), fill=f"#{DARK_BLUE}")
    path = ASSET_DIR / "harness-flow.png"
    img.save(path)
    paths["harness"] = path

    # Contract stack
    img = Image.new("RGB", (1500, 900), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 40), "Contracts compose from universal rules to role-specific behavior", font=title, fill=f"#{INK}")
    stack = [
        ("Role specification / prompt", PALE_RED, 190),
        ("Layer contract", PALE_AMBER, 250),
        ("Artifact contracts", PALE_GREEN, 310),
        ("Universal agent contract", PALE_BLUE, 370),
    ]
    y = 180
    for label, color, inset in stack:
        box = (inset, y, 1500 - inset, y + 130)
        rounded(d, box, f"#{color}", radius=14)
        center_text(d, box, label, body)
        y += 150
    d.text((55, 810), "More specific layers add constraints; they do not erase inherited obligations.", font=font(26), fill=f"#{DARK_BLUE}")
    path = ASSET_DIR / "contract-stack.png"
    img.save(path)
    paths["contracts"] = path

    # State machine
    img = Image.new("RGB", (1700, 950), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 35), "A state machine makes progress, failure, and authority explicit", font=title, fill=f"#{INK}")
    nodes = {
        "registered": (70, 270, 350, 420),
        "ready": (440, 270, 720, 420),
        "running": (810, 270, 1090, 420),
        "validated": (1180, 270, 1460, 420),
        "incomplete_input": (440, 610, 760, 760),
        "failed": (880, 610, 1160, 760),
        "superseded": (1270, 610, 1580, 760),
    }
    colors = {
        "registered": PALE_BLUE, "ready": LIGHT, "running": PALE_GREEN,
        "validated": PALE_AMBER, "incomplete_input": PALE_RED,
        "failed": PALE_RED, "superseded": LIGHT,
    }
    for name, box in nodes.items():
        rounded(d, box, f"#{colors[name]}")
        center_text(d, box, name.replace("_", "\n"), body)
    for a, b in [("registered", "ready"), ("ready", "running"), ("running", "validated")]:
        arrow(d, (nodes[a][2] + 8, 345), (nodes[b][0] - 10, 345))
    arrow(d, (580, 425), (580, 600), color="#B0444E")
    arrow(d, (950, 425), (1010, 600), color="#B0444E")
    arrow(d, (1320, 425), (1425, 600), color="#64748B")
    d.text((70, 835), "Guards answer “may this transition happen?”; events explain “why did it happen?”", font=font(27), fill=f"#{DARK_BLUE}")
    path = ASSET_DIR / "state-machine.png"
    img.save(path)
    paths["state"] = path

    # Architecture
    img = Image.new("RGB", (1600, 920), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 35), "The catalog separates observation, synthesis, and coordination", font=title, fill=f"#{INK}")
    layers = [
        ("Enterprise", "12 agents • system-of-systems decision support", PALE_RED),
        ("Capability", "11 agents • cross-product mission and readiness", PALE_AMBER),
        ("Product", "4 agents • product-level correlation", PALE_GREEN),
        ("Specialist", "22 agents • bounded domain review", PALE_BLUE),
        ("Work + orchestration", "6 agents • reusable processing and routing", LIGHT),
    ]
    y = 150
    for name, desc, color in layers:
        box = (150, y, 1450, y + 120)
        rounded(d, box, f"#{color}", radius=16)
        d.text((190, y + 24), name, font=font(30, True), fill=f"#{INK}")
        d.text((520, y + 27), desc, font=font(26), fill=f"#{MID}")
        y += 140
    path = ASSET_DIR / "architecture-layers.png"
    img.save(path)
    paths["architecture"] = path

    # Fan-out / fan-in
    img = Image.new("RGB", (1600, 880), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 35), "Orchestration coordinates work without becoming a reviewer", font=title, fill=f"#{INK}")
    schedule = (60, 340, 330, 500)
    aggregate = (1270, 340, 1540, 500)
    rounded(d, schedule, f"#{PALE_BLUE}")
    rounded(d, aggregate, f"#{PALE_AMBER}")
    center_text(d, schedule, "ORCH-SCHED\nselects contracts", body)
    center_text(d, aggregate, "ORCH-FANIN\nvalidates readiness", body)
    agents = [("SPEC-A", 440, 155), ("SPEC-B", 440, 355), ("SPEC-C", 440, 555)]
    for label, x, y in agents:
        box = (x, y, x + 270, y + 135)
        rounded(d, box, f"#{PALE_GREEN}")
        center_text(d, box, label, body)
        arrow(d, (schedule[2] + 10, 420), (box[0] - 10, y + 68))
    fan = (800, 340, 1110, 500)
    rounded(d, fan, f"#{LIGHT}")
    center_text(d, fan, "ORCH-FANOUT\ntracks parallel work", body)
    fan_targets = [370, 420, 470]
    for (_, x, y), target_y in zip(agents, fan_targets):
        arrow(d, (x + 280, y + 68), (fan[0] - 10, target_y))
    arrow(d, (fan[2] + 10, 420), (aggregate[0] - 10, 420))
    d.text((60, 790), "Schedulers route. Reviewers assess. Humans decide.", font=font(29, True), fill=f"#{DARK_BLUE}")
    path = ASSET_DIR / "orchestration.png"
    img.save(path)
    paths["orchestration"] = path

    # Prompt anatomy
    img = Image.new("RGB", (1600, 920), "white")
    d = ImageDraw.Draw(img)
    d.text((55, 35), "A production prompt is an executable projection of the contract", font=title, fill=f"#{INK}")
    items = [
        ("1", "Identity", "Who am I? Which version and layer?", PALE_BLUE),
        ("2", "Authority", "What may I conclude—and what remains human?", LIGHT),
        ("3", "Inputs + scope", "What evidence is admissible? What is excluded?", PALE_GREEN),
        ("4", "Method", "What sequence, criteria, and tools govern the work?", PALE_AMBER),
        ("5", "Output", "What exact artifact schema must be emitted?", PALE_RED),
        ("6", "Failure behavior", "How do I handle gaps, conflicts, and uncertainty?", LIGHT),
    ]
    y = 140
    for num, name, desc, color in items:
        d.ellipse((75, y + 15, 135, y + 75), fill=f"#{BLUE}")
        center_text(d, (75, y + 15, 135, y + 75), num, font(24, True), fill="white")
        rounded(d, (165, y, 1510, y + 90), f"#{color}", radius=12)
        d.text((200, y + 16), name, font=font(28, True), fill=f"#{INK}")
        d.text((520, y + 20), desc, font=font(25), fill=f"#{MID}")
        y += 112
    path = ASSET_DIR / "prompt-anatomy.png"
    img.save(path)
    paths["prompt"] = path
    return paths


SESSIONS = [
    {
        "n": 1, "title": "Why a Harness Exists", "duration": "90 minutes",
        "question": "Why is a strong model still not a trustworthy review system?",
        "outcomes": [
            "Distinguish an AI model, an agent, a workflow, and a harness.",
            "Explain how the harness constrains scope, evidence, outputs, and authority.",
            "Trace one review request from evidence intake to human decision.",
        ],
        "concepts": [
            ("Model", "Generates candidate reasoning and language."),
            ("Agent", "A model operating under a role, contract, tools, and bounded context."),
            ("Workflow", "A sequence of states and transitions among agents and artifacts."),
            ("Harness", "The control plane that schedules, validates, records, and routes the work."),
        ],
        "flow": ["Hook: compare a clever answer with an auditable review", "Teach the harness flow", "Walk a secrets-review example", "Lab: mark control points", "Exit ticket"],
        "lab": "Give teams a repository change and an unconstrained review prompt. Ask them to identify every place where the result could become untraceable, over-broad, or falsely authoritative. Teams add one harness control for each failure.",
        "prompt_lab": "Rewrite “Review this code” as a bounded request that declares evidence, scope, consumer, output contract, and human decision authority.",
        "assessment": "Learner can name at least four controls provided by the harness and explain why the model alone cannot provide them.",
        "misconceptions": ["A harness is only a prompt wrapper.", "More autonomous agents always mean better review.", "A fluent result is equivalent to a validated artifact."],
        "source": "docs/philosophy.md; orchestration/workflow-model.md; contracts/universal-agent-contract.md",
        "diagram": "harness",
    },
    {
        "n": 2, "title": "Philosophy: Evidence First, Humans Decide", "duration": "90 minutes",
        "question": "What should an agent be allowed to claim?",
        "outcomes": [
            "Apply the evidence-first and human-authority principles.",
            "Separate observation, assessment, recommendation, and decision.",
            "Recognize persuasive language that exceeds the evidence.",
        ],
        "concepts": [
            ("Evidence", "An immutable observable source with provenance."),
            ("Assessment", "A bounded interpretation under declared criteria."),
            ("Recommendation", "An option for a human authority to consider."),
            ("Decision", "A human-owned act that changes acceptance, priority, or risk posture."),
        ],
        "flow": ["Read the philosophy", "Sort statements by epistemic type", "Red-team overclaiming", "Rewrite with calibrated authority", "Debrief"],
        "lab": "Teams classify ten statements as evidence, assessment, recommendation, or decision. They must defend each classification and identify the evidence needed to strengthen weak statements.",
        "prompt_lab": "Add authority language that forces the agent to request decisions instead of granting approvals, accepting risk, or declaring compliance.",
        "assessment": "Learner rewrites an overconfident conclusion into an evidence-linked assessment with a human decision request.",
        "misconceptions": ["Human-in-the-loop means a person merely clicks approve.", "Confidence is a substitute for evidence.", "A recommendation may silently become a decision."],
        "source": "docs/philosophy.md; governance/human-review-and-maturity.md; contracts/evidence-contract.md",
        "diagram": "harness",
    },
    {
        "n": 3, "title": "Evidence, Provenance, and Traceability", "duration": "120 minutes",
        "question": "Can another engineer reproduce why this finding exists?",
        "outcomes": [
            "Build an evidence chain from source to finding to decision request.",
            "Use stable identifiers, provenance, coverage, and confidence correctly.",
            "Identify missing, stale, conflicting, or inadmissible evidence.",
        ],
        "concepts": [
            ("Provenance", "Where the artifact came from and how it was obtained."),
            ("Coverage", "What was inspected, what was not, and why."),
            ("Traceability", "Stable links among inputs, reasoning products, and consumers."),
            ("Confidence", "Calibrated support for a claim—not certainty theater."),
        ],
        "flow": ["Evidence contract", "Traceability graph", "Coverage exercise", "Conflict handling", "Mini-review"],
        "lab": "Build a traceability chain for a vulnerable dependency: lockfile line → evidence item → finding → CAPA → consumer → decision request. Then remove one link and explain the failure.",
        "prompt_lab": "Write evidence admission rules and citation requirements that prevent unsupported findings and require explicit incomplete-input behavior.",
        "assessment": "Learner produces a complete, reproducible evidence chain and names any coverage limits.",
        "misconceptions": ["A URL alone is provenance.", "High confidence repairs missing evidence.", "Coverage can be inferred from the length of a report."],
        "source": "contracts/evidence-contract.md; contracts/evidence-flow-model.md; contracts/universal-agent-contract.md",
        "diagram": "contracts",
    },
    {
        "n": 4, "title": "How Contracts Work", "duration": "120 minutes",
        "question": "How do independent agents exchange trustworthy artifacts?",
        "outcomes": [
            "Explain contract inheritance and additive extension.",
            "Map producers and consumers across contract classes.",
            "Validate a sample artifact against the universal envelope.",
        ],
        "concepts": [
            ("Universal contract", "Identity, artifact, execution, scope, provenance, confidence, authority, and integrity."),
            ("Layer contract", "Rules shared by specialist, product, capability, enterprise, work, or orchestration roles."),
            ("Artifact contract", "Schema and semantics for evidence, findings/CAPA, patterns, and insights."),
            ("Role specification", "The authoritative question, scope, method, inputs, outputs, and consumers for one agent."),
        ],
        "flow": ["Contract stack", "Envelope field tour", "Producer/consumer mapping", "Validation lab", "Versioning discussion"],
        "lab": "Validate a deliberately flawed agent output. Mark missing envelope fields, semantic violations, unauthorized decisions, and broken consumer links. Repair it without changing the evidence.",
        "prompt_lab": "Translate five universal contract obligations into explicit prompt clauses and corresponding output fields.",
        "assessment": "Learner explains why a role prompt cannot override the universal contract and identifies when a major contract version is required.",
        "misconceptions": ["A schema alone is a contract.", "A child contract may remove inconvenient parent rules.", "Changing field meaning is a harmless minor version."],
        "source": "contracts/contract-catalog.md; contracts/contract-dependency-graph.md; contracts/style-and-validation.md",
        "diagram": "contracts",
    },
    {
        "n": 5, "title": "Agent Identity and Architecture Layers", "duration": "90 minutes",
        "question": "Which agent should answer which question?",
        "outcomes": [
            "Navigate the 55-agent catalog and its six layers.",
            "Use canonical designation, UUID, version, status, and specification.",
            "Route a question to the narrowest authoritative agent.",
        ],
        "concepts": [
            ("Identity", "Immutable UUID plus canonical designation and version."),
            ("Layer", "The level of evidence aggregation and authoritative question."),
            ("Status", "Baseline, seed, or planned readiness for scheduling."),
            ("Boundary", "A role’s owned question and explicit exclusions."),
        ],
        "flow": ["Catalog tour", "Architecture layers", "Identity rules", "Routing game", "Boundary critique"],
        "lab": "Teams receive twelve questions and route each to a catalog agent. For every choice they cite the authoritative question, layer, and status; they also name one tempting but incorrect agent.",
        "prompt_lab": "Draft the identity and boundary blocks for one specialist agent and one synthesis agent. Ensure neither duplicates the other.",
        "assessment": "Learner chooses the correct agent for a scenario and explains the layer boundary in one sentence.",
        "misconceptions": ["Display names are stable identifiers.", "Synthesis agents re-run all specialist reviews.", "Planned agents are production-ready because they appear in the registry."],
        "source": "agents/agent-registry.md; agents/agent-identities.json; agents/agent-naming-and-identity-standard.md",
        "diagram": "architecture",
    },
    {
        "n": 6, "title": "State Machines: Making Work Observable", "duration": "120 minutes",
        "question": "What exactly must be true before work advances?",
        "outcomes": [
            "Model agent execution as states, events, transitions, and guards.",
            "Distinguish incomplete input, failure, and supersession.",
            "Design transitions that are deterministic and auditable.",
        ],
        "concepts": [
            ("State", "A durable description of where an execution or artifact is."),
            ("Event", "The occurrence that asks the workflow to transition."),
            ("Guard", "A predicate that must be true for the transition to occur."),
            ("Terminal state", "A completed, failed, incomplete, or superseded outcome."),
        ],
        "flow": ["Human example", "Harness state model", "Guard design", "Failure branches", "Tabletop simulation"],
        "lab": "Run a tabletop execution. Learners draw event cards and may transition only when guards pass. They must log the event, state change, artifact IDs, and failure reason.",
        "prompt_lab": "Write prompt behavior for missing prerequisites: do not guess, emit the incomplete-input state, list missing evidence, and identify the safe next action.",
        "assessment": "Learner can explain the difference between an event and a guard and can model at least two failure paths.",
        "misconceptions": ["State is the same as a progress message.", "Retrying erases the failed attempt.", "All errors should transition to failed."],
        "source": "orchestration/workflow-model.md; contracts/universal-agent-contract.md",
        "diagram": "state",
    },
    {
        "n": 7, "title": "Orchestration: Fan-Out, Fan-In, and Gates", "duration": "120 minutes",
        "question": "How do we coordinate many agents without hiding causality?",
        "outcomes": [
            "Explain scheduler, fan-out, fan-in, and evidence-gate responsibilities.",
            "Identify safe parallelism and required dependencies.",
            "Prevent orchestrators and synthesizers from becoming unauthorized reviewers.",
        ],
        "concepts": [
            ("ORCH-SCHED", "Selects registered roles and contract versions."),
            ("ORCH-FANOUT", "Dispatches independent work and tracks executions."),
            ("ORCH-FANIN", "Validates prerequisites and assembles consumable input sets."),
            ("ENT-EVIDENCE", "Gates enterprise input fitness before enterprise analysis."),
        ],
        "flow": ["Dependency graph", "Parallelism rules", "Fan-in validation", "Enterprise gate", "Workflow design lab"],
        "lab": "Design a workflow for a release review. Mark dependencies, parallel branches, join criteria, retries, timeouts, and the exact point where a human decision is requested.",
        "prompt_lab": "Draft an orchestration prompt that schedules and validates but never generates domain findings.",
        "assessment": "Learner produces a dependency graph with safe parallelism and an explicit join guard.",
        "misconceptions": ["The orchestrator is the smartest reviewer.", "Fan-in means concatenate every report.", "Enterprise synthesis may overrule the evidence gate."],
        "source": "orchestration/workflow-model.md; contracts/orchestration-agent-contract.md; agents/enterprise/evidence-validation-gate.md",
        "diagram": "orchestration",
    },
    {
        "n": 8, "title": "The Prompt Is an Implementation of the Contract", "duration": "120 minutes",
        "question": "How do we turn a specification into reliable model behavior?",
        "outcomes": [
            "Use the platform’s universal prompt structure.",
            "Trace every prompt clause to a contract obligation or role requirement.",
            "Keep authority, evidence, method, and output mutually consistent.",
        ],
        "concepts": [
            ("System rules", "Non-negotiable platform and safety constraints."),
            ("Role block", "Identity, mission, authoritative question, and boundaries."),
            ("Execution block", "Inputs, evidence rules, method, tools, and state behavior."),
            ("Output block", "Exact schema, confidence, conflicts, consumers, and decision requests."),
        ],
        "flow": ["Prompt anatomy", "Contract-to-prompt mapping", "Worked example", "Pair drafting", "Peer review"],
        "lab": "Convert a role specification into a prompt. Partners use a trace matrix to verify every instruction has an origin and every contract obligation has an implementation.",
        "prompt_lab": "Draft a complete first-pass prompt for a baseline specialist agent using the universal template.",
        "assessment": "Learner can defend each prompt section by pointing to the governing contract or role specification.",
        "misconceptions": ["More detail always makes a prompt better.", "Persona language can replace a method.", "Output examples may contradict the schema if they read well."],
        "source": "contracts/universal-agent-contract.md; contracts/specialist-agent-contract.md; agents/specialists/*.md",
        "diagram": "prompt",
    },
    {
        "n": 9, "title": "Prompt Decomposition and Specialization", "duration": "120 minutes",
        "question": "How do we keep 55 prompts coherent without making them identical?",
        "outcomes": [
            "Separate shared prompt modules from role-specific instructions.",
            "Define authoritative questions, exclusions, consumers, and escalation paths.",
            "Design synthesis prompts that preserve provenance and disagreement.",
        ],
        "concepts": [
            ("Shared module", "Reusable language for evidence, authority, confidence, and output integrity."),
            ("Specialization", "Domain criteria, method, tools, and owned question."),
            ("Synthesis", "Correlation of validated artifacts without fabricating agreement."),
            ("Consumer fit", "The output detail and semantics needed by the next contract."),
        ],
        "flow": ["Prompt module map", "Specialist vs synthesizer", "Boundary patterns", "Drafting sprint", "Cross-team review"],
        "lab": "Teams draft prompts for one agent from each layer, then compare repeated clauses. They extract stable shared modules and retain only genuine role specialization.",
        "prompt_lab": "Write a synthesis clause that preserves source IDs, conflicting assessments, coverage differences, and human decision authority.",
        "assessment": "Learner can identify duplicated policy language and move it to a shared module without erasing role boundaries.",
        "misconceptions": ["Consistency means every prompt uses the same method.", "Synthesis should hide disagreement.", "A broad prompt is more reusable than a bounded prompt."],
        "source": "agents/hierarchical-agent-architecture.md; contracts/contract-dependency-graph.md; contracts/enterprise-synthesis-contract.md",
        "diagram": "architecture",
    },
    {
        "n": 10, "title": "Prompt Failure Modes and Adversarial Testing", "duration": "120 minutes",
        "question": "How will this prompt fail under pressure?",
        "outcomes": [
            "Recognize ambiguity, scope drift, evidence fabrication, authority leakage, and schema failure.",
            "Design adversarial cases for missing, conflicting, malicious, and excessive inputs.",
            "Specify safe failure behavior instead of optimistic guessing.",
        ],
        "concepts": [
            ("Scope drift", "The agent answers adjacent questions it does not own."),
            ("Authority leakage", "Recommendations or scores become approvals or decisions."),
            ("Evidence laundering", "Unsupported claims appear credible after synthesis."),
            ("Prompt injection", "Input content attempts to override the governing instruction hierarchy."),
        ],
        "flow": ["Failure taxonomy", "Bad prompt teardown", "Adversarial case design", "Red-team exchange", "Repair sprint"],
        "lab": "Attack another team’s prompt with eight cases: missing inputs, contradictory evidence, stale evidence, malicious repository text, huge context, tool failure, schema conflict, and pressure to approve.",
        "prompt_lab": "Add explicit behavior for each attack without turning the prompt into an unreadable exception list.",
        "assessment": "Learner demonstrates that the repaired prompt fails closed, preserves provenance, and requests human action when appropriate.",
        "misconceptions": ["Prompt injection is only a web-browser problem.", "Refusal is the only safe failure behavior.", "A JSON schema prevents semantic overreach."],
        "source": "contracts/style-and-validation.md; contracts/sandboxed-contract-evolution.md; governance/integration-boundaries.md",
        "diagram": "state",
    },
    {
        "n": 11, "title": "Evaluation, Calibration, and Prompt Evolution", "duration": "120 minutes",
        "question": "How do we know a prompt is improving rather than merely changing?",
        "outcomes": [
            "Build a contract-derived evaluation rubric and test corpus.",
            "Measure completeness, grounding, boundary adherence, calibration, and usefulness.",
            "Evolve prompts and contracts through controlled, auditable change.",
        ],
        "concepts": [
            ("Evaluation case", "Inputs plus expected invariants and failure behavior."),
            ("Calibration", "Confidence and severity correspond to evidence strength and impact."),
            ("Regression", "A previously satisfied invariant no longer holds."),
            ("Sandboxed evolution", "Propose, test, compare, approve, and version changes before adoption."),
        ],
        "flow": ["Rubric design", "Golden cases and invariants", "Calibration exercise", "A/B prompt test", "Change governance"],
        "lab": "Score two prompt versions against the same test corpus. Teams may recommend adoption only when they can explain gains, regressions, and uncertainty.",
        "prompt_lab": "Create a ten-case evaluation suite for the team’s agent, including at least three negative and two conflict cases.",
        "assessment": "Learner produces a scorecard with observable criteria and a versioning recommendation tied to semantic impact.",
        "misconceptions": ["One impressive demo proves prompt quality.", "Higher finding count means better review.", "Prompt edits do not require version discipline."],
        "source": "governance/reviewer-calibration-and-evolution.md; contracts/sandboxed-contract-evolution.md; contracts/style-and-validation.md",
        "diagram": "prompt",
    },
    {
        "n": 12, "title": "Prompt Factory Capstone", "duration": "180 minutes",
        "question": "Can the team ship a prompt package that another team can operate and audit?",
        "outcomes": [
            "Produce a complete prompt package for assigned catalog agents.",
            "Demonstrate contract compliance through tests and traceability.",
            "Conduct a human review that accepts, rejects, or requests changes with evidence.",
        ],
        "concepts": [
            ("Prompt package", "Prompt, trace matrix, examples, tests, scores, known limits, and version record."),
            ("Coverage plan", "How the class will draft and review all 55 catalog agents."),
            ("Peer gate", "Independent verification before instructor acceptance."),
            ("Operational handoff", "Enough clarity for a new engineer to run and maintain the agent."),
        ],
        "flow": ["Team assignments", "Drafting sprint", "Adversarial test", "Peer gate", "Demo and review"],
        "lab": "Each team completes its assigned agent bundle, runs the evaluation suite, and demonstrates one success, one incomplete-input path, one conflict path, and one authority-boundary path.",
        "prompt_lab": "Finalize the production candidate and document every intentional deviation from the shared prompt modules.",
        "assessment": "A human review panel scores the package and records a decision request: accept as baseline, accept as seed, or return for change.",
        "misconceptions": ["The prompt text alone is the deliverable.", "Passing the happy path is sufficient.", "A capstone score grants autonomous deployment authority."],
        "source": "agents/agent-registry.md; contracts/universal-agent-contract.md; governance/human-review-and-maturity.md",
        "diagram": "orchestration",
    },
]


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_row_cant_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:cantSplit")) is None:
        tr_pr.append(OxmlElement("w:cantSplit"))


def style_table(table, widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    if widths:
        for row in table.rows:
            for idx, width in enumerate(widths):
                row.cells[idx].width = Inches(width)
    for idx, row in enumerate(table.rows):
        set_row_cant_split(row)
        for cell in row.cells:
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if idx == 0:
                set_cell_shading(cell, LIGHT)
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.bold = True
                        r.font.color.rgb = RGBColor.from_string(DARK_BLUE)
    if table.rows:
        set_repeat_table_header(table.rows[0])


def add_field(paragraph, instr):
    run = paragraph.add_run()
    fld_char = OxmlElement("w:fldChar")
    fld_char.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = instr
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "1"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char, instr_text, fld_sep, placeholder, fld_end])


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    p.add_run(text)
    return p


def new_numbering_instance(doc, start=1):
    numbering = doc.part.numbering_part.element
    abstract_ids = [
        int(node.get(qn("w:abstractNumId")))
        for node in numbering.findall(qn("w:abstractNum"))
    ]
    num_ids = [
        int(node.get(qn("w:numId")))
        for node in numbering.findall(qn("w:num"))
    ]
    abstract_id = max(abstract_ids, default=-1) + 1
    num_id = max(num_ids, default=0) + 1

    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)
    level = OxmlElement("w:lvl")
    level.set(qn("w:ilvl"), "0")
    start_node = OxmlElement("w:start")
    start_node.set(qn("w:val"), str(start))
    level.append(start_node)
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), "decimal")
    level.append(num_fmt)
    level_text = OxmlElement("w:lvlText")
    level_text.set(qn("w:val"), "%1.")
    level.append(level_text)
    level_jc = OxmlElement("w:lvlJc")
    level_jc.set(qn("w:val"), "left")
    level.append(level_jc)
    p_pr = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "720")
    tabs.append(tab)
    p_pr.append(tabs)
    indent = OxmlElement("w:ind")
    indent.set(qn("w:left"), "720")
    indent.set(qn("w:hanging"), "360")
    p_pr.append(indent)
    level.append(p_pr)
    abstract.append(level)
    numbering.append(abstract)

    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract_ref = OxmlElement("w:abstractNumId")
    abstract_ref.set(qn("w:val"), str(abstract_id))
    num.append(abstract_ref)
    numbering.append(num)
    return num_id


def add_number(doc, text, num_id):
    p = doc.add_paragraph()
    p_pr = p._p.get_or_add_pPr()
    num_pr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num = OxmlElement("w:numId")
    num.set(qn("w:val"), str(num_id))
    num_pr.extend([ilvl, num])
    p_pr.append(num_pr)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.25
    p.add_run(text)
    return p


def add_callout(doc, title, text, fill=PALE_BLUE):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_row_cant_split(table.rows[0])
    cell = table.cell(0, 0)
    set_cell_shading(cell, fill)
    set_cell_margins(cell, 140, 180, 140, 180)
    p = cell.paragraphs[0]
    run = p.add_run(title + "  ")
    run.bold = True
    run.font.color.rgb = RGBColor.from_string(DARK_BLUE)
    p.add_run(text)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_source(doc, source):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("Repository basis: ")
    r.bold = True
    r.font.color.rgb = RGBColor.from_string(DARK_BLUE)
    p.add_run(source)


def configure_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor.from_string(INK)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.25
    for name, size, color, before, after in [
        ("Heading 1", 16, BLUE, 18, 10),
        ("Heading 2", 13, BLUE, 14, 7),
        ("Heading 3", 12, DARK_BLUE, 10, 5),
    ]:
        style = doc.styles[name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
    for style_name in ["List Bullet", "List Bullet 2", "List Number"]:
        s = doc.styles[style_name]
        s.font.name = "Calibri"
        s.font.size = Pt(11)
        s.paragraph_format.space_after = Pt(4)
        s.paragraph_format.line_spacing = 1.25


def add_cover(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Inches(1.1)
    r = p.add_run("ENGINEERING ENABLEMENT")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor.from_string(BLUE)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(22)
    p.paragraph_format.space_after = Pt(16)
    r = p.add_run("Code Review Harness\nAgentic System Curriculum")
    r.bold = True
    r.font.size = Pt(30)
    r.font.color.rgb = RGBColor.from_string(INK)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(30)
    r = p.add_run("Instructor guide, learner labs, prompt-engineering standard, and 55-agent drafting plan")
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor.from_string(MID)

    add_callout(
        doc,
        "Core philosophy",
        "Evidence is observable. Assessment is bounded. Recommendations inform. Humans decide.",
        PALE_BLUE,
    )
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Inches(1.4)
    p.add_run("Repository-aligned edition").bold = True
    p.add_run("\nBased on the Agent Catalog, universal and layer contracts, workflow model, and governance guidance.")
    p.add_run("\nPrepared for young engineers learning to design, operate, and test contract-driven agents.")
    doc.add_page_break()


def add_front_matter(doc, diagrams):
    doc.add_heading("How to use this curriculum", level=1)
    doc.add_paragraph(
        "This is a twelve-session progression from first principles to a production-style prompt package. "
        "The course treats prompts as governed software artifacts: they inherit contracts, operate inside a stateful harness, "
        "produce typed artifacts, preserve evidence, and stop at the boundary of human authority."
    )
    add_callout(doc, "Recommended delivery", "Two sessions per week for six weeks, or one session per week for a twelve-week academy. Sessions 3–11 are designed for 120 minutes; the capstone uses 180 minutes.")
    doc.add_heading("Course-level outcomes", level=2)
    for text in [
        "Explain why the harness—not the model—is the trust boundary for agentic review.",
        "Read the catalog and route work to the correct agent, contract, and consumer.",
        "Design stateful workflows with explicit guards, failure paths, and human decision points.",
        "Draft role prompts that implement inherited contracts without scope or authority leakage.",
        "Test prompts against adversarial cases and evolve them through controlled evidence.",
        "Produce reviewed prompt packages for every agent in the catalog.",
    ]:
        add_bullet(doc, text)
    doc.add_heading("Course map", level=2)
    table = doc.add_table(rows=1, cols=4)
    for i, h in enumerate(["Phase", "Sessions", "Emphasis", "Learner artifact"]):
        table.rows[0].cells[i].text = h
    rows = [
        ("Foundations", "1–3", "Harness philosophy and evidence", "Evidence-flow map"),
        ("Architecture", "4–7", "Contracts, identities, states, orchestration", "Validated workflow design"),
        ("Prompt engineering", "8–11", "Drafting, specialization, red-teaming, evaluation", "Tested prompt candidate"),
        ("Capstone", "12", "Factory-scale authoring and review", "Operational prompt package"),
    ]
    for row in rows:
        cells = table.add_row().cells
        for i, text in enumerate(row):
            cells[i].text = text
    style_table(table, [1.1, 0.8, 2.5, 2.1])
    doc.add_picture(str(diagrams["harness"]), width=Inches(6.35))
    cap = doc.add_paragraph("Figure 1. The harness controls evidence, execution, validation, and routing.")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    doc.add_heading("Facilitation schema used in every session", level=2)
    facilitation_num_id = new_numbering_instance(doc)
    for item in [
        "Open with a concrete failure or decision question.",
        "Teach one mental model and tie it to repository artifacts.",
        "Walk a worked example using canonical agent and contract language.",
        "Run a guided lab that creates an inspectable artifact.",
        "Draft or improve a prompt component.",
        "Evaluate with a contract-derived exit ticket.",
    ]:
        add_number(doc, item, facilitation_num_id)
    doc.add_heading("Assessment philosophy", level=2)
    doc.add_paragraph(
        "Score observable behavior, not eloquence. Learners earn credit when their artifacts are grounded, complete, bounded, "
        "reproducible, calibrated, consumer-ready, and explicit about human authority. Every session contributes evidence to the capstone."
    )
    add_source(doc, "README.md; docs/philosophy.md; agents/agent-registry.md; contracts/contract-catalog.md")
    doc.add_page_break()


def add_session(doc, session, diagrams):
    doc.add_heading(f"Session {session['n']}: {session['title']}", level=1)
    p = doc.add_paragraph()
    p.add_run("Duration: ").bold = True
    p.add_run(session["duration"])
    p.add_run("   |   Driving question: ").bold = True
    p.add_run(session["question"])
    doc.add_heading("Learning outcomes", level=2)
    for item in session["outcomes"]:
        add_bullet(doc, item)
    doc.add_picture(str(diagrams[session["diagram"]]), width=Inches(6.35))
    cap = doc.add_paragraph(f"Session visual: {session['title']}.")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    doc.add_heading("Core mental model", level=2)
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Concept"
    table.rows[0].cells[1].text = "Working definition"
    for name, desc in session["concepts"]:
        cells = table.add_row().cells
        cells[0].text = name
        cells[1].text = desc
    style_table(table, [1.55, 4.75])
    doc.add_heading("Facilitation run of show", level=2)
    run_of_show_num_id = new_numbering_instance(doc)
    for item in session["flow"]:
        add_number(doc, f"{item}.", run_of_show_num_id)
    doc.add_heading("Instructor narrative", level=2)
    doc.add_paragraph(
        f"Open by asking: “{session['question']}” Accept initial answers, but require learners to name observable controls, "
        "contract fields, states, or evidence links. Use the diagram to build a shared vocabulary. Keep returning to the distinction "
        "between what the system may observe, what an agent may assess, and what a human must decide."
    )
    doc.add_paragraph(
        "During the worked example, narrate the artifact boundaries aloud: identify the producer, contract version, input evidence, "
        "coverage, confidence, consumer, and decision request. When learners use broad language, ask which agent owns that question "
        "and which evidence supports the claim."
    )
    doc.add_heading("Guided lab", level=2)
    add_callout(doc, "Team task", session["lab"], PALE_GREEN)
    doc.add_heading("Prompt engineering lab", level=2)
    add_callout(doc, "Drafting task", session["prompt_lab"], PALE_AMBER)
    doc.add_heading("Exit ticket and evidence of learning", level=2)
    doc.add_paragraph(session["assessment"])
    doc.add_heading("Watch for these misconceptions", level=2)
    for item in session["misconceptions"]:
        add_bullet(doc, item)
    doc.add_heading("Facilitator prompts", level=2)
    for item in [
        "What contract or repository source makes that statement true?",
        "What evidence would change your assessment?",
        "Who consumes this artifact, and what do they need preserved?",
        "What happens when required input is missing or conflicting?",
        "Where does human decision authority enter the flow?",
    ]:
        add_bullet(doc, item)
    add_source(doc, session["source"])
    if session["n"] != 12:
        doc.add_page_break()


PROMPT_TEMPLATE = [
    ("1. Identity and version", "Canonical designation, immutable UUID, display name, layer, contract version, status, and role specification."),
    ("2. Mission and authoritative question", "One owned question, the purpose of answering it, and the declared consumers."),
    ("3. Authority boundary", "The agent may observe, assess, and recommend within scope. It never approves, accepts risk, or substitutes for the human decision authority."),
    ("4. Inputs and evidence admission", "Required inputs, accepted evidence types, provenance rules, freshness, trust boundaries, and incomplete-input behavior."),
    ("5. Scope and exclusions", "Included systems, files, time horizon, criteria, and explicit adjacent questions owned elsewhere."),
    ("6. Method", "Ordered review procedure, criteria, required checks, tools, stopping rules, and treatment of conflicting evidence."),
    ("7. State behavior", "Ready guards, running behavior, validation conditions, retry rules, and terminal states."),
    ("8. Output contract", "Exact universal envelope plus applicable finding/CAPA, pattern/insight, synthesis, or orchestration fields."),
    ("9. Confidence and integrity", "Calibrated confidence, coverage limits, conflicts, integrity checks, and prohibition on fabricated evidence."),
    ("10. Decision requests and consumers", "Questions requiring human action, downstream consumers, routing metadata, and no autonomous decision language."),
]


def add_prompt_standard(doc, diagrams):
    doc.add_page_break()
    doc.add_heading("Platform Prompt Engineering Standard", level=1)
    doc.add_paragraph(
        "On this platform, a prompt is not a free-form persona. It is an executable projection of the agent’s registered identity, "
        "inherited contracts, role specification, workflow state, admissible evidence, and output obligations. The prompt should be "
        "shorter than the combined contracts because it references stable shared rules, but it must be complete enough that omissions "
        "cannot silently change behavior."
    )
    doc.add_picture(str(diagrams["prompt"]), width=Inches(6.35))
    doc.add_heading("Universal prompt template", level=2)
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Prompt block"
    table.rows[0].cells[1].text = "Required content"
    for name, text in PROMPT_TEMPLATE:
        cells = table.add_row().cells
        cells[0].text = name
        cells[1].text = text
    style_table(table, [2.0, 4.3])
    doc.add_heading("Contract-to-prompt trace matrix", level=2)
    table = doc.add_table(rows=1, cols=5)
    for i, h in enumerate(["Requirement ID", "Source", "Prompt clause", "Test case", "Status"]):
        table.rows[0].cells[i].text = h
    for row in [
        ("UAC-AUTH-01", "Universal contract", "Decision authority remains human", "Pressure-to-approve", "Draft"),
        ("EVID-PROV-01", "Evidence contract", "Every claim cites evidence ID", "Missing provenance", "Draft"),
        ("ROLE-SCOPE-01", "Role spec", "Assess only the authoritative question", "Adjacent-domain bait", "Draft"),
        ("FLOW-INCOMP-01", "Workflow model", "Emit incomplete_input when guards fail", "Missing prerequisite", "Draft"),
    ]:
        cells = table.add_row().cells
        for i, text in enumerate(row):
            cells[i].text = text
    style_table(table, [1.15, 1.15, 1.55, 1.35, 0.75])
    doc.add_heading("Prompt quality gates", level=2)
    gates = [
        ("Grounding", "Every non-trivial assessment is traceable to admitted evidence."),
        ("Completeness", "All inherited and role-specific obligations are implemented."),
        ("Boundary adherence", "The agent answers only its authoritative question."),
        ("Authority", "Human decisions are requested, never silently taken."),
        ("State correctness", "Missing inputs, failures, retries, and supersession are explicit."),
        ("Consumer fitness", "Downstream agents can parse, validate, and use the artifact."),
        ("Calibration", "Severity and confidence reflect evidence strength and impact."),
        ("Adversarial resilience", "Malicious or conflicting inputs do not override governing instructions."),
    ]
    table = doc.add_table(rows=1, cols=3)
    for i, h in enumerate(["Gate", "Pass condition", "Score"]):
        table.rows[0].cells[i].text = h
    for name, desc in gates:
        cells = table.add_row().cells
        cells[0].text = name
        cells[1].text = desc
        cells[2].text = "0–3"
    style_table(table, [1.35, 4.35, 0.6])
    doc.add_paragraph("Recommended release threshold: no zeroes, at least 20/24 overall, and mandatory passes for grounding, authority, and state correctness.")
    doc.add_heading("Adversarial test suite", level=2)
    for item in [
        "Required input is absent, malformed, stale, or outside the declared scope.",
        "Two high-quality evidence items conflict.",
        "Repository text attempts to redefine the agent’s role or output format.",
        "A stakeholder pressures the agent to approve, waive, or accept risk.",
        "The context is too large; relevant evidence competes with irrelevant volume.",
        "A required tool fails or returns partial results.",
        "An example output conflicts with the current schema.",
        "A downstream consumer expects a field that the prompt omitted.",
        "The run is superseded by a newer evidence set while in progress.",
        "A synthesis input has high confidence but weak provenance.",
    ]:
        add_bullet(doc, item)
    add_source(doc, "contracts/universal-agent-contract.md; contracts/style-and-validation.md; contracts/sandboxed-contract-evolution.md")


def add_agent_matrix(doc):
    doc.add_page_break()
    doc.add_heading("55-Agent Prompt Drafting Matrix", level=1)
    doc.add_paragraph(
        "Use this matrix to assign the catalog across teams. Every row produces the same seven-item package: prompt, trace matrix, "
        "positive example, incomplete-input example, conflict example, adversarial test suite, and evaluation scorecard. "
        "Baseline agents should target operational completeness; seed agents should document domain-design gaps; planned agents should "
        "remain design candidates until their contracts are ready."
    )
    registry = json.loads((ROOT / "agents" / "agent-identities.json").read_text(encoding="utf-8"))
    agents = registry["agents"]
    layer_order = ["specialist", "product", "capability", "enterprise", "work", "orchestration"]
    for layer in layer_order:
        doc.add_heading(layer.title() + " layer", level=2)
        subset = [a for a in agents if a["layer"] == layer]
        table = doc.add_table(rows=1, cols=5)
        for i, h in enumerate(["Designation", "Agent", "Status", "Contract", "Draft owner"]):
            table.rows[0].cells[i].text = h
        for agent in subset:
            cells = table.add_row().cells
            cells[0].text = agent["designation"]
            cells[1].text = agent["display_name"]
            cells[2].text = agent["status"]
            cells[3].text = agent["contract_version"]
            cells[4].text = "Team ___"
        style_table(table, [1.15, 2.55, 0.75, 0.8, 0.85])
    add_source(doc, "agents/agent-identities.json; agents/agent-registry.md")


def add_capstone(doc):
    doc.add_page_break()
    doc.add_heading("Capstone Package and Review Rubric", level=1)
    doc.add_heading("Required package", level=2)
    deliverables = [
        ("PROMPT.md", "Production candidate with identity, authority, inputs, scope, method, states, output, confidence, and consumers."),
        ("TRACE-MATRIX.md", "One row per inherited or role-specific requirement."),
        ("EXAMPLES/", "Success, incomplete-input, conflict, failure, and decision-request examples."),
        ("EVAL-CASES/", "At least ten repeatable cases with expected invariants."),
        ("SCORECARD.md", "Results, failures, calibration notes, and known limits."),
        ("VERSION.md", "Contract version, prompt version, change rationale, reviewers, and disposition."),
    ]
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Artifact"
    table.rows[0].cells[1].text = "Acceptance evidence"
    for row in deliverables:
        cells = table.add_row().cells
        cells[0].text, cells[1].text = row
    style_table(table, [1.55, 4.75])
    doc.add_heading("Human review questions", level=2)
    for item in [
        "Does the package implement the universal and layer contracts without contradiction?",
        "Is the authoritative question narrow, testable, and distinct from neighboring agents?",
        "Can every assessment be reproduced from stable evidence references?",
        "Are missing, conflicting, malicious, and superseded inputs handled safely?",
        "Does the output preserve what downstream consumers require?",
        "Are confidence, severity, and recommendations calibrated?",
        "Does the agent stop before approval, risk acceptance, or governance decisions?",
        "Do the tests demonstrate invariants rather than reward a single preferred wording?",
    ]:
        add_bullet(doc, item)
    doc.add_heading("Disposition", level=2)
    add_callout(
        doc,
        "Decision request",
        "Select one: accept as baseline; accept as seed with documented gaps; return for change; or reject because the role duplicates another agent. Record evidence and reviewer identity.",
        PALE_AMBER,
    )
    doc.add_heading("Instructor scoring rubric", level=2)
    table = doc.add_table(rows=1, cols=4)
    for i, h in enumerate(["Dimension", "3 — strong", "2 — usable", "1/0 — revise"]):
        table.rows[0].cells[i].text = h
    rows = [
        ("Contract fidelity", "Complete and traceable", "Minor omissions", "Contradictory or missing"),
        ("Evidence discipline", "Reproducible provenance", "Some weak links", "Unsupported claims"),
        ("Boundaries", "Precise authority and scope", "Mostly bounded", "Leaks or duplicates"),
        ("State behavior", "All key paths explicit", "Happy path plus failures", "Implicit or unsafe"),
        ("Output integrity", "Schema and semantics pass", "Small format defects", "Consumer-breaking"),
        ("Evaluation", "Adversarial and calibrated", "Adequate cases", "Demo-only"),
        ("Handoff", "Operable by a new team", "Needs coaching", "Author-dependent"),
    ]
    for row in rows:
        cells = table.add_row().cells
        for i, text in enumerate(row):
            cells[i].text = text
    style_table(table, [1.15, 1.75, 1.65, 1.75])
    add_source(doc, "governance/human-review-and-maturity.md; governance/reviewer-calibration-and-evolution.md")


def add_reference(doc):
    doc.add_page_break()
    doc.add_heading("Repository Reading Guide", level=1)
    refs = [
        ("Start here", "README.md; docs/philosophy.md"),
        ("Catalog and identity", "agents/agent-registry.md; agents/agent-identities.json; agents/agent-naming-and-identity-standard.md"),
        ("Architecture", "agents/hierarchical-agent-architecture.md; agents/enterprise/enterprise-agent-framework.md"),
        ("Contract system", "contracts/contract-catalog.md; contracts/contract-dependency-graph.md; contracts/universal-agent-contract.md"),
        ("Evidence and outputs", "contracts/evidence-contract.md; contracts/evidence-flow-model.md; contracts/capa-contract.md; contracts/pattern-and-insight-contract.md"),
        ("Layer rules", "contracts/specialist-agent-contract.md; product-agent-contract.md; capability-delivery-contract.md; enterprise-agent-contract.md"),
        ("Workflow", "orchestration/workflow-model.md; contracts/orchestration-agent-contract.md; contracts/work-agent-contract.md"),
        ("Quality and evolution", "contracts/style-and-validation.md; contracts/sandboxed-contract-evolution.md; governance/reviewer-calibration-and-evolution.md"),
        ("Human governance", "governance/human-review-and-maturity.md; governance/integration-boundaries.md"),
    ]
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Topic"
    table.rows[0].cells[1].text = "Repository sources"
    for topic, source in refs:
        cells = table.add_row().cells
        cells[0].text, cells[1].text = topic, source
    style_table(table, [1.55, 4.75])
    doc.add_heading("Instructor preparation checklist", level=2)
    for item in [
        "Select a small repository change that is safe to use in every worked example.",
        "Prepare one valid and one deliberately invalid artifact for each layer introduced.",
        "Assign agents to teams before Session 9 so specialization work accumulates.",
        "Keep contract documents open during labs; discourage memory-based guessing.",
        "Record prompt changes and test results as versioned engineering artifacts.",
        "Use human review language consistently: assess, recommend, request, decide.",
    ]:
        add_bullet(doc, item)
    add_callout(doc, "Final reminder", "The system is trustworthy only when evidence, contracts, state, prompts, and human authority agree.")


def build():
    diagrams = make_diagrams()
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    configure_styles(doc)

    header = section.header
    hp = header.paragraphs[0]
    hp.text = "CODE REVIEW HARNESS  |  ENGINEERING ENABLEMENT"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in hp.runs:
        run.font.name = "Calibri"
        run.font.size = Pt(8)
        run.font.bold = True
        run.font.color.rgb = RGBColor.from_string(BLUE)

    footer = section.footer
    table = footer.add_table(rows=1, cols=3, width=Inches(6.5))
    table.autofit = False
    left, center, right = table.rows[0].cells
    left.paragraphs[0].add_run("Agentic System Curriculum")
    center.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    center.paragraphs[0].add_run("Human decision authority")
    right.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_field(right.paragraphs[0], "PAGE")
    for cell in table.rows[0].cells:
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(8)
                run.font.color.rgb = RGBColor.from_string(MID)

    add_cover(doc)
    add_front_matter(doc, diagrams)
    for session in SESSIONS:
        add_session(doc, session, diagrams)
    add_prompt_standard(doc, diagrams)
    add_agent_matrix(doc)
    add_capstone(doc)
    add_reference(doc)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
