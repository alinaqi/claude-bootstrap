---
name: web-payments
description: Stripe Checkout, subscriptions, webhooks, customer portal
---

# Web Payments Skill (Stripe)

*Load with: base.md + [framework].md*

For integrating Stripe payments into web applications - one-time payments, subscriptions, and checkout flows.

**Sources:** [Stripe Checkout](https://docs.stripe.com/payments/checkout) | [Payment Element Best Practices](https://docs.stripe.com/payments/payment-element/best-practices) | [Building Solid Stripe Integrations](https://stripe.dev/blog/building-solid-stripe-integrations-developers-guide-success) | [Subscriptions](https://docs.stripe.com/billing/subscriptions/build-subscriptions)

---

## Setup

### 1. Create Stripe Account
1. Go to https://dashboard.stripe.com/register
2. Complete business verification
3. Get API keys from https://dashboard.stripe.com/apikeys

### 2. Environment Variables
```bash
# .env
STRIPE_SECRET_KEY=sk_test_xxx          # Server-side only
STRIPE_PUBLISHABLE_KEY=pk_test_xxx     # Client-side safe
STRIPE_WEBHOOK_SECRET=whsec_xxx        # For webhook verification

# Production
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

### 3. Install SDK
```bash
# Node.js
npm install stripe @stripe/stripe-js

# Python
pip install stripe
```

---

## Integration Options

| Method | Best For | Complexity |
|--------|----------|------------|
| **Checkout (Hosted)** | Quick setup, Stripe-hosted page | Low |
| **Checkout (Embedded)** | Custom site, embedded form | Low |
| **Payment Element** | Full customization, complex flows | Medium |
| **Custom Form** | Complete control (rare) | High |

**Recommendation**: Start with Checkout, migrate to Payment Element if needed.

---

## Stripe Checkout (Recommended)

### Server: Create Checkout Session

#### Node.js / Next.js
```typescript
// app/api/checkout/route.ts (Next.js App Router)
import Stripe from "stripe";
import { NextResponse } from "next/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(request: Request) {
  const { priceId, mode = "payment" } = await request.json();

  try {
    const session = await stripe.checkout.sessions.create({
      mode: mode as "payment" | "subscription",
      payment_method_types: ["card"],
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_URL}/canceled`,
      // Optional: Link to existing customer
      // customer: customerId,
      // Optional: Collect shipping
      // shipping_address_collection: { allowed_countries: ["US", "CA"] },
      // Optional: Add metadata for tracking
      metadata: {
        userId: "user_123",
        source: "pricing_page",
      },
    });

    return NextResponse.json({ sessionId: session.id, url: session.url });
  } catch (error) {
    console.error("Stripe error:", error);
    return NextResponse.json({ error: "Failed to create session" }, { status: 500 });
  }
}
```

#### Python / FastAPI
```python
# app/api/checkout.py
import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
router = APIRouter()

class CheckoutRequest(BaseModel):
    price_id: str
    mode: str = "payment"  # or "subscription"

@router.post("/api/checkout")
async def create_checkout_session(request: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            mode=request.mode,
            payment_method_types=["card"],
            line_items=[{
                "price": request.price_id,
                "quantity": 1,
            }],
            success_url=f"{os.environ['APP_URL']}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.environ['APP_URL']}/canceled",
            metadata={
                "user_id": "user_123",
            },
        )
        return {"session_id": session.id, "url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Client: Redirect to Checkout

```typescript
// components/CheckoutButton.tsx
"use client";

import { loadStripe } from "@stripe/stripe-js";

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export function CheckoutButton({ priceId }: { priceId: string }) {
  const handleCheckout = async () => {
    const response = await fetch("/api/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ priceId }),
    });

    const { url } = await response.json();

    // Redirect to Stripe Checkout
    window.location.href = url;
  };

  return (
    <button onClick={handleCheckout}>
      Subscribe Now
    </button>
  );
}
```

---

## Embedded Checkout

For keeping users on your site:

```typescript
// components/EmbeddedCheckout.tsx
"use client";

import { useEffect, useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import {
  EmbeddedCheckoutProvider,
  EmbeddedCheckout,
} from "@stripe/react-stripe-js";

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

export function EmbeddedCheckoutForm({ priceId }: { priceId: string }) {
  const [clientSecret, setClientSecret] = useState("");

  useEffect(() => {
    fetch("/api/checkout/embedded", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ priceId }),
    })
      .then((res) => res.json())
      .then((data) => setClientSecret(data.clientSecret));
  }, [priceId]);

  if (!clientSecret) return <div>Loading...</div>;

  return (
    <EmbeddedCheckoutProvider stripe={stripePromise} options={{ clientSecret }}>
      <EmbeddedCheckout />
    </EmbeddedCheckoutProvider>
  );
}
```

Server endpoint for embedded:
```typescript
// app/api/checkout/embedded/route.ts
export async function POST(request: Request) {
  const { priceId } = await request.json();

  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: priceId, quantity: 1 }],
    ui_mode: "embedded",
    return_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
  });

  return NextResponse.json({ clientSecret: session.client_secret });
}
```

---

## Webhooks (Critical)

**Never trust client-side data**. Always verify payments via webhooks.

### Webhook Endpoint

```typescript
// app/api/webhooks/stripe/route.ts
import Stripe from "stripe";
import { headers } from "next/headers";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

