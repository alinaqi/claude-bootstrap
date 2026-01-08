---
name: shopify-apps
description: Shopify app development - Remix, Admin API, checkout extensions
---

# Shopify App Development Skill

*Load with: base.md + typescript.md + react-web.md*

For building Shopify apps using Remix, the Shopify App framework, and checkout UI extensions.

**Sources:** [Shopify Dev Docs](https://shopify.dev/docs/apps) | [Shopify CLI](https://shopify.dev/docs/apps/tools/cli) | [Admin API](https://shopify.dev/docs/api/admin-graphql)

---

## Prerequisites

### Required Accounts & Tools

```bash
# 1. Shopify Partner Account (free)
# Sign up at: https://partners.shopify.com

# 2. Development Store
# Create in Partner Dashboard → Stores → Add store → Development store

# 3. Shopify CLI
npm install -g @shopify/cli

# 4. Node.js 18.20+ or 20.10+
node --version
```

### Partner Dashboard Setup

1. Create Partner account at partners.shopify.com
2. Create a development store for testing
3. Create an app in Partner Dashboard → Apps → Create app
4. Note your API key and API secret

---

## Quick Start

### Scaffold New App

```bash
# Create new Shopify app with Remix
shopify app init

# Answer prompts:
# - App name
# - Template: Remix (recommended)
# - Language: JavaScript or TypeScript

# Start development
cd your-app-name
shopify app dev
```

### Project Structure

```
shopify-app/
├── app/
│   ├── routes/
│   │   ├── app._index/          # Main app page
│   │   │   └── route.jsx
│   │   ├── app.jsx              # App layout with Polaris
│   │   ├── auth.$.jsx           # Auth catch-all
│   │   ├── auth.login/          # Login page
│   │   │   └── route.jsx
│   │   ├── webhooks.app.uninstalled.jsx
│   │   ├── webhooks.app.scopes_update.jsx
│   │   └── webhooks.gdpr.jsx    # GDPR compliance (REQUIRED)
│   ├── shopify.server.js        # Shopify app config
│   ├── db.server.js             # Prisma client
│   └── entry.server.jsx
├── extensions/                   # Checkout/theme extensions
│   └── my-extension/
│       ├── src/
│       │   └── index.tsx
│       ├── shopify.extension.toml
│       └── package.json
├── prisma/
│   └── schema.prisma            # Session storage
├── shopify.app.toml             # App configuration
├── package.json
└── vite.config.js
```

---

## App Configuration

### shopify.app.toml

```toml
# App configuration - managed by Shopify CLI
client_id = "your-api-key"
name = "Your App Name"
handle = "your-app-handle"
application_url = "https://your-app.onrender.com"
embedded = true

[webhooks]
api_version = "2025-01"

# Required: App lifecycle webhooks
[[webhooks.subscriptions]]
topics = ["app/uninstalled"]
uri = "/webhooks/app/uninstalled"

[[webhooks.subscriptions]]
topics = ["app/scopes_update"]
uri = "/webhooks/app/scopes_update"

# Required: GDPR compliance webhooks
[[webhooks.subscriptions]]
compliance_topics = [
  "customers/data_request",
  "customers/redact",
  "shop/redact",
]
uri = "/webhooks/gdpr"

[access_scopes]
scopes = "read_products,write_products"

[auth]
redirect_urls = [
  "https://your-app.onrender.com/auth/callback",
  "https://your-app.onrender.com/auth/shopify/callback",
]

[pos]
embedded = false

[build]
dev_store_url = "your-dev-store.myshopify.com"
automatically_update_urls_on_dev = true
```

### shopify.server.js

```javascript
import "@shopify/shopify-app-remix/adapters/node";
import {
  ApiVersion,
  AppDistribution,
  shopifyApp,
} from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import { prisma } from "./db.server";

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET || "",
  apiVersion: ApiVersion.January25,
  scopes: process.env.SCOPES?.split(","),
  appUrl: process.env.SHOPIFY_APP_URL || "",
  authPathPrefix: "/auth",
  sessionStorage: new PrismaSessionStorage(prisma),
  distribution: AppDistribution.AppStore,
  future: {
    unstable_newEmbeddedAuthStrategy: true,
    removeRest: true,  // Use GraphQL only
  },
});

export default shopify;
export const apiVersion = ApiVersion.January25;
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
export const authenticate = shopify.authenticate;
export const unauthenticated = shopify.unauthenticated;
export const login = shopify.login;
export const registerWebhooks = shopify.registerWebhooks;
export const sessionStorage = shopify.sessionStorage;
```

---

## Authentication

### Route Protection

```javascript
// app/routes/app._index/route.jsx
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { authenticate } from "../../shopify.server";

export const loader = async ({ request }) => {
  // This authenticates the request and redirects to login if needed
  const { admin, session } = await authenticate.admin(request);

  // Now you have access to admin API and session
  const shop = session.shop;

  return json({ shop });
};

export default function Index() {
  const { shop } = useLoaderData();
  return <div>Connected to: {shop}</div>;
}
```

### Webhook Authentication

```javascript
// app/routes/webhooks.app.uninstalled.jsx
import { authenticate } from "../shopify.server";
import { prisma } from "../db.server";

export const action = async ({ request }) => {
  const { shop, topic } = await authenticate.webhook(request);

  console.log(`Received ${topic} webhook for ${shop}`);

  // Clean up shop data on uninstall
  await prisma.session.deleteMany({ where: { shop } });

  return new Response(null, { status: 200 });
};
```

---

## GraphQL Admin API

### Basic Query Pattern

```javascript
// app/shopify/adminApi.server.js
export async function getShopId(admin) {
  const response = await admin.graphql(`
    query getShopId {
      shop {
        id
        name
        email
        myshopifyDomain
      }
    }
  `);

  const data = await response.json();
  return data.data?.shop;
}
```

### Query with Variables

```javascript
export async function getProducts(admin, first = 10) {
  const response = await admin.graphql(`
    query getProducts($first: Int!) {
      products(first: $first) {
        edges {
          node {
            id
            title
            status
            variants(first: 5) {
              edges {
                node {
                  id
                  price
                  inventoryQuantity
                }
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  `, {
    variables: { first }
  });

  const data = await response.json();
  return data.data?.products?.edges.map(e => e.node);
}
```

### Mutations

```javascript
export async function createProduct(admin, input) {
  const response = await admin.graphql(`
    mutation createProduct($input: ProductInput!) {
      productCreate(input: $input) {
        product {
          id
          title
        }
        userErrors {
          field
          message
        }
      }
    }
  `, {
    variables: {
      input: {
        title: input.title,
        descriptionHtml: input.description,
        status: "DRAFT"
      }
    }
  });

  const data = await response.json();
  const result = data.data?.productCreate;

  if (result?.userErrors?.length > 0) {
    throw new Error(result.userErrors.map(e => e.message).join(", "));
  }

  return result?.product;
}
```

### Metafields (App Settings Storage)

```javascript
// Get metafield
export async function getMetafield(admin, namespace, key) {
  const response = await admin.graphql(`
    query getShopMetafield($namespace: String!, $key: String!) {
      shop {
        id
        metafield(namespace: $namespace, key: $key) {
          id
          value
        }
      }
    }
  `, {
    variables: { namespace, key }
  });

  const data = await response.json();
  const metafield = data.data?.shop?.metafield;

  return {
    shopId: data.data?.shop?.id,
    value: metafield?.value ? JSON.parse(metafield.value) : null,
  };
}

// Set metafield
export async function setMetafield(admin, namespace, key, value, shopId) {
  const response = await admin.graphql(`
    mutation CreateMetafield($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields {
          id
          namespace
          key
          value
        }
        userErrors {
          field
          message
        }
      }
    }
  `, {
    variables: {
      metafields: [{
        namespace,
        key,
        type: "json",
        value: JSON.stringify(value),
        ownerId: shopId,
      }]
    }
  });

  const data = await response.json();
  const errors = data.data?.metafieldsSet?.userErrors;

  if (errors?.length > 0) {
    throw new Error(errors.map(e => e.message).join(", "));
  }

  return data.data?.metafieldsSet?.metafields?.[0];
}
```

---

## GDPR Compliance (REQUIRED)

**All Shopify apps MUST handle GDPR webhooks.** This is required for App Store approval.

```javascript
// app/routes/webhooks.gdpr.jsx
import { authenticate } from "../shopify.server";

export const action = async ({ request }) => {
  const { topic, shop, session } = await authenticate.webhook(request);

  console.log(`Received ${topic} webhook for ${shop}`);

  switch (topic) {
    case "customers/data_request":
      // Return any customer data you store
      // If you don't store customer data, return empty
      return json({ customer_data: null });

    case "customers/redact":
      // Delete customer data
      // Example: await deleteCustomerData(payload.customer.id);
      return json({ success: true });

    case "shop/redact":
      // Delete all shop data (48 hours after uninstall)
      // Clean up metafields, database records, etc.
      if (session) {
        const { admin } = await authenticate.admin(request);
        await admin.graphql(`
          mutation metafieldDelete($input: MetafieldsDeleteInput!) {
            metafieldsDelete(input: $input) {
              deletedId
            }
          }
        `, {
          variables: {
            input: {
              namespace: "your_app",
              key: "settings",
              ownerType: "SHOP"
            }
          }
        });
      }
      return json({ success: true });

    default:
      return json({ error: "Unhandled topic" }, { status: 400 });
  }
};
```

---

## UI with Polaris

### App Layout

```javascript
// app/routes/app.jsx
import { Outlet } from "@remix-run/react";
import { AppProvider } from "@shopify/polaris";
import "@shopify/polaris/build/esm/styles.css";
import polarisTranslations from "@shopify/polaris/locales/en.json";

export default function App() {
  return (
    <AppProvider i18n={polarisTranslations}>
      <Outlet />
    </AppProvider>
  );
}
```

### Settings Page Pattern

```javascript
// app/routes/app._index/route.jsx
import { useState } from "react";
import { json } from "@remix-run/node";
import { useActionData, useLoaderData, useSubmit } from "@remix-run/react";
import {
  Page,
  Layout,
  Card,
  FormLayout,
  TextField,
  Select,
  Banner,
  Button,
} from "@shopify/polaris";
import { authenticate } from "../../shopify.server";
import { getMetafield, setMetafield, getShopId } from "../../shopify/adminApi.server";

export const loader = async ({ request }) => {
  const { admin } = await authenticate.admin(request);
  const { shopId, value } = await getMetafield(admin, "your_app", "settings");
  return json({ shopId, settings: value });
};

export const action = async ({ request }) => {
  const { admin } = await authenticate.admin(request);
  const formData = await request.formData();

  const settings = {
    apiKey: formData.get("apiKey"),
    enabled: formData.get("enabled") === "true",
  };

  try {
    const shopId = await getShopId(admin);
    await setMetafield(admin, "your_app", "settings", settings, shopId.id);
    return json({ success: true, message: "Settings saved!" });
  } catch (error) {
    return json({ error: error.message }, { status: 500 });
  }
};

export default function Settings() {
  const { settings } = useLoaderData();
  const actionData = useActionData();
  const submit = useSubmit();

  const [formState, setFormState] = useState({
    apiKey: settings?.apiKey || "",
    enabled: settings?.enabled ?? true,
  });

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append("apiKey", formState.apiKey);
    formData.append("enabled", String(formState.enabled));
    submit(formData, { method: "post" });
  };

  return (
    <Page
      title="App Settings"
      primaryAction={{
        content: "Save",
        onAction: handleSubmit,
      }}
    >
      <Layout>
        {actionData?.message && (
          <Layout.Section>
            <Banner tone="success">{actionData.message}</Banner>
          </Layout.Section>
        )}

        {actionData?.error && (
          <Layout.Section>
            <Banner tone="critical">{actionData.error}</Banner>
          </Layout.Section>
        )}

        <Layout.Section>
          <Card>
            <FormLayout>
              <TextField
                label="API Key"
                value={formState.apiKey}
                onChange={(value) => setFormState({ ...formState, apiKey: value })}
                autoComplete="off"
              />

              <Select
                label="Enable Integration"
                options={[
                  { label: "Enabled", value: "true" },
                  { label: "Disabled", value: "false" },
                ]}
                value={String(formState.enabled)}
                onChange={(value) =>
                  setFormState({ ...formState, enabled: value === "true" })
                }
              />
            </FormLayout>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

---

## Checkout UI Extensions

### Extension Configuration

```toml
# extensions/my-extension/shopify.extension.toml
api_version = "2025-01"

[[extensions]]
name = "My Checkout Extension"
handle = "my-checkout-extension"
type = "ui_extension"

[[extensions.targeting]]
module = "./src/index.tsx"
target = "purchase.thank-you.block.render"

[extensions.capabilities]
api_access = true
network_access = true

# Access app metafields in extension
[[extensions.metafields]]
namespace = "your_app"
key = "settings"
```

### Extension Target Locations

| Target | Location |
|--------|----------|
| `purchase.thank-you.block.render` | Thank you page |
| `purchase.checkout.block.render` | Checkout page |
| `customer-account.order-status.block.render` | Order status |
| `customer-account.page.render` | Customer account pages |
| `admin.product-details.block.render` | Admin product page |

### Extension Component

```tsx
// extensions/my-extension/src/index.tsx
import {
  reactExtension,
  useShop,
  useAppMetafields,
  useApi,
  View,
  BlockStack,
  Heading,
  Text,
  Button,
  Spinner,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.thank-you.block.render", () => (
  <Extension />
));

function Extension() {
  const shop = useShop();
  const { orderConfirmation } = useApi();
  const order = orderConfirmation.current.order;

  // Access app metafields
  const metafields = useAppMetafields({
    namespace: "your_app",
    key: "settings"
  });

  const settings = metafields[0]?.metafield?.value
    ? JSON.parse(metafields[0].metafield.value)
    : null;

  if (!settings?.enabled) {
    return null;
  }

  return (
    <View border="base" padding="base">
      <BlockStack>
        <Heading level={2}>Thank You!</Heading>
        <Text>Order #{order.id} confirmed</Text>
        <Text appearance="subdued">
          Shop: {shop.myshopifyDomain}
        </Text>
      </BlockStack>
    </View>
  );
}
```

### Extension with External API

```tsx
// extensions/my-extension/src/hooks/useExternalApi.ts
import { useState, useEffect } from "react";

export function useExternalApi(surveyId: string) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!surveyId) {
      setLoading(false);
      return;
    }

    fetch(`https://api.example.com/surveys/${surveyId}`)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [surveyId]);

  return { data, loading, error };
}
```

---

## Database (Prisma)

### Session Storage Schema

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"  // or "sqlite" for dev
  url      = env("DATABASE_URL")
}

// Required for Shopify session storage
model Session {
  id            String    @id
  shop          String
  state         String
  isOnline      Boolean   @default(false)
  scope         String?
  expires       DateTime?
  accessToken   String
  userId        BigInt?
  firstName     String?
  lastName      String?
  email         String?
  accountOwner  Boolean   @default(false)
  locale        String?
  collaborator  Boolean?  @default(false)
  emailVerified Boolean?  @default(false)

  @@index([shop])
}

// Your app's custom models
model AppSettings {
  id        String   @id @default(uuid())
  shop      String   @unique
  settings  Json
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Database Client

```javascript
// app/db.server.js
import { PrismaClient } from "@prisma/client";

let prisma;

if (process.env.NODE_ENV === "production") {
  prisma = new PrismaClient();
} else {
  // Prevent multiple instances in development
  if (!global.__prisma) {
    global.__prisma = new PrismaClient();
  }
  prisma = global.__prisma;
}

export { prisma };
```

---

## Deployment

### Environment Variables

```bash
# .env (DO NOT COMMIT)
SHOPIFY_API_KEY=your_api_key
SHOPIFY_API_SECRET=your_api_secret
SCOPES=read_products,write_products
SHOPIFY_APP_URL=https://your-app.onrender.com
DATABASE_URL=postgresql://...
```

### Render Deployment

```yaml
# render.yaml
services:
  - type: web
    name: shopify-app
    runtime: node
    plan: starter
    buildCommand: npm install && npm run setup && npm run build
    startCommand: npm run start
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: shopify-db
          property: connectionString
      - key: SHOPIFY_API_KEY
        sync: false
      - key: SHOPIFY_API_SECRET
        sync: false
      - key: SCOPES
        sync: false
      - key: SHOPIFY_APP_URL
        sync: false

databases:
  - name: shopify-db
    plan: starter
```

### Deploy Commands

```bash
# Deploy app to Shopify
shopify app deploy

# This:
# 1. Builds extensions
# 2. Uploads to Shopify
# 3. Creates new app version
```

---

## Common Scopes

| Scope | Access |
|-------|--------|
| `read_products` | View products |
| `write_products` | Create/edit products |
| `read_orders` | View orders |
| `write_orders` | Create/edit orders |
| `read_customers` | View customers |
| `write_customers` | Create/edit customers |
| `read_checkouts` | View checkout data |
| `write_checkouts` | Modify checkout |
| `read_themes` | View themes |
| `write_themes` | Modify themes |
| `read_content` | View metafields/files |
| `write_content` | Modify metafields/files |

---

## CLI Commands

```bash
# Development
shopify app dev                    # Start dev server with tunnel
shopify app dev --reset            # Reset app config

# Configuration
shopify app config link            # Link to existing app
shopify app config use             # Switch config
shopify app env show               # Show env vars

# Extensions
shopify app generate extension     # Create new extension
shopify app build                  # Build all extensions

# Deployment
shopify app deploy                 # Deploy to Shopify
shopify app versions list          # List app versions

# Store
shopify app open                   # Open app in dev store
```

---

## Testing

### Unit Tests

```javascript
// __tests__/adminApi.test.js
import { describe, it, expect, vi } from 'vitest';
import { getShopId, setMetafield } from '../app/shopify/adminApi.server';

describe('Admin API', () => {
  it('gets shop ID', async () => {
    const mockAdmin = {
      graphql: vi.fn().mockResolvedValue({
        json: () => Promise.resolve({
          data: { shop: { id: 'gid://shopify/Shop/123' } }
        })
      })
    };

    const result = await getShopId(mockAdmin);
    expect(result.id).toBe('gid://shopify/Shop/123');
  });
});
```

### E2E with Playwright

```typescript
// e2e/app.spec.ts
import { test, expect } from '@playwright/test';

test('app settings page loads', async ({ page }) => {
  // Note: Requires authenticated session
  await page.goto('/app');

  await expect(page.getByRole('heading', { name: /settings/i })).toBeVisible();
  await expect(page.getByLabel('API Key')).toBeVisible();
});

test('saves settings successfully', async ({ page }) => {
  await page.goto('/app');

  await page.fill('[name="apiKey"]', 'test-key-123');
  await page.click('button:has-text("Save")');

  await expect(page.getByText('Settings saved')).toBeVisible();
});
```

---

## Rate Limits

### GraphQL Cost-Based Limits

```javascript
// Check rate limit status in response
const response = await admin.graphql(`
  query {
    shop { name }
  }
`);

const data = await response.json();

// Rate limit info in extensions
const throttleStatus = data.extensions?.cost?.throttleStatus;
// {
//   maximumAvailable: 1000,
//   currentlyAvailable: 950,
//   restoreRate: 50  // points per second
// }
```

### Handling Throttling

```javascript
async function graphqlWithRetry(admin, query, variables, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const response = await admin.graphql(query, { variables });
    const data = await response.json();

    if (data.errors?.some(e => e.extensions?.code === 'THROTTLED')) {
      const waitTime = Math.pow(2, attempt) * 1000; // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, waitTime));
      continue;
    }

    return data;
  }
  throw new Error('Max retries exceeded');
}
```

---

## Checklist

### Before Development

- [ ] Partner account created
- [ ] Development store created
- [ ] App created in Partner Dashboard
- [ ] Shopify CLI installed
- [ ] App scaffolded with Remix template

### Before Submission

- [ ] GDPR webhooks implemented (customers/data_request, customers/redact, shop/redact)
- [ ] App uninstall webhook cleans up data
- [ ] No hardcoded API keys
- [ ] Error handling for all API calls
- [ ] Rate limit handling
- [ ] Responsive UI (works on mobile admin)
- [ ] Polaris components used consistently
- [ ] Extension targets correct surfaces
- [ ] Privacy policy URL configured
- [ ] App listing completed

### Security

- [ ] Session tokens validated
- [ ] Webhook HMAC verification (handled by SDK)
- [ ] No sensitive data in client-side code
- [ ] Environment variables for all secrets
- [ ] HTTPS enforced

---

## Anti-Patterns

- **REST API usage** - Use GraphQL Admin API (REST is deprecated)
- **Storing secrets in metafields** - Use environment variables
- **Ignoring rate limits** - Implement exponential backoff
- **Skipping GDPR webhooks** - Required for App Store
- **Large GraphQL queries** - Paginate, query only needed fields
- **Polling for updates** - Use webhooks instead
- **Custom auth flow** - Use Shopify's OAuth flow via SDK
