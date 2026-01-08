---
name: credentials
description: Centralized API key management from Access.txt
---

# Credentials Management Skill

*Load with: base.md*

For securely loading API keys from a centralized access file and configuring project environments.

---

## Credentials File Discovery

**REQUIRED**: When a project needs API keys, ask the user:

```
I need API credentials for [service]. Do you have a centralized access keys file?

Please provide the path (e.g., ~/Documents/Access.txt) or type 'manual' to enter keys directly.
```

### Default Locations to Check

```bash
~/Documents/Access.txt
~/Access.txt
~/.secrets/keys.txt
~/.credentials.txt
```

---

## Supported File Formats

The credentials file can use any of these formats:

### Format 1: Colon-separated
```
Render API: rnd_xxxxx
OpenAI API: sk-proj-xxxxx
Claude API: sk-ant-xxxxx
Reddit client id: xxxxx
Reddit secret: xxxxx
```

### Format 2: Key=Value
```
RENDER_API_KEY=rnd_xxxxx
OPENAI_API_KEY=sk-proj-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### Format 3: Mixed/Informal
```
Reddit api access:
client id Y1FgKALKmb6f6UxFtyMXfA
and secret is -QLoYdxMqOJkYrgk5KeGPa6Ps6vIiQ
```

---

## Key Identification Patterns

Use these patterns to identify keys in the file:

| Service | Pattern | Env Variable |
|---------|---------|--------------|
| OpenAI | `sk-proj-*` or `sk-*` | `OPENAI_API_KEY` |
| Claude/Anthropic | `sk-ant-*` | `ANTHROPIC_API_KEY` |
| Render | `rnd_*` | `RENDER_API_KEY` |
| Eleven Labs | `sk_*` (not sk-ant/sk-proj) | `ELEVEN_LABS_API_KEY` |
| Replicate | `r8_*` | `REPLICATE_API_TOKEN` |
| Supabase | URL + `eyJ*` (JWT) | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` |
| Reddit | client_id + secret pair | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` |
| GitHub | `ghp_*` or `github_pat_*` | `GITHUB_TOKEN` |
| Vercel | `*_*` (from vercel.com) | `VERCEL_TOKEN` |
| Stripe (Test) | `sk_test_*`, `pk_test_*` | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` |
| Stripe (Live) | `sk_live_*`, `pk_live_*` | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` |
| Stripe Webhook | `whsec_*` | `STRIPE_WEBHOOK_SECRET` |
| Twilio | `SK*` + Account SID | `TWILIO_API_KEY`, `TWILIO_ACCOUNT_SID` |
| SendGrid | `SG.*` | `SENDGRID_API_KEY` |
| AWS | `AKIA*` + secret | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| PostHog | `phc_*` | `POSTHOG_API_KEY`, `NEXT_PUBLIC_POSTHOG_KEY` |

---

## Parsing Credentials File

When reading the user's access file, extract keys using these rules:

```python
# Python parsing logic
import re
from pathlib import Path

def parse_credentials_file(file_path: str) -> dict[str, str]:
    """Parse various credential file formats."""
    content = Path(file_path).expanduser().read_text()
    credentials = {}

    # Pattern matching for known key formats
    patterns = {
        'OPENAI_API_KEY': r'sk-proj-[A-Za-z0-9_-]+',
        'ANTHROPIC_API_KEY': r'sk-ant-[A-Za-z0-9_-]+',
        'RENDER_API_KEY': r'rnd_[A-Za-z0-9]+',
        'REPLICATE_API_TOKEN': r'r8_[A-Za-z0-9]+',
        'ELEVEN_LABS_API_KEY': r'sk_[a-f0-9]{40,}',
        'GITHUB_TOKEN': r'ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+',
        'STRIPE_SECRET_KEY': r'sk_(live|test)_[A-Za-z0-9]+',
        'STRIPE_PUBLISHABLE_KEY': r'pk_(live|test)_[A-Za-z0-9]+',
        'STRIPE_WEBHOOK_SECRET': r'whsec_[A-Za-z0-9]+',
        'POSTHOG_API_KEY': r'phc_[A-Za-z0-9]+',
    }

    # Supabase requires special handling (URL + JWT tokens)
    supabase_url = re.search(r'https://[a-z0-9]+\.supabase\.co', content)
    anon_key = re.search(r'anon[^:]*:\s*(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', content, re.I)
    service_role = re.search(r'service.?role[^:]*:\s*(eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)', content, re.I)

    if supabase_url:
        credentials['SUPABASE_URL'] = supabase_url.group(0)
    if anon_key:
        credentials['SUPABASE_ANON_KEY'] = anon_key.group(1)
    if service_role:
        credentials['SUPABASE_SERVICE_ROLE_KEY'] = service_role.group(1)

    for env_var, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            credentials[env_var] = match.group(0)

    # Reddit requires special handling (client_id + secret pair)
    reddit_id = re.search(r'client.?id[:\s]+([A-Za-z0-9_-]+)', content, re.I)
    reddit_secret = re.search(r'secret[:\s]+([A-Za-z0-9_-]+)', content, re.I)
    if reddit_id:
        credentials['REDDIT_CLIENT_ID'] = reddit_id.group(1)
    if reddit_secret:
        credentials['REDDIT_CLIENT_SECRET'] = reddit_secret.group(1)

    return credentials
