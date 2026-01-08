#!/bin/bash
# convert-skills-structure.sh
# Converts flat .md skills to folder/SKILL.md structure with YAML frontmatter

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$ROOT_DIR/skills"

echo "Converting skills from flat .md to folder/SKILL.md structure..."
echo "Skills directory: $SKILLS_DIR"
echo ""

# Function to get description for a skill
get_description() {
    local name="$1"
    case "$name" in
        "aeo-optimization") echo "AI Engine Optimization - semantic triples, page templates, content clusters for AI citations" ;;
        "agentic-development") echo "Build AI agents with Pydantic AI (Python) and Claude SDK (Node.js)" ;;
        "ai-models") echo "Latest AI models reference - Claude, OpenAI, Gemini, Eleven Labs, Replicate" ;;
        "base") echo "Universal coding patterns, constraints, TDD workflow, atomic todos" ;;
        "code-deduplication") echo "Prevent semantic code duplication with capability index and check-before-write" ;;
        "code-review") echo "Mandatory code reviews via /code-review before commits and deploys" ;;
        "commit-hygiene") echo "Atomic commits, PR size limits, commit thresholds, stacked PRs" ;;
        "credentials") echo "Centralized API key management from Access.txt" ;;
        "database-schema") echo "Schema awareness - read before coding, type generation, prevent column errors" ;;
        "iterative-development") echo "Ralph Wiggum loops - self-referential TDD iteration until tests pass" ;;
        "klaviyo") echo "Klaviyo email/SMS marketing - profiles, events, flows, segmentation" ;;
        "llm-patterns") echo "AI-first application patterns, LLM testing, prompt management" ;;
        "medusa") echo "Medusa headless commerce - modules, workflows, API routes, admin UI" ;;
        "ms-teams-apps") echo "Microsoft Teams bots and AI agents - Claude/OpenAI, Adaptive Cards, Graph API" ;;
        "nodejs-backend") echo "Node.js backend patterns with Express/Fastify, repositories" ;;
        "playwright-testing") echo "E2E testing with Playwright - Page Objects, cross-browser, CI/CD" ;;
        "posthog-analytics") echo "PostHog analytics, event tracking, feature flags, dashboards" ;;
        "project-tooling") echo "gh, vercel, supabase, render CLI and deployment platform setup" ;;
        "pwa-development") echo "Progressive Web Apps - service workers, caching strategies, offline, Workbox" ;;
        "python") echo "Python development with ruff, mypy, pytest - TDD and type safety" ;;
        "react-native") echo "React Native mobile patterns, platform-specific code" ;;
        "react-web") echo "React web development with hooks, React Query, Zustand" ;;
        "reddit-ads") echo "Reddit Ads API - campaigns, targeting, conversions, agentic optimization" ;;
        "reddit-api") echo "Reddit API with PRAW (Python) and Snoowrap (Node.js)" ;;
        "security") echo "OWASP security patterns, secrets management, security testing" ;;
        "session-management") echo "Context preservation, tiered summarization, resumability" ;;
        "shopify-apps") echo "Shopify app development - Remix, Admin API, checkout extensions" ;;
        "site-architecture") echo "Technical SEO - robots.txt, sitemap, meta tags, Core Web Vitals" ;;
        "supabase") echo "Core Supabase CLI, migrations, RLS, Edge Functions" ;;
        "supabase-nextjs") echo "Next.js with Supabase and Drizzle ORM" ;;
        "supabase-node") echo "Express/Hono with Supabase and Drizzle ORM" ;;
        "supabase-python") echo "FastAPI with Supabase and SQLAlchemy/SQLModel" ;;
        "team-coordination") echo "Multi-person projects - shared state, todo claiming, handoffs" ;;
        "typescript") echo "TypeScript strict mode with eslint and jest" ;;
        "ui-mobile") echo "Mobile UI patterns - React Native, iOS/Android, touch targets" ;;
        "ui-testing") echo "Visual testing - catch invisible buttons, broken layouts, contrast" ;;
        "ui-web") echo "Web UI - glassmorphism, Tailwind, dark mode, accessibility" ;;
        "user-journeys") echo "User experience flows - journey mapping, UX validation, error recovery" ;;
        "web-content") echo "SEO and AI discovery (GEO) - schema, ChatGPT/Perplexity optimization" ;;
        "web-payments") echo "Stripe Checkout, subscriptions, webhooks, customer portal" ;;
        "woocommerce") echo "WooCommerce REST API - products, orders, customers, webhooks" ;;
        *) echo "Skill for $name" ;;
    esac
}

converted=0

for skill_file in "$SKILLS_DIR"/*.md; do
    if [ -f "$skill_file" ]; then
        filename=$(basename "$skill_file" .md)
        skill_folder="$SKILLS_DIR/$filename"
        skill_md="$skill_folder/SKILL.md"

        echo -n "Converting: $filename ... "

        # Get description
        description=$(get_description "$filename")

        # Create folder
        mkdir -p "$skill_folder"

        # Create SKILL.md with YAML frontmatter + original content
        {
            echo "---"
            echo "name: $filename"
            echo "description: $description"
            echo "---"
            echo ""
            cat "$skill_file"
        } > "$skill_md"

        # Remove original flat file
        rm "$skill_file"

        echo "✓"
        converted=$((converted + 1))
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Conversion complete!"
echo "Converted: $converted skills"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
