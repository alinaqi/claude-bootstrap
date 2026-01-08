---
name: supabase-node
description: Express/Hono with Supabase and Drizzle ORM
---

# Supabase + Node.js Skill

*Load with: base.md + supabase.md + typescript.md*

Express/Hono patterns with Supabase Auth and Drizzle ORM.

**Sources:** [Supabase JS Client](https://supabase.com/docs/reference/javascript/introduction) | [Drizzle ORM](https://orm.drizzle.team/)

---

## Core Principle

**Drizzle for queries, Supabase for auth/storage, middleware for validation.**

Use Drizzle ORM for type-safe database access. Use Supabase client for auth verification, storage, and realtime. Express or Hono for the API layer.

---

## Project Structure

```
project/
├── src/
│   ├── routes/
│   │   ├── index.ts             # Route aggregator
│   │   ├── auth.ts
│   │   ├── posts.ts
│   │   └── users.ts
│   ├── middleware/
│   │   ├── auth.ts              # JWT validation
│   │   ├── error.ts             # Error handler
│   │   └── validate.ts          # Request validation
│   ├── db/
│   │   ├── index.ts             # Drizzle client
│   │   ├── schema.ts            # Schema definitions
│   │   └── queries/             # Query functions
│   ├── lib/
│   │   ├── supabase.ts          # Supabase client
│   │   └── config.ts            # Environment config
│   ├── types/
│   │   └── express.d.ts         # Express type extensions
│   └── index.ts                 # App entry point
├── supabase/
│   ├── migrations/
│   └── config.toml
├── drizzle.config.ts
├── package.json
├── tsconfig.json
└── .env
```

---

## Setup

### Install Dependencies
```bash
npm install express cors helmet dotenv @supabase/supabase-js drizzle-orm postgres zod
npm install -D typescript @types/express @types/cors @types/node tsx drizzle-kit
```

### package.json Scripts
```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "db:generate": "drizzle-kit generate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```

### Environment Variables
```bash
# .env
PORT=3000
NODE_ENV=development

# Supabase
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=<from supabase start>
SUPABASE_SERVICE_ROLE_KEY=<from supabase start>

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres
```

---

## Configuration

### src/lib/config.ts
```typescript
import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();

const envSchema = z.object({
  PORT: z.string().default('3000'),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  SUPABASE_URL: z.string().url(),
  SUPABASE_ANON_KEY: z.string(),
  SUPABASE_SERVICE_ROLE_KEY: z.string(),
  DATABASE_URL: z.string(),
});

export const config = envSchema.parse(process.env);
```

---

## Database Setup

### drizzle.config.ts
```typescript
import { defineConfig } from 'drizzle-kit';
import { config } from './src/lib/config';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './supabase/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: config.DATABASE_URL,
  },
  schemaFilter: ['public'],
});
```

### src/db/index.ts
```typescript
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';
import { config } from '../lib/config';

const client = postgres(config.DATABASE_URL, {
  prepare: false, // Required for Supabase pooling
});

export const db = drizzle(client, { schema });
```

### src/db/schema.ts
```typescript
import {
  pgTable,
  uuid,
  text,
  timestamp,
  boolean,
} from 'drizzle-orm/pg-core';

export const profiles = pgTable('profiles', {
  id: uuid('id').primaryKey(),
  email: text('email').notNull(),
  name: text('name'),
  avatarUrl: text('avatar_url'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
});

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  authorId: uuid('author_id').references(() => profiles.id).notNull(),
  title: text('title').notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

// Type exports
export type Profile = typeof profiles.$inferSelect;
export type NewProfile = typeof profiles.$inferInsert;
export type Post = typeof posts.$inferSelect;
export type NewPost = typeof posts.$inferInsert;
```

---

## Supabase Client

### src/lib/supabase.ts
```typescript
import { createClient, SupabaseClient, User } from '@supabase/supabase-js';
import { config } from './config';

// Client with anon key (respects RLS)
export const supabase = createClient(
  config.SUPABASE_URL,
  config.SUPABASE_ANON_KEY
);

// Admin client (bypasses RLS)
export const supabaseAdmin = createClient(
  config.SUPABASE_URL,
  config.SUPABASE_SERVICE_ROLE_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  }
);

// Verify JWT and get user
export async function verifyToken(token: string): Promise<User | null> {
  const { data: { user }, error } = await supabase.auth.getUser(token);

  if (error || !user) {
    return null;
  }

  return user;
}
```

---

## Type Extensions

### src/types/express.d.ts
```typescript
import { User } from '@supabase/supabase-js';

declare global {
  namespace Express {
    interface Request {
      user?: User;
    }
  }
}

export {};
```

---

## Middleware

### src/middleware/auth.ts
```typescript
import { Request, Response, NextFunction } from 'express';
import { verifyToken } from '../lib/supabase';

export async function requireAuth(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing authorization header' });
  }

  const token = authHeader.split(' ')[1];
  const user = await verifyToken(token);

  if (!user) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  req.user = user;
  next();
}

// Optional auth - continues even without token
export async function optionalAuth(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const authHeader = req.headers.authorization;

  if (authHeader?.startsWith('Bearer ')) {
    const token = authHeader.split(' ')[1];
    req.user = await verifyToken(token) ?? undefined;
  }

  next();
}
```

### src/middleware/error.ts
```typescript
import { Request, Response, NextFunction } from 'express';

export class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error(err);

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ error: err.message });
  }

  return res.status(500).json({ error: 'Internal server error' });
}
```

### src/middleware/validate.ts
```typescript
import { Request, Response, NextFunction } from 'express';
import { z, ZodSchema } from 'zod';

export function validate<T extends ZodSchema>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors,
        });
      }
      next(error);
    }
  };
}
```

---

## Routes

### src/routes/auth.ts
```typescript
import { Router } from 'express';
import { z } from 'zod';
import { supabase } from '../lib/supabase';
import { validate } from '../middleware/validate';

const router = Router();

const signUpSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const signInSchema = z.object({
  email: z.string().email(),
  password: z.string(),
});

router.post('/signup', validate(signUpSchema), async (req, res, next) => {
  try {
    const { email, password } = req.body;

    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      return res.status(400).json({ error: error.message });
    }

    return res.status(201).json({
      user: data.user,
      session: data.session,
    });
  } catch (error) {
    next(error);
  }
});

router.post('/signin', validate(signInSchema), async (req, res, next) => {
  try {
    const { email, password } = req.body;

    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    return res.json({
      user: data.user,
      session: data.session,
    });
  } catch (error) {
    next(error);
  }
});

router.post('/signout', async (req, res) => {
  await supabase.auth.signOut();
  return res.json({ message: 'Signed out' });
});

router.post('/refresh', async (req, res, next) => {
  try {
    const { refresh_token } = req.body;

    const { data, error } = await supabase.auth.refreshSession({
      refresh_token,
    });

    if (error) {
      return res.status(401).json({ error: 'Invalid refresh token' });
    }

    return res.json({
      session: data.session,
    });
  } catch (error) {
    next(error);
  }
});

export default router;
```

### src/routes/posts.ts
```typescript
import { Router } from 'express';
import { z } from 'zod';
import { eq, desc } from 'drizzle-orm';
import { db } from '../db';
import { posts, Post } from '../db/schema';
import { requireAuth, optionalAuth } from '../middleware/auth';
import { validate } from '../middleware/validate';
import { AppError } from '../middleware/error';

const router = Router();

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().optional(),
  published: z.boolean().default(false),
});

const updatePostSchema = createPostSchema.partial();

// List all published posts
router.get('/', optionalAuth, async (req, res, next) => {
  try {
    const result = await db
      .select()
      .from(posts)
      .where(eq(posts.published, true))
      .orderBy(desc(posts.createdAt));

    return res.json(result);
  } catch (error) {
    next(error);
  }
});

// List user's posts
router.get('/me', requireAuth, async (req, res, next) => {
  try {
    const result = await db
      .select()
      .from(posts)
      .where(eq(posts.authorId, req.user!.id))
      .orderBy(desc(posts.createdAt));

    return res.json(result);
  } catch (error) {
    next(error);
  }
});

// Get single post
router.get('/:id', async (req, res, next) => {
  try {
    const [post] = await db
      .select()
      .from(posts)
      .where(eq(posts.id, req.params.id))
      .limit(1);

    if (!post) {
      throw new AppError(404, 'Post not found');
    }

    return res.json(post);
  } catch (error) {
    next(error);
  }
});

// Create post
router.post('/', requireAuth, validate(createPostSchema), async (req, res, next) => {
  try {
    const [post] = await db
      .insert(posts)
      .values({
        ...req.body,
        authorId: req.user!.id,
      })
      .returning();

    return res.status(201).json(post);
  } catch (error) {
    next(error);
  }
});

// Update post
router.patch('/:id', requireAuth, validate(updatePostSchema), async (req, res, next) => {
  try {
    const [post] = await db
      .update(posts)
      .set(req.body)
      .where(eq(posts.id, req.params.id))
      .returning();

    if (!post) {
      throw new AppError(404, 'Post not found');
    }

    return res.json(post);
  } catch (error) {
    next(error);
  }
});

// Delete post
router.delete('/:id', requireAuth, async (req, res, next) => {
  try {
    const [post] = await db
      .delete(posts)
      .where(eq(posts.id, req.params.id))
      .returning();

    if (!post) {
      throw new AppError(404, 'Post not found');
    }

    return res.status(204).send();
  } catch (error) {
    next(error);
  }
});

export default router;
```

### src/routes/index.ts
```typescript
import { Router } from 'express';
import authRoutes from './auth';
import postRoutes from './posts';

const router = Router();

router.use('/auth', authRoutes);
router.use('/posts', postRoutes);

export default router;
```

---

## Main Application

### src/index.ts
```typescript
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import routes from './routes';
import { errorHandler } from './middleware/error';
import { config } from './lib/config';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// API routes
app.use('/api', routes);

// Error handler (must be last)
app.use(errorHandler);

app.listen(config.PORT, () => {
  console.log(`Server running on port ${config.PORT}`);
});

export default app;
```

---

## Query Functions

### src/db/queries/posts.ts
```typescript
import { db } from '../index';
import { posts, profiles } from '../schema';
import { eq, desc, and } from 'drizzle-orm';

export async function getPublishedPosts(limit = 10) {
  return db
    .select({
      id: posts.id,
      title: posts.title,
      content: posts.content,
      author: profiles.name,
      createdAt: posts.createdAt,
    })
    .from(posts)
    .innerJoin(profiles, eq(posts.authorId, profiles.id))
    .where(eq(posts.published, true))
    .orderBy(desc(posts.createdAt))
    .limit(limit);
}

export async function getUserPosts(userId: string) {
  return db
    .select()
    .from(posts)
    .where(eq(posts.authorId, userId))
    .orderBy(desc(posts.createdAt));
}

export async function getPostById(id: string) {
  const [post] = await db
    .select()
    .from(posts)
    .where(eq(posts.id, id))
    .limit(1);

  return post ?? null;
}

export async function createPost(data: {
  title: string;
  content?: string;
  authorId: string;
  published?: boolean;
}) {
  const [post] = await db.insert(posts).values(data).returning();
  return post;
}
```

---

## Storage

### Upload Endpoint
```typescript
import multer from 'multer';
import { supabase } from '../lib/supabase';

const upload = multer({ storage: multer.memoryStorage() });

router.post(
  '/avatar',
  requireAuth,
  upload.single('file'),
  async (req, res, next) => {
    try {
      if (!req.file) {
        throw new AppError(400, 'No file uploaded');
      }

      const fileExt = req.file.originalname.split('.').pop();
      const filePath = `${req.user!.id}/avatar.${fileExt}`;

      const { error } = await supabase.storage
        .from('avatars')
        .upload(filePath, req.file.buffer, {
          contentType: req.file.mimetype,
          upsert: true,
        });

      if (error) {
        throw new AppError(500, 'Upload failed');
      }

      const { data } = supabase.storage
        .from('avatars')
        .getPublicUrl(filePath);

      return res.json({ url: data.publicUrl });
    } catch (error) {
      next(error);
    }
  }
);
```

---

## Hono Alternative

For edge deployments or lighter weight:

### src/index.ts (Hono)
```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { jwt } from 'hono/jwt';
import { db } from './db';
import { posts } from './db/schema';
import { eq, desc } from 'drizzle-orm';
import { config } from './lib/config';

const app = new Hono();

app.use('/*', cors());

// Public routes
app.get('/posts', async (c) => {
  const result = await db
    .select()
    .from(posts)
    .where(eq(posts.published, true))
    .orderBy(desc(posts.createdAt));

  return c.json(result);
});

// Protected routes
app.use('/api/*', async (c, next) => {
  const auth = c.req.header('Authorization');
  if (!auth?.startsWith('Bearer ')) {
    return c.json({ error: 'Unauthorized' }, 401);
  }
  // Verify with Supabase...
  await next();
});

app.post('/api/posts', async (c) => {
  const body = await c.req.json();
  const [post] = await db.insert(posts).values(body).returning();
  return c.json(post, 201);
});

export default app;
```

---

## Testing

### tests/setup.ts
```typescript
import { beforeAll, afterAll, beforeEach } from 'vitest';
import { db } from '../src/db';
import { posts, profiles } from '../src/db/schema';

beforeAll(async () => {
  // Setup test database
});

beforeEach(async () => {
  // Clean tables
  await db.delete(posts);
  await db.delete(profiles);
});

afterAll(async () => {
  // Cleanup
});
```

### tests/posts.test.ts
```typescript
import { describe, it, expect } from 'vitest';
import request from 'supertest';
import app from '../src/index';

describe('Posts API', () => {
  it('should list published posts', async () => {
    const res = await request(app)
      .get('/api/posts')
      .expect(200);

    expect(Array.isArray(res.body)).toBe(true);
  });

  it('should require auth to create post', async () => {
    await request(app)
      .post('/api/posts')
      .send({ title: 'Test' })
      .expect(401);
  });
});
```

---

## Anti-Patterns

- **Using Supabase client for DB queries** - Use Drizzle
- **Sync JWT validation** - Keep it async
- **No input validation** - Use Zod middleware
- **Missing error handling** - Use centralized error handler
- **Hardcoded secrets** - Use environment variables
- **No request logging** - Add morgan or pino
- **Blocking the event loop** - Use async throughout
- **Service key in responses** - Never expose
