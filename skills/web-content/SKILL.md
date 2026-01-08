---
name: web-content
description: SEO and AI discovery (GEO) - schema, ChatGPT/Perplexity optimization
---

# Web Content Skill

*Load with: base.md + ui-web.md*

For creating web content optimized for both traditional SEO and AI discovery (ChatGPT, Perplexity, Claude, Gemini).

**Sources:** [GEO Complete Guide](https://skale.so/marketing/geo/) | [AI Search SEO](https://www.gravitatedesign.com/blog/ai-search-seo/) | [LLM Optimization](https://surferseo.com/blog/llm-optimization-seo/) | [Generative Engine Optimization](https://www.siddharthbharath.com/generative-engine-optimization/)

---

## Philosophy

**SEO gets clicks. GEO gets citations.**

Traditional SEO optimizes for Google rankings. Generative Engine Optimization (GEO) optimizes for being cited by AI assistants. Modern content needs both:

- **SEO**: Rank on search results pages
- **GEO**: Be cited in AI-generated answers (ChatGPT, Perplexity, Claude, Gemini)

AI traffic grew 1,200% between July 2024 and February 2025. Google's search share dropped below 90% for the first time in a decade. Optimize for both.

---

## Content Structure for AI + SEO

### The Golden Rule

**Write for humans, structure for machines.**

AI systems prefer:
- Short, clear, fact-based content
- Clean formatting (headers, bullets, tables)
- Standalone sections that can be quoted
- Direct answers to questions

---

## Page Types & Templates

### Homepage

```markdown
## Homepage Structure

### Above the Fold
- **Headline**: Clear value proposition (what you do + for whom)
- **Subheadline**: How you deliver that value
- **Primary CTA**: One clear action
- **Trust signals**: Logos, testimonials, stats

### Content Sections
1. **Problem Statement**: Pain point you solve
2. **Solution Overview**: How you solve it (3-4 key features)
3. **Social Proof**: Testimonials, case studies, logos
4. **How It Works**: 3-step process (simple)
5. **Pricing Preview**: Or link to pricing page
6. **FAQ Section**: 5-7 common questions (GEO gold)
7. **Final CTA**: Repeat primary action

### Schema Required
- Organization schema (name, logo, founding date, social links)
- WebSite schema with SearchAction
- FAQ schema for questions section
```

### Product/Service Page

```markdown
## Product Page Structure

### Hero Section
- **Product Name**: Clear, descriptive
- **One-line Description**: What it does in 10 words or less
- **Key Benefit**: Primary value proposition
- **CTA**: Buy/Try/Demo

### Content Sections
1. **TL;DR Box**: 3-5 bullet summary (AI-quotable)
2. **Problem → Solution**: What problem, how solved
3. **Features Grid**: 4-6 features with icons
4. **Comparison Table**: vs. alternatives (GEO loves these)
5. **Use Cases**: Who uses it and how
6. **Testimonials**: Real names, photos, companies
7. **Pricing**: Clear tiers if applicable
8. **FAQ**: Product-specific questions

### Schema Required
- Product schema (name, description, price, availability)
- Review schema (aggregate rating)
- FAQ schema
- BreadcrumbList schema
```

### Blog Post / Article

```markdown
## Blog Post Structure

### Opening (First 100 words)
- **TL;DR**: Direct answer to the title's question
- **What you'll learn**: Bullet list of takeaways
- This section should be quotable standalone

### Body Structure
- **H2 sections**: Main topics (5-7 per article)
- **H3 subsections**: Supporting points
- **Bullet lists**: For scanability
- **Stat boxes**: Highlight key numbers
- **Comparison tables**: When comparing options

### Content Elements
- Definition boxes ("What is X?")
- Step-by-step instructions
- Code examples (if technical)
- Original statistics/research
- Expert quotes with attribution

### Closing
- **Summary**: Key takeaways (bulleted)
- **Next steps**: What reader should do
- **Related content**: Internal links

### Metadata Required
- Author name + bio + photo
- Publication date
- Last updated date (visible!)
- Reading time
- Article schema with author
```

### FAQ Page

```markdown
## FAQ Page Structure

### Organization
- Group questions by category
- Most common questions first
- Direct, concise answers
- Link to detailed pages for more info

### Question Format
Q: [Exact question users ask]
A: [Direct answer in first sentence, then elaboration]

### Schema Required
- FAQPage schema (critical for AI discovery)
- Each Q&A as Question/Answer schema
```

### Landing Page

```markdown
## Landing Page Structure

### Single Focus
- One offer
- One audience
- One CTA (repeated)

### Sections
1. **Headline**: Benefit-focused, specific
2. **Problem Agitation**: Pain points
3. **Solution**: Your offer
4. **Proof**: Testimonials, stats, logos
5. **Features**: 3-5 key benefits
6. **Objection Handling**: FAQ or guarantee
7. **CTA**: Clear, urgent

### No Navigation
- Remove header nav (reduce exits)
- Single path: read → convert
```

---

## AI-Optimized Content Formats

### TL;DR Boxes

```html
<div class="tldr-box">
  <h3>TL;DR</h3>
  <ul>
    <li>Key point 1 with specific detail</li>
    <li>Key point 2 with number/stat</li>
    <li>Key point 3 with actionable insight</li>
  </ul>
</div>
```

Place at top of articles. AI systems extract these for summaries.

### Definition Blocks

```markdown
## What is [Term]?

[Term] is [concise definition in one sentence]. It [what it does] by [how it works].

**Key characteristics:**
- Characteristic 1
- Characteristic 2
- Characteristic 3
```

Start with "What is X?" - AI systems look for this pattern.

### Comparison Tables

```markdown
| Feature | Product A | Product B | Our Product |
|---------|-----------|-----------|-------------|
| Price | $99/mo | $149/mo | $79/mo |
| Feature 1 | ✓ | ✗ | ✓ |
| Feature 2 | ✗ | ✓ | ✓ |
| Best For | Enterprise | Startups | SMBs |
```

AI loves structured comparisons. Include in product and review pages.

### Stat Boxes

```html
<div class="stat-box">
  <span class="stat-number">73%</span>
  <span class="stat-label">of users prefer AI search for complex queries</span>
  <span class="stat-source">Source: Adobe Analytics, 2024</span>
</div>
```

Original statistics with sources get cited by AI.

### Step-by-Step Guides

```markdown
## How to [Do Thing]

### Step 1: [Action Verb] [Object]
[Explanation of what to do]

**Example:**
[Concrete example]

### Step 2: [Action Verb] [Object]
[Explanation]

### Step 3: [Action Verb] [Object]
[Explanation]

**Result:** [What user achieves]
```

Use HowTo schema markup for these.

---

## Schema Markup (Critical for AI)

### Organization Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Company",
  "url": "https://yoursite.com",
  "logo": "https://yoursite.com/logo.png",
  "foundingDate": "2020",
  "description": "One sentence description",
  "sameAs": [
    "https://twitter.com/yourcompany",
    "https://linkedin.com/company/yourcompany",
    "https://github.com/yourcompany"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "hello@yoursite.com",
    "contactType": "customer service"
  }
}
```

### Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "description": "Meta description",
  "image": "https://yoursite.com/article-image.jpg",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://yoursite.com/team/author-name",
    "jobTitle": "Role at Company",
    "sameAs": [
      "https://linkedin.com/in/author",
      "https://twitter.com/author"
    ]
  },
  "publisher": {
    "@type": "Organization",
    "name": "Your Company",
    "logo": {
      "@type": "ImageObject",
      "url": "https://yoursite.com/logo.png"
    }
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-01-20"
}
```

