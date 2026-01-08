---
name: database-schema
description: Schema awareness - read before coding, type generation, prevent column errors
---

# Database Schema Awareness Skill

*Load with: base.md + [your database skill]*

**Problem:** Claude forgets schema details mid-session - wrong column names, missing fields, incorrect types. TDD catches this at runtime, but we can prevent it earlier.

---

## Core Rule: Read Schema Before Writing Database Code

**MANDATORY: Before writing ANY code that touches the database:**

```
┌─────────────────────────────────────────────────────────────┐
│  1. READ the schema file (see locations below)              │
│  2. VERIFY columns/types you're about to use exist          │
│  3. REFERENCE schema in your response when writing queries  │
│  4. TYPE-CHECK using generated types (Drizzle/Prisma/etc)   │
└─────────────────────────────────────────────────────────────┘
```

**If schema file doesn't exist → CREATE IT before proceeding.**

---

## Schema File Locations (By Stack)

| Stack | Schema Location | Type Generation |
|-------|-----------------|-----------------|
| **Drizzle** | `src/db/schema.ts` or `drizzle/schema.ts` | Built-in TypeScript |
| **Prisma** | `prisma/schema.prisma` | `npx prisma generate` |
| **Supabase** | `supabase/migrations/*.sql` + types | `supabase gen types typescript` |
| **SQLAlchemy** | `app/models/*.py` or `src/models.py` | Pydantic models |
| **TypeORM** | `src/entities/*.ts` | Decorators = types |
| **Raw SQL** | `schema.sql` or `migrations/` | Manual types required |

### Schema Reference File (Recommended)

Create `_project_specs/schema-reference.md` for quick lookup:

```markdown
# Database Schema Reference

*Auto-generated or manually maintained. Claude: READ THIS before database work.*

## Tables

### users
| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | uuid | NO | gen_random_uuid() | PK |
| email | text | NO | - | Unique |
| name | text | YES | - | Display name |
| created_at | timestamptz | NO | now() | - |
| updated_at | timestamptz | NO | now() | - |

### orders
| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | uuid | NO | gen_random_uuid() | PK |
| user_id | uuid | NO | - | FK → users.id |
| status | text | NO | 'pending' | enum: pending/paid/shipped/delivered |
| total_cents | integer | NO | - | Amount in cents |
| created_at | timestamptz | NO | now() | - |

## Relationships
- users 1:N orders (user_id)

## Enums
- order_status: pending, paid, shipped, delivered
```

---

## Pre-Code Checklist (Database Work)

Before writing any database code, Claude MUST:

```markdown
### Schema Verification Checklist
- [ ] Read schema file: `[path to schema]`
- [ ] Columns I'm using exist: [list columns]
- [ ] Types match my code: [list type mappings]
- [ ] Relationships are correct: [list FKs]
- [ ] Nullable fields handled: [list nullable columns]
```

**Example in practice:**

```markdown
### Schema Verification for TODO-042 (Add order history endpoint)

- [x] Read schema: `src/db/schema.ts`
- [x] Columns exist: orders.id, orders.user_id, orders.status, orders.total_cents, orders.created_at
- [x] Types: id=uuid→string, total_cents=integer→number, status=text→OrderStatus enum
- [x] Relationships: orders.user_id → users.id (many-to-one)
- [x] Nullable: none of these columns are nullable
```

---

## Type Generation Commands

### Drizzle (TypeScript)

```typescript
// Schema defines types automatically
// src/db/schema.ts
import { pgTable, uuid, text, integer, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

export const orders = pgTable('orders', {
  id: uuid('id').primaryKey().defaultRandom(),
  userId: uuid('user_id').notNull().references(() => users.id),
  status: text('status').notNull().default('pending'),
  totalCents: integer('total_cents').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

// Inferred types - USE THESE
export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type Order = typeof orders.$inferSelect;
export type NewOrder = typeof orders.$inferInsert;
```

### Prisma

```prisma
// prisma/schema.prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  orders    Order[]
  createdAt DateTime @default(now()) @map("created_at")

  @@map("users")
}

model Order {
  id         String   @id @default(uuid())
  userId     String   @map("user_id")
  user       User     @relation(fields: [userId], references: [id])
  status     String   @default("pending")
  totalCents Int      @map("total_cents")
  createdAt  DateTime @default(now()) @map("created_at")

  @@map("orders")
}
```

```bash
# Generate types after schema changes
npx prisma generate
```

### Supabase

```bash
# Generate TypeScript types from live database
supabase gen types typescript --local > src/types/database.ts

# Or from remote
supabase gen types typescript --project-id your-project-id > src/types/database.ts
```

```typescript
// Use generated types
import { Database } from '@/types/database';

type User = Database['public']['Tables']['users']['Row'];
type NewUser = Database['public']['Tables']['users']['Insert'];
type Order = Database['public']['Tables']['orders']['Row'];
```

### SQLAlchemy (Python)

```python
# app/models/user.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    orders = relationship("Order", back_populates="user")
```

