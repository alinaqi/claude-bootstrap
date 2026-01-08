---
name: user-journeys
description: User experience flows - journey mapping, UX validation, error recovery
---

# User Journeys Skill

*Load with: base.md + playwright-testing.md*

For defining and testing real user experiences - not just specs, but actual flows humans take through your application.

---

## Philosophy

**Specs test features. Journeys test experiences.**

A feature can pass all specs but still deliver a terrible experience. User journeys capture:
- How users actually navigate (not how we think they should)
- Emotional states at each step (frustrated, confused, delighted)
- Recovery from mistakes (users will make them)
- Real-world conditions (slow networks, interruptions, distractions)

---

## Journey Documentation Structure

```
_project_specs/
├── journeys/
│   ├── _template.md              # Journey template
│   ├── critical/                 # Must-work journeys (revenue, core value)
│   │   ├── signup-to-first-value.md
│   │   ├── checkout-purchase.md
│   │   └── login-to-dashboard.md
│   ├── common/                   # Frequent user paths
│   │   ├── browse-and-search.md
│   │   ├── update-profile.md
│   │   └── invite-team-member.md
│   └── edge-cases/               # Error recovery, unusual paths
│       ├── payment-failure-retry.md
│       ├── session-timeout-recovery.md
│       └── offline-reconnection.md
```

---

## Journey Template

```markdown
# Journey: [Name]

## Overview
| Attribute | Value |
|-----------|-------|
| **Priority** | Critical / High / Medium |
| **User Type** | New / Returning / Admin |
| **Frequency** | Daily / Weekly / One-time |
| **Success Metric** | Conversion rate, time to complete, drop-off rate |

## User Goal
What is the user trying to accomplish? Write from their perspective.

> "I want to [goal] so that I can [benefit]."

## Preconditions
- User state (logged in, has subscription, first visit)
- Data state (has items in cart, has team members)
- Environment (mobile, desktop, slow connection)

## Journey Steps

### Step 1: [Entry Point]
**User Action:** What the user does
**System Response:** What they should see/experience
**Success Criteria:**
- [ ] Page loads in < 2 seconds
- [ ] Primary CTA is immediately visible
- [ ] User understands what to do next

**Potential Friction:**
- Slow load time → Show skeleton/loader
- Unclear CTA → A/B test copy variations

---

### Step 2: [Next Action]
**User Action:** ...
**System Response:** ...
**Success Criteria:**
- [ ] ...

**Potential Friction:**
- ...

---

## Error Scenarios

### E1: [Error Name]
**Trigger:** What causes this error
**User Sees:** Error message/state
**Recovery Path:** How user gets back on track
**Test:** How to verify recovery works

## Metrics to Track
- Time to complete journey
- Drop-off rate at each step
- Error rate and recovery rate
- User satisfaction (if surveyed)

## E2E Test Reference
Link to Playwright test: `e2e/tests/journeys/[name].spec.ts`
```

---

## Critical Journey Examples

### Signup to First Value

