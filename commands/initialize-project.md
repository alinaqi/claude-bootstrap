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

# Check for Flutter project
ls pubspec.yaml 2>/dev/null

# Check for Android project
ls android/build.gradle android/app/build.gradle 2>/dev/null

# Check for native language in Android projects
find android -name "*.java" -type f 2>/dev/null | head -1
find android -name "*.kt" -type f 2>/dev/null | head -1
```

Based on findings, determine:
- **New project**: No CLAUDE.md, no .claude/skills/, no code files
- **Existing project with skills**: Has .claude/skills/ - offer to UPDATE
- **Existing codebase without skills**: Has code but no Claude setup - **AUTO-RUN ANALYSIS**

Inform the user:
- "Detected new project - will do full setup"
- "Detected existing Claude project - will update skills and add any missing structure"
- "Detected existing codebase - **analyzing before making changes...**"

**For existing codebases without Claude setup, AUTOMATICALLY proceed to Phase 1b.**

---

## Phase 1b: Analyze Existing Codebase (Auto-triggered)

**This phase runs automatically when an existing codebase is detected without Claude setup.**

### Step 1: Repository Structure Detection

```bash
echo "=== Analyzing Repository Structure ===" && \

# Detect repo type
if [ -d "packages" ] || [ -d "apps" ] || grep -q '"workspaces"' package.json 2>/dev/null; then
    REPO_TYPE="MONOREPO"
elif [ -d "frontend" ] && [ -d "backend" ]; then
    REPO_TYPE="FULL_STACK"
elif [ -d "src" ] && grep -q '"react\|vue\|angular"' package.json 2>/dev/null; then
    REPO_TYPE="FRONTEND"
elif [ -f "pyproject.toml" ] || grep -q '"express\|fastify"' package.json 2>/dev/null; then
    REPO_TYPE="BACKEND"
else
    REPO_TYPE="STANDARD"
fi
echo "Repo Type: $REPO_TYPE"

# Directory structure (3 levels, excluding noise)
find . -type d -maxdepth 3 \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/venv/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    2>/dev/null | head -30
```

### Step 2: Tech Stack Detection

```bash
echo "=== Tech Stack ===" && \

# Primary language/framework
[ -f "package.json" ] && echo "JavaScript/TypeScript project"
[ -f "tsconfig.json" ] && echo "  → TypeScript configured"
[ -f "pyproject.toml" ] && echo "Python project"
[ -f "pubspec.yaml" ] && echo "Flutter project"
[ -d "android" ] && echo "Android project"

# Frameworks (from package.json)
if [ -f "package.json" ]; then
    grep -q '"react"' package.json && echo "  → React"
    grep -q '"next"' package.json && echo "  → Next.js"
    grep -q '"express"' package.json && echo "  → Express"
    grep -q '"fastify"' package.json && echo "  → Fastify"
fi

# Frameworks (from pyproject.toml)
if [ -f "pyproject.toml" ]; then
    grep -q "fastapi" pyproject.toml && echo "  → FastAPI"
    grep -q "django" pyproject.toml && echo "  → Django"
    grep -q "flask" pyproject.toml && echo "  → Flask"
fi
```

### Step 3: Guardrails Audit

```bash
echo "=== Guardrails Status ===" && \

# Pre-commit hooks
echo "Pre-commit Hooks:"
[ -d ".husky" ] && echo "  ✓ Husky installed" || echo "  ✗ Husky NOT installed"
[ -f ".pre-commit-config.yaml" ] && echo "  ✓ pre-commit framework" || echo "  ✗ pre-commit NOT installed"

# Linting
echo "Linting:"
(grep -q '"eslint"' package.json 2>/dev/null && echo "  ✓ ESLint") || \
(grep -q "ruff" pyproject.toml 2>/dev/null && echo "  ✓ Ruff") || \
echo "  ✗ No linter detected"

# Formatting
echo "Formatting:"
(grep -q '"prettier"' package.json 2>/dev/null && echo "  ✓ Prettier") || \
(grep -q "ruff\|black" pyproject.toml 2>/dev/null && echo "  ✓ Ruff/Black") || \
echo "  ✗ No formatter detected"

# Type checking
echo "Type Checking:"
([ -f "tsconfig.json" ] && echo "  ✓ TypeScript") || \
(grep -q "mypy" pyproject.toml 2>/dev/null && echo "  ✓ mypy") || \
echo "  ✗ No type checker detected"

