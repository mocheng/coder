# AGENTS.md

Authoritative specification of autonomous (or semi‑autonomous) agent roles, interaction contracts, guardrails, and evolution roadmap for this repository. This file is read at startup to guide AI assistance. It supersedes any prior agent design notes.

## 1. Purpose & Scope
Provide a clear, incremental path from the current single "Reviewer" capability toward a modular constellation of cooperating agents that operate under a Kanban, confirmation‑driven workflow (see spec/workflow.md & spec/kanban.md). All automation MUST remain user‑approved, minimal, reversible, and safety‑conscious.

## 2. Core Principles
- Human Confirmation First: No file mutations or board updates without explicit approval.
- Kanban Flow Enforcement: WIP limit = 1 active development task.
- Incremental Expansion: Add one agent capability at a time; ship value early.
- Structured Outputs Preferred: When possible, agents emit JSON + human summary.
- Deterministic Transparency: Every agent action declares rationale, inputs, and proposed outputs before execution.
- Non‑Destructive Defaults: Read / analyze > generate patch proposals > apply only if approved.

## 3. Current Implemented Capability (Reviewer Agent)
The existing CLI command `cr` orchestrates a synchronous review pipeline:
1. Parse Input (file / git diff / commit / branch) – input_parser.py
2. Collect Sources & Diffs – source_collector.py + git_operations.py
3. Analyze with LLM – llm_client.py + review_orchestrator.py
4. Present Findings & Inline Context – results_formatter.py + code_context.py

This set = ReviewerAgent (monolithic). All other agents are conceptual until implemented.

## 4. Target Agent Roles
| Agent | Mission | Initial Deliverable | Escalation Path |
|-------|---------|---------------------|-----------------|
| BacklogCurator | Surface new improvement tasks from diffs/architecture | Draft K### tasks (not auto-added) | Retry with refined filters |
| TriageAnalyst | Score & suggest movement of tasks to Ready | Priority + Feasibility + Size table | Ask user to split / defer |
| ImplementationPlanner | Produce PlanOutline before coding | Modules list + test intents + risks | Request clarification on ambiguity |
| ReviewerAgent (exists) | Identify actionable issues in code/diffs | Structured ReviewFindings | Re-run narrowed scope prompt |
| RefactorAdvisor | Suggest safe, minimal refactors | Patch previews (diff blocks) | Defer if risk > threshold |
| TestStrategist | Detect coverage gaps & propose tests | TestGap objects + stub templates | Flag missing metrics |
| DocumentationSynthesizer | Summarize accepted changes | Draft changelog / README delta | Ask for scope trimming |
| GovernanceGatekeeper | Enforce workflow rules & confirmations | Validation report | Block action; propose resolution |

## 5. Data Contracts (Planned)
All structures are additive; fall back to plain text if model output not parseable.
```jsonc
TaskDescriptor {
  id: string,             // K### (assigned only after approval)
  title: string,
  description: string,
  acceptance_criteria: string[],
  size_estimate: "S"|"M"|"L",
  risk_score: 1-5
}
ReviewFinding {
  file: string,
  line: number|null,      // null for file-level issues
  severity: "low"|"medium"|"high"|"critical",
  category: string,       // e.g. security, performance, correctness, style
  message: string,
  suggestion?: string
}
PlanOutline {
  task_id: string,
  rationale: string,
  modules: string[],
  test_items: string[],
  risks: string[]
}
TestGap {
  file: string,
  symbol: string,
  rationale: string,
  suggested_test_stub: string
}
AgentAction {
  agent: string,
  type: string,           // e.g. "ADD_TASKS", "MOVE_TASK", "APPLY_PATCH"
  preview_diff?: string,
  description: string,
  requires_confirmation: true
}
```

## 6. Interaction & Escalation Rules
1. Every multi-step process ends with an explicit question: proceed? y/n/adjust.
2. If schema parse fails → provide raw model text + offer retry with tightened prompt.
3. If ambiguity detected (missing acceptance criteria, conflicting size vs scope) → agent must ask rather than assume.
4. GovernanceGatekeeper validates: (a) WIP limit, (b) Required plan exists before implementation, (c) Post-review tasks optionally spawned (not auto‑accepted).
5. No agent self‑approves its own proposed state change.

## 7. Prompt Design Guidelines
- Always constrain scope: “Only include high‑impact issues; exclude nit style unless blocking.”
- Request dual output: concise JSON array + human-readable markdown summary.
- Include explicit FAIL SAFE clause: “If uncertain, respond with NEED_CLARIFICATION and list questions.”
- For review diffs: emphasize ADDED lines primary, REMOVED for context only.

## 8. Security & Safety
- Never execute arbitrary code.
- Never write outside repository root.
- Strip tokens / credentials from model context.
- RefactorAdvisor patches limited to explicit line ranges; no mass rewrites.

## 9. Minimal Near-Term Implementation Roadmap
Stage 1: (K011) Enhance ReviewerAgent prompt to request JSON ReviewFinding[] + summary (graceful fallback).  
Stage 2: (K012) Severity + category colorization in results_formatter.py.  
Stage 3: (K013) BacklogCurator prototype (dry run scanning recent git diff).  
Stage 4: (K014) TriageAnalyst scoring heuristic (lines touched, risk keywords, file criticality).  
Stage 5: (K015) ImplementationPlanner enforcing PlanOutline before coding task accepted.  
Stage 6: (K016) TestStrategist coverage gap extraction (parse pytest --cov JSON output if available).  
Stage 7: (K017) GovernanceGatekeeper decorator to protect state transitions.  
Stage 8: (K018) DocumentationSynthesizer changelog draft.

## 10. Success Metrics
- Structured findings parse success rate > 85% after Stage 1.
- False-positive review items reduced (subjective user feedback) after severity filtering.
- Time from code change to accepted task creation reduced (qualitative) with Curator.
- Coverage maintained ≥ 80% after introducing TestStrategist.

## 11. Change Control
Any modification to this file requires an explicit commit referencing rationale (e.g., `docs: update AGENTS.md for Planner schema tweak`). Large structural shifts should propose a task first.

## 12. Open Questions
- Introduce persistent agent state file (e.g., `.coder_state.json`) now or post Stage 3?
- Adopt streaming LLM responses for large diffs? (Deferred until performance need arises.)
- Patch safety scoring heuristics (cyclomatic delta, removed lines ratio) location: Planner or Gatekeeper?

## 13. Summary
This AGENTS.md codifies a disciplined, human‑centric expansion path from a single reviewer into a modular agent ecosystem. Every step emphasizes safety, confirmation, and measurable incremental value.

(End of AGENTS.md)