```python
# app/schemas/user.py - Pydantic for API validation
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
```

---

## Schema-Aware TDD Workflow

Extend the standard TDD workflow for database work:

```
┌─────────────────────────────────────────────────────────────┐
│  0. SCHEMA: Read and verify schema before anything else     │
│     └─ Read schema file                                     │
│     └─ Complete Schema Verification Checklist               │
│     └─ Note any missing columns/tables needed               │
├─────────────────────────────────────────────────────────────┤
│  1. RED: Write tests that use correct column names          │
│     └─ Import generated types                               │
│     └─ Use type-safe queries in tests                       │
│     └─ Tests should fail on logic, NOT schema errors        │
├─────────────────────────────────────────────────────────────┤
│  2. GREEN: Implement with type-safe queries                 │
│     └─ Use ORM types, not raw strings                       │
│     └─ TypeScript/mypy catches column mismatches            │
├─────────────────────────────────────────────────────────────┤
│  3. VALIDATE: Type check catches schema drift               │
│     └─ tsc --noEmit / mypy catches wrong columns            │
│     └─ Tests validate runtime behavior                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Common Schema Mistakes (And How to Prevent)

| Mistake | Example | Prevention |
|---------|---------|------------|
| Wrong column name | `user.userName` vs `user.name` | Read schema, use generated types |
| Wrong type | `totalCents` as string | Type generation catches this |
| Missing nullable check | `user.name!` when nullable | Schema shows nullable fields |
| Wrong FK relationship | `order.userId` vs `order.user_id` | Check schema column names |
| Missing column | Using `user.avatar` that doesn't exist | Read schema before coding |
| Wrong enum value | `status: 'complete'` vs `'completed'` | Document enums in schema reference |

### Type-Safe Query Examples

**Drizzle (catches errors at compile time):**
```typescript
// ✅ Correct - uses schema-defined columns
const user = await db.select().from(users).where(eq(users.email, email));

// ❌ Wrong - TypeScript error: 'userName' doesn't exist
const user = await db.select().from(users).where(eq(users.userName, email));
```

**Prisma (catches errors at compile time):**
```typescript
// ✅ Correct
const user = await prisma.user.findUnique({ where: { email } });

// ❌ Wrong - TypeScript error
const user = await prisma.user.findUnique({ where: { userName: email } });
```

**Raw SQL (NO protection - avoid):**
```typescript
// ❌ Dangerous - no type checking, easy to get wrong
const result = await db.query('SELECT * FROM users WHERE user_name = $1', [email]);
// Should be 'email' not 'user_name' - won't catch until runtime
```

---

## Migration Workflow

When schema changes are needed:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Update schema file (Drizzle/Prisma/SQLAlchemy)          │
├─────────────────────────────────────────────────────────────┤
│  2. Generate migration                                       │
│     └─ Drizzle: npx drizzle-kit generate                    │
│     └─ Prisma: npx prisma migrate dev --name add_column     │
│     └─ Supabase: supabase migration new add_column          │
├─────────────────────────────────────────────────────────────┤
│  3. Regenerate types                                         │
│     └─ Prisma: npx prisma generate                          │
│     └─ Supabase: supabase gen types typescript              │
├─────────────────────────────────────────────────────────────┤
│  4. Update schema-reference.md                               │
├─────────────────────────────────────────────────────────────┤
│  5. Run type check - find all broken code                    │
│     └─ npm run typecheck                                    │
├─────────────────────────────────────────────────────────────┤
│  6. Fix type errors, update tests, run full validation       │
└─────────────────────────────────────────────────────────────┘
```

---

## Session Start Protocol

**When starting a session that involves database work:**

1. Read schema file immediately
2. Read `_project_specs/schema-reference.md` if exists
3. Note in session state what tables/columns are relevant
4. Reference schema explicitly when writing code

**Session state example:**
```markdown
## Current Session - Database Context

**Schema read:** ✓ src/db/schema.ts
**Tables in scope:** users, orders, order_items
**Key columns:**
- users: id, email, name, created_at
- orders: id, user_id, status, total_cents
- order_items: id, order_id, product_id, quantity, price_cents
```

---

## Anti-Patterns

- ❌ **Guessing column names** - Always read schema first
- ❌ **Using raw SQL strings** - Use ORM with type generation
- ❌ **Hardcoding without verification** - Check schema before using any column
- ❌ **Ignoring type errors** - Schema drift shows up as type errors
- ❌ **Not regenerating types** - After migration, always regenerate
- ❌ **Assuming nullable** - Check schema for nullable columns

---

## Checklist

### Setup
- [ ] Schema file exists in standard location
- [ ] Type generation configured
- [ ] `_project_specs/schema-reference.md` created
- [ ] Types regenerate on schema change

### Per-Task
- [ ] Schema read before writing database code
- [ ] Schema Verification Checklist completed
- [ ] Using generated types (not raw strings)
- [ ] Type check passes (catches column errors)
- [ ] Tests use correct schema
