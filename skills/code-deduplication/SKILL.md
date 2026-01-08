---
name: code-deduplication
description: Prevent semantic code duplication with capability index and check-before-write
---

# Code Deduplication Skill

*Load with: base.md*

**Purpose:** Prevent semantic duplication and code bloat. Maintain a capability index so Claude always knows what exists before writing something new.

---

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│  CHECK BEFORE YOU WRITE                                         │
│  ─────────────────────────────────────────────────────────────  │
│  AI doesn't copy/paste - it reimplements.                       │
│  The problem isn't duplicate code, it's duplicate PURPOSE.      │
│                                                                 │
│  Before writing ANY new function:                               │
│  1. Check CODE_INDEX.md for existing capabilities               │
│  2. Search codebase for similar functionality                   │
│  3. Extend existing code if possible                            │
│  4. Only create new if nothing suitable exists                  │
├─────────────────────────────────────────────────────────────────┤
│  AFTER WRITING: Update the index immediately.                   │
│  PERIODICALLY: Run /audit-duplicates to catch overlap.          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Code Index Structure

Maintain `CODE_INDEX.md` in project root, organized by **capability** not file location:

```markdown
# Code Index

*Last updated: [timestamp]*
*Run `/update-code-index` to regenerate*

## Quick Reference

| Category | Count | Location |
|----------|-------|----------|
| Date/Time | 5 functions | src/utils/dates.ts |
| Validation | 8 functions | src/utils/validate.ts |
| API Clients | 12 functions | src/api/*.ts |
| Auth | 6 functions | src/auth/*.ts |

---

## Date/Time Operations

| Function | Location | Does What | Params |
|----------|----------|-----------|--------|
| `formatDate()` | utils/dates.ts:15 | Formats Date → "Jan 15, 2024" | `(date: Date, format?: string)` |
| `formatRelative()` | utils/dates.ts:32 | Formats Date → "2 days ago" | `(date: Date)` |
| `parseDate()` | utils/dates.ts:48 | Parses string → Date | `(str: string, format?: string)` |
| `isExpired()` | auth/tokens.ts:22 | Checks if timestamp past now | `(timestamp: number)` |
| `addDays()` | utils/dates.ts:61 | Adds days to date | `(date: Date, days: number)` |

---

## Validation

| Function | Location | Does What | Params |
|----------|----------|-----------|--------|
| `isEmail()` | utils/validate.ts:10 | Validates email format | `(email: string)` |
| `isPhone()` | utils/validate.ts:25 | Validates phone with country | `(phone: string, country?: string)` |
| `isURL()` | utils/validate.ts:42 | Validates URL format | `(url: string)` |
| `isUUID()` | utils/validate.ts:55 | Validates UUID v4 | `(id: string)` |
| `sanitizeHTML()` | utils/sanitize.ts:12 | Strips XSS from input | `(html: string)` |
| `sanitizeSQL()` | utils/sanitize.ts:28 | Escapes SQL special chars | `(input: string)` |

---

## String Operations

| Function | Location | Does What | Params |
|----------|----------|-----------|--------|
| `slugify()` | utils/strings.ts:8 | Converts to URL slug | `(str: string)` |
| `truncate()` | utils/strings.ts:20 | Truncates with ellipsis | `(str: string, len: number)` |
| `capitalize()` | utils/strings.ts:32 | Capitalizes first letter | `(str: string)` |
| `pluralize()` | utils/strings.ts:40 | Adds s/es correctly | `(word: string, count: number)` |

---

## API Clients

| Function | Location | Does What | Returns |
|----------|----------|-----------|---------|
| `fetchUser()` | api/users.ts:15 | GET /users/:id | `Promise<User>` |
| `fetchUsers()` | api/users.ts:28 | GET /users with pagination | `Promise<User[]>` |
| `createUser()` | api/users.ts:45 | POST /users | `Promise<User>` |
| `updateUser()` | api/users.ts:62 | PATCH /users/:id | `Promise<User>` |
| `deleteUser()` | api/users.ts:78 | DELETE /users/:id | `Promise<void>` |

---

## Error Handling

| Function/Class | Location | Does What |
|----------------|----------|-----------|
| `AppError` | utils/errors.ts:5 | Base error class with code |
| `ValidationError` | utils/errors.ts:20 | Input validation failures |
| `NotFoundError` | utils/errors.ts:32 | Resource not found |
| `handleAsync()` | utils/errors.ts:45 | Wraps async route handlers |
| `errorMiddleware()` | middleware/error.ts:10 | Express error handler |

---

## Hooks (React)

| Hook | Location | Does What |
|------|----------|-----------|
| `useAuth()` | hooks/useAuth.ts | Auth state + login/logout |
| `useUser()` | hooks/useUser.ts | Current user data |
| `useDebounce()` | hooks/useDebounce.ts | Debounces value changes |
| `useLocalStorage()` | hooks/useLocalStorage.ts | Persisted state |
| `useFetch()` | hooks/useFetch.ts | Data fetching with loading/error |

---

## Components (React)

| Component | Location | Does What |
|-----------|----------|-----------|
| `Button` | components/Button.tsx | Styled button with variants |
| `Input` | components/Input.tsx | Form input with validation |
| `Modal` | components/Modal.tsx | Dialog overlay |
| `Toast` | components/Toast.tsx | Notification popup |
| `Spinner` | components/Spinner.tsx | Loading indicator |
```

