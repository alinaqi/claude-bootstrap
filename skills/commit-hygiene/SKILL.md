---
name: commit-hygiene
description: Atomic commits, PR size limits, commit thresholds, stacked PRs
---

# Commit Hygiene Skill

*Load with: base.md*

**Purpose:** Keep commits atomic, PRs reviewable, and git history clean. Advise when it's time to commit before changes become too large.

---

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│  ATOMIC COMMITS                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  One logical change per commit.                                  │
│  Each commit should be self-contained and deployable.            │
│  If you need "and" to describe it, split it.                     │
├─────────────────────────────────────────────────────────────────┤
│  SMALL PRS WIN                                                   │
│  ─────────────────────────────────────────────────────────────  │
│  < 400 lines changed = reviewed in < 1 hour                      │
│  > 1000 lines = likely rubber-stamped or abandoned               │
│  Smaller PRs = faster reviews, fewer bugs, easier reverts        │
├─────────────────────────────────────────────────────────────────┤
│  COMMIT EARLY, COMMIT OFTEN                                      │
│  ─────────────────────────────────────────────────────────────  │
│  Working code? Commit it.                                        │
│  Test passing? Commit it.                                        │
│  Don't wait for "done" - commit at every stable point.           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Commit Size Thresholds

### Warning Thresholds (Time to Commit!)

| Metric | Yellow Zone | Red Zone | Action |
|--------|-------------|----------|--------|
| **Files changed** | 5-10 files | > 10 files | Commit NOW |
| **Lines added** | 150-300 lines | > 300 lines | Commit NOW |
| **Lines deleted** | 100-200 lines | > 200 lines | Commit NOW |
| **Total changes** | 250-400 lines | > 400 lines | Commit NOW |
| **Time since last commit** | 30-60 min | > 60 min | Consider committing |

### Ideal Commit Size

```
┌─────────────────────────────────────────────────────────────────┐
│  IDEAL COMMIT                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  Files: 1-5                                                      │
│  Lines: 50-200 total changes                                     │
│  Scope: Single logical unit of work                              │
│  Message: Describes ONE thing                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Check Current State (Run Frequently)

### Quick Status Check

```bash
# See what's changed (staged + unstaged)
git status --short

# Count files and lines changed
git diff --stat
git diff --cached --stat  # Staged only

# Get totals
git diff --shortstat
# Example output: 8 files changed, 245 insertions(+), 32 deletions(-)
```

### Detailed Change Analysis

```bash
# Full diff summary with file names
git diff --stat HEAD

# Just the numbers
git diff --numstat HEAD | awk '{add+=$1; del+=$2} END {print "+"add" -"del" total:"add+del}'

# Files changed count
git status --porcelain | wc -l
```

### Pre-Commit Check Script

```bash
#!/bin/bash
# scripts/check-commit-size.sh

# Thresholds
MAX_FILES=10
MAX_LINES=400
WARN_FILES=5
WARN_LINES=200

# Get stats
FILES=$(git status --porcelain | wc -l | tr -d ' ')
STATS=$(git diff --shortstat HEAD 2>/dev/null)
INSERTIONS=$(echo "$STATS" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo 0)
DELETIONS=$(echo "$STATS" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo 0)
TOTAL=$((INSERTIONS + DELETIONS))

echo "📊 Current changes: $FILES files, +$INSERTIONS -$DELETIONS ($TOTAL total lines)"

# Check thresholds
if [ "$FILES" -gt "$MAX_FILES" ] || [ "$TOTAL" -gt "$MAX_LINES" ]; then
    echo "🔴 RED ZONE: Commit immediately! Changes are too large."
    echo "   Consider splitting into multiple commits."
    exit 1
elif [ "$FILES" -gt "$WARN_FILES" ] || [ "$TOTAL" -gt "$WARN_LINES" ]; then
    echo "🟡 WARNING: Changes getting large. Commit soon."
    exit 0
else
    echo "🟢 OK: Changes are within healthy limits."
    exit 0
fi
```

---

## When to Commit

### Commit Triggers (Any One = Commit)

| Trigger | Example |
|---------|---------|
| **Test passes** | Just got a test green → commit |
| **Feature complete** | Finished a function → commit |
| **Refactor done** | Renamed variable across files → commit |
| **Bug fixed** | Fixed the issue → commit |
| **Before switching context** | About to work on something else → commit |
| **Clean compile** | Code compiles/lints clean → commit |
| **Threshold hit** | > 5 files or > 200 lines → commit |

### Commit Immediately If

- ✅ Tests are passing after being red
- ✅ You're about to make a "big change"
- ✅ You've been coding for 30+ minutes
- ✅ You're about to try something risky
- ✅ The current state is "working"

### Don't Wait For

- ❌ "Perfect" code
- ❌ All features done
- ❌ Full test coverage
- ❌ Code review from yourself
- ❌ Documentation complete

---

## Atomic Commit Patterns

### Good Atomic Commits

```
✅ "Add email validation to signup form"
   - 3 files: validator.ts, signup.tsx, signup.test.ts
   - 120 lines changed
   - Single purpose: email validation

