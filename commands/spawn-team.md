# /spawn-team - Spawn Agent Team

Spawn the default agent team for this project. Creates a coordinated team of agents that implement features in parallel following the strict TDD pipeline.

**Pipeline:** Specs > Tests > Ensure tests fail > Implement > Test again > /code-review > Create branch > Create PR

---

## Phase 1: Prerequisites Check

### 1.1 Check Agent Teams Environment Variable

```bash
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
```

If not set to `1`:
> Agent teams require the experimental flag. Setting it now:
>
> ```bash
> export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
> ```
>
> To make permanent, add to your settings.json:
> ```json
> { "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
> ```

### 1.2 Check Agent Definitions

Verify `.claude/agents/` exists and has the required agent definitions:

```bash
ls .claude/agents/
```

Required files:
- `team-lead.md`
- `quality.md`
- `security.md`
- `code-review.md`
- `merger.md`
- `feature.md`

If missing, copy from the agent-teams skill:
```bash
cp -r ~/.claude/skills/agent-teams/agents/ .claude/agents/
```

### 1.3 Check Feature Specs

```bash
ls _project_specs/features/
```

If no feature specs exist, ask the user:

> **No feature specs found.** The agent team needs features to implement.
>
> What are the key features of this project? I'll create a spec file for each one.
>
> List your features (e.g., "user authentication, dashboard, payment processing"):

For each feature the user lists:
1. Create `_project_specs/features/{feature-name}.md` with a skeleton:

```markdown
# Feature: {Feature Name}

## Description
{Brief description based on user input}

## Acceptance Criteria
1. TODO: Define acceptance criteria

## Test Cases
| # | Test | Input | Expected Output |
|---|------|-------|-----------------|
| 1 | TODO | TODO | TODO |

## Dependencies
None

## Files
TBD (to be determined by feature agent)
```

2. The feature agent will flesh out the full spec as its first task

### 1.4 Check GitHub CLI

```bash
gh auth status
```

Needed by the merger agent for PR creation. Warn if not authenticated but don't block.

---

## Phase 2: Create Team

Create the team using the project directory name:

```
TeamCreate with team_name = {basename of current working directory}
```

---

## Phase 3: Spawn Default Agents

Spawn the 5 permanent agents. Each agent reads `.claude/agents/{type}.md` for its instructions.

### 3.1 Team Lead
```
Task tool:
  name: "team-lead"
  team_name: {team name}
  subagent_type: "general-purpose"
  mode: "delegate"
  prompt: "You are the team lead. Read .claude/agents/team-lead.md for your full instructions. Read .claude/skills/agent-teams/SKILL.md for the team workflow. Your job is to orchestrate - NEVER write code. Start by reading _project_specs/features/*.md to identify features, then create task chains and spawn feature agents."
```

### 3.2 Quality Agent
```
Task tool:
  name: "quality-agent"
  team_name: {team name}
  subagent_type: "general-purpose"
  prompt: "You are the quality agent. Read .claude/agents/quality.md for your full instructions. You enforce TDD discipline by verifying specs, RED phases (tests fail), and GREEN phases (tests pass + coverage). Watch TaskList for tasks assigned to you. Process them in task ID order."
```

### 3.3 Security Agent
```
Task tool:
  name: "security-agent"
  team_name: {team name}
  subagent_type: "general-purpose"
  prompt: "You are the security agent. Read .claude/agents/security.md for your full instructions. You perform security scans on completed features. Watch TaskList for security-scan tasks assigned to you. Block on Critical/High findings."
```

### 3.4 Code Review Agent
```
Task tool:
  name: "review-agent"
  team_name: {team name}
  subagent_type: "general-purpose"
  prompt: "You are the code review agent. Read .claude/agents/code-review.md for your full instructions. You run /code-review on completed features. Watch TaskList for code-review tasks assigned to you. Block on Critical/High severity."
```

### 3.5 Merger Agent
```
Task tool:
  name: "merger-agent"
  team_name: {team name}
  subagent_type: "general-purpose"
  prompt: "You are the merger agent. Read .claude/agents/merger.md for your full instructions. You create feature branches and PRs for completed features. Watch TaskList for branch-pr tasks assigned to you. NEVER merge - only create PRs."
```

---

## Phase 4: Spawn Feature Agents

For each feature spec in `_project_specs/features/`:

```
Task tool:
  name: "feature-{feature-name}"
  team_name: {team name}
  subagent_type: "general-purpose"
  prompt: "You are the feature agent for {feature-name}. Read .claude/agents/feature.md for your full instructions. Read .claude/skills/agent-teams/SKILL.md for the team workflow. Your feature spec is at _project_specs/features/{feature-name}.md. Start by checking TaskList for your first task ({feature-name}-spec)."
```

---

## Phase 5: Create Task Chains

The team lead creates the task dependency chains. For each feature, 10 tasks are created with `addBlockedBy` dependencies:

```
{name}-spec               -> {name}-spec-review
{name}-spec-review        -> {name}-tests
{name}-tests              -> {name}-tests-fail-verify
{name}-tests-fail-verify  -> {name}-implement
{name}-implement          -> {name}-tests-pass-verify
{name}-tests-pass-verify  -> {name}-validate
{name}-validate           -> {name}-code-review
{name}-code-review        -> {name}-security-scan
{name}-security-scan      -> {name}-branch-pr
```

The team lead handles this automatically based on its instructions.

---

## Phase 6: Team Status Summary

Show the user the team status:

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENT TEAM DEPLOYED                                             │
│  ──────────────────────────────────────────────────────────────  │
│                                                                  │
│  Team: {project-name}                                            │
│  Features: {N}                                                   │
│  Total tasks: {N * 10}                                           │
│                                                                  │
│  AGENTS                                                          │
│  ───────                                                         │
│  ● Team Lead        Orchestrating                                │
│  ● Quality Agent    Watching for verification tasks              │
│  ● Security Agent   Watching for security scan tasks             │
│  ● Code Review      Watching for review tasks                    │
│  ● Merger Agent     Watching for branch/PR tasks                 │
│  ● feature-{name1}  Starting spec for {name1}                   │
│  ● feature-{name2}  Starting spec for {name2}                   │
│  ...                                                             │
│                                                                  │
│  PIPELINE                                                        │
│  ────────                                                        │
│  Spec > Review > Tests > RED Verify > Implement >                │
│  GREEN Verify > Validate > Code Review > Security > Branch+PR    │
│                                                                  │
│  Use Shift+Up/Down to select and message individual agents.      │
│  Use Ctrl+T to toggle the shared task list.                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Monitoring

After the team is spawned, the user can:

- **View task list:** Press Ctrl+T or ask team lead for status
- **Message any agent:** Use Shift+Up/Down to select, then type
- **Check progress:** Ask team lead: "What's the status?"
- **Handle blockers:** Message the blocked agent or team lead

The team runs autonomously until all PRs are created, then the team lead shuts everything down.
