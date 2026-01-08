---
name: site-architecture
description: Technical SEO - robots.txt, sitemap, meta tags, Core Web Vitals
---

# Site Architecture Skill

*Load with: base.md + web-content.md*

For technical website structure that enables discovery by search engines AND AI crawlers (GPTBot, ClaudeBot, PerplexityBot).

---

## Philosophy

**Content is king. Architecture is the kingdom.**

Great content buried in poor architecture won't be discovered. This skill covers the technical foundation that makes your content findable by:
- Google, Bing (traditional search)
- GPTBot (ChatGPT), ClaudeBot, PerplexityBot (AI assistants)
- Social platforms (Open Graph, Twitter Cards)

---

## robots.txt

### Basic Template

```txt
# robots.txt

# Allow all crawlers by default
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /private/
Disallow: /_next/
Disallow: /cdn-cgi/

# Sitemap location
Sitemap: https://yoursite.com/sitemap.xml

# Crawl delay (optional - be careful, not all bots respect this)
# Crawl-delay: 1
```

### AI Bot Configuration

```txt
# robots.txt with AI bot rules

# === SEARCH ENGINES ===
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# === AI ASSISTANTS (Allow for discovery) ===
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

# === BLOCK AI TRAINING (Optional - block training, allow chat) ===
# Uncomment these if you want to be cited but not used for training
# User-agent: CCBot
# Disallow: /

# User-agent: GPTBot
# Disallow: /  # Blocks both chat and training

# === BLOCK SCRAPERS ===
User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /

User-agent: MJ12bot
Disallow: /

# === DEFAULT ===
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /auth/
Disallow: /private/
Disallow: /*.json$
Disallow: /*?*

Sitemap: https://yoursite.com/sitemap.xml
```

### Next.js robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const baseUrl = process.env.NEXT_PUBLIC_URL || 'https://yoursite.com';

  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/admin/', '/private/', '/_next/'],
      },
      {
        userAgent: 'GPTBot',
        allow: '/',
      },
      {
        userAgent: 'ClaudeBot',
        allow: '/',
      },
      {
        userAgent: 'PerplexityBot',
        allow: '/',
      },
    ],
    sitemap: `${baseUrl}/sitemap.xml`,
  };
}
```

---

## Sitemap

### XML Sitemap Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://yoursite.com/</loc>
    <lastmod>2025-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://yoursite.com/pricing</loc>
    <lastmod>2025-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://yoursite.com/blog/article-slug</loc>
    <lastmod>2025-01-12</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>https://yoursite.com/images/article-image.jpg</image:loc>
    </image:image>
  </url>
</urlset>
```

