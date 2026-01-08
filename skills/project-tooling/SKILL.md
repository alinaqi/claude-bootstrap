---
name: project-tooling
description: gh, vercel, supabase, render CLI and deployment platform setup
---

# Project Tooling Skill

*Load with: base.md*

Standard CLI tools for project infrastructure management.

---

## Required CLI Tools

Before starting any project, verify these tools are installed and authenticated:

### 1. GitHub CLI (gh)
```bash
# Verify installation
gh --version

# Verify authentication
gh auth status

# If not authenticated:
gh auth login
```

### 2. Vercel CLI
```bash
# Verify installation
vercel --version

# Verify authentication
vercel whoami

# If not authenticated:
vercel login
```

### 3. Supabase CLI
```bash
# Verify installation
supabase --version

# Verify authentication (check if linked to a project or logged in)
supabase projects list

# If not authenticated:
supabase login
```

### 4. Render CLI (optional - for Render deployments)
```bash
# Verify installation
render --version

# If using Render API instead:
# Ensure RENDER_API_KEY is set in environment
```

---

## Validation Script

Run this at project initialization to verify all tools:

```bash
#!/bin/bash
# scripts/verify-tooling.sh

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
  echo "✗ GitHub CLI not installed. Run: brew install gh"
  exit 1
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
  echo "✗ Vercel CLI not installed. Run: npm i -g vercel"
  exit 1
fi

# Supabase CLI
if command -v supabase &> /dev/null; then
  if supabase projects list &> /dev/null; then
    echo "✓ Supabase CLI authenticated"
  else
    echo "✗ Supabase CLI not authenticated. Run: supabase login"
    exit 1
  fi
else
  echo "✗ Supabase CLI not installed. Run: brew install supabase/tap/supabase"
  exit 1
fi

echo ""
echo "All tools verified!"
```

---

## GitHub Repository Setup

### Create New Repository
```bash
# Create and push in one command
gh repo create <repo-name> --private --source=. --remote=origin --push

# Or public:
gh repo create <repo-name> --public --source=. --remote=origin --push
```

### Connect Existing Repository
```bash
# If repo exists on GitHub but not linked locally
gh repo clone <owner>/<repo>

# Or add remote to existing local project
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

### Repository Settings
```bash
# Enable branch protection on main
gh api repos/{owner}/{repo}/branches/main/protection -X PUT \
  -F required_status_checks='{"strict":true,"contexts":["quality"]}' \
  -F enforce_admins=false \
  -F required_pull_request_reviews='{"required_approving_review_count":1}'

# Set default branch
gh repo edit --default-branch main
```

---

## Vercel Deployment

### Link Project
```bash
# Link current directory to Vercel project
vercel link

# Or create new project
vercel
```

### Environment Variables
```bash
# Add environment variable
vercel env add ANTHROPIC_API_KEY production

# Pull env vars to local .env
vercel env pull .env.local
```

### Deploy
```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

---

## Supabase Setup

### Create New Project
```bash
# Create project (interactive)
supabase projects create <project-name> --org-id <org-id>

# Link local to remote
supabase link --project-ref <project-ref>
```

### Local Development
```bash
# Start local Supabase
supabase start

# Stop local Supabase
supabase stop

# Reset database (apply all migrations fresh)
supabase db reset
```

### Migrations
```bash
# Create new migration
supabase migration new <migration-name>

# Apply migrations to remote
supabase db push

# Pull remote schema to local
supabase db pull
```

### Generate Types
```bash
# Generate TypeScript types from schema
supabase gen types typescript --local > src/types/database.ts

# Or from remote
supabase gen types typescript --project-id <ref> > src/types/database.ts
```

---

## Render Setup (API-based)

### Environment
```bash
# Set API key
export RENDER_API_KEY=<your-api-key>
```

### Common Operations via API
```bash
# List services
curl -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services

# Trigger deploy
curl -X POST -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services/<service-id>/deploys

# Get deploy status
curl -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services/<service-id>/deploys/<deploy-id>
```

---

## Package.json Scripts

Add these scripts for common operations:

