---
name: supabase-nextjs
description: Next.js with Supabase and Drizzle ORM
---

# Supabase + Next.js Skill

*Load with: base.md + supabase.md + typescript.md*

Next.js App Router patterns with Supabase Auth and Drizzle ORM.

**Sources:** [Supabase Next.js Guide](https://supabase.com/docs/guides/auth/server-side/nextjs) | [Drizzle + Supabase](https://supabase.com/docs/guides/database/drizzle)

---

## Core Principle

**Drizzle for queries, Supabase for auth/storage, server components by default.**

Use Drizzle ORM for type-safe database access. Use Supabase client for auth, storage, and realtime. Prefer server components; use client components only when needed.

---

## Project Structure

```
project/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   ├── signup/page.tsx
│   │   │   └── callback/route.ts
│   │   ├── (dashboard)/
│   │   │   └── page.tsx
│   │   ├── api/
│   │   │   └── [...]/route.ts
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   └── ui/
│   ├── db/
│   │   ├── index.ts              # Drizzle client
│   │   ├── schema.ts             # Schema definitions
│   │   └── queries/              # Query functions
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts         # Browser client
│   │   │   ├── server.ts         # Server client
│   │   │   └── middleware.ts     # Auth middleware helper
│   │   └── auth.ts               # Auth helpers
│   └── middleware.ts             # Next.js middleware
├── supabase/
│   ├── migrations/
│   └── config.toml
├── drizzle.config.ts
└── .env.local
```

---

## Setup

### Install Dependencies
```bash
npm install @supabase/supabase-js @supabase/ssr drizzle-orm postgres
npm install -D drizzle-kit
```

### Environment Variables
```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<from supabase start>

# Server-side only
SUPABASE_SERVICE_ROLE_KEY=<from supabase start>
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres
```

---

## Drizzle Setup

### drizzle.config.ts
```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './supabase/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  schemaFilter: ['public'],
});
```

### src/db/index.ts
```typescript
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!, {
  prepare: false, // Required for Supabase connection pooling
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
  id: uuid('id').primaryKey(), // References auth.users
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

## Supabase Clients

### src/lib/supabase/client.ts (Browser)
```typescript
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### src/lib/supabase/server.ts (Server Components/Actions)
```typescript
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Called from Server Component - ignore
          }
        },
      },
    }
  );
}
```

### src/lib/supabase/middleware.ts (For Middleware)
```typescript
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh session
  const { data: { user } } = await supabase.auth.getUser();

  return { supabaseResponse, user };
}
```

---

## Middleware

### src/middleware.ts
```typescript
import { type NextRequest, NextResponse } from 'next/server';
import { updateSession } from '@/lib/supabase/middleware';

const publicRoutes = ['/', '/login', '/signup', '/auth/callback'];

export async function middleware(request: NextRequest) {
  const { supabaseResponse, user } = await updateSession(request);

  const isPublicRoute = publicRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // Redirect unauthenticated users to login
  if (!user && !isPublicRoute) {
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    url.searchParams.set('redirectTo', request.nextUrl.pathname);
    return NextResponse.redirect(url);
  }

  // Redirect authenticated users away from auth pages
  if (user && (request.nextUrl.pathname === '/login' || request.nextUrl.pathname === '/signup')) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return supabaseResponse;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

---

## Auth Helpers

### src/lib/auth.ts
```typescript
import { redirect } from 'next/navigation';
import { createClient } from '@/lib/supabase/server';

export async function getUser() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  return user;
}

export async function requireAuth() {
  const user = await getUser();
  if (!user) {
    redirect('/login');
  }
  return user;
}

export async function requireGuest() {
  const user = await getUser();
  if (user) {
    redirect('/dashboard');
  }
}
```

---

## Auth Pages

### src/app/(auth)/login/page.tsx
```typescript
import { requireGuest } from '@/lib/auth';
import { LoginForm } from '@/components/auth/login-form';

export default async function LoginPage() {
  await requireGuest();

  return (
    <div className="flex min-h-screen items-center justify-center">
      <LoginForm />
    </div>
  );
}
```

### src/components/auth/login-form.tsx
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const supabase = createClient();
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    router.push('/dashboard');
    router.refresh();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 w-full max-w-sm">
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      {error && <p className="text-red-500">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  );
}
```

### src/app/(auth)/callback/route.ts
```typescript
import { createClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get('code');
  const next = searchParams.get('next') ?? '/dashboard';

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (!error) {
      return NextResponse.redirect(`${origin}${next}`);
    }
  }

  return NextResponse.redirect(`${origin}/login?error=auth_error`);
}
```

