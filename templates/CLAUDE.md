# CLAUDE.md - Project Instructions

## Skills Loaded
- base.md (TDD workflow, atomic todos, simplicity rules)
- iterative-development.md (Ralph Wiggum loops)
- [Add your stack-specific skills here]

---

## Default Behavior: Automatic Iterative TDD

**IMPORTANT:** For any implementation task, automatically use Ralph Wiggum loops with TDD.

### Auto-Invoke Rules

When I ask you to implement something (feature, bug fix, refactor, API, etc.):

1. **DO NOT** just start coding
2. **DO** automatically invoke `/ralph-loop` with:
   - Requirements extracted from my request
   - TDD workflow (write failing tests first)
   - Clear completion criteria
   - `--max-iterations 25` (adjust by complexity)
   - `--completion-promise` based on task

### Example Transformation

If I say: "Add user authentication"

You automatically run:
```bash
/ralph-loop "
## Task: Add user authentication

### Requirements
- [Extract from my request + reasonable defaults]

### TDD Workflow
1. Write failing tests
2. Verify tests FAIL
3. Implement feature
4. Verify tests PASS
5. Run lint + typecheck
6. Repeat if failures

### Completion Criteria
- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] Lint clean

<promise>AUTH COMPLETE</promise>
" --completion-promise "AUTH COMPLETE" --max-iterations 25
```

### Opt-Out Phrases

Only skip Ralph loop if I explicitly say:
- "Just explain..."
- "Quick fix..."
- "Don't loop..."
- "Help me understand..."

---

## Project-Specific Context

### Tech Stack
- Language: [e.g., TypeScript]
- Framework: [e.g., Next.js]
- Database: [e.g., Supabase/PostgreSQL]
- Testing: [e.g., Jest, Vitest]

### Commands
```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Lint
npm run lint

# Type check
npm run typecheck

# Full validation
npm run lint && npm run typecheck && npm test -- --coverage
```

### Schema Location
- Schema file: `src/db/schema.ts`
- Read schema before any database code

---

## Quality Gates (Enforced)

| Constraint | Limit |
|------------|-------|
| Lines per function | 20 max |
| Parameters per function | 3 max |
| Lines per file | 200 max |
| Test coverage | 80% minimum |

---

## Session Persistence

- Checkpoint after completing tasks
- Log decisions to `_project_specs/session/decisions.md`
- Update `_project_specs/session/current-state.md` regularly