```json
{
  "scripts": {
    "verify-tools": "./scripts/verify-tooling.sh",
    "deploy:preview": "vercel",
    "deploy:prod": "vercel --prod",
    "db:start": "supabase start",
    "db:stop": "supabase stop",
    "db:reset": "supabase db reset",
    "db:migrate": "supabase db push",
    "db:types": "supabase gen types typescript --local > src/types/database.ts"
  }
}
```

---

## CI/CD Integration

### GitHub Actions with Vercel
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: ${{ github.ref == 'refs/heads/main' && '--prod' || '' }}
```

### GitHub Actions with Supabase
```yaml
# .github/workflows/migrate.yml
name: Migrate Database

on:
  push:
    branches: [main]
    paths:
      - 'supabase/migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Supabase CLI
        uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Push migrations
        run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
          SUPABASE_DB_PASSWORD: ${{ secrets.SUPABASE_DB_PASSWORD }}
```

---

## Deployment Platform Setup

**REQUIRED**: When initializing a project, always create todos for deployment platform connection based on the stack.

### Platform Selection by Stack

| Stack | Default Platform | Action Required |
|-------|-----------------|-----------------|
| Next.js / Node.js | **Vercel** | Connect Git repo to Vercel |
| Python (FastAPI, Flask) | **Render** | Connect Git repo to Render, get API key |
| Static sites | **Vercel** or **Cloudflare Pages** | Connect Git repo |

### Vercel: Connect Git Repository

When Vercel is the deployment platform, create this todo:
```
TODO: Connect Git repository to Vercel for automatic deployments
```

Steps:
```bash
# Option 1: Via CLI
vercel link
vercel git connect

# Option 2: Via Dashboard (recommended for first setup)
# 1. Go to vercel.com/new
# 2. Import Git repository
# 3. Configure project settings
# 4. Deploy
```

After connecting:
- Push to `main` → Production deploy
- Push to other branches → Preview deploy
- PRs get deploy previews automatically

### Render: Connect Git Repository (Python)

When Render is the deployment platform for Python projects:

**Step 1: Ask user for Render API key**
```
Before proceeding, please provide your Render API key.
Get it from: https://dashboard.render.com/u/settings/api-keys

Store it securely - we'll add it to your environment.
```

**Step 2: Create todos**
```
TODO: Get Render API key from user
TODO: Connect Git repository to Render
TODO: Configure Render service (web service or background worker)
TODO: Set environment variables on Render
```

**Step 3: Connect via Dashboard (recommended)**
```bash
# 1. Go to dashboard.render.com/create
# 2. Select "Web Service" for APIs, "Background Worker" for async
# 3. Connect your GitHub/GitLab repository
# 4. Configure:
#    - Name: <project-name>
#    - Runtime: Python 3
#    - Build Command: pip install -r requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Step 4: Store API key for CI/CD**
```bash
# Add to GitHub secrets for CI/CD
gh secret set RENDER_API_KEY

# Or add to local env
echo "RENDER_API_KEY=<your-key>" >> .env
```

**Step 5: Configure render.yaml (optional - Infrastructure as Code)**
```yaml
# render.yaml
services:
  - type: web
    name: <project-name>-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
      - key: DATABASE_URL
        fromDatabase:
          name: <project-name>-db
          property: connectionString

databases:
  - name: <project-name>-db
    plan: free
```

### Deployment Checklist Template

Add to project todos when setting up deployment:

```markdown
## Deployment Setup
- [ ] Create Git repository (gh repo create)
- [ ] Choose deployment platform (Vercel/Render/other)
- [ ] Connect Git to deployment platform
- [ ] Configure environment variables
- [ ] Set up CI/CD workflow
- [ ] Verify preview deployments work
- [ ] Configure production domain
```

---

## Tooling Anti-Patterns

- ❌ Hardcoded secrets - use CLI env management or GitHub secrets
- ❌ Manual deployments - automate via CI/CD
- ❌ Skipping local Supabase - always develop locally first
- ❌ Direct production database changes - use migrations
- ❌ No branch protection - require PR reviews and CI checks
- ❌ Missing environment separation - keep dev/staging/prod separate