```markdown
# Journey: Signup to First Value

## Overview
| Attribute | Value |
|-----------|-------|
| **Priority** | Critical |
| **User Type** | New |
| **Frequency** | One-time |
| **Success Metric** | % reaching "aha moment" within 5 min |

## User Goal
> "I want to try this product quickly to see if it solves my problem."

## Preconditions
- First visit to site
- No account
- Came from landing page or ad

## Journey Steps

### Step 1: Landing Page
**User Action:** Clicks "Get Started Free" or "Try Now"
**System Response:** Signup form appears (modal or new page)
**Success Criteria:**
- [ ] CTA visible above fold
- [ ] No distracting elements
- [ ] Clear value proposition visible

**Potential Friction:**
- Too many form fields → Reduce to email + password only
- Social login missing → Add Google/GitHub options

### Step 2: Account Creation
**User Action:** Enters email and password (or uses social login)
**System Response:**
- Creates account
- Sends verification email (don't block on it)
- Redirects to onboarding

**Success Criteria:**
- [ ] Account created in < 3 seconds
- [ ] No email verification wall (verify later)
- [ ] Clear next step shown

**Potential Friction:**
- Email already exists → Offer login link
- Weak password → Show requirements inline, not after submit

### Step 3: Onboarding (Quick Win)
**User Action:** Completes 1-2 setup questions
**System Response:**
- Personalizes experience
- Shows progress indicator
- Leads to first action

**Success Criteria:**
- [ ] Max 3 questions
- [ ] Skip option available
- [ ] < 60 seconds total

**Potential Friction:**
- Too many questions → User abandons
- No skip option → User feels trapped

### Step 4: First Value (Aha Moment)
**User Action:** Completes core action (creates first X, sees first result)
**System Response:**
- Celebrates success
- Shows value delivered
- Suggests next step

**Success Criteria:**
- [ ] User experiences core value
- [ ] Completion feels rewarding
- [ ] Clear path to continue

## Error Scenarios

### E1: Email Already Registered
**Trigger:** User tries existing email
**User Sees:** "Already have an account? Log in or reset password"
**Recovery Path:** Click to login or reset
**Test:** `signup-existing-email.spec.ts`

### E2: Social Login Fails
**Trigger:** OAuth provider error
**User Sees:** "Couldn't connect. Try email signup or try again."
**Recovery Path:** Email signup form shown as fallback
**Test:** `social-login-failure.spec.ts`

## Metrics to Track
- Signup → First Value: Target < 5 min
- Drop-off at each step
- Social vs email signup ratio
- Skip rate on onboarding
```

---

### Checkout Purchase

```markdown
# Journey: Checkout Purchase

## Overview
| Attribute | Value |
|-----------|-------|
| **Priority** | Critical (Revenue) |
| **User Type** | Any |
| **Frequency** | Variable |
| **Success Metric** | Checkout completion rate |

## User Goal
> "I want to pay quickly and securely without surprises."

## Journey Steps

### Step 1: Cart Review
**User Action:** Views cart before checkout
**System Response:**
- Shows all items with images, prices
- Shows subtotal, taxes, shipping
- Clear "Checkout" CTA

**Success Criteria:**
- [ ] No hidden fees revealed later
- [ ] Easy to modify quantities
- [ ] Saved items visible

### Step 2: Checkout Start
**User Action:** Clicks "Checkout"
**System Response:**
- Shows checkout form or redirect to payment
- Progress indicator (Step 1 of 3)
- Order summary sidebar

**Success Criteria:**
- [ ] Guest checkout option
- [ ] Express checkout (Apple/Google Pay) prominent
- [ ] Form fields pre-filled if logged in

### Step 3: Payment
**User Action:** Enters payment info
**System Response:**
- Secure input fields (Stripe/payment provider)
- Real-time validation
- Clear "Pay $XX" button

**Success Criteria:**
- [ ] Card validation inline, not after submit
- [ ] Multiple payment options
- [ ] Security indicators visible

### Step 4: Confirmation
**User Action:** Submits payment
**System Response:**
- Processing indicator
- Success page with order details
- Email confirmation sent

**Success Criteria:**
- [ ] Confirmation within 5 seconds
- [ ] Order number clearly visible
- [ ] Next steps clear (shipping, access, etc.)

## Error Scenarios

### E1: Payment Declined
**Trigger:** Card declined by processor
**User Sees:** "Payment declined. Please try another card."
**Recovery Path:**
- Stay on payment step
- Pre-fill other fields
- Offer alternative payment methods
**Test:** `payment-declined-recovery.spec.ts`

### E2: Session Timeout During Checkout
**Trigger:** User away too long
**User Sees:** Cart preserved, re-auth required
**Recovery Path:**
- Quick login
- Return to same checkout step
- Cart contents intact
**Test:** `checkout-session-timeout.spec.ts`
```

---

## Journey Testing with Playwright

### Journey Test Structure

