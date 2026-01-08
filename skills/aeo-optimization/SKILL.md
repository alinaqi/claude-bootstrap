---
name: aeo-optimization
description: AI Engine Optimization - semantic triples, page templates, content clusters for AI citations
---

# AI Engine Optimization (AEO) Skill

*Load with: base.md + web-content.md + site-architecture.md*

**Purpose:** Optimize content for AI engines (ChatGPT, Claude, Perplexity, Google AI Overviews) so your brand gets cited in AI-generated answers.

**Source:** Based on [HubSpot's AEO Guide](https://www.hubspot.com/aeo) and industry best practices.

---

## Why AEO Matters Now

```
┌────────────────────────────────────────────────────────────────┐
│  THE GREAT DECOUPLING                                          │
│  ────────────────────────────────────────────────────────────  │
│  Impressions ≠ Clicks anymore.                                 │
│  AI engines compile answers from multiple sources.             │
│  More buyer journey happens inside chat experiences.           │
│  58% of Google searches = zero clicks (AI overviews).          │
├────────────────────────────────────────────────────────────────┤
│  THE OPPORTUNITY                                               │
│  ────────────────────────────────────────────────────────────  │
│  Shape what AI engines say about your category and product.    │
│  Get cited as the authoritative source.                        │
│  Best answer > Best page ranking.                              │
└────────────────────────────────────────────────────────────────┘
```

**Key Stats:**
- 70% of consumers use ChatGPT for searches
- 47% of Google queries show AI overviews
- Average ChatGPT prompt: 23 words (vs 4.2 for Google)
- AEO market: $886M (2024) → $7.3B (2031)

---

## How AI Engines Choose Answers

AI engines use three main signals to select content for answers:

### 1. Consensus

Facts that appear across multiple credible sources get trusted and reused.

**How to build consensus:**
- Repeat key facts consistently across your own pages
- Use same terminology as industry leaders
- Link to and from authoritative external sources
- Create internal content clusters that reinforce each other

### 2. Information Gain

Net-new insight beats generic advice. AI engines prefer content that adds value.

**How to add information gain:**
- Original research and data
- Concrete examples with specifics
- Clear point of view (not fence-sitting)
- Expert quotes with credentials
- Case studies with metrics

### 3. Entities & Structure

Clear entities and tidy structure reduce ambiguity and boost quotability.

**How to optimize structure:**
- Use semantic triples (Subject → Verb → Object)
- Clear headings with entity names
- Schema markup (Article, FAQ, Product)
- Short, scannable paragraphs (2-4 sentences)

---

## Semantic Triples (Critical for AEO)

**What they are:** Compact facts that AI engines (and humans) can't misread.

**Pattern:** `[Subject]` `[verb]` `[object]`.

### Examples

```
✅ GOOD (clear triples):
- HubSpot CRM syncs contact and company data.
- Lead Scoring assigns priority based on engagement.
- Workflows trigger email sequences from events.

❌ BAD (vague, no clear entity):
- The system helps with various tasks.
- It can do many things for users.
- This improves overall performance.
```

### Triple Checklist

For every key claim, ask:
- [ ] Is the subject a clear entity (product, feature, brand)?
- [ ] Is the verb specific and active?
- [ ] Is the object concrete and measurable?

---

## Paragraph Pattern (Feature → How → Outcome)

Every substantive paragraph should follow this structure:

```
[Feature] helps [User/Role] with [Job].
It [mechanism/inputs] to [process].
Teams see [metric/result] in [timeframe/context].

Triples:
- [Subject] [verb] [object].
- [Subject] [verb] [object].
```

### Example

```markdown
Lead Scoring helps sales teams prioritize prospects. It combines
page views, email engagement, and firmographic data to assign a
numeric score, then auto-enrolls high scorers into follow-up
sequences. Reps focus on qualified accounts and book 40% more
meetings.

- Lead Scoring assigns scores from engagement data.
- High scorers trigger automated follow-up sequences.
```

---

## Page Templates

### Template 1: Category Explainer

**Goal:** Define the category, tie it to your product, earn citations.

```markdown
# What is [Category]? — [1-2 line value promise]

## What is [Category]? (~80 words)
[Plain definition in everyday language. Name adjacent entities.]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

## Why it matters now (~60 words)
[One paragraph. Mention shift to answers over links; tie to buyer outcomes.]

## How to apply it (3-5 bullets)
- [Action 1]
- [Action 2]
- [Action 3]

## FAQ
**Q: [Question]?**
A: [~1 sentence answer]

**Q: [Question]?**
A: [~1 sentence answer]

**Q: [Question]?**
A: [~1 sentence answer]

---
**Links:** [Category hub] | [Product/Feature] | [Credible source 1] | [Credible source 2]
**CTA:** [Demo / Template / Signup]
**Schema:** Article + FAQ. Author + last updated.
```

---

### Template 2: Product & Feature Page

**Goal:** Clarify capability, fit, and next step; reinforce category linkage.

```markdown
# [Product/Feature] — [Outcome in 3-5 words]

**[Product/Feature] enables [Outcome] for [User/Role].**

## [Feature Area 1]
[2-4 sentences using Feature → How → Outcome]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

## [Feature Area 2]
[2-4 sentences using Feature → How → Outcome]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

## [Feature Area 3]
[2-4 sentences using Feature → How → Outcome]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

## FAQ
**Q: [Question]?**
A: [~1 sentence]

**Q: [Question]?**
A: [~1 sentence]

**Q: [Question]?**
A: [~1 sentence]

---
**Links:** Back to [Category Explainer] | Forward to [Demo/Trial]
**Proof:** [Benchmark/Analyst/Customer proof]
**Notes:** Requirements/limits (pricing tier, integrations)
**Schema:** Article + FAQ. Author + last updated.
```

---

### Template 3: Comparison / Alternatives Page

**Goal:** Help readers decide with clear criteria; earn fair citations.

```markdown
# [Product] vs. [Alternative] — Which fits [Use case]?

## Comparison Table

| Criterion | [Product] | [Alt A] | [Alt B] | Source |
|-----------|-----------|---------|---------|--------|
| [Feature/Limit] | [value] | [value] | [value] | [link] |
| [Requirement] | [value] | [value] | [value] | [link] |
| [Best for] | [value] | [value] | [value] | [link] |

*Source-back all claims in the table or footnotes.*

## Fit Statements

1. **[Product]** suits [Team/Use case] when [Condition].
2. **[Alt A]** fits [Team/Use case] when [Condition].
3. **[Alt B]** works for [Team/Use case] when [Condition].

---
**Links:** [Category Explainer] | [Feature pages]
**CTA:** [Try / Demo / Talk to Sales]
**Schema:** Article. Author + last updated.
```

---

### Template 4: Use Case / Industry Page

**Goal:** Connect product to outcomes in a context readers recognize.

```markdown
# [Industry/Use Case] — [Outcome KPI]

**Teams reduce [Metric] by [Y%] in [Timeframe].**

## Mini Case Study
[Company/Role] used [Product/Feature] to [Action], resulting in
[Metric improvement] within [Timeframe].

## How It Works

### [Feature 1]
[Feature → How → Outcome paragraph]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

### [Feature 2]
[Feature → How → Outcome paragraph]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

## Who Uses This
**Roles:** [Role 1], [Role 2], [Role 3]
**Workflows:** [Workflow 1], [Workflow 2]
**Integrations:** [Integration 1], [Integration 2]

---
**Links:** [Product/Feature pages] | [Supporting blog]
**CTA:** [Industry template / Demo variant]
**Schema:** Article. Author + last updated.
```

---

### Template 5: Supporting Blog Post

**Goal:** Add information gain and support your content cluster.

```markdown
# [Topic] — [Specific promise]

## Opening (~60-80 words)
[State the problem. Align terminology with Category Explainer. Preview outcome.]

## [Section 1 Heading] (~120 words max)
[Feature → How → Outcome]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

**Internal link:** [Related page]
**External citation:** [Credible source]

## [Section 2 Heading] (~120 words max)
[Feature → How → Outcome]

Triples:
1. [Subject] [verb] [object].
2. [Subject] [verb] [object].

**Internal link:** [Related page]
**External citation:** [Credible source]

## Key Takeaway
[1-2 lines summarizing the main point]

**CTA:** [Single primary action]

---
**Schema:** Article. Author + last updated.
```

---

## Site-Wide Trust Signals

### Required on Every Page

| Element | Implementation |
|---------|----------------|
| **Schema markup** | Article + FAQ (if FAQ exists) |
| **Author attribution** | Name, bio, credentials, photo |
| **Last updated date** | Visible, machine-readable |
| **Internal links** | 3-5 per page (upstream/downstream) |
| **External citations** | 1-2 credible sources per section |
| **Single CTA** | Demo, template, or signup (repeated once near end) |

### Schema Implementation

```html
<!-- Article Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Page Title]",
  "author": {
    "@type": "Person",
    "name": "[Author Name]",
    "url": "[Author Bio URL]"
  },
  "datePublished": "[ISO Date]",
  "dateModified": "[ISO Date]",
  "publisher": {
    "@type": "Organization",
    "name": "[Company]",
    "logo": "[Logo URL]"
  }
}
</script>

<!-- FAQ Schema (if FAQ section exists) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question 1]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer 1]"
      }
    },
    {
      "@type": "Question",
      "name": "[Question 2]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer 2]"
      }
    }
  ]
}
</script>
```

---

## Content Cluster Architecture

```
                    ┌─────────────────────┐
                    │  Category Explainer │
                    │   "What is AEO?"    │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Product Page  │    │ Product Page  │    │ Product Page  │
│  "Feature A"  │    │  "Feature B"  │    │  "Feature C"  │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Blog Post    │    │  Use Case     │    │  Comparison   │
│  (supports)   │    │  (industry)   │    │  (vs. alt)    │
└───────────────┘    └───────────────┘    └───────────────┘
```

**Linking Rules:**
- Category Explainer links DOWN to all product pages
- Product pages link UP to Category Explainer
- Product pages link ACROSS to related features
- Blog posts link UP to Product pages
- Comparison pages link to Category Explainer + relevant Product pages

---

## AEO Writing Checklist

### Per-Paragraph Checklist

- [ ] Follows Feature → How → Outcome pattern
- [ ] Contains 2-4 sentences (scannable)
- [ ] Includes 1-2 semantic triples
- [ ] Names specific entities (not vague "it" or "this")
- [ ] Uses active voice verbs

### Per-Section Checklist

- [ ] Has 1 internal link (upstream or downstream)
- [ ] Has 1 external citation (credible source)
- [ ] Section heading names an entity
- [ ] ~120 words max

### Per-Page Checklist

- [ ] H1 contains primary entity + value promise
- [ ] Opening claim is a semantic triple
- [ ] 3-5 internal links total
- [ ] 1-2 external citations total
- [ ] Mini-FAQ with 3 questions (if applicable)
- [ ] Single primary CTA
- [ ] Schema markup (Article + FAQ)
- [ ] Author name + bio link
- [ ] Last updated date visible

### Site-Wide Checklist

- [ ] Category Explainer exists for each key category
- [ ] Product pages link back to Category Explainer
- [ ] Content cluster architecture documented
- [ ] Author bio pages exist with credentials
- [ ] Consistent terminology across all pages

---

## Measuring AEO Success

### Key Metrics

| Metric | How to Track |
|--------|--------------|
| **AI citations** | Manual checks in ChatGPT, Claude, Perplexity |
| **Brand mentions in AI** | Search "[brand] + [category]" in AI engines |
| **Share of answer** | How often you're cited vs competitors |
| **LLM traffic** | GA4 referral from chatgpt.com, claude.ai, perplexity.ai |
| **Impressions-to-clicks gap** | GSC impressions vs actual clicks |

### Tools

- **HubSpot AEO Grader** - Grade your brand's AI visibility
- **Google Analytics 4** - Track LLM referral traffic
- **Google Search Console** - Monitor impressions vs clicks gap
- **Manual AI queries** - Regularly test your brand in AI engines

---

## Common AEO Mistakes

| Mistake | Fix |
|---------|-----|
| Vague language ("it helps with things") | Use specific entities and triples |
| No clear structure | Use Feature → How → Outcome |
| Missing schema | Add Article + FAQ schema |
| No author attribution | Add author name, bio, credentials |
| Generic content | Add original data, examples, POV |
| Orphan pages | Link into content cluster |
| Fence-sitting ("it depends") | Take a clear position |
| No external citations | Add 1-2 credible sources per section |

---

## AEO vs Traditional SEO

| Aspect | Traditional SEO | AEO |
|--------|-----------------|-----|
| **Goal** | Rank on page 1 | Get cited in AI answers |
| **Success metric** | Click-through rate | Share of answer |
| **Content focus** | Keywords | Entities + facts |
| **Structure** | Headers for scanning | Triples for extraction |
| **Links** | Backlinks for authority | Citations for consensus |
| **Updates** | Periodic refresh | Continuous accuracy |

---

## Quick Reference

### Semantic Triple Pattern
```
[Entity/Product] [active verb] [concrete object/result].
```

### Paragraph Pattern
```
[Feature] helps [User] with [Job].
It [mechanism] to [process].
Teams see [result] in [timeframe].
```

### Page Minimums
- 3-5 internal links
- 1-2 external citations per section
- 3 FAQ questions with schema
- Author + last updated
- Single CTA

### Content Hierarchy
1. Category Explainer (top)
2. Product/Feature pages (middle)
3. Use case / Comparison / Blog (supporting)
