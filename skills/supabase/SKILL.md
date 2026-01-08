---
name: supabase
description: Core Supabase CLI, migrations, RLS, Edge Functions
---

# Supabase Core Skill

*Load with: base.md + [supabase-nextjs.md | supabase-python.md | supabase-node.md]*

Core concepts, CLI workflow, and patterns common to all Supabase projects.

**Sources:** [Supabase Docs](https://supabase.com/docs) | [Supabase CLI](https://supabase.com/docs/guides/local-development/cli/getting-started)

---

## Core Principle

**Local-first, migrations in version control, never touch production directly.**

Develop locally with the Supabase CLI, capture all changes as migrations, and deploy through CI/CD.

---

## Supabase Stack

| Service | Purpose |
|---------|---------|
| **Database** | PostgreSQL with extensions |
| **Auth** | User authentication, OAuth providers |
| **Storage** | File storage with RLS |
| **Edge Functions** | Serverless Deno functions |
| **Realtime** | WebSocket subscriptions |
| **Vector** | AI embeddings (pgvector) |

---

## CLI Setup

### Install & Login
```bash
# macOS
brew install supabase/tap/supabase

# npm (alternative)
npm install -g supabase

# Login
supabase login
```

### Initialize Project
```bash
# In your project directory
supabase init

# Creates:
# supabase/
# ├── config.toml      # Local config
# ├── seed.sql         # Seed data
# └── migrations/      # SQL migrations
```

### Link to Remote
```bash
# Get project ref from dashboard URL: https://supabase.com/dashboard/project/<ref>
supabase link --project-ref <project-id>

# Pull existing schema
supabase db pull
```

### Start Local Stack
```bash
supabase start

# Output:
# API URL: http://localhost:54321
# GraphQL URL: http://localhost:54321/graphql/v1
# DB URL: postgresql://postgres:postgres@localhost:54322/postgres
# Studio URL: http://localhost:54323
# Anon key: eyJ...
# Service role key: eyJ...
```

---

## Migration Workflow

### Option 1: Dashboard + Diff (Quick Prototyping)
```bash
# 1. Make changes in local Studio (localhost:54323)
# 2. Generate migration from diff
supabase db diff -f <migration_name>

# 3. Review generated SQL
cat supabase/migrations/*_<migration_name>.sql

# 4. Reset to test
supabase db reset
```

### Option 2: Write Migrations Directly (Recommended)
```bash
# 1. Create empty migration
supabase migration new create_users_table

# 2. Edit the migration file
# supabase/migrations/<timestamp>_create_users_table.sql

# 3. Apply locally
supabase db reset
```

### Option 3: ORM Migrations (Best DX)
Use Drizzle (TypeScript) or SQLAlchemy (Python) - see framework-specific skills.

### Deploy Migrations
```bash
# Push to remote (staging/production)
supabase db push

# Check migration status
supabase migration list
```

---

## Database Patterns

### Enable RLS on All Tables
```sql
-- Always enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Default deny - must create policies
CREATE POLICY "Users can view own profile"
  ON public.profiles
  FOR SELECT
  USING (auth.uid() = id);
```

### Common RLS Policies
```sql
-- Public read
CREATE POLICY "Public read access"
  ON public.posts FOR SELECT
  USING (true);

-- Authenticated users only
CREATE POLICY "Authenticated users can insert"
  ON public.posts FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');

-- Owner access
CREATE POLICY "Users can update own records"
  ON public.posts FOR UPDATE
  USING (auth.uid() = user_id);

-- Admin access (using custom claim)
CREATE POLICY "Admins have full access"
  ON public.posts FOR ALL
  USING (auth.jwt() ->> 'role' = 'admin');
```

### Link to auth.users
```sql
-- Profile table linked to auth
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE NOT NULL,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

---

## Seed Data

### supabase/seed.sql
```sql
-- Runs on `supabase db reset`
-- Use ON CONFLICT for idempotency

INSERT INTO public.profiles (id, username, avatar_url)
VALUES
  ('d0e1f2a3-b4c5-6d7e-8f9a-0b1c2d3e4f5a', 'testuser', null),
  ('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'admin', null)
ON CONFLICT (id) DO NOTHING;
```

---

## Environment Variables

### Required Variables
```bash
# Public (safe for client-side)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...

# Private (server-side only - NEVER expose)
SUPABASE_SERVICE_ROLE_KEY=eyJ...
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-region.pooler.supabase.com:6543/postgres
```

### Local vs Production
```bash
# .env.local (local development)
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=<from supabase start>
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# .env.production (remote)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=<from dashboard>
DATABASE_URL=<connection pooler URL>
```

### Connection Pooling
```bash
# Transaction mode (recommended for serverless)
# Add ?pgbouncer=true to URL
DATABASE_URL=postgresql://...@pooler.supabase.com:6543/postgres?pgbouncer=true

# Session mode (for migrations, long transactions)
DATABASE_URL=postgresql://...@pooler.supabase.com:5432/postgres
```

---

## Edge Functions

### Create Function
```bash
supabase functions new hello-world
```

### Basic Structure
```typescript
// supabase/functions/hello-world/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

serve(async (req) => {
  const { name } = await req.json();

  return new Response(
    JSON.stringify({ message: `Hello ${name}!` }),
    { headers: { 'Content-Type': 'application/json' } }
  );
});
```

### With Auth Context
```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    {
      global: {
        headers: { Authorization: req.headers.get('Authorization')! },
      },
    }
  );

  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return new Response('Unauthorized', { status: 401 });
  }

  return new Response(JSON.stringify({ user_id: user.id }));
});
```

### Deploy
```bash
# Serve locally
supabase functions serve