✅ "Fix null pointer in user lookup"
   - 2 files: userService.ts, userService.test.ts
   - 25 lines changed
   - Single purpose: fix one bug

✅ "Refactor: Extract PaymentProcessor class"
   - 4 files: payment.ts → paymentProcessor.ts + types
   - 180 lines changed
   - Single purpose: refactoring
```

### Bad Commits (Too Large)

```
❌ "Add authentication, fix bugs, update styles"
   - 25 files changed
   - 800 lines changed
   - Multiple purposes mixed

❌ "WIP"
   - Unknown scope
   - No clear purpose
   - Hard to review/revert

❌ "Updates"
   - 15 files changed
   - Mix of features, fixes, refactors
   - Impossible to review properly
```

---

## Splitting Large Changes

### Strategy 1: By Layer

```
Instead of one commit with:
  - API endpoint + database migration + frontend + tests

Split into:
  1. "Add users table migration"
  2. "Add User model and repository"
  3. "Add GET /users endpoint"
  4. "Add UserList component"
  5. "Add integration tests for user flow"
```

### Strategy 2: By Feature Slice

```
Instead of one commit with:
  - All CRUD operations for users

Split into:
  1. "Add create user functionality"
  2. "Add read user functionality"
  3. "Add update user functionality"
  4. "Add delete user functionality"
```

### Strategy 3: Refactor First

```
Instead of:
  - Feature + refactoring mixed

Split into:
  1. "Refactor: Extract validation helpers" (no behavior change)
  2. "Add email validation using new helpers" (new feature)
```

### Strategy 4: By Risk Level

```
Instead of:
  - Safe changes + risky changes together

Split into:
  1. "Update dependencies" (safe, isolated)
  2. "Migrate to new API version" (risky, separate)
```

---

## PR Size Guidelines

### Optimal PR Size

| Metric | Optimal | Acceptable | Too Large |
|--------|---------|------------|-----------|
| **Files** | 1-10 | 10-20 | > 20 |
| **Lines changed** | 50-200 | 200-400 | > 400 |
| **Commits** | 1-5 | 5-10 | > 10 |
| **Review time** | < 30 min | 30-60 min | > 60 min |

### PR Size vs Defect Rate

```
┌─────────────────────────────────────────────────────────────────┐
│  RESEARCH FINDINGS (Google, Microsoft studies)                  │
│  ─────────────────────────────────────────────────────────────  │
│  PRs < 200 lines: 15% defect rate                               │
│  PRs 200-400 lines: 23% defect rate                             │
│  PRs > 400 lines: 40%+ defect rate                              │
│                                                                 │
│  Review quality drops sharply after 200-400 lines.              │
│  Large PRs get "LGTM" rubber stamps, not real reviews.          │
└─────────────────────────────────────────────────────────────────┘
```

### When PR is Too Large

```bash
# Check PR size before creating
git diff main --stat
git diff main --shortstat

# If too large, consider:
# 1. Split into multiple PRs (stacked PRs)
# 2. Create feature flag and merge incrementally
# 3. Use draft PR for early feedback
```

---

## Commit Message Format

### Structure

```
<type>: <description> (50 chars max)

[optional body - wrap at 72 chars]

[optional footer]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding/updating tests |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `chore` | Build, config, dependencies |

### Examples

```
feat: Add email validation to signup form

fix: Prevent null pointer in user lookup

refactor: Extract PaymentProcessor class

test: Add integration tests for checkout flow

chore: Update dependencies to latest versions
```

---

## Git Workflow Integration

### Pre-Commit Hook for Size Check

```bash
#!/bin/bash
# .git/hooks/pre-commit

MAX_LINES=400
MAX_FILES=15

FILES=$(git diff --cached --name-only | wc -l | tr -d ' ')
STATS=$(git diff --cached --shortstat)
INSERTIONS=$(echo "$STATS" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo 0)
DELETIONS=$(echo "$STATS" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo 0)
TOTAL=$((INSERTIONS + DELETIONS))

if [ "$TOTAL" -gt "$MAX_LINES" ]; then
    echo "❌ Commit too large: $TOTAL lines (max: $MAX_LINES)"
    echo "   Consider splitting into smaller commits."
    echo "   Use 'git add -p' for partial staging."
    exit 1
fi

if [ "$FILES" -gt "$MAX_FILES" ]; then
    echo "❌ Too many files: $FILES (max: $MAX_FILES)"
    echo "   Consider splitting into smaller commits."
    exit 1
fi

echo "✅ Commit size OK: $FILES files, $TOTAL lines"
```