```

```typescript
// TypeScript parsing logic
function parseCredentialsFile(content: string): Record<string, string> {
  const credentials: Record<string, string> = {};

  const patterns: Record<string, RegExp> = {
    OPENAI_API_KEY: /sk-proj-[A-Za-z0-9_-]+/,
    ANTHROPIC_API_KEY: /sk-ant-[A-Za-z0-9_-]+/,
    RENDER_API_KEY: /rnd_[A-Za-z0-9]+/,
    REPLICATE_API_TOKEN: /r8_[A-Za-z0-9]+/,
    ELEVEN_LABS_API_KEY: /sk_[a-f0-9]{40,}/,
    GITHUB_TOKEN: /ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+/,
    STRIPE_SECRET_KEY: /sk_(live|test)_[A-Za-z0-9]+/,
    STRIPE_PUBLISHABLE_KEY: /pk_(live|test)_[A-Za-z0-9]+/,
    STRIPE_WEBHOOK_SECRET: /whsec_[A-Za-z0-9]+/,
    POSTHOG_API_KEY: /phc_[A-Za-z0-9]+/,
  };

  for (const [envVar, pattern] of Object.entries(patterns)) {
    const match = content.match(pattern);
    if (match) credentials[envVar] = match[0];
  }

  // Reddit pair
  const redditId = content.match(/client.?id[:\s]+([A-Za-z0-9_-]+)/i);
  const redditSecret = content.match(/secret[:\s]+([A-Za-z0-9_-]+)/i);
  if (redditId) credentials.REDDIT_CLIENT_ID = redditId[1];
  if (redditSecret) credentials.REDDIT_CLIENT_SECRET = redditSecret[1];

  return credentials;
}
```

---

## Validation Commands

After extracting keys, validate them:

### OpenAI
```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
# 200 = valid
```

### Anthropic/Claude
```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  https://api.anthropic.com/v1/models
# 200 = valid
```

### Render
```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  https://api.render.com/v1/services
# 200 = valid
```

### Reddit
```bash
# Get OAuth token first
TOKEN=$(curl -s -X POST \
  -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
  -d "grant_type=client_credentials" \
  -A "CredentialTest/1.0" \
  https://www.reddit.com/api/v1/access_token | jq -r '.access_token')
# Non-null token = valid
```

### Replicate
```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Token $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/models
# 200 = valid
```

---

## Project Setup Workflow

When initializing a project that needs API keys:

### Step 1: Ask for Credentials File
```
This project needs the following API keys:
- ANTHROPIC_API_KEY (for Claude)
- SUPABASE_URL and SUPABASE_ANON_KEY

Do you have an access keys file? Please provide the path:
```

### Step 2: Read and Parse
```python
# Read the file
credentials = parse_credentials_file("~/Documents/Access.txt")

# Show what was found
print("Found credentials:")
for key, value in credentials.items():
    masked = value[:8] + "..." + value[-4:]
    print(f"  {key}: {masked}")
```

### Step 3: Validate Keys
```
Validating credentials...
✓ ANTHROPIC_API_KEY: Valid
✓ REDDIT_CLIENT_ID: Valid
✗ SUPABASE_URL: Not found in file
```

### Step 4: Create .env File
```bash
# Write to project .env
cat > .env << EOF
# Auto-generated from ~/Documents/Access.txt
ANTHROPIC_API_KEY=sk-ant-xxx...
REDDIT_CLIENT_ID=xxx...
REDDIT_CLIENT_SECRET=xxx...
EOF

# Add to .gitignore if not present
echo ".env" >> .gitignore
```

### Step 5: Report Missing Keys
```
Missing credentials that need manual setup:
- SUPABASE_URL: Get from supabase.com/dashboard/project/[ref]/settings/api
- SUPABASE_ANON_KEY: Same location as above

Would you like me to open these URLs?
```

---

## Service-Specific Setup Guides

### Reddit (from Access.txt)
```
Found in your access file:
- REDDIT_CLIENT_ID: Y1FgKA...
- REDDIT_CLIENT_SECRET: -QLoYd...

Also needed (add to Access.txt or enter manually):
- REDDIT_USER_AGENT: YourApp/1.0 by YourUsername
```

### Supabase (typically not in file)
```
Supabase credentials are project-specific. Get them from:
https://supabase.com/dashboard/project/[your-ref]/settings/api

Required:
- SUPABASE_URL
- SUPABASE_ANON_KEY
- SUPABASE_SERVICE_ROLE_KEY (for admin operations)
```

---

## Security Rules

- **NEVER** commit Access.txt or its path to git
- **NEVER** log full API keys - always mask middle characters
- **ALWAYS** add `.env` to `.gitignore`
- **ALWAYS** use environment variables, never hardcode keys
- **VALIDATE** keys before using them in production setup

---

## Quick Reference

```bash
# Check if credentials file exists
ls -la ~/Documents/Access.txt

# Common env var names
OPENAI_API_KEY
ANTHROPIC_API_KEY
RENDER_API_KEY
REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET
REPLICATE_API_TOKEN
ELEVEN_LABS_API_KEY
SUPABASE_URL
SUPABASE_ANON_KEY
GITHUB_TOKEN
```

### Prompt Template
```
I need API credentials for this project.

Do you have a centralized access keys file (like ~/Documents/Access.txt)?

If yes, provide the path and I'll:
1. Read and parse your keys
2. Validate they're working
3. Set up your project's .env file
4. Tell you which keys are missing
```
