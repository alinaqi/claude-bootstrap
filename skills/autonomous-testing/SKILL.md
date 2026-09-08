---
name: autonomous-testing
description: AI-driven testing agent that auto-discovers, generates, executes, evaluates, and fixes tests for any project type
when-to-use: When setting up automated test generation or running an autonomous test-fix loop across Python, TypeScript, API, or web projects
user-invocable: false
effort: high
---

# Autonomous Testing Agent

## Overview

An AI-driven testing agent that auto-discovers, generates, executes, evaluates, and fixes tests for any project type. Inspired by the edubites autonomous test runner pattern, generalized for Claude Bootstrap + Maggy.

## Pipeline

```
Source Scan → Discover Gaps → Generate Tests → Execute → Evaluate → Report → Fix Loop
```

## Phase 1: Discover — What Needs Testing?

```
Auto-detect project type:
  Python    → scan for *.py files, extract public functions/classes
  TypeScript → scan for *.ts/*.tsx files, extract exports
  API       → scan FastAPI/Express routes, extract endpoints + methods
  Web       → scan React/Vue components, extract user flows

Map existing tests:
  Python    → pytest --collect-only
  TypeScript → vitest --list
  API       → scan tests/ for endpoint coverage

Compute coverage gaps:
  - Functions with 0 tests
  - API endpoints with 0 tests
  - Components with 0 tests
  - Branches with <80% coverage
```

## Phase 2: Generate — AI-Written Tests

```
For each uncovered function/endpoint/component:
  1. Read source code → understand inputs, outputs, edge cases
  2. Generate test scaffold using ~/bin/deepseek --pro
  3. Include: happy path, error cases, edge cases, auth checks
  4. Write to appropriate test directory

Model routing for generation:
  - Simple functions    → ~/bin/deepseek --flash (cheap, fast)
  - Complex logic       → ~/bin/deepseek --pro (thorough)
  - Auth/security tests → ~/bin/deepseek --pro (quality-critical)
```

## Phase 3: Execute — Run Everything

```bash
# Python
pytest -x --cov --cov-report=json

# TypeScript
npx vitest run --coverage

# E2E (if Playwright detected)
npx playwright test

# Parse results → structured TestRun { pass/fail, coverage, duration, failures[] }
```

## Phase 4: Evaluate — AI-Powered Assessment

```
For each test failure:
  1. Capture: test name, error message, stack trace, source code diff
  2. Classify failure:
     - TEST_BUG: test is wrong (outdated expectation, bad mock)
     - CODE_BUG: code is wrong (regression, edge case)
     - ENV_BUG: environment issue (missing dep, config)
  3. AI evaluation: ~/bin/deepseek --pro analyzes failure and classifies

For E2E/web tests:
  - Capture screenshots at failure points
  - ~/bin/gemini --flash evaluates visual state (multimodal)
```

## Phase 5: Fix — Autonomous Repair

```
TEST_BUG → regenerate test with corrected expectation
CODE_BUG → propose fix with ~/bin/deepseek --pro, apply, re-run
ENV_BUG → report to user with fix instructions

Auto-fix loop:
  while test_failures > 0 and attempts < 3:
    for each failure:
      classify → fix → re-run
    if fixed: record as "auto-fixed"
    if not: escalate to CLAUDE tier
```

## Phase 6: Report — Structured Output

```json
{
  "project": "my-app",
  "timestamp": "2026-05-16T12:00:00Z",
  "summary": {
    "tests_run": 247,
    "passed": 231,
    "failed": 12,
    "auto_fixed": 8,
    "needs_manual": 4,
    "coverage": 0.83
  },
  "gaps_found": 15,
  "tests_generated": 15,
  "next_actions": [
    "4 manual fixes needed in auth module",
    "Coverage gap: src/payment.py has 0 tests",
    "3 E2E flows untested: signup, checkout, profile-edit"
  ]
}
```

## Integration with Maggy

```
Maggy Dashboard → Testing tab shows:
  - Coverage trend over time
  - Auto-generated test count
  - Failure classification (TEST_BUG vs CODE_BUG)
  - "Generate tests for gaps" one-click button

Heartbeat job: auto-generate tests weekly for new untested code
Auto-review hook: triggers test generation after significant PR merges
```

## Usage

```bash
# Discover test gaps
maggy test discover

# Generate tests for all gaps
maggy test generate --all

# Generate tests for specific module
maggy test generate --module auth

# Run full test cycle (discover → generate → execute → fix → report)
maggy test autonomous

# Watch mode — auto-test on file changes
maggy test watch
```

## Configuration

```json
// ~/.claude/testing-config.json
{
  "auto_generate": true,
  "auto_fix": true,
  "max_fix_attempts": 3,
  "min_coverage": 0.8,
  "generate_model": "deepseek-pro",
  "evaluate_model": "gemini-flash",
  "fix_model": "deepseek-pro",
  "exclude_patterns": ["*/migrations/*", "*/node_modules/*"]
}
```
