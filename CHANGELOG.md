# Changelog

All notable changes to Claude Bootstrap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.5.0] - 2026-02-07

### Added

#### Agent Teams (Default Workflow)
- **Agent Teams skill** - Coordinated team of AI agents as the default development workflow
  - Strict TDD pipeline: Specs > Tests > Fail > Implement > Test > Review > Security > Branch > PR
  - Task dependency chains enforce pipeline ordering (no step can be skipped)
  - Multiple features run in parallel with shared verification agents
  - Quality gates at every stage with cross-agent verification

- **Default agent roster** (5 permanent agents):
  - **Team Lead** - Orchestration only (delegate mode), task breakdown, feature agent spawning
  - **Quality Agent** - TDD verification (RED/GREEN phases), spec review, coverage >= 80%
  - **Security Agent** - OWASP scanning, secrets detection, dependency audit
  - **Code Review Agent** - Multi-engine code review (Claude/Codex/Gemini)
  - **Merger Agent** - Feature branches, PR creation via `gh` CLI

- **Feature agents** - One per feature, each follows the strict pipeline end-to-end
  - Writes spec, tests, implementation, validation
  - Hands off to Quality, Review, Security, Merger at each gate

- **Agent definition files** in `skills/agent-teams/agents/`:
  - `team-lead.md`, `quality.md`, `security.md`, `code-review.md`, `merger.md`, `feature.md`
  - Copied to `.claude/agents/` during project initialization

- **`/spawn-team` command** - Spawn the agent team on any project
  - Checks prerequisites (env var, agent definitions, feature specs)
  - Spawns all agents and creates task dependency chains
  - Shows team status summary

- **10-task dependency chain per feature**:
  1. Spec → 2. Spec Review → 3. Tests → 4. RED Verify → 5. Implement →
  6. GREEN Verify → 7. Validate → 8. Code Review → 9. Security Scan → 10. Branch+PR

### Changed
- Total skills increased from 53 to **54 skills**
- `/initialize-project` Phase 6 now sets up agent team by default (replaces manual next steps)
- CLAUDE.md template includes agent teams section
- `team-coordination.md` superseded by `agent-teams.md` for automated coordination

---

## [2.4.0] - 2026-01-20

### Added

#### Multi-Repo Workspace Awareness
- **Workspace skill** - Dynamic multi-repo and monorepo awareness for Claude Code
  - Workspace topology discovery (monorepo, multi-repo, hybrid detection)
  - Dependency graph generation (who calls whom)
  - API contract extraction (OpenAPI, GraphQL, tRPC, TypeScript, Pydantic)
  - Key file identification with token estimates
  - Cross-repo capability index (search before reimplementing)
  - Token budget management (P0-P3 priority allocation)

- **`/analyze-workspace` command** - Full workspace analysis
  - Phase 1: Topology discovery (~30s)
  - Phase 2: Module analysis (~60s)
  - Phase 3: Contract extraction (~45s)
  - Phase 4: Dependency graph (~30s)
  - Phase 5: Key file identification (~30s)
  - Generates TOPOLOGY.md, CONTRACTS.md, DEPENDENCY_GRAPH.md, KEY_FILES.md, CROSS_REPO_INDEX.md

- **`/sync-contracts` command** - Lightweight incremental contract sync
  - Checks only contract source files (~15s)
  - Diff mode to preview changes
  - Validate mode to check consistency
  - Lightweight mode for hooks

#### Contract Freshness System
- **Session start hook** - Staleness check (~5s, advisory)
- **Post-commit hook** - Auto-sync when contracts change (~15s)
- **Pre-push hook** - Validation gate (~10s, blocking)
- `.contract-sources` file to track monitored files
- Freshness indicators: 🟢 Fresh, 🟡 Stale, 🔴 Outdated, ⚠️ Drift

#### Cross-Repo Change Detection
- Automatic detection when changes affect other modules
- Impact analysis with recommended action order
- Breaking change protocol

