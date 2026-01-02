# Claude Bootstrap

> An opinionated project initialization system for Claude Code. **TDD-first, iterative loops, security-first, AI-native.**

**The bottleneck has moved from code generation to code comprehension.** AI can generate infinite code, but humans still need to review, understand, and maintain it. Claude Bootstrap provides guardrails that keep AI-generated code simple, secure, and verifiable.

## Core Philosophy

```
┌────────────────────────────────────────────────────────────────┐
│  ITERATIVE LOOPS BY DEFAULT                                    │
│  ─────────────────────────────────────────────────────────────│
│  Every task runs in a self-referential loop until tests pass.  │
│  Claude iterates autonomously. You describe what, not how.     │
│  Powered by Ralph Wiggum - iteration > perfection.             │
├────────────────────────────────────────────────────────────────┤
│  TESTS FIRST, ALWAYS                                           │
│  ─────────────────────────────────────────────────────────────│
│  Features: Write tests → Watch them fail → Implement → Pass    │
│  Bugs: Find test gap → Write failing test → Fix → Pass         │
│  No code ships without a test that failed first.               │
├────────────────────────────────────────────────────────────────┤
│  SIMPLICITY IS NON-NEGOTIABLE                                  │
│  ─────────────────────────────────────────────────────────────│
│  20 lines per function │ 200 lines per file │ 3 params max     │
│  If you can't understand the whole system in one session,      │
│  it's too complex.                                             │
├────────────────────────────────────────────────────────────────┤
│  SECURITY BY DEFAULT                                           │
│  ─────────────────────────────────────────────────────────────│
│  No secrets in code │ No secrets in client env vars            │
│  Dependency scanning │ Pre-commit hooks │ CI enforcement       │
└────────────────────────────────────────────────────────────────┘
```

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

## Automatic Iterative Loops (Ralph Wiggum)

**You talk naturally. Claude automatically runs iterative TDD loops.**

```
┌─────────────────────────────────────────────────────────────┐
│  You say: "Add email validation to signup"                  │
├─────────────────────────────────────────────────────────────┤
│  Claude automatically:                                       │
│  1. Extracts requirements from your request                 │
│  2. Structures as TDD loop with completion criteria         │
│  3. Runs /ralph-loop with tests as exit condition           │
│  4. Iterates until all tests pass + lint clean              │
└─────────────────────────────────────────────────────────────┘
```

No need to manually invoke `/ralph-loop`. Just describe what you want:

| You Say | Claude Does |
|---------|-------------|
| "Add user authentication" | Loops until auth tests pass |
| "Fix the login bug" | Finds test gap → writes test → loops until fixed |
| "Build a REST API for todos" | Loops until all endpoint tests pass |
| "Refactor the auth module" | Loops with tests as safety net |