### FAQ Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is your product?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Direct answer here. Keep concise but complete."
      }
    },
    {
      "@type": "Question",
      "name": "How much does it cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Pricing starts at $X/month for basic plan..."
      }
    }
  ]
}
```

### Product Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description",
  "image": "https://yoursite.com/product.jpg",
  "brand": {
    "@type": "Brand",
    "name": "Your Company"
  },
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127"
  }
}
```

### HowTo Schema

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Set Up Your Account",
  "description": "Step-by-step guide to getting started",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Create account",
      "text": "Go to signup page and enter your email"
    },
    {
      "@type": "HowToStep",
      "name": "Verify email",
      "text": "Click the link in the verification email"
    }
  ]
}
```

---

## Platform-Specific Optimization

### ChatGPT Optimization

```markdown
✅ DO:
- TL;DR sections at top of articles
- Consistent formatting (headers, bullets)
- Named authors with credentials
- Original research and statistics
- Multi-intent content (covers related questions)

❌ AVOID:
- Thin content without substance
- Missing author attribution
- Outdated information (no dates)
```

### Perplexity Optimization

```markdown
✅ DO:
- Original statistics with sources
- Comparison tables and structured data
- Clean URL slugs (/topic-name not /p=123)
- Short, declarative statements
- Images, charts, diagrams
- YouTube videos (Perplexity shows these)

❌ AVOID:
- Generic content without unique insights
- Missing citations/sources
- Poor URL structure
```

### Claude Optimization

```markdown
✅ DO:
- Well-structured, logical content
- Clear definitions and explanations
- Technical accuracy
- Balanced perspectives
- Proper citations

❌ AVOID:
- Misleading or sensational content
- Missing context
- Outdated technical information
```

### Gemini Optimization

```markdown
✅ DO:
- Rich schema markup
- Detailed image alt-text
- YouTube content (Google-owned)
- Multimedia (video, audio with transcripts)