---

## File Header Format

Every file should have a summary header:

### TypeScript/JavaScript

```typescript
/**
 * @file User authentication utilities
 * @description Handles login, logout, session management, and token refresh.
 *
 * Key exports:
 * - login(email, password) - Authenticates user, returns tokens
 * - logout() - Clears session and tokens
 * - refreshToken() - Gets new access token
 * - validateSession() - Checks if session is valid
 *
 * @see src/api/auth.ts for API endpoints
 * @see src/hooks/useAuth.ts for React hook
 */

import { ... } from '...';
```

### Python

```python
"""
User authentication utilities.

Handles login, logout, session management, and token refresh.

Key exports:
    - login(email, password) - Authenticates user, returns tokens
    - logout() - Clears session and tokens
    - refresh_token() - Gets new access token
    - validate_session() - Checks if session is valid

See Also:
    - src/api/auth.py for API endpoints
    - src/services/user.py for user operations
"""

from typing import ...
```

---

## Function Documentation

Every function needs a one-line summary:

### TypeScript

```typescript
/**
 * Formats a date into a human-readable relative string.
 * Examples: "2 minutes ago", "yesterday", "3 months ago"
 */
export function formatRelative(date: Date): string {
  // ...
}

/**
 * Validates email format and checks for disposable domains.
 * Returns true for valid non-disposable emails.
 */
export function isValidEmail(email: string): boolean {
  // ...
}
```

### Python

```python
def format_relative(date: datetime) -> str:
    """Formats a date into a human-readable relative string.

    Examples: "2 minutes ago", "yesterday", "3 months ago"
    """
    ...

def is_valid_email(email: str) -> bool:
    """Validates email format and checks for disposable domains.

    Returns True for valid non-disposable emails.
    """
    ...
```

---

## Check Before Write Process

### Before Creating ANY New Function

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE WRITING NEW CODE                                        │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  1. DESCRIBE what you need in plain English                     │
│     "I need to format a date as relative time"                  │
│                                                                 │
│  2. CHECK CODE_INDEX.md                                         │
│     Search for: date, time, format, relative                    │
│     → Found: formatRelative() in utils/dates.ts                 │
│                                                                 │
│  3. EVALUATE if existing code works                             │
│     - Does it do what I need? → Use it                          │
│     - Close but not quite? → Extend it                          │
│     - Nothing suitable? → Create new, update index              │
│                                                                 │
│  4. If extending, check for breaking changes                    │
│     - Add optional params, don't change existing behavior       │
│     - Update tests for new functionality                        │
└─────────────────────────────────────────────────────────────────┘
```

### Decision Tree

```
Need new functionality
        │
        ▼
Check CODE_INDEX.md for similar
        │
        ├─► Found exact match ──────► USE IT
        │
        ├─► Found similar ──────────► Can it be extended?
        │                                   │
        │                    ┌──────────────┴──────────────┐
        │                    ▼                             ▼
        │               Yes: Extend                   No: Create new
        │               (add params)                  (update index)
        │
        └─► Nothing found ──────────► Create new (update index)
```

---

## Common Duplication Patterns

### Pattern 1: Utility Function Reimplementation

❌ **Bad:** Creating `validateEmail()` when `isEmail()` exists
```typescript
// DON'T: This already exists as isEmail()
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

✅ **Good:** Check index first, use existing
```typescript
import { isEmail } from '@/utils/validate';

if (isEmail(userInput)) { ... }
```

### Pattern 2: Slightly Different Versions

❌ **Bad:** Multiple date formatters with slight variations
```typescript
// In file A
function formatDate(d: Date) { return d.toLocaleDateString(); }

// In file B
function displayDate(d: Date) { return d.toLocaleDateString('en-US'); }

// In file C
function showDate(d: Date) { return d.toLocaleDateString('en-US', { month: 'short' }); }
```

✅ **Good:** One function with options
```typescript
// utils/dates.ts
function formatDate(d: Date, options?: { locale?: string; format?: 'short' | 'long' }) {
  const locale = options?.locale ?? 'en-US';
  const formatOpts = options?.format === 'short'
    ? { month: 'short', day: 'numeric' }
    : { month: 'long', day: 'numeric', year: 'numeric' };
  return d.toLocaleDateString(locale, formatOpts);
}
```

### Pattern 3: Inline Logic That Should Be Extracted

