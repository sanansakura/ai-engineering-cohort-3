# Multi-Agent Workflow Implementation Guide

This supplementary guide captures best practices for creating ExecPlans that involve multi-agent workflows, git work trees, and granular implementation steps. Use this guide when your ExecPlan requires multiple specialized agents working in sequence or parallel to complete a project.

This document complements PLANS.md and provides specific guidance for complex workflows that benefit from agent specialization, parallel work, and detailed step-by-step orchestration.

## When to Use Multi-Agent Workflows

Multi-agent workflows are appropriate when:

- The work requires distinct phases that benefit from specialized expertise (development, code review, plan alignment, testing, deployment)
- Parallel work is needed without conflicts (using git work trees)
- Quality gates are important (code review, plan verification, automated testing)
- The workflow should minimize human intervention once triggered
- Multiple iterations and feedback loops are expected

## Core Concepts

### Git Work Trees

A Git work tree is a separate working directory that shares the same Git repository but allows independent checkouts. This enables agents to work in parallel without interfering with each other. Each agent can have its own work tree, allowing simultaneous work on different branches or the same branch without conflicts.

**Key benefits:**
- Agents can work independently without blocking each other
- No need to stash or commit incomplete work
- Clean separation of concerns
- Easy cleanup (just remove the work tree directory)

**Basic usage:**
```bash
# Create a work tree in a temporary directory
git worktree add /tmp/agent-work-tree -b feature-branch-name
cd /tmp/agent-work-tree
# Work normally - commits, pushes, etc.
# When done, remove the work tree
git worktree remove /tmp/agent-work-tree
```

### Agent Specialization

Different agents should have distinct, well-defined responsibilities:

- **Development Agent**: Implements code according to the ExecPlan, creates feature branches, handles implementation details
- **Code Review Agent**: Reviews code quality, best practices, correctness, performance, maintainability
- **Plan Alignment Agent**: Verifies implementation matches ExecPlan requirements, manages merge conflicts, ensures completeness
- **Testing Agent** (optional): Runs tests, validates functionality, checks integration
- **Deployment Agent** (optional): Handles deployment configuration, environment setup, deployment verification

Each agent should have clear inputs, outputs, and checkpoints.

### Checkpoints and Handoffs

Agents communicate through Git and GitHub using clear checkpoints:

- **Checkpoint format**: Agent completes work → Signals completion (PR creation, approval, merge) → Next agent begins
- **Communication channels**: Pull requests, PR comments, branch status, merge commits
- **State preservation**: All work is in Git, so workflow can resume from any checkpoint

## ExecPlan Structure for Multi-Agent Workflows

When creating an ExecPlan that uses multi-agent workflows, include these sections:

### Workflow Orchestration and Agent Coordination

This section should detail:

**Initial Trigger (Human Action):**
- What the human must do once to start the workflow
- What information agents need (repository URLs, source paths, branch names)
- Prerequisites that must be in place

**Agent Execution Sequence:**
- Step-by-step sequence of agent actions
- Clear checkpoints between agents
- What each agent waits for before starting
- What each agent signals when complete

**Agent Communication Protocol:**
- How agents communicate (Git, GitHub, PRs, comments)
- What signals trigger the next agent
- How feedback flows between agents

**Work Tree Management:**
- Which agents need work trees and why
- Where work trees are created (temporary directories)
- How work trees are cleaned up

**Error Handling and Recovery:**
- What happens if an agent fails
- How to resume from checkpoints
- Recovery procedures for common failure modes

**Automation Requirements:**
- What tools agents need (Git CLI, GitHub CLI, API access)
- What permissions are required
- What environment setup is needed

### Concrete Steps with Agent-Specific Granularity

Break down steps by agent, with extreme detail:

**For Development Agent:**
- Exact git commands to set up work tree
- Specific file paths and locations
- Detailed code structure and component mapping
- Exact commit messages and PR creation commands
- Step numbering (e.g., Step 1.1, Step 1.2) for clarity

**For Review Agents:**
- Specific review criteria and checklists
- How to read PR diffs and changed files
- What to look for in each category (quality, correctness, performance)
- How to provide feedback (PR comments format)
- Approval criteria and change request triggers

**For Alignment/Verification Agents:**
- Specific files and requirements to verify
- How to check for merge conflicts
- Conflict resolution procedures
- Merge criteria and procedures

### Idempotence and Recovery

Detail how the workflow handles:

**Workflow Idempotence:**
- Which operations can be safely repeated
- How to restart from any checkpoint
- How to clean up and start fresh if needed

**Recovery Scenarios:**
- Agent failure mid-task
- Review feedback requiring changes
- Merge conflicts
- PR restart scenarios
- Deployment failures

**Workflow Interruption:**
- How to detect where the workflow stopped
- How to resume from the last checkpoint
- What state is preserved in Git

## Best Practices for Granular Steps

### Step Organization

1. **Group by Agent**: All steps for Agent 1 together, then Agent 2, etc.
2. **Number Hierarchically**: Use Step X.Y format (e.g., Step 1.1, Step 1.2, Step 2.1)
3. **Include Context**: Each step should be understandable without reading previous steps
4. **Show Commands**: Provide exact commands with variable placeholders
5. **Show Expected Output**: Include sample output or success indicators

### Command Examples