# Commit validation
echo "Commit Validation:"
([ -f "commitlint.config.js" ] && echo "  ✓ commitlint") || \
(grep -q "conventional-pre-commit" .pre-commit-config.yaml 2>/dev/null && echo "  ✓ conventional-pre-commit") || \
echo "  ✗ No commit validation"

# CI/CD
echo "CI/CD:"
[ -d ".github/workflows" ] && echo "  ✓ GitHub Actions" || echo "  ✗ No GitHub Actions"
```

### Step 4: Convention Detection

```bash
echo "=== Conventions Detected ===" && \

# File naming pattern
echo "File Naming:"
ls src/**/*.ts 2>/dev/null | head -3 || ls src/**/*.py 2>/dev/null | head -3

# Import style
echo "Import Style:"
grep -h "^import" src/**/*.ts 2>/dev/null | head -3 || \
grep -h "^from\|^import" src/**/*.py 2>/dev/null | head -3

# Test location
echo "Test Location:"
[ -d "tests" ] && echo "  Separate tests/ directory"
[ -d "__tests__" ] && echo "  __tests__/ directory"
find . -name "*.test.*" -o -name "*.spec.*" 2>/dev/null | head -1 && echo "  Colocated tests"
```

### Step 5: Generate Analysis Summary

After running the analysis, present this summary to the user:

```markdown
## Repository Analysis Complete

**Type:** [Monorepo | Full-Stack | Frontend | Backend | Standard]
**Language:** [TypeScript | Python | Flutter | ...]
**Framework:** [React | FastAPI | ...]

### Guardrails Status

| Category | Status | Recommendation |
|----------|--------|----------------|
| Pre-commit hooks | ✗ Missing | Add Husky (JS) or pre-commit (Python) |
| Linting | ✓ ESLint | - |
| Formatting | ✗ Missing | Add Prettier |
| Type checking | ✓ TypeScript | - |
| Commit validation | ✗ Missing | Add commitlint |