❌ **Bad:** Same validation logic scattered across files
```typescript
// In signup.ts
if (!email || !email.includes('@') || email.length < 5) { ... }

// In profile.ts
if (!email || !email.includes('@') || email.length < 5) { ... }

// In invite.ts
if (!email || !email.includes('@') || email.length < 5) { ... }
```

✅ **Good:** Extract once, import everywhere
```typescript
// utils/validate.ts
export const isEmail = (email: string) =>
  email && email.includes('@') && email.length >= 5;

// Everywhere else
import { isEmail } from '@/utils/validate';
if (!isEmail(email)) { ... }
```

---

## Periodic Audit

Run `/audit-duplicates` periodically to catch semantic overlap:

### Audit Checklist

- [ ] **Utility functions**: Any functions doing similar things?
- [ ] **API calls**: Multiple ways to fetch same data?
- [ ] **Validation**: Scattered inline validation logic?
- [ ] **Error handling**: Inconsistent error patterns?
- [ ] **Components**: Similar UI components that could merge?
- [ ] **Hooks**: Custom hooks with overlapping logic?

### Audit Output Format

```markdown
## Duplicate Audit - [DATE]

### 🔴 High Priority (Merge These)

1. **Date formatting** - 3 similar functions found
   - `formatDate()` in utils/dates.ts
   - `displayDate()` in components/Header.tsx
   - `showDate()` in pages/Profile.tsx
   - **Action:** Consolidate into utils/dates.ts

2. **Email validation** - Inline logic in 5 files
   - signup.ts:42
   - profile.ts:28
   - invite.ts:15
   - settings.ts:67
   - admin.ts:33
   - **Action:** Extract to utils/validate.ts

### 🟡 Medium Priority (Consider Merging)

1. **User fetching** - 2 different patterns
   - `fetchUser()` in api/users.ts
   - `getUser()` in services/user.ts
   - **Action:** Decide on one pattern

### 🟢 Low Priority (Monitor)

1. **Button components** - 3 variants exist
   - May be intentional for different use cases
   - **Action:** Document the differences
```

---

## Vector DB Integration (Optional)

For large codebases (100+ files), add vector search:

### Setup with ChromaDB

```python
# scripts/index_codebase.py
import chromadb
from chromadb.utils import embedding_functions

# Initialize
client = chromadb.PersistentClient(path="./.chroma")
ef = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection("code_index", embedding_function=ef)

# Index a function
collection.add(
    documents=["Formats a date into human-readable relative string like '2 days ago'"],
    metadatas=[{"function": "formatRelative", "file": "utils/dates.ts", "line": 32}],
    ids=["formatRelative"]
)

# Search before writing
results = collection.query(
    query_texts=["format date as relative time"],
    n_results=5
)
# Returns: formatRelative in utils/dates.ts - 0.92 similarity
```

### Setup with LanceDB (Lighter)

```python
# scripts/index_codebase.py
import lancedb

db = lancedb.connect("./.lancedb")

# Create table
data = [
    {"function": "formatRelative", "file": "utils/dates.ts", "description": "Formats date as relative time"},
    {"function": "isEmail", "file": "utils/validate.ts", "description": "Validates email format"},
]
table = db.create_table("code_index", data)

# Search
results = table.search("validate email address").limit(5).to_list()
```

### When to Use Vector DB

| Codebase Size | Recommendation |
|---------------|----------------|
| < 50 files | Markdown index only |
| 50-200 files | Markdown + periodic audit |
| 200+ files | Add vector DB |
| 500+ files | Vector DB essential |

---

## Claude Instructions

### At Session Start

1. Read `CODE_INDEX.md` if it exists
2. Note the categories and key functions available
3. Keep this context for the session

### Before Writing New Code

1. **Pause and check**: "Does something like this exist?"
2. Search CODE_INDEX.md for similar capabilities
3. If unsure, search the codebase: `grep -r "functionName\|similar_term" src/`
4. Only create new if confirmed nothing suitable exists

### After Writing New Code

1. **Immediately update CODE_INDEX.md**
2. Add file header if new file
3. Add function docstring
4. Commit index update with code

### When User Says "Add X functionality"

```
Before implementing, let me check if we already have something similar...

[Checks CODE_INDEX.md]

Found: `existingFunction()` in utils/file.ts does something similar.
Options:
1. Use existing function as-is
2. Extend it with new capability
3. Create new (if truly different use case)

Which approach would you prefer?
```

---

## Quick Reference

### Update Index Command
```bash
/update-code-index
```

### Audit Command
```bash
/audit-duplicates
```

### File Header Template
```typescript
/**
 * @file [Short description]
 * @description [What this file does]
 *
 * Key exports:
 * - function1() - [what it does]
 * - function2() - [what it does]
 */
```

### Function Template
```typescript
/**
 * [One line description of what it does]
 */
export function name(params): ReturnType {
```

### Index Entry Template
```markdown
| `functionName()` | path/file.ts:line | Does what in plain English | `(params)` |
```