Always show:
- Working directory context
- Exact command syntax
- Variable definitions (REPO_URL, WORK_TREE_DIR, etc.)
- Expected outcomes or how to verify success

Example format:
```bash
# Set up variables
REPO_URL="<repository-url>"
WORK_TREE_DIR="/tmp/project-dev-worktree"
REPO_DIR="/tmp/project-repo"

# Clone repository
git clone $REPO_URL $REPO_DIR
cd $REPO_DIR

# Create work tree
git worktree add $WORK_TREE_DIR -b feature/implementation
cd $WORK_TREE_DIR

# Verify setup
git branch  # Should show feature/implementation checked out
```

### File and Path Specifications

Be extremely specific:
- Use full repository-relative paths
- Specify exact file names and locations
- Include directory structure when creating new files
- Show expected file structure after completion

### Progress Tracking

In the Progress section, break down by agent:
- [ ] Agent 1: Step 1.1 - Set up git work tree
- [ ] Agent 1: Step 1.2 - Extract source code
- [ ] Agent 1: Step 1.3 - Implement feature X
- [ ] Agent 2: Step 2.1 - Review code quality
- [ ] Agent 2: Step 2.2 - Provide feedback
- [ ] Agent 3: Step 3.1 - Verify plan alignment

This makes it clear which agent is responsible for each task and where the workflow is in the sequence.

## Validation and Acceptance for Multi-Agent Workflows

Include acceptance criteria for:

1. **Each Agent's Completion**: What signals that Agent 1, 2, 3, etc. have completed successfully
2. **PR State**: What the PR should look like at each stage
3. **Code Quality**: How to verify code meets standards
4. **Plan Alignment**: How to verify implementation matches ExecPlan
5. **Merge Success**: What indicates successful merge
6. **Final State**: What the repository should look like when complete
7. **Functional Verification**: How to test that the implementation works

## Decision Log for Workflow Design

When designing the workflow, document decisions about:

- **Agent Responsibilities**: Why certain tasks are assigned to specific agents
- **Work Tree Usage**: Why work trees are needed and how they're organized
- **Review Process**: Why certain review criteria are important
- **Iteration Strategy**: How feedback loops work and when to iterate
- **Tool Choices**: Why specific tools (Git, GitHub CLI, etc.) are used

## Example Workflow Pattern

Here's a template pattern you can adapt:

```
## Workflow Orchestration and Agent Coordination

**Initial Trigger (Human Action - One Time):**
1. Create GitHub repository
2. Push ExecPlan to repository
3. Provide agents with: [list of required information]

**Agent Execution Sequence:**

1. **Agent 1 (Development) starts**: 
   - Creates git work tree in temporary directory
   - Creates feature branch
   - Implements code according to ExecPlan
   - Commits and pushes feature branch
   - Creates pull request targeting main branch
   - **Checkpoint**: PR created and ready for review

2. **Agent 2 (Code Review) starts** (after Agent 1 checkpoint):
   - Reads PR diff and all changed files
   - Reviews [specific criteria]
   - Adds PR comments with feedback
   - Approves PR or requests changes
   - **Checkpoint**: PR approved OR change requests provided

3. **Agent 3 (Plan Alignment) starts** (after Agent 2 checkpoint):
   - If Agent 2 requested changes: Wait for Agent 1 to address feedback
   - If Agent 2 approved: Proceed to alignment check
   - Verifies implementation matches ExecPlan requirements
   - Checks for merge conflicts and resolves if needed
   - Merges PR to main if all checks pass
   - **Checkpoint**: PR merged to main OR specific fixes requested

4. **Iteration Loop** (if fixes needed):
   - Agent 1 addresses feedback
   - Pushes new commits to feature branch
   - Agents re-review as needed
   - Loop continues until all agents approve

5. **Completion**:
   - PR merged to main branch
   - Work tree cleaned up
   - Repository ready for [next phase]
```

## Integration with PLANS.md

This guide supplements PLANS.md. When creating an ExecPlan:

1. **Follow PLANS.md structure**: Use the skeleton from PLANS.md (Purpose, Progress, Decision Log, etc.)
2. **Add workflow sections**: Include "Workflow Orchestration and Agent Coordination" section
3. **Enhance Concrete Steps**: Use the granular step format shown here
4. **Expand Idempotence**: Include detailed recovery scenarios
5. **Detail Validation**: Include agent-specific acceptance criteria

The ExecPlan should still be self-contained and follow all PLANS.md requirements, but with the added detail and structure for multi-agent workflows.

## Key Takeaways

1. **Granularity is critical**: Break down every step, especially for agents. What seems obvious to you may not be to an agent executing the plan.

2. **Checkpoints enable recovery**: Clear checkpoints allow the workflow to resume from any point if interrupted.

3. **Work trees enable parallelism**: Use git work trees to allow agents to work without conflicts.

4. **Communication through Git**: Use PRs, comments, and branch status as the communication mechanism between agents.

5. **Idempotence enables safety**: Design every step to be safely repeatable.

6. **Document decisions**: Use the Decision Log to explain why the workflow is structured a certain way.

7. **Test locally first**: Before deploying a multi-agent workflow, verify that individual agent steps work correctly.

8. **Plan for failure**: Include comprehensive recovery scenarios so the workflow can handle unexpected situations gracefully.