### Changed
- Total skills increased from 52 to **53 skills**
- Added 3 new commands: `/analyze-workspace`, `/sync-contracts`, `/workspace-status`
- Added 3 workspace hooks for contract freshness

---

## [2.3.0] - 2026-01-17

### Added

#### Google Gemini Code Review
- **Gemini Review skill** - Google Gemini CLI for code review with Gemini 2.5 Pro
  - 1M token context window - analyze entire repositories at once
  - Free tier: 1,000 requests/day with Google account
  - Code Review Extension: `/code-review` command in Gemini CLI
  - Headless mode for CI/CD: `gemini -p "prompt"`
  - Benchmarks: 63.8% SWE-Bench, 56.3% Qodo PR, 70.4% LiveCodeBench

- **Multi-engine code review** - `/code-review` now supports up to 3 engines
  - Claude (built-in) - quick, context-aware reviews
  - OpenAI Codex - 88% security issue detection
  - Google Gemini - 1M token context for large codebases
  - Dual engine mode - run any two engines, compare findings
  - Triple engine mode - maximum coverage for critical/security code

- **GitHub Actions workflows** for all configurations
  - Gemini-only workflow
  - Triple engine (Claude + Codex + Gemini) workflow
  - Updated dual engine workflow

### Changed
- Total skills increased from 51 to **52 skills**
- Updated `/code-review` to support engine selection: `--engine claude,codex,gemini`
- Added `--gemini` and `--all` shortcuts for common configurations

---

## [2.2.0] - 2026-01-17

### Added

#### Existing Repository Support
- **Existing Repo skill** - Analyze existing codebases, maintain structure, setup guardrails
  - Repo structure detection (monorepo, full-stack, frontend-only, backend-only)
  - Tech stack auto-detection (TypeScript, Python, Flutter, Android, etc.)
  - Convention detection (naming, imports, exports, test patterns)
  - Guardrails audit (pre-commit hooks, linting, formatting, type checking)
  - Structure preservation rules - work within existing patterns, don't reorganize
  - Gradual implementation strategy for adding guardrails to legacy projects
  - Cross-repo coordination for separate frontend/backend repos

- **`/analyze-repo` command** - Quick analysis of any existing repository
  - Directory structure mapping
  - Guardrails status audit (Husky, pre-commit, ESLint, Ruff, commitlint, etc.)
  - Convention detection and documentation
  - Generates analysis report with recommendations
  - Offers to add missing guardrails
  - **Auto-triggered** by `/initialize-project` when existing codebase detected

#### Initialize Project Enhancement
- **Auto-analysis for existing codebases** - `/initialize-project` now automatically analyzes existing repos before making changes
- **User choice after analysis** - Options: skills only, skills + guardrails, full setup, or just view analysis
- **Existing-repo skill auto-copied** - When working with existing codebases

#### Guardrails Setup (for JS/TS and Python)
- **Husky + lint-staged** setup for JavaScript/TypeScript projects
- **pre-commit framework** setup for Python projects
- **commitlint** configuration for conventional commits
- **ESLint 9 flat config** template
- **Ruff + mypy** configuration for Python

### Changed
- Total skills increased from 50 to **51 skills**
- Updated README with `/analyze-repo` usage pattern

---

## [2.1.0] - 2026-01-17

### Added

#### Mobile Development (contributed by @tyr4n7)
- **Android Java skill** - MVVM architecture, ViewBinding, Espresso testing, GitHub Actions CI
- **Android Kotlin skill** - Coroutines, Jetpack Compose, Hilt DI, MockK/Turbine testing
- **Flutter skill** - Riverpod state management, Freezed models, go_router, mocktail testing
- **Android/Flutter auto-detection** - `/initialize-project` now detects Flutter, Android Java, and Android Kotlin projects

