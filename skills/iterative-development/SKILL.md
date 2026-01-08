---
name: iterative-development
description: Ralph Wiggum loops - self-referential TDD iteration until tests pass
---

# Iterative Development Skill (Ralph Wiggum Integration)

*Load with: base.md*

**Concept:** Self-referential development loops where Claude iterates on the same task until completion criteria are met. Based on the [Ralph Wiggum plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum).

---

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│  ITERATION > PERFECTION                                     │
│  ─────────────────────────────────────────────────────────  │
│  Don't aim for perfect on first try.                        │
│  Let the loop refine the work. Each iteration builds on     │
│  previous attempts visible in files and git history.        │
├─────────────────────────────────────────────────────────────┤
│  FAILURES ARE DATA                                          │
│  ─────────────────────────────────────────────────────────  │
│  Failed tests, lint errors, type mismatches are signals.    │
│  Use them to guide the next iteration.                      │
├─────────────────────────────────────────────────────────────┤
│  CLEAR COMPLETION CRITERIA                                  │
│  ─────────────────────────────────────────────────────────  │
│  Define exactly what "done" looks like.                     │
│  Tests passing. Coverage met. Lint clean.                   │
│  No ambiguity about when to stop.                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Installing Ralph Wiggum Plugin

```bash
# Clone the plugin
git clone https://github.com/anthropics/claude-code.git /tmp/claude-code
cp -r /tmp/claude-code/plugins/ralph-wiggum ~/.claude/plugins/

# Or add to project-local plugins
mkdir -p .claude/plugins
cp -r /tmp/claude-code/plugins/ralph-wiggum .claude/plugins/
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. /ralph-loop "Your task prompt" --max-iterations 20      │
├─────────────────────────────────────────────────────────────┤
│  2. Claude works on task                                    │
├─────────────────────────────────────────────────────────────┤
│  3. Claude attempts to exit                                 │
├─────────────────────────────────────────────────────────────┤
│  4. Stop hook blocks exit, feeds SAME PROMPT back           │
├─────────────────────────────────────────────────────────────┤
│  5. Claude sees modified files + git history from before    │
├─────────────────────────────────────────────────────────────┤
│  6. Claude iterates and improves                            │
├─────────────────────────────────────────────────────────────┤
│  7. Loop continues until:                                   │
│     • Completion promise detected: <promise>DONE</promise>  │
│     • Max iterations reached                                │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** The prompt never changes. Only the file state evolves. Claude reads its own previous work and refines it.

---

## TDD-Integrated Prompt Templates

### Feature Development (TDD Loop)

```bash
/ralph-loop "
## Task: [Feature Name]

### Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### TDD Workflow (MUST FOLLOW)
1. Write failing tests based on requirements
2. Run tests - verify they FAIL (RED phase)
3. Implement minimum code to pass tests
4. Run tests - verify they PASS (GREEN phase)
5. Run lint and typecheck
6. If any failures, debug and fix
7. Repeat until all green

### Completion Criteria
- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] Lint clean (no errors)
- [ ] TypeScript/type check passing

### Exit Condition
When ALL criteria above are TRUE, output:
<promise>ALL TESTS PASSING AND LINT CLEAN</promise>
" --completion-promise "ALL TESTS PASSING AND LINT CLEAN" --max-iterations 30
```

### Bug Fix (TDD Loop)

```bash
/ralph-loop "
## Bug: [Bug Description]

### Reproduction
1. [Step 1]
2. [Step 2]
3. Observe: [Wrong behavior]
4. Expected: [Correct behavior]

### TDD Bug Fix Workflow (MUST FOLLOW)
1. Run existing tests - note if any catch the bug
2. Write a failing test that reproduces the bug
3. Run test - verify it FAILS (proves test catches bug)
4. Fix the bug with minimum code change
5. Run test - verify it PASSES
6. Run FULL test suite for regressions
7. Run lint and typecheck
8. If any failures, debug and fix
9. Repeat until all green

### Completion Criteria
- [ ] New test for bug exists
- [ ] New test passes
- [ ] All existing tests pass
- [ ] No regressions
- [ ] Lint clean

