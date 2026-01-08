# Initialize Project

Full project setup with Claude coding guardrails. Works for both new and existing projects.

**This command is idempotent** - run it anytime to update skills, add missing structure, or reconfigure.

---

## Phase 0: Validate Bootstrap Installation

**FIRST**, verify claude-bootstrap is properly installed:

```bash
# Run quick validation
~/.claude-bootstrap/tests/validate-structure.sh --quick
```

This checks:
- Skills are installed with correct structure (folder/SKILL.md)
- Commands are installed (~/.claude/commands/)
- Hooks are installed (~/.claude/hooks/)

**If validation fails:**
- Show the error to user
- Suggest running: `cd ~/.claude-bootstrap && git pull && ./install.sh`
- Offer to continue anyway or abort

**If validation passes:**
- Continue to Phase 1

---

## Phase 1: Detect Project State

First, check what already exists:

```bash
# Check for existing Claude setup
ls -la .claude/skills/ 2>/dev/null
ls -la CLAUDE.md 2>/dev/null
ls -la _project_specs/ 2>/dev/null

# Check for existing git repo
git remote -v 2>/dev/null

# Check for existing package files
ls package.json pyproject.toml 2>/dev/null
```

Based on findings, determine:
- **New project**: No CLAUDE.md, no .claude/skills/
- **Existing project with skills**: Has .claude/skills/ - offer to UPDATE
- **Existing codebase without skills**: Has code but no Claude setup - offer to ADD

Inform the user:
- "Detected new project - will do full setup"
- "Detected existing Claude project - will update skills and add any missing structure"
- "Detected existing codebase - will add Claude setup while preserving your code"

---

## Phase 2: Validate CLI Tools

Check required CLI tools are installed and authenticated:

```bash
# Check GitHub CLI
gh auth status

# Check Vercel CLI
vercel whoami

# Check Supabase CLI
supabase projects list
```

If any tool fails, inform the user and offer to skip:
- "GitHub CLI not authenticated. Run: `gh auth login` (or skip if not using GitHub)"
- "Vercel CLI not authenticated. Run: `vercel login` (or skip if not using Vercel)"
- "Supabase CLI not authenticated. Run: `supabase login` (or skip if not using Supabase)"

---

## Phase 3: Project Questions

**For existing projects with CLAUDE.md**: Read existing config first, then ask what to update.

**For new or unconfigured projects**: Ask these questions one at a time:

### 1. What are you building?
Ask for a brief description (1-2 sentences).
*Skip if CLAUDE.md exists and has Project Overview - show current and ask if they want to update.*

### 2. What language/runtime?
- Python
- TypeScript
- JavaScript (Node)
- Multiple (specify which)

*Auto-detect from package.json or pyproject.toml if present.*

### 3. What type of project?
- Backend API
- Frontend Web (React)
- Mobile App (React Native)
- Full Stack (Backend + Frontend)
- CLI Tool
- Library/Package

*Auto-detect from dependencies if possible.*

### 4. Is this an AI-first application?
- Yes (LLMs handle core logic)
- No (traditional application)

*Check for anthropic/openai in dependencies.*

### 5. What framework? (based on previous answers)
**Backend:**
- Python: FastAPI, Flask, Django
- Node: Express, Fastify, Hono

**Frontend Web:**
- React (Vite, Next.js)

**Mobile:**
- React Native, Expo

*Auto-detect from dependencies.*

### 6. What database?
- Supabase (Postgres)
- None / SQLite
- Other (specify)

*Skip if supabase/ directory exists.*

### 7. Where will this be deployed?
- Vercel
- Render
- Other (specify)

*Skip if vercel.json or render.yaml exists.*

### 8. Repository setup? (skip if git remote already configured)
- Create new repository
- Connect to existing repository
- Skip (local only for now)

If creating new:
- What should the repo be named?
- Public or private?

---

## Phase 4: Execute Setup

### Step 1: Create/update directory structure
```bash
mkdir -p .claude/skills
mkdir -p docs
mkdir -p _project_specs/features
mkdir -p _project_specs/todos
mkdir -p _project_specs/prompts
mkdir -p _project_specs/session/archive
mkdir -p scripts
```

