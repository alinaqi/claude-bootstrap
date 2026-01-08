# Changelog

All notable changes to Claude Bootstrap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- **Android Java skill** - MVVM architecture, ViewBinding, Espresso testing, GitHub Actions CI (contributed by @tyr4n7)
- **Android Kotlin skill** - Coroutines, Jetpack Compose, Hilt DI, MockK/Turbine testing (contributed by @tyr4n7)

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