### Exit Condition
When ALL criteria are TRUE, output:
<promise>BUG FIXED WITH TEST</promise>
" --completion-promise "BUG FIXED WITH TEST" --max-iterations 25
```

### Refactoring (Safe Loop)

```bash
/ralph-loop "
## Refactor: [What to refactor]

### Goals
- [Goal 1: e.g., Extract function, reduce complexity]
- [Goal 2: e.g., Improve naming]
- [Goal 3: e.g., Split file if > 200 lines]

### Safety Constraints
- All existing tests MUST continue to pass
- No behavior changes (refactor only)
- Coverage must not decrease

### Workflow
1. Run all tests - establish baseline (must pass)
2. Make ONE refactoring change
3. Run tests - must still pass
4. Run lint and typecheck
5. If failures, REVERT and try different approach
6. Commit working refactor
7. Repeat for next change

### Completion Criteria
- [ ] All refactoring goals met
- [ ] All tests passing
- [ ] Coverage same or higher
- [ ] Lint clean

### Exit Condition
<promise>REFACTOR COMPLETE ALL TESTS GREEN</promise>
" --completion-promise "REFACTOR COMPLETE ALL TESTS GREEN" --max-iterations 20
```

### API Development

```bash
/ralph-loop "
## Task: Build [API Name] API

### Endpoints Required
- POST /api/resource - Create
- GET /api/resource - List
- GET /api/resource/:id - Get one
- PUT /api/resource/:id - Update
- DELETE /api/resource/:id - Delete

### Requirements
- Input validation (Zod/Pydantic)
- Error handling with proper status codes
- Tests for each endpoint
- OpenAPI/Swagger docs

### TDD Workflow
1. Write integration tests for each endpoint
2. Run tests - all should FAIL
3. Implement endpoints one by one
4. Run tests after each endpoint
5. Continue until all pass
6. Add validation and error handling
7. Run full test suite
8. Generate API docs

### Completion Criteria
- [ ] All endpoint tests passing
- [ ] Input validation working
- [ ] Error responses correct
- [ ] Coverage >= 80%
- [ ] Lint clean

### Exit Condition
<promise>API COMPLETE WITH TESTS</promise>
" --completion-promise "API COMPLETE WITH TESTS" --max-iterations 40
```

---

## Prompt Writing Rules

### 1. Clear Completion Criteria (REQUIRED)

```markdown
❌ BAD: "Build a todo API and make it good."

✅ GOOD:
### Completion Criteria
- [ ] CRUD endpoints implemented
- [ ] All tests passing
- [ ] Input validation working
- [ ] Coverage >= 80%
- [ ] Lint clean

### Exit Condition
<promise>ALL TESTS PASSING</promise>
```

### 2. Always Set Max Iterations

```bash
# ❌ DANGEROUS - runs forever
/ralph-loop "Build something"

# ✅ SAFE - stops after 30 iterations
/ralph-loop "Build something" --max-iterations 30
```

### 3. Include TDD in Every Prompt

```markdown
### TDD Workflow (MUST FOLLOW)
1. Write failing tests first
2. Verify tests fail
3. Implement feature
4. Verify tests pass
5. Run lint + typecheck
6. Repeat if failures
```

### 4. Break Large Tasks into Phases

```markdown
## Phase 1: Authentication
- [ ] Login endpoint with JWT
- [ ] Tests passing
- Output: <promise>AUTH COMPLETE</promise>

## Phase 2: User CRUD (after Phase 1)
- [ ] User endpoints
- [ ] Tests passing
- Output: <promise>USERS COMPLETE</promise>