export async function POST(request: Request) {
  const body = await request.text();
  const signature = headers().get("stripe-signature")!;

  let event: Stripe.Event;

  // Verify webhook signature
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    console.error("Webhook signature verification failed");
    return new Response("Invalid signature", { status: 400 });
  }

  // Handle events
  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object as Stripe.Checkout.Session;
      await handleCheckoutComplete(session);
      break;
    }
    case "customer.subscription.created":
    case "customer.subscription.updated": {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionUpdate(subscription);
      break;
    }
    case "customer.subscription.deleted": {
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionCanceled(subscription);
      break;
    }
    case "invoice.payment_failed": {
      const invoice = event.data.object as Stripe.Invoice;
      await handlePaymentFailed(invoice);
      break;
    }
    default:
      console.log(`Unhandled event type: ${event.type}`);
  }

  // Return 200 quickly - process async if needed
  return new Response("OK", { status: 200 });
}

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId;
  const customerId = session.customer as string;
  const subscriptionId = session.subscription as string;

  // Update your database
  await db.user.update({
    where: { id: userId },
    data: {
      stripeCustomerId: customerId,
      stripeSubscriptionId: subscriptionId,
      subscriptionStatus: "active",
    },
  });
}
```

### Python Webhook
```python
# app/api/webhooks.py
import stripe
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ["STRIPE_WEBHOOK_SECRET"]
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_checkout_complete(session)
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        await handle_subscription_canceled(subscription)

    return {"status": "success"}
```

### Key Webhook Events

| Event | When | Action |
|-------|------|--------|
| `checkout.session.completed` | Payment successful | Provision access |
| `customer.subscription.created` | New subscription | Store subscription ID |
| `customer.subscription.updated` | Plan change | Update plan in DB |
| `customer.subscription.deleted` | Canceled | Revoke access |
| `invoice.payment_failed` | Payment failed | Notify user, retry |
| `invoice.paid` | Renewal successful | Extend access |

---

## Products & Prices

### Create via Dashboard (Recommended)
1. Go to https://dashboard.stripe.com/products
2. Create product with name, description
3. Add price(s) - one-time or recurring
4. Copy Price ID (`price_xxx`)

### Create via API
```typescript
// One-time product
const product = await stripe.products.create({
  name: "Pro Plan",
  description: "Full access to all features",
});

const price = await stripe.prices.create({
  product: product.id,
  unit_amount: 2999, // $29.99 in cents
  currency: "usd",
});