### Next.js Dynamic Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_URL || 'https://yoursite.com';

  // Static pages
  const staticPages = [
    { url: '/', priority: 1.0, changeFrequency: 'weekly' as const },
    { url: '/pricing', priority: 0.9, changeFrequency: 'monthly' as const },
    { url: '/about', priority: 0.8, changeFrequency: 'monthly' as const },
    { url: '/contact', priority: 0.7, changeFrequency: 'yearly' as const },
  ];

  // Dynamic pages (e.g., blog posts)
  const posts = await getBlogPosts(); // Your data fetching function
  const blogPages = posts.map((post) => ({
    url: `/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'monthly' as const,
    priority: 0.8,
  }));

  return [
    ...staticPages.map((page) => ({
      url: `${baseUrl}${page.url}`,
      lastModified: new Date(),
      changeFrequency: page.changeFrequency,
      priority: page.priority,
    })),
    ...blogPages.map((page) => ({
      url: `${baseUrl}${page.url}`,
      lastModified: page.lastModified,
      changeFrequency: page.changeFrequency,
      priority: page.priority,
    })),
  ];
}
```

### Sitemap Index (Large Sites)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://yoursite.com/sitemap-pages.xml</loc>
    <lastmod>2025-01-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://yoursite.com/sitemap-blog.xml</loc>
    <lastmod>2025-01-14</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://yoursite.com/sitemap-products.xml</loc>
    <lastmod>2025-01-13</lastmod>
  </sitemap>
</sitemapindex>
```

---

## Meta Tags

### Essential Meta Tags

```html
<head>
  <!-- Basic -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title | Brand Name</title>
  <meta name="description" content="Compelling 150-160 character description with keywords and CTA.">

  <!-- Canonical (prevent duplicate content) -->
  <link rel="canonical" href="https://yoursite.com/current-page">

  <!-- Language -->
  <html lang="en">
  <meta name="language" content="English">

  <!-- Robots -->
  <meta name="robots" content="index, follow">
  <meta name="googlebot" content="index, follow">

  <!-- Author -->
  <meta name="author" content="Author Name">

  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/icon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.webmanifest">
</head>
```

### Open Graph (Social Sharing)

```html
<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://yoursite.com/page">
<meta property="og:title" content="Page Title - Brand">
<meta property="og:description" content="Description for social sharing (can be longer).">
<meta property="og:image" content="https://yoursite.com/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="Brand Name">
<meta property="og:locale" content="en_US">

<!-- Article-specific (for blog posts) -->
<meta property="og:type" content="article">
<meta property="article:published_time" content="2025-01-15T08:00:00Z">
<meta property="article:modified_time" content="2025-01-20T10:00:00Z">
<meta property="article:author" content="https://yoursite.com/team/author">
<meta property="article:section" content="Technology">
<meta property="article:tag" content="AI, SEO, Content">
```

### Twitter Cards

```html
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@yourbrand">
<meta name="twitter:creator" content="@authorhandle">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Description for Twitter (max 200 chars).">
<meta name="twitter:image" content="https://yoursite.com/twitter-image.jpg">
```

### Next.js Metadata

```typescript
// app/layout.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://yoursite.com'),
  title: {
    default: 'Brand Name',
    template: '%s | Brand Name',
  },
  description: 'Your default site description.',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  authors: [{ name: 'Brand Name', url: 'https://yoursite.com' }],
  creator: 'Brand Name',
  publisher: 'Brand Name',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://yoursite.com',
    siteName: 'Brand Name',
    title: 'Brand Name',
    description: 'Your site description.',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Brand Name',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    site: '@yourbrand',
    creator: '@yourbrand',
  },
  verification: {
    google: 'google-verification-code',
    yandex: 'yandex-verification-code',
  },
};

// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author.name],
      images: [post.coverImage],
    },
  };
}
```

---

## URL Structure

### Best Practices

```markdown
✅ GOOD URLs:
/blog/ai-seo-best-practices
/products/pro-plan
/pricing
/about/team

❌ BAD URLs:
/blog?id=123
/p/12345
/index.php?page=about
/Products/Pro_Plan (inconsistent casing)
```

### URL Guidelines

| Rule | Example |
|------|---------|
| Lowercase only | `/blog/my-post` not `/Blog/My-Post` |
| Hyphens not underscores | `/my-page` not `/my_page` |
| No trailing slashes | `/about` not `/about/` |
| Descriptive slugs | `/pricing` not `/p` |
| No query params for content | `/blog/post-title` not `/blog?id=123` |
| Max 3-4 levels deep | `/blog/category/post` |

### Redirect Configuration

```typescript
// next.config.js
module.exports = {
  async redirects() {
    return [
      // Redirect old URLs to new
      {
        source: '/old-page',
        destination: '/new-page',
        permanent: true, // 301 redirect
      },
      // Redirect with wildcard
      {
        source: '/blog/old/:slug',
        destination: '/articles/:slug',
        permanent: true,
      },
      // Trailing slash redirect
      {
        source: '/:path+/',
        destination: '/:path+',
        permanent: true,
      },
    ];
  },
};
```

---

## Canonical URLs

### Implementation

```html
<!-- Always include canonical, even for primary URL -->
<link rel="canonical" href="https://yoursite.com/current-page">
```

### When to Use

```markdown
✅ USE CANONICAL:
- Every page (even if only version exists)
- Paginated content (point to page 1 or use rel=prev/next)
- URL parameters that don't change content (?utm_source=...)
- HTTP vs HTTPS (canonical to HTTPS)
- www vs non-www (pick one, canonical to it)