### Step 2: Update skill files from ~/.claude/skills/

**Skills use folder structure:** Each skill is a folder containing `SKILL.md`.

```bash
# Copy skill folders (not flat .md files)
cp -r ~/.claude/skills/base/ .claude/skills/
cp -r ~/.claude/skills/security/ .claude/skills/
cp -r ~/.claude/skills/project-tooling/ .claude/skills/
cp -r ~/.claude/skills/session-management/ .claude/skills/
```

**Always copy (overwrite with latest):**
- `base/` → `.claude/skills/base/`
- `security/` → `.claude/skills/security/`
- `project-tooling/` → `.claude/skills/project-tooling/`
- `session-management/` → `.claude/skills/session-management/`

**Based on language:**
- Python → copy `python/`
- TypeScript/JavaScript → copy `typescript/`

**Based on project type:**
- React Native → copy `typescript/` AND `react-native/`
- React Web → copy `typescript/` AND `react-web/`
- Node Backend → copy `typescript/` AND `nodejs-backend/`
- Full Stack (Node + React) → copy `typescript/`, `nodejs-backend/`, AND `react-web/`

**If AI-first:**
- Copy `llm-patterns/`

**Note:** Skills are always overwritten with the latest version from ~/.claude/skills/. This ensures updates propagate when user updates their global skills.

### Step 3: Create/update .gitignore (if missing or incomplete)

Ensure these security-critical entries exist:
```gitignore
# Environment files - NEVER commit
.env
.env.*
!.env.example

# Secrets
*.pem
*.key
*.p12
credentials.json
secrets.json
service-account*.json

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Build outputs
dist/
build/

# IDE
.idea/
.vscode/settings.json
.DS_Store
```

### Step 4: Create .env.example (if missing)

Based on project type:
```bash
# .env.example - Copy to .env and fill in values
# Server-side only (NEVER prefix with VITE_ or NEXT_PUBLIC_)
DATABASE_URL=
ANTHROPIC_API_KEY=

# Client-side safe (public, non-sensitive)
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
```

### Step 5: Create/update verification script
Create or overwrite `scripts/verify-tooling.sh`:

```bash
#!/bin/bash
set -e

echo "Verifying project tooling..."

# GitHub CLI
if command -v gh &> /dev/null; then
  if gh auth status &> /dev/null; then
    echo "✓ GitHub CLI authenticated"
  else
    echo "✗ GitHub CLI not authenticated. Run: gh auth login"
    exit 1
  fi
else
  echo "⚠ GitHub CLI not installed. Run: brew install gh"
fi

# Vercel CLI
if command -v vercel &> /dev/null; then
  if vercel whoami &> /dev/null; then
    echo "✓ Vercel CLI authenticated"
  else
    echo "✗ Vercel CLI not authenticated. Run: vercel login"
    exit 1
  fi
else
  echo "⚠ Vercel CLI not installed. Run: npm i -g vercel"
fi

# Supabase CLI
if command -v supabase &> /dev/null; then
  if supabase projects list &> /dev/null 2>&1; then
    echo "✓ Supabase CLI authenticated"
  else
    echo "✗ Supabase CLI not authenticated. Run: supabase login"
    exit 1
  fi
else
  echo "⚠ Supabase CLI not installed. Run: brew install supabase/tap/supabase"
fi

echo ""
echo "Tooling verification complete!"
```

```bash
chmod +x scripts/verify-tooling.sh
```

### Step 6: Create security check script