## Phase 3: Products (after Phase 2)
...
```

### 5. Include Fallback Behavior

```markdown
### If Stuck After 15 Iterations
- Document what's blocking progress
- List approaches attempted
- Suggest alternative approaches
- Output: <promise>BLOCKED NEED HELP</promise>
```

---

## Error Classification (Critical for Loops)

**Not all test failures are equal. Claude MUST classify errors before iterating.**

### Error Types

| Type | Examples | Claude Can Fix? | Action |
|------|----------|-----------------|--------|
| **Code Error** | Logic bug, wrong algorithm, missing validation | ✅ YES | Continue loop |
| **Type Error** | Wrong types, missing properties | ✅ YES | Continue loop |
| **Test Error** | Wrong assertion, incomplete test | ✅ YES | Continue loop |
| **Access Error** | Missing API key, DB connection refused | ❌ NO | STOP + report |
| **Permission Error** | File access denied, auth failed | ❌ NO | STOP + report |
| **Environment Error** | Missing dependency, wrong Node version | ❌ NO | STOP + report |
| **Network Error** | Service unreachable, timeout | ❌ NO | STOP + report |

### Error Detection Pattern

```markdown
### Before Each Iteration

1. Run tests
2. If tests fail, classify the error:

   **Code/Logic Error?** (Claude can fix)
   - "Expected X but received Y"
   - "TypeError: cannot read property"
   - "AssertionError"
   → CONTINUE LOOP

   **Access/Environment Error?** (Human must fix)
   - "ECONNREFUSED" (DB not running)
   - "401 Unauthorized" (bad API key)
   - "ENOENT" (file/path not found)
   - "EACCES" (permission denied)
   - "MODULE_NOT_FOUND" (missing package)
   - "Connection timeout"
   → STOP LOOP + OUTPUT BLOCKER
```

### Blocker Report Format

When Claude detects an access/environment error, output this IMMEDIATELY:

```markdown
## 🛑 LOOP BLOCKED - Human Action Required

**Error Type:** Access/Environment (cannot be fixed by code changes)

**Error Message:**
\`\`\`
ECONNREFUSED 127.0.0.1:5432 - Connection refused
\`\`\`

**Root Cause:**
PostgreSQL database is not running or not accessible.

**Required Human Actions:**
1. [ ] Start PostgreSQL: `brew services start postgresql`
2. [ ] Verify connection: `psql -U postgres -c "SELECT 1"`
3. [ ] Check DATABASE_URL in .env matches running instance

**After Fixing:**
Run `/ralph-loop` again with the same prompt, or tell me to continue.

<promise>BLOCKED ENVIRONMENT</promise>
```

### Common Blockers Checklist

| Error Pattern | Likely Cause | Human Fix |
|---------------|--------------|-----------|
| `ECONNREFUSED :5432` | PostgreSQL not running | `brew services start postgresql` |
| `ECONNREFUSED :6379` | Redis not running | `brew services start redis` |
| `ECONNREFUSED :27017` | MongoDB not running | `brew services start mongodb` |
| `401 Unauthorized` | Invalid/missing API key | Check `.env` file |
| `403 Forbidden` | Wrong permissions/scopes | Check API key permissions |
| `ENOENT .env` | Missing .env file | Create from `.env.example` |
| `MODULE_NOT_FOUND` | Missing npm package | Run `npm install` |
| `ENOMEM` | Out of memory | Close other apps, increase swap |

### Updated Prompt Template with Error Handling

```bash
/ralph-loop "
## Task: [Feature Name]

### Requirements
- [Requirements here]

### TDD Workflow
1. Write failing tests
2. Run tests
3. **CLASSIFY ERROR:**
   - Code/logic error → fix and continue
   - Access/env error → STOP and report blocker
4. Implement fix
5. Run tests again
6. Repeat until pass or blocked

### Completion Criteria
- [ ] All tests passing
- [ ] Lint clean

### Exit Conditions
- SUCCESS: <promise>FEATURE COMPLETE</promise>
- BLOCKED: <promise>BLOCKED ENVIRONMENT</promise>
" --completion-promise "FEATURE COMPLETE" --max-iterations 25
```

### Multiple Completion Promises

Since Ralph only supports one `--completion-promise`, handle blockers in prompt:

```markdown
### Exit Logic
IF all tests pass AND lint clean:
  Output: <promise>COMPLETE</promise>

IF access/environment error detected:
  Output blocker report (see format above)
  Output: <promise>COMPLETE</promise>  # Exits loop, user sees blocker report
```

---

## When to Use Ralph Loops

### Good For

