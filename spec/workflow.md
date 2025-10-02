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
- **Ask for Confirmation:** Explicitly ask user if they want to proceed to next workflow

## AI Work Processes

### 1. Feature Brainstorming Process (Interactive)
**Purpose:** Generate new feature ideas based on project objectives and architecture

**Steps:**
1. **Analyze Current State** - Review existing functionality and architecture
2. **Identify Opportunities** - Consider user needs, technical improvements, and extensibility
3. **Propose Features** - Present categorized feature suggestions with rationale
   - **Wait for user feedback** on which features to pursue
4. **Generate Tasks** - Create detailed work items for approved features
   - **Wait for user confirmation** on task details before proceeding
5. **Add to Backlog** - Insert new tasks into Backlog column with proper IDs
   - **Wait for user confirmation** before actually updating kanban.md
6. **Git Commit** - Commit the updated kanban.md with new tasks
   - Format: `feat: Add new tasks [K###-K###] to backlog`

**Trigger:** User requests feature brainstorming or when Backlog is empty

### 2. Triage Process (Interactive)
**Purpose:** Analyze and prioritize tasks for execution readiness

**Steps:**
1. **Analyze Backlog** - Review all tasks in Backlog column
2. **Assess Priority** - Evaluate business value and user impact
3. **Assess Feasibility** - Evaluate technical complexity and dependencies
4. **Propose Candidates** - Present high priority + high feasibility tasks to user
5. **Get Approval** - Wait for user confirmation on task selection
6. **Move to Ready** - Transfer approved tasks to Ready column
7. **Git Commit** - Commit the kanban.md changes
   - Format: `triage: Move [K###] to Ready for development`
8. **Ask for Confirmation** - Explicitly ask user if they want to proceed to Code Process

**Trigger:** User requests triage or when Ready column has less than 2 tasks

### 3. Code Process (Autonomous)
**Purpose:** Execute tasks from Ready column

**Steps:**
1. **Pull Task** - Take highest priority task from Ready column
2. **Move to In Progress** - Update KANBAN board
3. **Analyze** - Understand requirements and constraints
4. **Design** - Plan minimal implementation approach
5. **Implement** - Write essential code only
6. **Write Tests** - Create comprehensive unit tests for all new functionality
7. **Verify** - Test functionality works and all tests pass
8. **Move to Review** - Present working result to user
9. **Ask for Confirmation** - Explicitly ask user for approval to move to Done

**Trigger:** User requests code execution and Ready column has tasks

### 4. Completion Process (On User Approval)
**Purpose:** Finalize completed work with proper version control

**Steps:**
1. **Move to Done** - Update KANBAN board from Review to Done
2. **Git Commit** - Commit all changes with descriptive message
   - Format: `[TaskID] Task Title`
   - Example: `[K002] Basic CLI Structure`
   - Include all modified/created files
3. **Confirm Completion** - Notify user of commit and completion
4. **Ask for Confirmation** - Explicitly ask user what to do next (new features, triage, etc.)

**Trigger:** User approves work in Review column

## Workflow Control Rules

### Mandatory Confirmations
- **After each major workflow step** - Always ask user for confirmation to proceed
- **Before updating kanban.md** - Get explicit approval for any board changes
- **Before starting implementation** - Confirm task selection and approach
- **After completing work** - Get approval before moving to Done

### Git Commit Requirements
- **After feature brainstorming** - Commit new tasks added to backlog
- **After triage** - Commit task movements to Ready
- **After completion** - Commit all implementation changes
- **Never commit without user approval** - All commits require explicit or implicit user consent

### Communication Protocol
- **Explicit questions** - Always end workflow steps with clear questions
- **Wait for responses** - Never proceed without user input on interactive steps
- **Status updates** - Clearly communicate current workflow position
- **Next step proposals** - Always propose what to do next and wait for confirmation

### Code Standards
- **Minimal viable code** - Write only what's needed
- **LLM-first approach** - Let LLM handle complex analysis
- **Iterative refinement** - Improve based on feedback
- **Clean structure** - Maintain clear separation of concerns
- **Comprehensive testing** - Every feature must include unit tests
- **Test coverage** - Aim for minimum 80% coverage on new code
- **Test organization** - Follow tests/ directory structure mirroring src/

### Decision Making
- Ask for clarification on ambiguous requirements
- Propose options when multiple approaches exist
- Prioritize working software over perfect design
- Focus on immediate user value