```typescript
// e2e/tests/journeys/signup-to-value.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Journey: Signup to First Value', () => {
  test.describe.configure({ mode: 'serial' }); // Run in order

  test('Step 1: Landing page has clear CTA', async ({ page }) => {
    await page.goto('/');

    // CTA visible above fold without scrolling
    const cta = page.getByRole('button', { name: /get started|try free/i });
    await expect(cta).toBeVisible();
    await expect(cta).toBeInViewport();
  });

  test('Step 2: Can create account quickly', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: /get started/i }).click();

    // Minimal fields
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();

    // Complete signup
    const startTime = Date.now();
    await page.getByLabel('Email').fill('newuser@example.com');
    await page.getByLabel('Password').fill('SecurePass123!');
    await page.getByRole('button', { name: /sign up|create/i }).click();

    // Should reach onboarding quickly
    await expect(page).toHaveURL(/onboarding|welcome|setup/);
    expect(Date.now() - startTime).toBeLessThan(5000); // < 5 seconds
  });

  test('Step 3: Onboarding is skippable', async ({ page }) => {
    // ... login as new user ...
    await page.goto('/onboarding');

    // Skip option exists
    const skipButton = page.getByRole('button', { name: /skip/i });
    await expect(skipButton).toBeVisible();
  });

  test('Step 4: Can reach first value in < 5 min', async ({ page }) => {
    // Full journey timing
    const journeyStart = Date.now();

    // ... complete full journey ...

    // Verify first value delivered
    await expect(page.getByText(/success|created|done/i)).toBeVisible();

    // Total time check
    const totalTime = (Date.now() - journeyStart) / 1000 / 60; // minutes
    expect(totalTime).toBeLessThan(5);
  });
});
```

### Error Recovery Tests

```typescript
// e2e/tests/journeys/checkout-recovery.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Journey: Checkout Error Recovery', () => {
  test('recovers from payment decline gracefully', async ({ page }) => {
    // Setup: Add item to cart, go to checkout
    await page.goto('/products');
    await page.getByTestId('add-to-cart').first().click();
    await page.getByRole('link', { name: 'Checkout' }).click();

    // Use Stripe test card that declines
    const stripeFrame = page.frameLocator('iframe[name*="stripe"]');
    await stripeFrame.getByPlaceholder('Card number').fill('4000000000000002');
    await stripeFrame.getByPlaceholder('MM / YY').fill('12/30');
    await stripeFrame.getByPlaceholder('CVC').fill('123');

    await page.getByRole('button', { name: /pay/i }).click();

    // Verify friendly error
    await expect(page.getByText(/declined|try another/i)).toBeVisible();

    // Verify still on checkout (not kicked out)
    await expect(page).toHaveURL(/checkout/);

    // Verify can try again with different card
    await stripeFrame.getByPlaceholder('Card number').fill('4242424242424242');
    await page.getByRole('button', { name: /pay/i }).click();

    // Should succeed now
    await expect(page).toHaveURL(/success|confirmation/);
  });

  test('preserves cart after session timeout', async ({ page, context }) => {
    // Add items to cart
    await page.goto('/products');
    await page.getByTestId('add-to-cart').first().click();

    // Clear session (simulate timeout)
    await context.clearCookies();

    // Return to site
    await page.goto('/cart');

    // Cart should be preserved (local storage or recovered)
    await expect(page.getByTestId('cart-item')).toHaveCount(1);
  });
});
```

---

## User Experience Validation

### UX Checklist per Journey Step

```markdown
## UX Validation Checklist

### Clarity
- [ ] User knows where they are (breadcrumbs, progress)
- [ ] User knows what to do next (clear CTA)
- [ ] User knows what just happened (feedback)

### Speed
- [ ] Page loads < 2 seconds
- [ ] Actions complete < 3 seconds
- [ ] Progress shown for longer operations

### Forgiveness
- [ ] Mistakes are easy to undo
- [ ] Errors explain what went wrong
- [ ] Recovery path is clear

### Accessibility
- [ ] Keyboard navigation works
- [ ] Screen reader announces changes
- [ ] Focus management correct
- [ ] Color contrast sufficient

### Mobile
- [ ] Touch targets >= 44px
- [ ] No horizontal scroll
- [ ] Forms don't zoom unexpectedly
- [ ] Works on slow 3G
```

### Automated UX Checks