# Deploy single function
supabase functions deploy hello-world

# Deploy all
supabase functions deploy
```

---

## Storage

### Create Bucket (in migration)
```sql
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

-- Storage policies
CREATE POLICY "Avatar images are publicly accessible"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload own avatar"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );
```

---

## CLI Quick Reference

```bash
# Lifecycle
supabase start                   # Start local stack
supabase stop                    # Stop local stack
supabase status                  # Show status & credentials

# Database
supabase db reset                # Reset + migrations + seed
supabase db push                 # Push to remote
supabase db pull                 # Pull remote schema
supabase db diff -f <name>       # Generate migration from diff
supabase db lint                 # Check for issues

# Migrations
supabase migration new <name>    # Create migration
supabase migration list          # List migrations
supabase migration up            # Apply pending (remote)

# Functions
supabase functions new <name>    # Create function
supabase functions serve         # Local dev
supabase functions deploy        # Deploy all

# Types
supabase gen types typescript --local > types/database.ts

# Project
supabase link --project-ref <id> # Link to remote
supabase projects list           # List projects
```

---

## CI/CD Template

```yaml
# .github/workflows/supabase.yml
name: Supabase CI/CD

on:
  push:
    branches: [main]
  pull_request:

env:
  SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
  SUPABASE_DB_PASSWORD: ${{ secrets.SUPABASE_DB_PASSWORD }}
  SUPABASE_PROJECT_ID: ${{ secrets.SUPABASE_PROJECT_ID }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1

      - name: Start Supabase
        run: supabase start

      - name: Run migrations
        run: supabase db reset

      - name: Lint database
        run: supabase db lint

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1

      - name: Link project
        run: supabase link --project-ref $SUPABASE_PROJECT_ID

      - name: Push migrations
        run: supabase db push

      - name: Deploy functions
        run: supabase functions deploy
```

---

## Anti-Patterns

- **Direct production changes** - Always use migrations
- **Disabled RLS** - Enable on all user-data tables
- **Service key in client** - Never expose service role key
- **No connection pooling** - Use pooler for serverless
- **Committing .env** - Add to .gitignore
- **Skipping migration review** - Always check generated SQL
- **No seed data** - Use seed.sql for consistent local dev
