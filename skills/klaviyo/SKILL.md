---
name: klaviyo
description: Klaviyo email/SMS marketing - profiles, events, flows, segmentation
---

# Klaviyo E-Commerce Marketing Skill

*Load with: base.md + (typescript.md or python.md)*

For integrating Klaviyo email/SMS marketing - customer profiles, event tracking, campaigns, flows, and segmentation.

**Sources:** [Klaviyo API Docs](https://developers.klaviyo.com/en/docs) | [API Reference](https://developers.klaviyo.com/en/reference/api-overview)

---

## Why Klaviyo

| Feature | Benefit |
|---------|---------|
| **E-commerce Native** | Built for online stores, deep integrations |
| **Event-Based** | Trigger flows from any customer action |
| **Segmentation** | Advanced filtering on behavior + properties |
| **Email + SMS** | Unified platform for both channels |
| **Analytics** | Revenue attribution per campaign |

---

## API Basics

### Base URLs

| Type | URL |
|------|-----|
| Server-side (Private) | `https://a.klaviyo.com/api` |
| Client-side (Public) | `https://a.klaviyo.com/client` |

### Authentication

```typescript
// Server-side: Private API Key
const headers = {
  "Authorization": "Klaviyo-API-Key pk_xxxxxxxxxxxxxxxxxxxxxxxx",
  "Content-Type": "application/json",
  "revision": "2024-10-15",  // API version
};

// Client-side: Public API Key (6 characters)
const publicKey = "XXXXXX";  // Company ID
// Use as query param: ?company_id=XXXXXX
```

### API Key Scopes

| Scope | Access |
|-------|--------|
| Read-only | View data only |
| Full | Read + write (default) |
| Custom | Specific permissions |

---

## Installation

### Node.js

```bash
npm install klaviyo-api
```

```typescript
// lib/klaviyo.ts
import { ApiClient, EventsApi, ProfilesApi, ListsApi } from "klaviyo-api";

const client = new ApiClient();
client.setApiKey(process.env.KLAVIYO_PRIVATE_KEY!);

export const eventsApi = new EventsApi(client);
export const profilesApi = new ProfilesApi(client);
export const listsApi = new ListsApi(client);
```

### Python

```bash
pip install klaviyo-api
```

```python
# lib/klaviyo.py
from klaviyo_api import KlaviyoAPI

klaviyo = KlaviyoAPI(
    api_key=os.environ["KLAVIYO_PRIVATE_KEY"],
    max_delay=60,
    max_retries=3
)
```

### Direct HTTP (Any Language)

```typescript
// lib/klaviyo.ts
const KLAVIYO_BASE_URL = "https://a.klaviyo.com/api";

async function klaviyoRequest(
  endpoint: string,
  method: "GET" | "POST" | "PATCH" | "DELETE" = "GET",
  body?: object
) {
  const response = await fetch(`${KLAVIYO_BASE_URL}${endpoint}`, {
    method,
    headers: {
      Authorization: `Klaviyo-API-Key ${process.env.KLAVIYO_PRIVATE_KEY}`,
      "Content-Type": "application/json",
      revision: "2024-10-15",
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`Klaviyo API error: ${JSON.stringify(error)}`);
  }

  return response.json();
}
```

---

## Profiles (Customers)

### Create/Update Profile

```typescript
// Upsert profile (create or update)
async function upsertProfile(data: ProfileInput) {
  return klaviyoRequest("/profiles", "POST", {
    data: {
      type: "profile",
      attributes: {
        email: data.email,
        phone_number: data.phone, // E.164 format: +1234567890
        first_name: data.firstName,
        last_name: data.lastName,
        properties: {
          // Custom properties
          lifetime_value: data.ltv,
          plan: data.plan,
          signup_source: data.source,
        },
        location: {
          city: data.city,
          region: data.state,
          country: data.country,
          zip: data.zip,
        },
      },
    },
  });
}
```

```python
# Python
def upsert_profile(data):
    return klaviyo.Profiles.create_or_update_profile({
        "data": {
            "type": "profile",
            "attributes": {
                "email": data["email"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "properties": {
                    "plan": data.get("plan"),
                }
            }
        }
    })
```

### Get Profile

```typescript
async function getProfileByEmail(email: string) {
  const response = await klaviyoRequest(
    `/profiles?filter=equals(email,"${email}")`
  );
  return response.data[0];
}

async function getProfileById(profileId: string) {
  return klaviyoRequest(`/profiles/${profileId}`);
}
```

### Update Profile Properties

```typescript
async function updateProfileProperties(
  profileId: string,
  properties: Record<string, any>
) {
  return klaviyoRequest(`/profiles/${profileId}`, "PATCH", {
    data: {
      type: "profile",
      id: profileId,
      attributes: {
        properties,
      },
    },
  });
}

// Usage
await updateProfileProperties("profile_id", {
  last_purchase_date: new Date().toISOString(),
  total_orders: 5,
  vip_status: true,
});
```

---

## Events (Tracking)

### Track Event (Server-Side)

```typescript
async function trackEvent(data: EventInput) {
  return klaviyoRequest("/events", "POST", {
    data: {
      type: "event",
      attributes: {
        profile: {
          data: {
            type: "profile",
            attributes: {
              email: data.email,
              // or phone_number, or external_id
            },
          },
        },
        metric: {
          data: {
            type: "metric",
            attributes: {
              name: data.eventName,
            },
          },
        },
        properties: data.properties,
        value: data.value, // For revenue tracking
        unique_id: data.uniqueId, // Deduplication
        time: data.timestamp || new Date().toISOString(),
      },
    },
  });
}
```

### Common E-Commerce Events

```typescript
// Viewed Product
await trackEvent({
  email: customer.email,
  eventName: "Viewed Product",
  properties: {
    ProductID: product.id,
    ProductName: product.name,
    ProductURL: product.url,
    ImageURL: product.image,
    Price: product.price,
    Categories: product.categories,
  },
});

// Added to Cart
await trackEvent({
  email: customer.email,
  eventName: "Added to Cart",
  properties: {
    ProductID: product.id,
    ProductName: product.name,
    Quantity: quantity,
    Price: product.price,
    CartTotal: cart.total,
    ItemNames: cart.items.map(i => i.name),
  },
  value: product.price * quantity,
});

// Started Checkout
await trackEvent({
  email: customer.email,
  eventName: "Started Checkout",
  properties: {
    CheckoutURL: checkout.url,
    ItemCount: cart.itemCount,
    Categories: cart.categories,
    ItemNames: cart.items.map(i => i.name),
  },
  value: cart.total,
});

// Placed Order
await trackEvent({
  email: customer.email,
  eventName: "Placed Order",
  properties: {
    OrderId: order.id,
    ItemCount: order.itemCount,
    Categories: order.categories,
    ItemNames: order.items.map(i => i.name),
    Items: order.items.map(i => ({
      ProductID: i.productId,
      ProductName: i.name,
      Quantity: i.quantity,
      Price: i.price,
      ImageURL: i.image,
      ProductURL: i.url,
    })),
    BillingAddress: order.billingAddress,
    ShippingAddress: order.shippingAddress,
  },
  value: order.total,
  uniqueId: order.id, // Prevent duplicate orders
});

// Fulfilled Order
await trackEvent({
  email: customer.email,
  eventName: "Fulfilled Order",
  properties: {
    OrderId: order.id,
    TrackingNumber: fulfillment.trackingNumber,
    TrackingURL: fulfillment.trackingUrl,
    Carrier: fulfillment.carrier,
  },
});

// Cancelled Order
await trackEvent({
  email: customer.email,
  eventName: "Cancelled Order",
  properties: {
    OrderId: order.id,
    Reason: cancellation.reason,
  },
  value: -order.total, // Negative value for refunds
});
```

### Client-Side Tracking (JavaScript)

```html
<!-- Add to your site -->
<script async src="https://static.klaviyo.com/onsite/js/klaviyo.js?company_id=XXXXXX"></script>

<script>
  // Identify user
  klaviyo.identify({
    email: "customer@example.com",
    first_name: "John",
    last_name: "Doe",
  });

  // Track event
  klaviyo.track("Viewed Product", {
    ProductID: "prod_123",
    ProductName: "Blue T-Shirt",
    Price: 29.99,
  });

  // Track with value
  klaviyo.track("Added to Cart", {
    ProductID: "prod_123",
    ProductName: "Blue T-Shirt",
    Price: 29.99,
    $value: 29.99,  // Revenue tracking
  });
</script>
```

---

## Lists & Segments

### Add Profile to List

```typescript
async function addToList(listId: string, emails: string[]) {
  return klaviyoRequest(`/lists/${listId}/relationships/profiles`, "POST", {
    data: emails.map(email => ({
      type: "profile",
      attributes: { email },
    })),
  });
}

// By profile ID
async function addProfileToList(listId: string, profileId: string) {
  return klaviyoRequest(`/lists/${listId}/relationships/profiles`, "POST", {
    data: [{ type: "profile", id: profileId }],
  });
}
```

### Remove from List

```typescript
async function removeFromList(listId: string, profileId: string) {
  return klaviyoRequest(
    `/lists/${listId}/relationships/profiles`,
    "DELETE",
    {
      data: [{ type: "profile", id: profileId }],
    }
  );
}
```

### Get List Members

```typescript
async function getListMembers(listId: string, cursor?: string) {
  const params = new URLSearchParams({
    "page[size]": "100",
  });
  if (cursor) {
    params.set("page[cursor]", cursor);
  }

  return klaviyoRequest(`/lists/${listId}/profiles?${params}`);
}
```

### Create List

```typescript
async function createList(name: string) {
  return klaviyoRequest("/lists", "POST", {
    data: {
      type: "list",
      attributes: { name },
    },
  });
}
```

---

## Campaigns

### Get Campaigns

```typescript
async function getCampaigns(status?: "draft" | "scheduled" | "sent") {
  const params = new URLSearchParams();
  if (status) {
    params.set("filter", `equals(status,"${status}")`);
  }

  return klaviyoRequest(`/campaigns?${params}`);
}
```

### Get Campaign Performance

```typescript
async function getCampaignMetrics(campaignId: string) {
  return klaviyoRequest(
    `/campaign-recipient-estimations/${campaignId}`,
    "GET"
  );
}
```

---

## Flows (Automations)

### Get Flows

```typescript
async function getFlows() {
  return klaviyoRequest("/flows");
}

async function getFlowById(flowId: string) {
  return klaviyoRequest(`/flows/${flowId}`);
}
```

### Common Flow Triggers

| Flow Type | Trigger Event |
|-----------|---------------|
| Welcome Series | Added to List |
| Abandoned Cart | Added to Cart + No Purchase |
| Browse Abandon | Viewed Product + No Cart |
| Post-Purchase | Placed Order |
| Winback | No Order in X Days |
| Review Request | Fulfilled Order |

---

## Webhooks

### Create Webhook

```typescript
async function createWebhook(data: WebhookInput) {
  return klaviyoRequest("/webhooks", "POST", {
    data: {
      type: "webhook",
      attributes: {
        name: data.name,
        endpoint_url: data.url,
        secret_key: data.secret,
        topics: data.topics, // e.g., ["profile.created", "event.created"]
      },
    },
  });
}
```

### Webhook Topics

| Topic | Trigger |
|-------|---------|
| `profile.created` | New profile created |
| `profile.updated` | Profile properties changed |
| `profile.merged` | Profiles merged |
| `event.created` | New event tracked |
| `list.member.added` | Profile added to list |
| `list.member.removed` | Profile removed from list |

### Verify Webhook Signature

```typescript
import crypto from "crypto";

function verifyKlaviyoWebhook(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expectedSignature = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("base64");

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

// Express handler
app.post("/webhooks/klaviyo", (req, res) => {
  const signature = req.headers["klaviyo-webhook-signature"] as string;

  if (!verifyKlaviyoWebhook(JSON.stringify(req.body), signature, WEBHOOK_SECRET)) {
    return res.status(401).json({ error: "Invalid signature" });
  }

  const { type, data } = req.body;

  switch (type) {
    case "profile.created":
      handleNewProfile(data);
      break;
    case "event.created":
      handleNewEvent(data);
      break;
  }

  res.status(200).json({ received: true });
});
```

---

## Rate Limits

| Window | Limit |
|--------|-------|
| Burst | 75 requests/second |
| Steady | 700 requests/minute |

### Handle Rate Limiting

```typescript
async function klaviyoRequestWithRetry(
  endpoint: string,
  method: "GET" | "POST" | "PATCH" | "DELETE" = "GET",
  body?: object,
  retries = 3
): Promise<any> {
  for (let attempt = 0; attempt < retries; attempt++) {
    const response = await fetch(`${KLAVIYO_BASE_URL}${endpoint}`, {
      method,
      headers: {
        Authorization: `Klaviyo-API-Key ${process.env.KLAVIYO_PRIVATE_KEY}`,
        "Content-Type": "application/json",
        revision: "2024-10-15",
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (response.status === 429) {
      const retryAfter = parseInt(response.headers.get("Retry-After") || "5");
      await new Promise(r => setTimeout(r, retryAfter * 1000));
      continue;
    }

    if (!response.ok) {
      throw new Error(`Klaviyo error: ${response.status}`);
    }

    return response.json();
  }

  throw new Error("Max retries exceeded");
}
```

---

## Pagination

```typescript
async function getAllProfiles() {
  const profiles = [];
  let cursor: string | undefined;

  do {
    const params = new URLSearchParams({ "page[size]": "100" });
    if (cursor) {
      params.set("page[cursor]", cursor);
    }

    const response = await klaviyoRequest(`/profiles?${params}`);
    profiles.push(...response.data);

    cursor = response.links?.next
      ? new URL(response.links.next).searchParams.get("page[cursor]")
      : undefined;
  } while (cursor);

  return profiles;
}
```

---

## Filtering & Sorting

```typescript
// Filter by date
const recentEvents = await klaviyoRequest(
  `/events?filter=greater-than(datetime,2024-01-01T00:00:00Z)`
);

// Filter by property
const vipProfiles = await klaviyoRequest(
  `/profiles?filter=equals(properties.vip_status,true)`
);

// Multiple filters (AND)
const filtered = await klaviyoRequest(
  `/profiles?filter=and(equals(properties.plan,"pro"),greater-than(properties.ltv,1000))`
);

// Sorting
const sorted = await klaviyoRequest(
  `/profiles?sort=-created`  // Descending by created date
);

// Sparse fieldsets (only return specific fields)
const sparse = await klaviyoRequest(
  `/profiles?fields[profile]=email,first_name,properties`
);
```

---

## Integration Patterns

### E-Commerce Order Sync

```typescript
// After order is placed
async function syncOrderToKlaviyo(order: Order) {
  // 1. Upsert customer profile
  await upsertProfile({
    email: order.customerEmail,
    firstName: order.customerFirstName,
    lastName: order.customerLastName,
    phone: order.customerPhone,
  });

  // 2. Update lifetime metrics
  await updateProfileProperties(
    await getProfileIdByEmail(order.customerEmail),
    {
      last_order_date: new Date().toISOString(),
      total_orders: order.customerOrderCount,
      lifetime_value: order.customerLifetimeValue,
    }
  );

  // 3. Track order event
  await trackEvent({
    email: order.customerEmail,
    eventName: "Placed Order",
    properties: {
      OrderId: order.id,
      Items: order.items,
      // ... other properties
    },
    value: order.total,
    uniqueId: order.id,
  });
}
```

### Subscription Status Sync

```typescript
// When subscription changes
async function syncSubscriptionStatus(user: User, status: string) {
  await updateProfileProperties(user.klaviyoProfileId, {
    subscription_status: status,
    subscription_plan: user.plan,
    subscription_updated_at: new Date().toISOString(),
  });

  await trackEvent({
    email: user.email,
    eventName: `Subscription ${status}`,
    properties: {
      plan: user.plan,
      mrr: user.mrr,
    },
    value: status === "cancelled" ? -user.mrr : user.mrr,
  });
}
```

---

## Environment Variables

```bash
# .env
KLAVIYO_PRIVATE_KEY=pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
KLAVIYO_PUBLIC_KEY=XXXXXX
KLAVIYO_WEBHOOK_SECRET=your_webhook_secret
```

Add to `credentials.md`:
```python
'KLAVIYO_PRIVATE_KEY': r'pk_[a-f0-9]{32}',
'KLAVIYO_PUBLIC_KEY': r'[A-Z0-9]{6}',
```

---

## Checklist

### Setup

- [ ] Klaviyo account created
- [ ] Private API key generated
- [ ] Public API key noted (company ID)
- [ ] API revision set in headers

### Integration

- [ ] Profile sync on signup/update
- [ ] Key events tracked (view, cart, order)
- [ ] Order events include Items array
- [ ] Revenue tracked with $value
- [ ] Unique IDs for deduplication

### Testing

- [ ] Test profile creation
- [ ] Test event tracking
- [ ] Verify events in Klaviyo dashboard
- [ ] Test webhook delivery
- [ ] Test rate limit handling

---

## Anti-Patterns

- **Missing email/phone** - Every profile needs at least one identifier
- **Duplicate events** - Use unique_id for orders/transactions
- **Missing Items array** - Required for product recommendations
- **Client-side only** - Server-side tracking is more reliable
- **Ignoring rate limits** - Implement exponential backoff
- **Hardcoded API keys** - Use environment variables
- **Missing revenue tracking** - Include $value for ROI attribution