// Subscription product
const subscriptionPrice = await stripe.prices.create({
  product: product.id,
  unit_amount: 999, // $9.99/month
  currency: "usd",
  recurring: {
    interval: "month",
  },
});
```

---

## Customer Portal

Let users manage their subscriptions:

```typescript
// app/api/portal/route.ts
export async function POST(request: Request) {
  const { customerId } = await request.json();

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${process.env.NEXT_PUBLIC_URL}/settings`,
  });

  return NextResponse.json({ url: session.url });
}
```

Configure portal at: https://dashboard.stripe.com/settings/billing/portal

---

## Subscriptions

### Create Subscription with Trial
```typescript
const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  line_items: [{ price: priceId, quantity: 1 }],
  subscription_data: {
    trial_period_days: 14,
    // Cancel if no payment method after trial
    trial_settings: {
      end_behavior: { missing_payment_method: "cancel" },
    },
  },
  success_url: successUrl,
  cancel_url: cancelUrl,
});
```

### Check Subscription Status
```typescript
// lib/subscription.ts
export async function getSubscriptionStatus(customerId: string) {
  const subscriptions = await stripe.subscriptions.list({
    customer: customerId,
    status: "all",
    limit: 1,
  });

  if (subscriptions.data.length === 0) {
    return { status: "none", plan: null };
  }

  const subscription = subscriptions.data[0];
  return {
    status: subscription.status,
    plan: subscription.items.data[0].price.id,
    currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    cancelAtPeriodEnd: subscription.cancel_at_period_end,
  };
}
```

---

## Testing

### Test Cards
| Card Number | Scenario |
|-------------|----------|
| `4242424242424242` | Success |
| `4000000000000002` | Declined |
| `4000002500003155` | Requires 3D Secure |
| `4000000000009995` | Insufficient funds |

### Stripe CLI for Webhooks
```bash
# Install CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.deleted
```

---

## Project Structure

```
project/
├── app/
│   ├── api/
│   │   ├── checkout/
│   │   │   └── route.ts          # Create checkout session
│   │   ├── portal/
│   │   │   └── route.ts          # Customer portal
│   │   └── webhooks/
│   │       └── stripe/
│   │           └── route.ts      # Webhook handler
│   ├── pricing/
│   │   └── page.tsx              # Pricing page
│   ├── success/
│   │   └── page.tsx              # Post-checkout success
│   └── settings/
│       └── page.tsx              # Manage subscription
├── lib/
│   ├── stripe.ts                 # Stripe client
│   └── subscription.ts           # Subscription helpers
└── .env.local
```

---

## Security Best Practices

### Non-Negotiable Rules
1. **Server-side only for secrets** - Never expose `STRIPE_SECRET_KEY`
2. **Always verify webhooks** - Check signature before processing
3. **Idempotency** - Store webhook event IDs, skip duplicates
4. **Use metadata** - Track user IDs, sources for debugging
5. **Handle all states** - Success, failure, pending, canceled

### Idempotent Webhook Handler
```typescript
const processedEvents = new Set<string>(); // Use Redis in production

export async function POST(request: Request) {
  // ... verify signature ...

  // Skip duplicate events
  if (processedEvents.has(event.id)) {
    return new Response("Already processed", { status: 200 });
  }
  processedEvents.add(event.id);

  // Process event...
}
```

### Amount Handling
```typescript
// Always use cents (smallest currency unit)
const priceInCents = 2999; // $29.99

// Helper functions
const toCents = (dollars: number) => Math.round(dollars * 100);
const toDollars = (cents: number) => cents / 100;

// Display
const displayPrice = (cents: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(toDollars(cents));
```

---

## Common Patterns

### Pricing Page
```typescript
// app/pricing/page.tsx
const plans = [
  {
    name: "Starter",
    price: "$9/mo",
    priceId: "price_starter_monthly",
    features: ["Feature 1", "Feature 2"],
  },
  {
    name: "Pro",
    price: "$29/mo",
    priceId: "price_pro_monthly",
    features: ["Everything in Starter", "Feature 3", "Feature 4"],
    popular: true,
  },
];

export default function PricingPage() {
  return (
    <div className="grid md:grid-cols-2 gap-8">
      {plans.map((plan) => (
        <div key={plan.name} className={plan.popular ? "border-blue-500" : ""}>
          <h3>{plan.name}</h3>
          <p>{plan.price}</p>
          <ul>
            {plan.features.map((f) => <li key={f}>{f}</li>)}
          </ul>
          <CheckoutButton priceId={plan.priceId} />
        </div>
      ))}
    </div>
  );
}
```

### Protect Routes by Subscription
```typescript
// middleware.ts
import { getSubscriptionStatus } from "@/lib/subscription";

export async function middleware(request: NextRequest) {
  const session = await getSession();

  if (request.nextUrl.pathname.startsWith("/pro")) {
    const { status } = await getSubscriptionStatus(session.stripeCustomerId);

    if (status !== "active" && status !== "trialing") {
      return NextResponse.redirect(new URL("/pricing", request.url));
    }
  }
}
```

---

## Anti-Patterns

- **Hardcoding API keys** - Use environment variables
- **Client-side payment creation** - Always create PaymentIntent/Session server-side
- **Skipping webhook verification** - Always verify signatures
- **Processing duplicate webhooks** - Implement idempotency
- **Floating-point currency math** - Use integers (cents)
- **Trusting client data** - Verify everything server-side
- **Ignoring failed payments** - Handle `invoice.payment_failed`
- **No error handling** - Catch and handle Stripe errors

---

## Quick Reference

```bash
# Install
npm install stripe @stripe/stripe-js @stripe/react-stripe-js

# Stripe CLI
stripe login
stripe listen --forward-to localhost:3000/api/webhooks/stripe
stripe trigger checkout.session.completed

# Test mode prefix
sk_test_xxx  # Secret key
pk_test_xxx  # Publishable key

# Live mode prefix
sk_live_xxx
pk_live_xxx
```

### Key Endpoints
| Endpoint | Purpose |
|----------|---------|
| `POST /api/checkout` | Create checkout session |
| `POST /api/portal` | Customer billing portal |
| `POST /api/webhooks/stripe` | Handle Stripe events |

### Environment Variables
```bash
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
```