| Use Case | Why It Works |
|----------|--------------|
| **TDD feature development** | Tests provide clear pass/fail feedback |
| **Bug fixes** | Clear reproduction → test → fix cycle |
| **Refactoring** | Tests ensure no regressions |
| **API development** | Each endpoint is independently testable |
| **Greenfield projects** | Can iterate without human oversight |
| **Getting tests to pass** | Clear success criteria |

### Not Good For

| Use Case | Why It Fails |
|----------|--------------|
| **Subjective design decisions** | No clear "done" criteria |
| **UI/UX work** | Requires human judgment |
| **One-shot operations** | No need for iteration |
| **Unclear requirements** | Will loop forever |
| **Production debugging** | Needs human oversight |

---

## Monitoring and Control

### Check Current Iteration

```bash
grep '^iteration:' .claude/ralph-loop.local.md
```

### View Full State

```bash
head -10 .claude/ralph-loop.local.md
```

### Cancel Loop

```bash
/cancel-ralph
```

### State File Location

```
.claude/ralph-loop.local.md
```

---

## Integration with Claude Bootstrap

### Project Structure Addition

```
project/
├── _project_specs/
│   └── ralph-prompts/           # Saved Ralph prompts
│       ├── feature-template.md
│       ├── bug-fix-template.md
│       └── refactor-template.md
└── .claude/
    └── ralph-loop.local.md      # Active loop state (gitignored)
```

### Gitignore Addition

```gitignore
# Ralph loop state (session-specific)
.claude/ralph-loop.local.md
```

### Todo Integration

```markdown
## [TODO-042] Add email validation

**Status:** in-progress
**Method:** Ralph loop

### Ralph Prompt
/ralph-loop "..." --max-iterations 20 --completion-promise "..."

### TDD Execution Log
| Iteration | Tests | Lint | Status |
|-----------|-------|------|--------|
| 1 | 0/5 pass | errors | RED |
| 2 | 2/5 pass | errors | RED |
| 3 | 5/5 pass | clean | GREEN ✓ |

### Completion
- Iterations used: 3/20
- Promise detected: <promise>ALL TESTS PASSING</promise>
```

---

## Anti-Patterns

- ❌ **No max iterations** - Loop runs forever
- ❌ **Vague completion criteria** - Can't determine when done
- ❌ **No TDD in prompt** - No objective success metric
- ❌ **Lying to exit** - Outputting false promise to escape
- ❌ **Manual intervention** - Loop is designed for autonomy
- ❌ **Skipping test verification** - Tests must fail first

---

## Example: Real TDD Ralph Session

```bash
/ralph-loop "
## Task: Add email validation to signup form

### Requirements
- Email field shows error for invalid format
- Error clears when user fixes email
- Form cannot submit with invalid email
- Valid emails pass without error

### Test Cases
| Input | Expected |
|-------|----------|
| user@example.com | Valid |
| user@sub.example.com | Valid |
| notanemail | Error |
| user@ | Error |
| @example.com | Error |

### TDD Workflow
1. Create test file: signup-validation.test.ts
2. Write tests for ALL test cases above
3. Run: npm test -- --grep 'email validation'
4. Verify: All 5 tests FAIL (RED)
5. Implement: validateEmail function
6. Run: npm test -- --grep 'email validation'
7. Verify: All 5 tests PASS (GREEN)
8. Run: npm run lint && npm run typecheck
9. If any errors, fix and re-run
10. When all green, output completion

### Completion Criteria
- [ ] 5 tests exist for email validation
- [ ] All 5 tests passing
- [ ] Lint clean
- [ ] TypeCheck passing

### Exit Condition
<promise>EMAIL VALIDATION COMPLETE</promise>
" --completion-promise "EMAIL VALIDATION COMPLETE" --max-iterations 15
```

---

## Checklist

### Before Starting Ralph Loop
- [ ] Clear completion criteria defined
- [ ] `--max-iterations` set (safety net)
- [ ] `--completion-promise` set
- [ ] TDD workflow included in prompt
- [ ] Test cases defined

### During Loop
- [ ] Monitor iteration count
- [ ] Check test results each iteration
- [ ] Watch for stuck patterns

### After Completion
- [ ] Verify tests actually pass
- [ ] Run full test suite
- [ ] Check coverage threshold
- [ ] Commit changes
