---
name: build-in-public
description: Best practices for sharing engineering work publicly — what to post, what to withhold, and channel-specific guidance
when-to-use: When drafting build-in-public posts, changelogs, or launch content for social channels
user-invocable: false
effort: low
---

# Build in Public — Best Practices

## Philosophy

Build in public isn't marketing. It's letting people watch you work. The best posts feel like you're narrating your thought process to a friend who's also a senior engineer. No hype sludge. No "I'm excited to announce." Just: here's what I built, here's why it matters, here's what I learned.

## What to Share (and What Not To)

**Share:**
- Technical decisions and the reasoning behind them ("Chose SQLite over Postgres because...")
- Architecture insights ("Here's how the 9-tier routing pipeline works")
- Failures and what you learned ("Spent 3 hours debugging a race condition. Root cause: ...")
- Before/after metrics ("Compaction death spirals: 26 → 0 after Mnemos")
- Open source releases with context, not just links
- Counter-intuitive findings that surprised you

**Never share:**
- Revenue numbers, user counts, valuation
- Customer names or identifiable client details
- Internal URLs, API keys, credentials
- Anything covered by NDA
- Roadmap promises you might not keep
- "We're hiring" disguised as content

## Channel-Specific Best Practices

### LinkedIn

**Audience:** Engineers, CTOs, founders who build. They scroll between meetings looking for something that makes them think.

**Format:**
- 1-3 paragraphs, 800-2000 characters sweet spot
- Lead with the insight, not the context
- Use line breaks generously — wall of text kills engagement
- One clear takeaway per post
- No external links in first paragraph (LinkedIn penalizes off-platform clicks)

**Tone:** Confident, teaches something. You're the senior engineer explaining your approach to a peer. No jargon without explanation. If you used a technique others might not know, explain it briefly.

**When to post:** Tuesday-Thursday, 8-10 AM in target timezone. Avoid weekends and Monday mornings (everyone's catching up).

**What works:**
- Technical deep dives with concrete code examples
- "How I built X" narratives with architecture diagrams
- Lessons learned from failures (these outperform success stories 3:1)
- Opinionated takes on industry trends (but only if you have data)

**What flops:**
- "Excited to announce" press releases
- Pure product updates without technical insight
- Motivational content without substance
- Posts longer than 2500 chars without strong hook

### X (Twitter)

**Audience:** Developers who ship. They scroll fast and judge faster. You have one sentence to earn their attention.

**Format:**
- 280 characters max
- No threads unless the insight genuinely needs 3+ posts
- Lead with the counter-intuitive or surprising element
- One idea per post. If you have two ideas, make two posts.
- Screenshots need alt-text describing what's shown

**Tone:** Sharp, opinionated, zero filler. Imagine you're texting a builder friend. If it sounds like marketing, delete it.

**When to post:** Tuesday-Friday, 9-11 AM or 2-4 PM in target timezone. Weekends can work for developer audience (they're building side projects).

**What works:**
- One-sentence technical insights ("The difference between a good API and a great one is error messages.")
- Before/after comparisons with metrics
- "Just shipped X. Here's the one thing that surprised me."
- Asking genuine technical questions (engagement bait backfires)

**What flops:**
- Hashtag stuffing
- Threads that could be one post
- Generic "hot take" without personal experience
- Posting links without context

## Content Calendar Rhythm

**Daily (if you have something to say):**
- One X post about what you're working on or learned today

**Weekly:**
- One LinkedIn post: deeper technical insight or project milestone

**Per event (triggered by plugin):**
- PR merged → LinkedIn within 24h, X same day
- Feature shipped → both channels, LinkedIn first, X 90 min later
- Review passed → X only (architecture insights are punchy)
- Major release → LinkedIn deep dive + X announcement

## Anti-Patterns to Avoid

1. **The "we" trap** — Solo builders using "we" sounds insecure. Use "I" unless you're actually a team.
2. **Engagement bait** — "Agree?" or "Thoughts?" at the end of every post reads as desperate. Let the insight stand alone.
3. **Posting without building** — If you haven't shipped in 2 weeks, don't post. Your content should be a byproduct of your work, not a substitute for it.
4. **The LinkedIn bro voice** — "I'm humbled and honored to share..." Delete immediately. You're not accepting an award.
5. **Over-polishing** — A post that sounds like it went through 5 rounds of editing reads as corporate. Ship the draft.
6. **Ignoring replies** — If someone takes time to engage, reply within 24h. The conversation in comments often outperforms the original post.

## Measuring What Works

Track these signals (Buffer, LinkedIn analytics, X analytics):
- **Impressions** — how many people saw it
- **Engagement rate** — (likes + comments + reposts) / impressions
- **Profile visits** — did the post drive people to learn more?
- **Inbound** — DMs, connection requests, or emails referencing specific posts

A good LinkedIn post: 3-5% engagement rate. A great one: 8%+. On X, anything above 2% is solid for technical content.

## Plugin Integration

The build-in-public plugin follows these practices automatically:

```yaml
# What gets shared vs skipped:
on_pr_merged:
  - Share if: >3 files changed, meaningful commit message
  - Skip if: typo fix, dependency bump, config change only

on_feature_shipped:
  - Share: always, with screenshot
  - LinkedIn: deep dive on architecture decisions
  - X: punchy one-liner on impact

on_review_passed:
  - Share if: 3/3 unanimous approval
  - X only: architecture insights are punchy
  - Skip if: 1/3 or 0/3 (revisions aren't share-worthy)
```

## Anonymous by Default

All posts are redacted through `anonymize.yaml` before publishing. Company names become generic descriptors. Revenue becomes "at scale." The reader learns about your engineering, not your employer's financials.