### Partial Staging (Split Large Changes)

```bash
# Stage specific hunks interactively
git add -p

# Stage specific files
git add path/to/specific/file.ts

# Stage with preview
git add -N file.ts  # Intent to add
git diff            # See what would be added
git add file.ts     # Actually add
```

### Unstage If Too Large

```bash
# Unstage everything
git reset HEAD

# Unstage specific files
git reset HEAD path/to/file.ts

# Stage just what you need for THIS commit
git add -p
```

---

## Claude Integration

### Periodic Check During Development

**Claude should run this check after every significant change:**

```bash
# Quick status
git diff --shortstat HEAD
```

**Thresholds for Claude to advise committing:**

| Condition | Claude Action |
|-----------|---------------|
| > 5 files changed | Suggest: "Consider committing current changes" |
| > 200 lines changed | Suggest: "Changes are getting large, commit recommended" |
| > 10 files OR > 400 lines | Warn: "⚠️ Commit now before changes become unmanageable" |
| Test just passed | Suggest: "Good checkpoint - commit these passing tests" |
| Refactoring complete | Suggest: "Refactoring done - commit before adding features" |

### Claude Commit Reminder Messages

```
📊 Status: 7 files changed, +180 -45 (225 total)
💡 Approaching commit threshold. Consider committing current work.

---

📊 Status: 12 files changed, +320 -80 (400 total)
⚠️ Changes are large! Commit now to keep PRs reviewable.
   Suggested commit: "feat: Add user authentication flow"

---

📊 Status: 3 files changed, +85 -10 (95 total)
✅ Tests passing. Good time to commit!
   Suggested commit: "fix: Validate email format on signup"
```

---

## Stacked PRs (For Large Features)

When a feature is genuinely large, use stacked PRs:

```
┌─────────────────────────────────────────────────────────────────┐
│  STACKED PR PATTERN                                             │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  main ─────────────────────────────────────────────────────────│
│    └── PR #1: Database schema (200 lines) ← Review first       │
│         └── PR #2: API endpoints (250 lines) ← Review second   │
│              └── PR #3: Frontend (300 lines) ← Review third    │
│                                                                 │
│  Each PR is reviewable independently.                           │
│  Merge in order: #1 → #2 → #3                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Creating Stacked PRs

```bash
# Create base branch
git checkout -b feature/auth-schema
# ... make changes ...
git commit -m "feat: Add users table schema"
git push -u origin feature/auth-schema
gh pr create --base main --title "feat: Add users table schema"

# Create next branch FROM the first
git checkout -b feature/auth-api
# ... make changes ...
git commit -m "feat: Add authentication API endpoints"
git push -u origin feature/auth-api
gh pr create --base feature/auth-schema --title "feat: Add auth API endpoints"

# And so on...
```

---

## Checklist

### Before Every Commit

- [ ] Changes are for ONE logical purpose
- [ ] Tests pass (if applicable)
- [ ] Lint/typecheck pass
- [ ] < 10 files changed
- [ ] < 400 lines total
- [ ] Commit message describes ONE thing

### Before Creating PR

- [ ] Total lines < 400 (ideal < 200)
- [ ] All commits are atomic
- [ ] No "WIP" or "fixup" commits
- [ ] PR title describes the change
- [ ] Description explains why, not just what

### Red Flags (Stop and Split)

- ❌ Commit message needs "and"
- ❌ > 10 files in one commit
- ❌ > 400 lines in one commit
- ❌ Mix of features, fixes, and refactors
- ❌ "I'll clean this up later"

---

## Quick Reference

### Thresholds

```
Files:  ≤ 5 = 🟢  |  6-10 = 🟡  |  > 10 = 🔴
Lines:  ≤ 200 = 🟢  |  201-400 = 🟡  |  > 400 = 🔴
Time:   ≤ 30min = 🟢  |  30-60min = 🟡  |  > 60min = 🔴
```

### Commands

```bash
# Quick status
git diff --shortstat HEAD

# Detailed file list
git diff --stat HEAD

# Partial staging
git add -p

# Check before PR
git diff main --shortstat
```

### Commit Now If

- ✅ Tests just passed
- ✅ > 200 lines changed
- ✅ > 5 files changed
- ✅ About to switch tasks
- ✅ Current state is "working"
