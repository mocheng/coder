# AI Workflow Specification

## Project Overview
Building a CLI Coding Agent using Python with KANBAN-style continuous development.

## KANBAN Process

### Board Columns
1. **Backlog** - All identified tasks and features
2. **Ready** - Tasks with clear requirements, ready to start
3. **In Progress** - Currently being worked on (WIP limit: 1)
4. **Review** - Completed, awaiting user feedback
5. **Done** - Accepted and complete

## Work Item Tracking
Work items are tracked in markdown files:
- `spec/kanban.md` - Current KANBAN board state
- Each work item has: ID, Title, Description, Acceptance Criteria

### Work Flow Rules
- **Pull-based:** Only start new work when current task is complete
- **WIP Limit:** Maximum 1 task in progress at any time
- **Continuous delivery:** Each task should produce working functionality
- **Just-in-time planning:** Define tasks as needed, not all upfront

## AI Work Processes

### 1. Triage Process (Interactive)
**Purpose:** Analyze and prioritize tasks for execution readiness

**Steps:**
1. **Analyze Backlog** - Review all tasks in Backlog column
2. **Assess Priority** - Evaluate business value and user impact
3. **Assess Feasibility** - Evaluate technical complexity and dependencies
4. **Propose Candidates** - Present high priority + high feasibility tasks to user
5. **Get Approval** - Wait for user confirmation on task selection
6. **Move to Ready** - Transfer approved tasks to Ready column

**Trigger:** User requests triage or when Ready column has less than 2 tasks

### 2. Code Process (Autonomous)
**Purpose:** Execute tasks from Ready column

**Steps:**
1. **Pull Task** - Take highest priority task from Ready column
2. **Move to In Progress** - Update KANBAN board
3. **Analyze** - Understand requirements and constraints
4. **Design** - Plan minimal implementation approach
5. **Implement** - Write essential code only
6. **Verify** - Test functionality works
7. **Move to Review** - Present working result to user

**Trigger:** User requests code execution and Ready column has tasks

### Code Standards
- **Minimal viable code** - Write only what's needed
- **LLM-first approach** - Let LLM handle complex analysis
- **Iterative refinement** - Improve based on feedback
- **Clean structure** - Maintain clear separation of concerns

### Decision Making
- Ask for clarification on ambiguous requirements
- Propose options when multiple approaches exist
- Prioritize working software over perfect design
- Focus on immediate user value