### Conventions I'll Follow
- File naming: camelCase
- Imports: Absolute (@/...)
- Tests: Colocated (*.test.ts)
```

### Step 6: Present Options

After showing the analysis, ask:

> **I've analyzed this codebase. Here's what I found:** [summary above]
>
> What would you like me to do?
> 1. **Add Claude skills only** - Add skills, preserve everything else
> 2. **Add skills + missing guardrails** - Also setup Husky/pre-commit, commitlint, etc.
> 3. **Full setup** - Skills, guardrails, project specs structure, CI/CD
> 4. **Just show analysis** - Don't change anything yet

**Based on user choice:**
- Option 1 → Skip to Phase 4, only copy skills
- Option 2 → Phase 4 + guardrails setup from `existing-repo` skill
- Option 3 → Full Phase 4 execution
- Option 4 → End here, user can run `/initialize-project` again later

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
- Android Java
- Android Kotlin
- Flutter (Dart)
- Multiple (specify which)

*Auto-detect from package.json, pyproject.toml, pubspec.yaml, or android/ directory if present.*

### 3. What type of project?
- Backend API
- Frontend Web (React)
- Mobile App (React Native)
- Mobile App (Android Native)
- Mobile App (Flutter)
- Mobile App (Flutter + Native Android)
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

**For existing codebases (detected in Phase 1b):**
- `existing-repo/` → `.claude/skills/existing-repo/` - Structure preservation, guardrails setup

**Based on language:**
- Python → copy `python/`
- TypeScript/JavaScript → copy `typescript/`

**Based on project type:**
- React Native → copy `typescript/` AND `react-native/`
- React Web → copy `typescript/` AND `react-web/`
- Node Backend → copy `typescript/` AND `nodejs-backend/`
- Full Stack (Node + React) → copy `typescript/`, `nodejs-backend/`, AND `react-web/`

**For Android/Flutter projects (auto-detect from project structure):**

| Detection | Skills to Copy |
|-----------|---------------|
| `pubspec.yaml` exists | `flutter/` |
| `android/*.java` exists | `android-java/` |
| `android/*.kt` exists | `android-kotlin/` |
| Flutter + Java files | `flutter/` + `android-java/` |
| Flutter + Kotlin files | `flutter/` + `android-kotlin/` |
| Flutter + Both | `flutter/` + `android-java/` + `android-kotlin/` |

```bash
# Detect and copy Android/Flutter skills
if [ -f "pubspec.yaml" ]; then
  cp -r ~/.claude/skills/flutter/ .claude/skills/
fi

if find android -name "*.java" -type f 2>/dev/null | head -1 | grep -q .; then
  cp -r ~/.claude/skills/android-java/ .claude/skills/
fi

if find android -name "*.kt" -type f 2>/dev/null | head -1 | grep -q .; then
  cp -r ~/.claude/skills/android-kotlin/ .claude/skills/
fi
```

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

## Phase 6: Agent Team Setup (Default Workflow)

Every project uses Claude Agent Teams by default. This phase sets up the team infrastructure and spawns agents to implement features in parallel.

### Step 1: Set Environment Variable

Ensure the agent teams experimental flag is set:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Also add to the project's `.env.example` if not present:
```
# Agent Teams (required for claude-bootstrap team workflow)
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### Step 2: Copy Agent Definitions

Copy agent definitions from the agent-teams skill to the project:

```bash
mkdir -p .claude/agents
cp ~/.claude/skills/agent-teams/agents/*.md .claude/agents/
```

This creates:
```
.claude/agents/
  team-lead.md      # Orchestration only, delegate mode
  quality.md        # TDD verification (RED/GREEN phases)
  security.md       # OWASP scanning, secrets detection
  code-review.md    # Multi-engine code review
  merger.md         # Branch creation, PR management
  feature.md        # Feature implementation template
```

### Step 3: Add Agent Teams to CLAUDE.md

Add the agent-teams skill to the Skills section in CLAUDE.md:
```
- .claude/skills/agent-teams/SKILL.md
```

Add a new section to CLAUDE.md:
```markdown
## Agent Teams (Default Workflow)

This project uses Claude Code Agent Teams as the default development workflow.
Every feature is implemented by a dedicated agent following a strict TDD pipeline.

### Strict Pipeline (per feature)
Spec > Spec Review > Tests > RED Verify > Implement > GREEN Verify > Validate > Code Review > Security Scan > Branch + PR

### Team Roster
- **Team Lead**: Orchestrates, breaks work into features, assigns tasks (NEVER writes code)
- **Quality Agent**: Verifies TDD discipline - RED/GREEN phases, coverage >= 80%
- **Security Agent**: OWASP scanning, secrets detection, dependency audit
- **Code Review Agent**: Multi-engine code reviews (Claude/Codex/Gemini)
- **Merger Agent**: Creates feature branches and PRs via gh CLI
- **Feature Agents**: One per feature, follows strict TDD pipeline

### Commands
- `/spawn-team` - Spawn the agent team (auto-run after init, or run manually)

### Required Environment
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### Step 4: Prompt for Features

**For new projects:**
> **Project initialized! Ready to deploy the agent team.**
>
> The agent team implements features in parallel using a strict TDD pipeline:
> ```
> Spec > Tests > Verify Fail > Implement > Verify Pass > Review > Security > PR
> ```
>
> What are the key features of this project? List them and I'll create a spec
> skeleton for each, then spawn the team to implement them in parallel.
>
> Example: "user authentication, dashboard, payment processing"

For each feature the user lists:
1. Create `_project_specs/features/{feature-name}.md` with skeleton spec
2. Include: description (from user input), empty acceptance criteria, empty test cases table

**For existing projects:**
> **Project updated with latest skills and agent team support!**
>
> I've added agent team infrastructure. Your options:
> 1. Define features and spawn the team now
> 2. Continue working on existing todos (solo mode)
> 3. Review what's new in skills

### Step 5: Spawn Team

After the user provides features (or if feature specs already exist), automatically run the `/spawn-team` workflow:

1. Create the team (TeamCreate)
2. Spawn 5 default agents (team-lead, quality-agent, security-agent, review-agent, merger-agent)
3. Spawn 1 feature agent per feature
4. Team lead creates 10-task dependency chains per feature
5. Work begins automatically

### Step 6: Show Team Status

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENT TEAM DEPLOYED                                             │
│  ──────────────────────────────────────────────────────────────  │
│                                                                  │
│  Team: {project-name}                                            │
│  Features: {N}                                                   │
│  Total tasks: {N * 10}                                           │
│  Agents: {5 + N}                                                 │
│                                                                  │
│  PIPELINE (per feature)                                          │
│  Spec > Review > Tests > RED > Implement > GREEN >               │
│  Validate > Code Review > Security > Branch+PR                   │
│                                                                  │
│  Use Shift+Up/Down to select and message agents.                 │
│  Use Ctrl+T to toggle the shared task list.                      │
│  The team runs autonomously until all PRs are created.           │
└─────────────────────────────────────────────────────────────────┘
```

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