```typescript
// e2e/utils/ux-validators.ts
import { Page, expect } from '@playwright/test';

export async function validatePageLoad(page: Page, maxMs = 2000) {
  const timing = await page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    return nav.loadEventEnd - nav.startTime;
  });
  expect(timing).toBeLessThan(maxMs);
}

export async function validateCTAVisible(page: Page, ctaText: RegExp) {
  const cta = page.getByRole('button', { name: ctaText });
  await expect(cta).toBeVisible();
  await expect(cta).toBeInViewport();
}

export async function validateNoLayoutShift(page: Page) {
  const cls = await page.evaluate(() => {
    return new Promise<number>((resolve) => {
      let clsValue = 0;
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            clsValue += (entry as any).value;
          }
        }
      });
      observer.observe({ type: 'layout-shift', buffered: true });
      setTimeout(() => {
        observer.disconnect();
        resolve(clsValue);
      }, 1000);
    });
  });
  expect(cls).toBeLessThan(0.1); // Good CLS score
}

export async function validateAccessibility(page: Page) {
  // Check focus visible on interactive elements
  const buttons = page.getByRole('button');
  const count = await buttons.count();

  for (let i = 0; i < Math.min(count, 5); i++) {
    await buttons.nth(i).focus();
    await expect(buttons.nth(i)).toBeFocused();
  }
}
```

---

## Journey Metrics Dashboard

Track journey health with these metrics:

```typescript
// lib/journey-metrics.ts
interface JourneyMetric {
  journey: string;
  step: string;
  timestamp: Date;
  duration: number;
  success: boolean;
  userId?: string;
}

// Track in your analytics (PostHog, Mixpanel, etc.)
export function trackJourneyStep(metric: JourneyMetric) {
  analytics.track('journey_step', {
    journey_name: metric.journey,
    step_name: metric.step,
    duration_ms: metric.duration,
    success: metric.success,
  });
}

// Example usage in app
const journeyStart = Date.now();
// ... user completes step ...
trackJourneyStep({
  journey: 'signup_to_value',
  step: 'account_creation',
  timestamp: new Date(),
  duration: Date.now() - journeyStart,
  success: true,
});
```

---

## Common Journey Patterns

### Progressive Disclosure Journey
User sees simple view first, complexity revealed as needed.

```markdown
Step 1: Show basic options only
Step 2: "Advanced" expands more options
Step 3: Expert mode unlocks everything
```

### Guided Setup Journey
Hand-hold new users through initial configuration.

```markdown
Step 1: Welcome + single choice
Step 2: Core preference
Step 3: Optional integrations (skippable)
Step 4: First action with guidance
Step 5: Success + remove training wheels
```

### Recovery Journey
User returns after failure or abandonment.

```markdown
Step 1: Recognize returning user
Step 2: Restore previous state
Step 3: Acknowledge what happened
Step 4: Offer clear path forward
Step 5: Complete original goal
```

---

## Anti-Patterns

- **Happy path only** - Test error recovery, not just success
- **Spec-driven testing** - Test user goals, not features
- **Ignoring time** - Measure how long journeys take
- **Desktop-only** - Test mobile journeys separately
- **Skipping emotions** - Consider user frustration points
- **No metrics** - Track journey completion and drop-off
- **Static journeys** - Update as user behavior evolves

---

## Quick Reference

### Journey Priorities
| Priority | Criteria | Test Frequency |
|----------|----------|----------------|
| Critical | Revenue, core value | Every deploy |
| High | Daily user actions | Daily |
| Medium | Weekly features | Weekly |
| Low | Edge cases | On change |

### Package.json Scripts

```json
{
  "scripts": {
    "test:journeys": "playwright test e2e/tests/journeys/",
    "test:journeys:critical": "playwright test e2e/tests/journeys/critical/",
    "test:journeys:report": "playwright show-report"
  }
}
```

### Journey Documentation Checklist
- [ ] User goal clearly stated
- [ ] All steps documented
- [ ] Success criteria per step
- [ ] Error scenarios covered
- [ ] Recovery paths defined
- [ ] Metrics identified
- [ ] E2E test linked