Create `scripts/security-check.sh`:
```bash
#!/bin/bash
set -e

echo "Running security checks..."

# Check .env is not staged
if git diff --cached --name-only | grep -E '^\.env$|^\.env\.' | grep -v '\.example$'; then
  echo "ERROR: .env file is staged for commit!"
  exit 1
fi

# Check for common secret patterns
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)
if [ -n "$STAGED_FILES" ]; then
  if echo "$STAGED_FILES" | xargs grep -l -E '(password|secret|api_key|apikey|token)\s*[:=]\s*["\047][^"\047]{8,}["\047]' 2>/dev/null; then
    echo "WARNING: Possible secrets found in staged files - please verify"
  fi
fi

# Check for VITE_* secrets (common mistake)
if [ -n "$STAGED_FILES" ]; then
  if echo "$STAGED_FILES" | xargs grep -l -E 'VITE_.*SECRET|VITE_.*KEY.*=.*[a-zA-Z0-9]{20,}' 2>/dev/null; then
    echo "ERROR: Secrets in VITE_* env vars are exposed to client!"
    exit 1
  fi
fi

# Dependency audit
if [ -f "package.json" ]; then
  echo "Checking npm dependencies..."
  npm audit --audit-level=high 2>/dev/null || echo "Warning: npm audit found issues"
fi

if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  if command -v safety &> /dev/null; then
    echo "Checking Python dependencies..."
    safety check 2>/dev/null || echo "Warning: safety found issues"
  fi
fi

echo "Security checks complete!"
```

```bash
chmod +x scripts/security-check.sh
```

### Step 7: Create/update CLAUDE.md

**If CLAUDE.md exists:**
- Preserve Project Overview, Tech Stack, and Project-Specific Patterns sections
- Update Skills list to reference current .claude/skills/ contents
- Update Key Commands section with latest

**If new:**
```markdown
# CLAUDE.md

## Skills
Read and follow these skills before writing any code:
- .claude/skills/base/SKILL.md
- .claude/skills/security/SKILL.md
- .claude/skills/project-tooling/SKILL.md
- .claude/skills/session-management/SKILL.md
- .claude/skills/[language]/SKILL.md
- .claude/skills/[framework]/SKILL.md (if applicable)
- .claude/skills/llm-patterns/SKILL.md (if AI-first)

## Project Overview
[Description from question 1]

## Tech Stack
- Language: [X]
- Framework: [X]
- Database: [X]
- Deployment: [X]
- Testing: [X]

## Key Commands
```bash
# Verify all CLI tools are working
./scripts/verify-tooling.sh

# Install dependencies
npm install          # or: pip install -e ".[dev]"

# Run tests
npm test             # or: pytest

# Lint
npm run lint         # or: ruff check .

# Type check
npm run typecheck    # or: mypy src/

# Pre-commit hooks (run once after clone)
npx husky init       # or: pre-commit install

# Database (if using Supabase)
npm run db:start     # Start local Supabase
npm run db:migrate   # Push migrations

# Deploy
npm run deploy:preview  # Deploy to preview
npm run deploy:prod     # Deploy to production
```

## Documentation
- `docs/` - Technical documentation
- `_project_specs/` - Project specifications and todos

## Atomic Todos
All work is tracked in `_project_specs/todos/`:
- `active.md` - Current work
- `backlog.md` - Future work
- `completed.md` - Done (for reference)

Every todo must have validation criteria and test cases. See base.md skill for format.

## Session Management

### State Tracking
Maintain session state in `_project_specs/session/`:
- `current-state.md` - Live session state (update every 15-20 tool calls)
- `decisions.md` - Key architectural/implementation decisions (append-only)
- `code-landmarks.md` - Important code locations for quick reference
- `archive/` - Past session summaries

### Automatic Updates
Update `current-state.md`:
- After completing any todo item
- Every 15-20 tool calls during active work
- Before any significant context shift
- When encountering blockers

### Decision Logging
Log to `decisions.md` when:
- Choosing between architectural approaches
- Selecting libraries or tools
- Making security-related choices
- Deviating from standard patterns

### Context Compression
When context feels heavy (~50+ tool calls):
1. Summarize completed work in current-state.md
2. Archive verbose exploration notes to archive/
3. Keep only essential context for next steps

### Session Handoff
When ending a session or approaching context limits, update current-state.md with:
- What was completed this session
- Current state of work
- Immediate next steps (numbered, specific)
- Open questions or blockers
- Files to review first when resuming

### Resuming Work
When starting a new session:
1. Read `_project_specs/session/current-state.md`
2. Check `_project_specs/todos/active.md`
3. Review recent entries in `decisions.md` if context needed
4. Continue from "Next Steps" in current-state.md

## Project-Specific Patterns
[Any specific patterns for this project]
```