Example: /products?sort=price should canonical to /products
```

### Next.js Canonical

```typescript
// Automatic in metadata
export const metadata: Metadata = {
  alternates: {
    canonical: '/current-page',
  },
};
```

---

## Security Headers

### Essential Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on',
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload',
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()',
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

---

## Core Web Vitals

### Target Metrics

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | ≤4.0s | >4.0s |
| INP (Interaction to Next Paint) | ≤200ms | ≤500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | ≤0.25 | >0.25 |

### Optimization Checklist

```markdown
## LCP (Loading)
- [ ] Optimize largest image (WebP, proper sizing)
- [ ] Preload critical assets
- [ ] Use CDN for static assets
- [ ] Enable compression (gzip/brotli)
- [ ] Minimize render-blocking resources

## INP (Interactivity)
- [ ] Minimize JavaScript execution time
- [ ] Break up long tasks
- [ ] Use web workers for heavy computation
- [ ] Optimize event handlers
- [ ] Lazy load non-critical JS

## CLS (Visual Stability)
- [ ] Set dimensions on images/videos
- [ ] Reserve space for dynamic content
- [ ] Avoid inserting content above existing
- [ ] Use transform for animations
- [ ] Preload fonts
```

### Next.js Performance

```typescript
// Image optimization
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={630}
  priority // Preload for LCP
  placeholder="blur"
  blurDataURL={blurDataUrl}
/>

// Font optimization
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap', // Prevent FOIT
});

// Dynamic imports
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false, // Client-only if needed
});
```

---

## Internal Linking

### Structure

```markdown
## Link Architecture

Homepage
├── /pricing (1 click)
├── /features (1 click)
├── /blog (1 click)
│   ├── /blog/category-1 (2 clicks)
│   │   └── /blog/category-1/post (3 clicks)
│   └── /blog/category-2 (2 clicks)
└── /about (1 click)

Rule: Every page within 3 clicks of homepage
```

### Best Practices

```markdown
✅ DO:
- Use descriptive anchor text
- Link contextually within content
- Create hub pages for topics
- Link to related content at end of posts
- Use breadcrumbs for navigation

❌ AVOID:
- "Click here" as anchor text
- Orphan pages (no internal links)
- Too many links per page (>100)
- Broken internal links
- Redirect chains
```

### Breadcrumbs

```typescript
// components/Breadcrumbs.tsx
import Link from 'next/link';

interface BreadcrumbItem {
  name: string;
  href: string;
}

export function Breadcrumbs({ items }: { items: BreadcrumbItem[] }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: `https://yoursite.com${item.href}`,
    })),
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <nav aria-label="Breadcrumb">
        <ol className="flex gap-2">
          {items.map((item, index) => (
            <li key={item.href}>
              {index > 0 && <span>/</span>}
              <Link href={item.href}>{item.name}</Link>
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
}
```

---

## AI Crawler Handling

### Known AI Crawlers

| Bot | User Agent | Purpose |
|-----|------------|---------|
| GPTBot | `GPTBot` | ChatGPT web browsing |
| ChatGPT-User | `ChatGPT-User` | ChatGPT user browsing |
| ClaudeBot | `ClaudeBot` | Claude web access |
| Claude-Web | `Claude-Web` | Claude web features |
| PerplexityBot | `PerplexityBot` | Perplexity search |
| Google-Extended | `Google-Extended` | Gemini/Bard training |
| Amazonbot | `Amazonbot` | Alexa/Amazon AI |
| CCBot | `CCBot` | Common Crawl (AI training) |

### Allow AI Discovery, Block Training (Optional)

```txt
# robots.txt

# Allow GPTBot for ChatGPT browsing
User-agent: GPTBot
Allow: /

# Block CCBot (used for training datasets)
User-agent: CCBot
Disallow: /

# Block Google AI training, allow search
User-agent: Google-Extended
Disallow: /
```

### AI-Specific Meta Tags

```html
<!-- Block AI training but allow indexing -->
<meta name="robots" content="index, follow, max-image-preview:large">

<!-- Opt out of AI training (proposed standard) -->
<meta name="ai-training" content="disallow">
```

---

## Structured Data Placement

### Where to Add Schema

```html
<!-- Option 1: In <head> with JSON-LD (recommended) -->
<head>
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Your Company"
    }
  </script>
</head>

<!-- Option 2: Before closing </body> -->
<body>
  <!-- Page content -->
  <script type="application/ld+json">
    { "@context": "https://schema.org", ... }
  </script>
</body>
```

### Multiple Schema Per Page

```html
<head>
  <!-- Organization (site-wide) -->
  <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "Organization", ... }
  </script>

  <!-- BreadcrumbList (navigation) -->
  <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "BreadcrumbList", ... }
  </script>

  <!-- Article (page-specific) -->
  <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "Article", ... }
  </script>

  <!-- FAQPage (if FAQ section exists) -->
  <script type="application/ld+json">
    { "@context": "https://schema.org", "@type": "FAQPage", ... }
  </script>