---

## Server Actions

### src/app/actions/posts.ts
```typescript
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { db } from '@/db';
import { posts, NewPost } from '@/db/schema';
import { requireAuth } from '@/lib/auth';
import { eq } from 'drizzle-orm';

export async function createPost(formData: FormData) {
  const user = await requireAuth();

  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const [post] = await db.insert(posts).values({
    authorId: user.id,
    title,
    content,
  }).returning();

  revalidatePath('/dashboard');
  redirect(`/posts/${post.id}`);
}

export async function updatePost(id: string, formData: FormData) {
  const user = await requireAuth();

  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.update(posts)
    .set({ title, content })
    .where(eq(posts.id, id));

  revalidatePath(`/posts/${id}`);
}

export async function deletePost(id: string) {
  const user = await requireAuth();

  await db.delete(posts).where(eq(posts.id, id));

  revalidatePath('/dashboard');
  redirect('/dashboard');
}
```

---

## Data Fetching

### src/db/queries/posts.ts
```typescript
import { db } from '@/db';
import { posts, profiles } from '@/db/schema';
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
```

### In Server Components
```typescript
// src/app/dashboard/page.tsx
import { requireAuth } from '@/lib/auth';
import { getUserPosts } from '@/db/queries/posts';

export default async function DashboardPage() {
  const user = await requireAuth();
  const posts = await getUserPosts(user.id);

  return (
    <div>
      <h1>Your Posts</h1>
      {posts.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  );
}
```

---

## Storage

### Upload Component
```typescript
'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';

export function AvatarUpload({ userId }: { userId: string }) {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const supabase = createClient();

    const fileExt = file.name.split('.').pop();
    const filePath = `${userId}/avatar.${fileExt}`;

    const { error } = await supabase.storage
      .from('avatars')
      .upload(filePath, file, { upsert: true });

    if (error) {
      console.error('Upload error:', error);
    }

    setUploading(false);
  };

  return (
    <input
      type="file"
      accept="image/*"
      onChange={handleUpload}
      disabled={uploading}
    />
  );
}
```

### Get Public URL
```typescript
import { createClient } from '@/lib/supabase/server';

export async function getAvatarUrl(userId: string) {
  const supabase = await createClient();

  const { data } = supabase.storage
    .from('avatars')
    .getPublicUrl(`${userId}/avatar.png`);

  return data.publicUrl;
}
```

---

## Realtime

### Client Component with Subscription
```typescript
'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { Post } from '@/db/schema';

export function RealtimePosts({ initialPosts }: { initialPosts: Post[] }) {
  const [posts, setPosts] = useState(initialPosts);

  useEffect(() => {
    const supabase = createClient();

    const channel = supabase
      .channel('posts')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'posts' },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setPosts((prev) => [payload.new as Post, ...prev]);
          } else if (payload.eventType === 'DELETE') {
            setPosts((prev) => prev.filter((p) => p.id !== payload.old.id));
          } else if (payload.eventType === 'UPDATE') {
            setPosts((prev) =>
              prev.map((p) => (p.id === payload.new.id ? payload.new as Post : p))
            );
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

---

## OAuth Providers

### src/components/auth/oauth-buttons.tsx
```typescript
'use client';

import { createClient } from '@/lib/supabase/client';

export function OAuthButtons() {
  const handleOAuth = async (provider: 'google' | 'github') => {
    const supabase = createClient();

    await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
  };

  return (
    <div className="space-y-2">
      <button onClick={() => handleOAuth('google')}>
        Continue with Google
      </button>
      <button onClick={() => handleOAuth('github')}>
        Continue with GitHub
      </button>
    </div>
  );
}
```

---

## Sign Out

### Server Action
```typescript
// src/app/actions/auth.ts
'use server';

import { redirect } from 'next/navigation';
import { createClient } from '@/lib/supabase/server';

export async function signOut() {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect('/login');
}
```

### Sign Out Button
```typescript
'use client';

import { signOut } from '@/app/actions/auth';

export function SignOutButton() {
  return (
    <form action={signOut}>
      <button type="submit">Sign Out</button>
    </form>
  );
}
```

---

## Anti-Patterns

- **Using Supabase client for DB queries** - Use Drizzle for type-safety
- **Fetching in client components** - Prefer server components
- **Not using middleware for auth** - Session refresh is critical
- **Calling `cookies()` synchronously** - Must await in Next.js 15+
- **Service key in client** - Never expose, server-only
- **Missing revalidatePath** - Always revalidate after mutations
- **Not handling auth errors** - Show user-friendly messages
