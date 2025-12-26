# Claude Bootstrap

> An opinionated project initialization system for Claude Code. Security-first, spec-driven, AI-native.

**The bottleneck has moved from code generation to code comprehension.** AI can generate infinite code, but humans still need to review, understand, and maintain it. Claude Bootstrap provides guardrails that keep AI-generated code simple, secure, and verifiable.

## Why This Exists

After hundreds of AI-assisted projects across Node, React, Python, and React Native, patterns emerged:

1. **Engineers struggle with Claude Code not because of the tool, but because of how they instruct it** - The delta is in the guardrails
2. **Complexity has a ceiling** - There's a point where AI loses coherent understanding of the system. That's a signal, not a failure
3. **Restart is a feature, not failure** - When fixing something increases complexity, restart with learnings. Each iteration is faster

This toolkit encodes those learnings into reusable skills.

## Quick Start

```bash
# Clone and install
git clone https://github.com/alinaqi/claude-bootstrap.git ~/.claude-bootstrap
cd ~/.claude-bootstrap && ./install.sh

# In any project directory
claude
> /initialize-project
```

Claude will:
1. **Validate tools** - Check gh, vercel, supabase CLIs
2. **Ask questions** - Language, framework, AI-first?, database
3. **Set up repository** - Create or connect GitHub repo
4. **Create structure** - Skills, security, CI/CD, specs, todos
5. **Prompt for specs** - Transition to defining first feature

## What Gets Created

```
your-project/
├── .claude/skills/           # Coding guardrails
│   ├── base.md               # Universal patterns
│   ├── security.md           # Security requirements
│   ├── [language].md         # Language-specific
│   └── [framework].md        # Framework-specific
├── .github/workflows/
│   ├── quality.yml           # Lint, type-check, test (80% coverage)
│   └── security.yml          # Secret scanning, dependency audit
├── _project_specs/
│   ├── overview.md           # Project vision
│   ├── features/             # Feature specifications
│   └── todos/                # Atomic todos with test cases
├── docs/                     # Technical documentation
├── scripts/
│   ├── verify-tooling.sh     # CLI validation
│   └── security-check.sh     # Pre-commit security
└── CLAUDE.md                 # Claude instructions
```

## Philosophy

### Complexity is the Enemy

Every line of code is a liability. The goal is software simple enough that any engineer (or AI) can understand the entire system in one session.

**Measurable constraints, not vague guidance:**

| Constraint | Limit |
|------------|-------|
| Lines per function | 20 max |
| Parameters per function | 3 max |
| Nesting depth | 2 levels max |
| Lines per file | 200 max |
| Test coverage | 80% minimum |

### Security is Non-Negotiable

- No secrets in code - ever
- No secrets in `VITE_*` or `NEXT_PUBLIC_*` env vars (client-exposed!)
- `.env` files always gitignored
- Dependency scanning on every PR
- Pre-commit security checks

### AI-First Architecture

For applications where LLMs handle core logic:

- **LLM for logic, code for plumbing** - Classification, extraction, decisions via LLM; validation, routing, auth via code
- **Test LLM calls properly** - Mocks for unit tests, fixtures for parsing, evals for accuracy
- **Track costs** - Monitor token usage and latency

### Spec-Driven Development

Define before you build:

1. **Feature specs** in `_project_specs/features/`
2. **Atomic todos** with validation criteria and test cases
3. **Move, don't delete** - Completed todos go to `completed.md` for reference

## Skills Included

| Skill | Purpose |
|-------|---------|
| `base.md` | Universal patterns, constraints, atomic todos format |
| `security.md` | OWASP patterns, secrets management, security testing |
| `ui-web.md` | Web UI - glassmorphism, Tailwind, dark mode, accessibility |
| `ui-mobile.md` | Mobile UI - React Native, iOS/Android patterns, touch targets |
| `ui-testing.md` | Visual testing - catch invisible buttons, broken layouts, contrast |
| `project-tooling.md` | gh, vercel, supabase CLI integration |
| `python.md` | Python + ruff + mypy + pytest |
| `typescript.md` | TypeScript strict + eslint + jest |
| `nodejs-backend.md` | Express/Fastify patterns, repositories |
| `react-web.md` | React + hooks + React Query + Zustand |
| `react-native.md` | Mobile patterns, platform-specific code |
| `llm-patterns.md` | AI-first apps, LLM testing, prompt management |
| `ai-models.md` | Latest models reference - Claude, OpenAI, Gemini, Eleven Labs, Replicate |

## Usage Patterns

### New Project
```bash
mkdir my-new-app && cd my-new-app
claude
> /initialize-project
# Answer questions, get full setup
```

### Existing Project
```bash
cd my-existing-app
claude
> /initialize-project
# Skills updated, existing config preserved
```

### Update Skills Globally
```bash
cd ~/.claude-bootstrap
git pull
./install.sh

# Then in any project:
claude
> /initialize-project
# Gets latest skills
```

## Prerequisites

Install and authenticate these CLIs:

```bash
# GitHub CLI
brew install gh
gh auth login

# Vercel CLI
npm i -g vercel
vercel login

# Supabase CLI
brew install supabase/tap/supabase
supabase login
```

## Quality Gates

Every project gets automated enforcement:

### Pre-Commit (Local)
- Linting with auto-fix
- Type checking
- Security checks (no secrets, no .env)
- Unit tests on changed files

### CI (GitHub Actions)
- Full lint + type check
- All tests with 80% coverage
- Secret scanning (trufflehog)
- Dependency audit (npm audit / safety)

## Atomic Todos

All work is tracked with validation and test cases:

```markdown
## [TODO-042] Add email validation to signup form

**Status:** pending
**Priority:** high
**Estimate:** S

### Acceptance Criteria
- [ ] Email field shows error for invalid format
- [ ] Form cannot submit with invalid email

### Validation
- Manual: Enter "notanemail", verify error
- Automated: `npm test -- --grep "email validation"`

### Test Cases
| Input | Expected |
|-------|----------|
| user@example.com | Valid |
| notanemail | Error |
```

## Comparison

| Feature | Other Tools | Claude Bootstrap |
|---------|-------------|------------------|
| Approach | Collection of rules | Integrated, opinionated system |
| Security | Rarely covered | First-class with CI enforcement |
| AI-First | Not addressed | LLM patterns + testing |
| Todos | Basic tasks | Atomic with validation + test cases |
| Update model | Copy once | Idempotent - sync anytime |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Key principles:
- Measurable constraints over vague guidance
- Working code examples
- Maintain idempotency
- Test locally before submitting

## License

MIT - See [LICENSE](LICENSE)

## Credits

Built on learnings from 100+ projects across customer experience management, agentic AI platforms, mobile apps, and full-stack web applications.