### Step 5: Create project specs structure (if missing)

Only create files that don't exist - never overwrite existing specs.

**_project_specs/overview.md** (if missing):
```markdown
# Project Overview

## Vision
[Description from question 1]

## Goals
- [ ] Goal 1
- [ ] Goal 2

## Non-Goals
- What this project will NOT do

## Success Metrics
- How we measure success
```

**_project_specs/todos/active.md** (if missing):
```markdown
# Active Todos

Current work in progress. Each todo follows the atomic todo format from base.md skill.

---

<!-- Add todos here -->
```

**_project_specs/todos/backlog.md** (if missing):
```markdown
# Backlog

Future work, prioritized. Move to active.md when starting.

---

<!-- Add todos here -->
```

**_project_specs/todos/completed.md** (if missing):
```markdown
# Completed

Done items for reference. Move here from active.md when complete.

---

<!-- Add completed todos here -->
```

**_project_specs/session/current-state.md** (if missing):
```markdown
<!--
CHECKPOINT RULES (from session-management.md):
- Quick update: After any todo completion
- Full checkpoint: After ~20 tool calls or decisions
- Archive: End of session or major feature complete

After each task, ask: Decision made? >10 tool calls? Feature done?
-->

# Current Session State

*Last updated: [timestamp]*

## Active Task
[What are we working on right now - one sentence]

## Current Status
- **Phase**: exploring | planning | implementing | testing | debugging
- **Progress**: [X of Y steps, or description]
- **Blocking Issues**: None

## Context Summary
[2-3 sentences summarizing current state of work]

## Files Being Modified
| File | Status | Notes |
|------|--------|-------|
| - | - | - |

## Next Steps
1. [ ] First next action
2. [ ] Second next action

## Key Context to Preserve
- [Important decisions or context for this task]

## Resume Instructions
To continue this work:
1. [Specific starting point]
2. [What to check/read first]
```

**_project_specs/session/decisions.md** (if missing):
```markdown
<!--
LOG DECISIONS WHEN:
- Choosing between architectural approaches
- Selecting libraries or tools
- Making security-related choices
- Deviating from standard patterns

This is append-only. Never delete entries.
-->

# Decision Log

Track key architectural and implementation decisions.

## Format
```
## [YYYY-MM-DD] Decision Title

**Decision**: What was decided
**Context**: Why this decision was needed
**Options Considered**: What alternatives existed
**Choice**: Which option was chosen
**Reasoning**: Why this choice was made
**Trade-offs**: What we gave up
**References**: Related code/docs
```

---

<!-- Add decisions below -->
```

**_project_specs/session/code-landmarks.md** (if missing):
```markdown
<!--
UPDATE WHEN:
- Adding new entry points or key files
- Introducing new patterns
- Discovering non-obvious behavior

Helps quickly navigate the codebase when resuming work.
-->

# Code Landmarks

Quick reference to important parts of the codebase.

## Entry Points
| Location | Purpose |
|----------|---------|
| - | Main application entry |

## Core Business Logic
| Location | Purpose |
|----------|---------|
| - | - |

## Configuration
| Location | Purpose |
|----------|---------|
| - | Environment/app config |

## Key Patterns
| Pattern | Example Location | Notes |
|---------|------------------|-------|
| - | - | - |

## Testing
| Location | Purpose |
|----------|---------|
| tests/ | Test files |

## Gotchas & Non-Obvious Behavior
| Location | Issue | Notes |
|----------|-------|-------|
| - | - | - |
```

### Step 9: Create/update GitHub Actions workflows

**Quality workflow** (`.github/workflows/quality.yml`):
Create based on language (copy from the relevant skill file).

**Security workflow** (`.github/workflows/security.yml`):
```yaml
name: Security

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday

jobs:
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Detect secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./

  dependency-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        if: hashFiles('package.json') != ''
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: NPM Audit
        if: hashFiles('package.json') != ''
        run: npm audit --audit-level=high
      - name: Setup Python
        if: hashFiles('pyproject.toml') != ''
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Safety check
        if: hashFiles('pyproject.toml') != ''
        run: pip install safety && safety check
```