❌ AVOID:
- Missing structured data
- Images without alt-text
- Text-only content
```

---

## E-E-A-T for AI Discovery

### Experience
- First-person case studies
- "We tested X and found Y"
- Original screenshots and data
- User testimonials with real details

### Expertise
- Author bios with credentials
- Link to author's other work
- Industry-specific terminology
- Technical depth appropriate to topic

### Authoritativeness
- Backlinks from trusted sources
- Mentions in industry publications
- Citations from other experts
- Social proof (followers, engagement)

### Trustworthiness
- Contact information visible
- About page with team details
- Privacy policy and terms
- Secure site (HTTPS)
- Accurate, up-to-date info

---

## Content Freshness

### Visible Dates (Required)

```html
<article>
  <header>
    <h1>Article Title</h1>
    <div class="meta">
      <span class="author">By John Smith</span>
      <span class="published">Published: January 15, 2025</span>
      <span class="updated">Last updated: January 20, 2025</span>
    </div>
  </header>
</article>
```

AI systems prefer recent content. Show dates prominently.

### Update Schedule

| Content Type | Update Frequency |
|--------------|------------------|
| Product pages | On feature changes |
| Pricing | Immediately on change |
| Blog posts | Quarterly review |
| Statistics | When new data available |
| Guides | Semi-annually |

---

## Analytics for AI Traffic

### GA4 Regex Filter

```regex
.*chatgpt\.com.*|.*perplexity\.ai.*|.*gemini\.google\.com.*|.*copilot\.microsoft\.com.*|.*openai\.com.*|.*claude\.ai.*|.*poe\.com.*|.*you\.com.*|.*phind\.com.*
```

### Track AI Referrals

```javascript
// Check for AI referrer
const aiReferrers = [
  'chatgpt.com',
  'chat.openai.com',
  'perplexity.ai',
  'claude.ai',
  'gemini.google.com',
  'copilot.microsoft.com',
  'poe.com',
  'you.com',
  'phind.com'
];

const referrer = document.referrer;
const isAIReferral = aiReferrers.some(ai => referrer.includes(ai));

if (isAIReferral) {
  analytics.track('ai_referral', {
    source: referrer,
    page: window.location.pathname
  });
}
```

### Survey for AI Discovery

Add to forms:
```markdown
How did you hear about us?
- [ ] Google Search
- [ ] ChatGPT
- [ ] Perplexity
- [ ] Claude
- [ ] Social Media
- [ ] Referral
- [ ] Other
```

---

## Content Checklist

### Before Publishing

```markdown
## SEO Checklist
- [ ] Title tag (50-60 chars) with primary keyword
- [ ] Meta description (150-160 chars) with CTA
- [ ] URL slug is clean and descriptive
- [ ] H1 matches title intent
- [ ] H2/H3 hierarchy is logical
- [ ] Images have descriptive alt-text
- [ ] Internal links to related content
- [ ] External links to authoritative sources

## GEO Checklist
- [ ] TL;DR or summary at top
- [ ] Direct answer to main question in first paragraph
- [ ] Stat boxes with sources
- [ ] Comparison tables where applicable
- [ ] FAQ section with schema
- [ ] Author name, bio, and credentials
- [ ] Publication and last-updated dates visible
- [ ] Schema markup validated
- [ ] Content can be quoted standalone
- [ ] Original insights or data included
```

### Schema Validation

```bash
# Validate schema markup
# Use: https://validator.schema.org/
# Or: https://search.google.com/test/rich-results
```

---

## Project Structure

```
project/
├── content/
│   ├── pages/
│   │   ├── home.md
│   │   ├── about.md
│   │   ├── pricing.md
│   │   └── contact.md
│   ├── blog/
│   │   ├── post-1.md
│   │   └── post-2.md
│   └── legal/
│       ├── privacy.md
│       └── terms.md
├── components/
│   ├── SchemaMarkup.tsx
│   ├── TLDRBox.tsx
│   ├── StatBox.tsx
│   ├── FAQSection.tsx
│   └── AuthorBio.tsx
└── lib/
    └── schema.ts           # Schema generators
```

---

## Anti-Patterns

- **No dates** - AI deprioritizes undated content
- **Anonymous content** - No author = no E-E-A-T
- **Walls of text** - Break up with headers, bullets, boxes
- **Generic content** - Add original insights, data, opinions
- **Missing schema** - Invisible to structured data crawlers
- **Outdated info** - Update quarterly minimum
- **No FAQ** - Missing easy GEO win
- **Poor URL structure** - Use /topic-name not /p=12345

---

## Quick Reference

### Content Formats AI Loves
1. TL;DR summaries
2. Definition boxes ("What is X?")
3. Comparison tables
4. Step-by-step guides
5. FAQ sections
6. Stat boxes with sources
7. Listicles with numbers

### Required Schema by Page Type

| Page Type | Schema |
|-----------|--------|
| Homepage | Organization, WebSite |
| Blog Post | Article, Author, FAQ |
| Product | Product, Review, FAQ |
| FAQ | FAQPage |
| How-to | HowTo |
| About | Organization, Person |