#### Database Skills (addresses #7)
- **Firebase skill** - Firestore, Auth, Storage, real-time listeners, security rules, offline persistence
- **Cloudflare D1 skill** - Serverless SQLite with Workers, Drizzle ORM integration, migrations
- **AWS DynamoDB skill** - Single-table design, GSI patterns, SDK v3 TypeScript/Python
- **AWS Aurora skill** - Serverless v2, RDS Proxy, Data API, connection pooling for Lambda
- **Azure Cosmos DB skill** - Partition key design, consistency levels, change feed, SDK patterns

#### Code Review Enhancements
- **Codex Review skill** - OpenAI Codex CLI for code review with GPT-5.2-Codex (88% detection rate)
- **Code review engine choice** - `/code-review` now lets you choose: Claude, OpenAI Codex, or both engines
- **Dual engine review mode** - Run both Claude and Codex, compare findings, catch more issues
- **CI/CD templates** - GitHub Actions workflows for Claude, Codex, and dual-engine reviews

### Changed
- Total skills increased from 44 to **50 skills**
- Updated README with new database and mobile skill listings

### Contributors
- @tyr4n7 - Android Java, Android Kotlin, Flutter skills and auto-detection
- @johnsfuller - Feature request for database skills (#7)

---

## [2.0.0] - 2026-01-08

### Breaking Changes
- **Skills structure changed** - Skills now use folder/SKILL.md structure instead of flat .md files
  - Before: `~/.claude/skills/base.md`
  - After: `~/.claude/skills/base/SKILL.md`
- All skills now require YAML frontmatter with `name` and `description` fields

### Added
- **Validation test** (`tests/validate-structure.sh`) - Validates skills structure, commands, hooks
  - `--full` mode: All 142 checks
  - `--quick` mode: Essential checks for initialize-project
- **Phase 0 validation** in `/initialize-project` - Checks bootstrap installation before setup
- **Conversion script** (`scripts/convert-skills-structure.sh`) - Migrates flat skills to folder structure
- Install script now runs validation automatically
- Symlink created at `~/.claude-bootstrap` for easy access to validation tools

### Fixed
- Skills now load properly in Claude Code (fixes #1)
- Install script properly copies skill folders instead of merging contents

### Migration
```bash
cd ~/.claude-bootstrap
git pull
./install.sh
```

---

## [1.5.0] - 2026-01-07

### Added
- **Code Deduplication skill** - Prevent semantic code duplication with capability index
- **Team Coordination skill** - Multi-person projects with shared state and todo claiming
- `/check-contributors` command - Detect solo vs team projects
- `/update-code-index` command - Regenerate CODE_INDEX.md
- Pre-push hook for code review enforcement

### Changed
- Code reviews now mandatory before push (blocks on Critical/High issues)

---

## [1.4.0] - 2026-01-06

### Added
- **Code Review skill** - Mandatory code reviews via `/code-review`
- **Commit Hygiene skill** - Atomic commits, PR size limits
- Pre-push hooks installation script

---

## [1.3.0] - 2026-01-05

### Added
- **MS Teams Apps skill** - Teams bots and AI agents with Claude/OpenAI
- **Reddit Ads skill** - Agentic ad optimization service
- **PWA Development skill** - Service workers, caching, offline support

---

## [1.2.0] - 2026-01-04

### Added
- **Playwright Testing skill** - E2E testing with Page Objects
- **PostHog Analytics skill** - Event tracking, feature flags
- **Shopify Apps skill** - Remix, Admin API, checkout extensions

---

## [1.1.0] - 2026-01-03

### Added
- Session management with automatic state tracking
- Decision logging for architectural choices
- Code landmarks for quick navigation

---

## [1.0.0] - 2026-01-01

### Added
- Initial release with 30+ skills
- `/initialize-project` command
- TDD-first workflow with Ralph Wiggum loops
- Security-first patterns
- Support for Python, TypeScript, React, React Native
- Supabase integration skills
- AI/LLM patterns for Claude and OpenAI