### Step 7: Set up pre-commit hooks (if not already configured)

**For Python projects** (if .pre-commit-config.yaml missing):
Create `.pre-commit-config.yaml`

**For TypeScript/JavaScript projects** (if .husky/ missing):
Set up Husky + lint-staged

### Step 7b: Install pre-push code review hook

**Always install the pre-push hook for code review enforcement:**

```bash
# Check if .git exists
if [ -d ".git" ]; then
    # Copy pre-push hook from ~/.claude/hooks/
    cp ~/.claude/hooks/pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push
    echo "✓ Pre-push code review hook installed"
fi
```

This hook:
- Runs `/code-review` before every `git push`
- Blocks push if 🔴 Critical or 🟠 High severity issues found
- Allows push with advisory for 🟡 Medium and 🟢 Low issues

To disable: `rm .git/hooks/pre-push`

### Step 8: GitHub repository setup (if selected and not already configured)

**Create new repository:**
```bash
git init  # if needed
git add .
git commit -m "Initial project setup"
gh repo create [repo-name] --[public|private] --source=. --remote=origin --push
```

**Connect to existing:**
```bash
git remote add origin https://github.com/[owner]/[repo].git
git push -u origin main
```

### Step 9: Initialize deployment (if not already configured)

**Vercel** (if vercel.json missing):
```bash
vercel link
```

**Supabase** (if supabase/ missing):
```bash
supabase init
```

---

## Phase 5: Summary

After setup, show what was done:

### For Updates (existing project):
```
Updated:
✓ Skills updated to latest versions
  - base.md (updated)
  - typescript.md (updated)
  - react-web.md (updated)
✓ Pre-push code review hook (installed/updated)

Added:
✓ llm-patterns.md (new skill added)
✓ _project_specs/prompts/ (new directory)

Unchanged:
- CLAUDE.md (preserved your customizations)
- _project_specs/todos/ (preserved your todos)
- Git repository (already configured)
```

### For New Projects:
```
Created:
✓ .claude/skills/ with 5 skill files
✓ CLAUDE.md
✓ _project_specs/ structure
✓ scripts/verify-tooling.sh
✓ .github/workflows/quality.yml
✓ Pre-commit hooks configured
✓ Pre-push code review hook (blocks on Critical/High issues)
✓ GitHub repository: https://github.com/[owner]/[repo]
```

### Quick Start
```bash
# Verify setup
./scripts/verify-tooling.sh

# Install dependencies
[appropriate command]

# Start development
[appropriate command]
```

---

## Phase 6: Next Steps

**For new projects**, prompt to start specs:
> **Project initialized! Ready to start building.**
>
> Would you like to start defining your first feature? I'll help you:
> 1. Create a feature spec in `_project_specs/features/`
> 2. Break it down into atomic todos with validation and test cases
> 3. Add them to `_project_specs/todos/active.md`
>
> What's the first feature you want to build?

**For existing projects**, offer options:
> **Project updated with latest skills!**
>
> What would you like to do?
> 1. Review changes to skills (see what's new)
> 2. Add a new feature spec
> 3. Continue working on existing todos
> 4. Something else

---

## Updating Skills System-Wide

To update skills for all future projects:

```bash
# Pull latest skills
cd ~/.claude-bootstrap
git pull

# Reinstall
./install.sh

# Validate installation
./tests/validate-structure.sh
```

Then in any existing project:
```
/initialize-project
```

Skills will be updated while preserving project-specific configuration.

## Troubleshooting

If `/initialize-project` shows validation errors:

```bash
# Full validation to see all issues
~/.claude-bootstrap/tests/validate-structure.sh --full

# Quick validation (what initialize-project runs)
~/.claude-bootstrap/tests/validate-structure.sh --quick
```

Common issues:
- **Flat .md files**: Skills should be folders with SKILL.md, not flat files
- **Missing commands**: Reinstall with `./install.sh`
- **Missing hooks**: Reinstall with `./install.sh`