**Opt-out phrases** (for when you don't want loops):
- "Just explain..." → explanation only
- "Quick fix..." → one-liner, no loop
- "Don't loop..." → explicit opt-out

### Setup Ralph Wiggum Plugin

```bash
# Clone Claude Code repo and copy plugin
git clone https://github.com/anthropics/claude-code.git /tmp/claude-code
cp -r /tmp/claude-code/plugins/ralph-wiggum ~/.claude/plugins/
```

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

### TDD-First Development (Mandatory)

**Every feature and bug fix follows the same pattern:**

| Phase | Feature Development | Bug Fixing |
|-------|---------------------|------------|
| **1. RED** | Write tests based on acceptance criteria | Identify test gap, write test that reproduces bug |
| **2. RUN** | Execute tests → ALL MUST FAIL | Execute test → MUST FAIL (proves it catches bug) |
| **3. GREEN** | Write minimum code to pass | Fix the bug |
| **4. RUN** | Execute tests → ALL MUST PASS | Execute test → MUST PASS |
| **5. VALIDATE** | Lint + TypeCheck + Coverage ≥80% | Full test suite + Lint + TypeCheck |

**Why tests must fail first:**
- Proves the test actually validates the requirement
- For bugs: proves the test would have caught it
- Prevents false confidence from tests that always pass

**Anti-patterns we prevent:**
- ❌ Fixing bugs without adding a test first
- ❌ Writing tests after implementation
- ❌ Marking todos complete with failing tests
- ❌ Skipping lint/typecheck before completion

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

### Centralized Credentials

Store all your API keys in one file (e.g., `~/Documents/Access.txt`):

```
OpenAI API: sk-proj-xxx
Claude API: sk-ant-xxx
Stripe: sk_test_xxx
Supabase url: https://xxx.supabase.co
Anon key: eyJxxx
```

When starting a project, Claude asks for your access file location, auto-detects keys by pattern, validates them, and creates your `.env`.

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

## Skills Included (34 Skills)

### Core Skills
| Skill | Purpose |
|-------|---------|
| `base.md` | Universal patterns, constraints, TDD workflow, atomic todos |
| `iterative-development.md` | Ralph Wiggum loops - self-referential TDD iteration until tests pass |
| `security.md` | OWASP patterns, secrets management, security testing |
| `credentials.md` | Centralized API key management from Access.txt |
| `session-management.md` | Context preservation, tiered summarization, resumability |
| `project-tooling.md` | gh, vercel, supabase, render CLI + deployment platform setup |

### Language & Framework Skills
| Skill | Purpose |
|-------|---------|
| `python.md` | Python + ruff + mypy + pytest |
| `typescript.md` | TypeScript strict + eslint + jest |
| `nodejs-backend.md` | Express/Fastify patterns, repositories |
| `react-web.md` | React + hooks + React Query + Zustand |
| `react-native.md` | Mobile patterns, platform-specific code |

### UI Skills
| Skill | Purpose |
|-------|---------|
| `ui-web.md` | Web UI - glassmorphism, Tailwind, dark mode, accessibility |
| `ui-mobile.md` | Mobile UI - React Native, iOS/Android patterns, touch targets |
| `ui-testing.md` | Visual testing - catch invisible buttons, broken layouts, contrast |
| `playwright-testing.md` | E2E testing - Playwright, Page Objects, cross-browser, CI/CD |
| `user-journeys.md` | User experience flows - journey mapping, UX validation, error recovery |

### AI & Agentic Skills
| Skill | Purpose |
|-------|---------|
| `agentic-development.md` | Build AI agents - Pydantic AI (Python), Claude SDK (Node.js) |
| `llm-patterns.md` | AI-first apps, LLM testing, prompt management |
| `ai-models.md` | Latest models reference - Claude, OpenAI, Gemini, Eleven Labs, Replicate |

### Database & Backend Skills
| Skill | Purpose |
|-------|---------|
| `database-schema.md` | Schema awareness - read before coding, type generation, prevent column errors |
| `supabase.md` | Core Supabase CLI, migrations, RLS, Edge Functions |
| `supabase-nextjs.md` | Next.js + Supabase + Drizzle ORM |
| `supabase-python.md` | FastAPI + Supabase + SQLAlchemy/SQLModel |
| `supabase-node.md` | Express/Hono + Supabase + Drizzle ORM |

### Content & SEO Skills
| Skill | Purpose |
|-------|---------|
| `aeo-optimization.md` | AI Engine Optimization - semantic triples, page templates, content clusters for AI citations |
| `web-content.md` | SEO + AI discovery (GEO) - schema, content structure, ChatGPT/Perplexity optimization |
| `site-architecture.md` | Technical SEO - robots.txt, sitemap, meta tags, AI crawler handling, Core Web Vitals |

### Integration Skills
| Skill | Purpose |
|-------|---------|
| `web-payments.md` | Stripe Checkout, subscriptions, webhooks, customer portal |
| `reddit-api.md` | Reddit API with PRAW (Python) and Snoowrap (Node.js) |
| `posthog-analytics.md` | PostHog analytics, event tracking, feature flags, project-specific dashboards |
| `shopify-apps.md` | Shopify app development - Remix, Admin API, checkout extensions, GDPR compliance |
| `woocommerce.md` | WooCommerce REST API - products, orders, customers, webhooks |
| `medusa.md` | Medusa headless commerce - modules, workflows, API routes, admin UI |
| `klaviyo.md` | Klaviyo email/SMS marketing - profiles, events, flows, segmentation |

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

All work is tracked with validation, test cases, and **TDD execution logs**:

```markdown
## [TODO-042] Add email validation to signup form

**Status:** in-progress
**Priority:** high
**Estimate:** S

### Acceptance Criteria
- [ ] Email field shows error for invalid format
- [ ] Form cannot submit with invalid email

### Test Cases
| Input | Expected |
|-------|----------|
| user@example.com | Valid |
| notanemail | Error |

### TDD Execution Log
| Phase | Command | Result |
|-------|---------|--------|
| RED | `npm test -- --grep "email validation"` | 2 tests failed ✓ |
| GREEN | `npm test -- --grep "email validation"` | 2 tests passed ✓ |
| VALIDATE | `npm run lint && npm run typecheck && npm test -- --coverage` | Pass, 84% ✓ |
```

**Bug reports include test gap analysis:**

```markdown
## [BUG-007] Email validation accepts "user@"

### Test Gap Analysis
- Existing tests: `signup.test.ts` - only tested valid emails
- Gap: Missing test for email without domain
- New test: Add case for partial emails

### TDD Execution Log
| Phase | Command | Result |
|-------|---------|--------|
| DIAGNOSE | `npm test` | All pass (test gap!) |
| RED | `npm test -- --grep "partial email"` | 1 test failed ✓ |
| GREEN | `npm test -- --grep "partial email"` | 1 test passed ✓ |
| VALIDATE | `npm run lint && npm test -- --coverage` | Pass ✓ |
```

## Error Handling in Loops

**Not all failures are equal. Claude classifies errors before iterating:**

| Error Type | Examples | Claude Fixes? | Action |
|------------|----------|---------------|--------|
| **Code Error** | Logic bug, wrong assertion | ✅ Yes | Continue loop |
| **Access Error** | Missing API key, DB refused | ❌ No | Stop + report |
| **Environment Error** | Missing package, wrong version | ❌ No | Stop + report |

**When Claude hits an access/environment error:**

```
🛑 LOOP BLOCKED - Human Action Required

Error: ECONNREFUSED 127.0.0.1:5432

Required Actions:
1. Start PostgreSQL: brew services start postgresql
2. Verify connection: psql -U postgres -c "SELECT 1"
3. Check DATABASE_URL in .env

After fixing, run /ralph-loop again.
```

**Common blockers and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `ECONNREFUSED :5432` | PostgreSQL not running | `brew services start postgresql` |
| `ECONNREFUSED :6379` | Redis not running | `brew services start redis` |
| `401 Unauthorized` | Bad API key | Check `.env` file |
| `MODULE_NOT_FOUND` | Missing package | `npm install` |

---

## FAQ

### How is this different from just using Claude Code?

Claude Code is powerful but unpredictable without guardrails. Claude Bootstrap adds:
- **TDD enforcement** - Tests must fail before implementation
- **Automatic iteration** - Loops until tests pass, not one-shot
- **Error classification** - Knows when to stop and ask for help
- **Complexity limits** - Hard caps prevent unmaintainable code

### Do I need to manually run `/ralph-loop` every time?

No. With Claude Bootstrap skills loaded, Claude **automatically** transforms your requests into iterative TDD loops. Just say "add email validation" and it loops until tests pass.

### What if I don't want a loop for something?

Use opt-out phrases:
- "Just explain..." → explanation only
- "Quick fix..." → one-liner
- "Don't loop..." → explicit opt-out

### What if the loop runs forever?

Three safety mechanisms:
1. **`--max-iterations`** - Hard limit (default 20-30)
2. **Error classification** - Stops on access/environment errors
3. **Blocker detection** - Reports when stuck and needs human help

### Does this work with existing projects?

Yes. Run `/initialize-project` in any directory. It adds skills without breaking existing config.

### What about test coverage?

Minimum 80% coverage enforced. CI blocks PRs below threshold.

### How do I update skills?

```bash
cd ~/.claude-bootstrap
git pull
./install.sh
```

Then run `/initialize-project` in your project to get latest skills.

### Can I customize the skills?

Yes. Skills are markdown files in `.claude/skills/`. Edit or add your own.

### What languages/frameworks are supported?

| Category | Supported |
|----------|-----------|
| Languages | TypeScript, Python |
| Frontend | React, Next.js, React Native |
| Backend | Node.js, Express, FastAPI |
| Database | Supabase, PostgreSQL, Drizzle, Prisma |
| E-commerce | Shopify, WooCommerce, Medusa |
| Marketing | Klaviyo, PostHog |

---

## Comparison

| Feature | Other Tools | Claude Bootstrap |
|---------|-------------|------------------|
| **Testing** | Optional, often skipped | TDD mandatory - tests fail first |
| **Iteration** | One-shot | Loops until tests pass |
| **Bug Fixes** | Jump to fix | Test gap analysis → failing test → fix |
| **Error Handling** | Loop forever | Classifies errors, stops on blockers |
| **Security** | Rarely covered | First-class with CI enforcement |
| **Complexity** | Vague guidance | Hard limits (20 lines/function, 200/file) |

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