</head>
```

---

## Project Structure

```
project/
├── public/
│   ├── robots.txt              # Or generate dynamically
│   ├── sitemap.xml             # Or generate dynamically
│   ├── favicon.ico
│   ├── icon.svg
│   ├── apple-touch-icon.png
│   ├── og-image.jpg            # Default OG image (1200x630)
│   └── manifest.webmanifest
├── app/
│   ├── layout.tsx              # Global metadata
│   ├── robots.ts               # Dynamic robots.txt
│   ├── sitemap.ts              # Dynamic sitemap
│   └── [page]/
│       └── page.tsx            # Page-specific metadata
├── components/
│   ├── SchemaMarkup.tsx
│   ├── Breadcrumbs.tsx
│   └── MetaTags.tsx
└── lib/
    ├── schema.ts               # Schema generators
    └── seo.ts                  # SEO utilities
```

---

## Verification & Submission

### Search Console Setup

```bash
# Verify ownership methods
1. HTML file upload (google*.html to public/)
2. Meta tag (add to <head>)
3. DNS TXT record
4. Google Analytics (if already installed)
```

### Submit Sitemap

```markdown
1. Google Search Console
   - Sitemaps → Add new sitemap → yoursite.com/sitemap.xml

2. Bing Webmaster Tools
   - Sitemaps → Submit sitemap

3. Yandex Webmaster (if relevant)
   - Indexing → Sitemap files
```

---

## Checklist

```markdown
## Technical SEO Checklist

### robots.txt
- [ ] Allow search engines
- [ ] Allow AI bots (GPTBot, ClaudeBot, PerplexityBot)
- [ ] Block admin/private areas
- [ ] Include sitemap reference
- [ ] Test with Google's robots.txt tester

### Sitemap
- [ ] Include all indexable pages
- [ ] Exclude noindex pages
- [ ] Include lastmod dates
- [ ] Submit to Search Console
- [ ] Auto-update on content changes

### Meta Tags
- [ ] Unique title per page (50-60 chars)
- [ ] Unique description per page (150-160 chars)
- [ ] Canonical URL on every page
- [ ] Open Graph tags
- [ ] Twitter Card tags

### URL Structure
- [ ] Lowercase, hyphenated
- [ ] Descriptive slugs
- [ ] No query params for content
- [ ] 301 redirects for moved content
- [ ] No broken links

### Performance
- [ ] LCP < 2.5s
- [ ] INP < 200ms
- [ ] CLS < 0.1
- [ ] HTTPS enabled
- [ ] Security headers configured

### Structured Data
- [ ] Organization schema (homepage)
- [ ] BreadcrumbList (all pages)
- [ ] Article schema (blog posts)
- [ ] FAQ schema (FAQ sections)
- [ ] Validate with Rich Results Test
```

---

## Quick Reference

### File Checklist

```
public/
├── robots.txt          ✓ Required
├── sitemap.xml         ✓ Required
├── favicon.ico         ✓ Required
├── og-image.jpg        ✓ Required (1200x630)
└── manifest.json       ○ Recommended
```

### Meta Tag Lengths

| Tag | Length |
|-----|--------|
| Title | 50-60 characters |
| Description | 150-160 characters |
| OG Title | 60-90 characters |
| OG Description | 200 characters |
| Twitter Description | 200 characters |

### Image Sizes

| Image | Dimensions |
|-------|------------|
| OG Image | 1200 x 630 |
| Twitter Image | 1200 x 628 |
| Favicon | 32 x 32 |
| Apple Touch Icon | 180 x 180 |
