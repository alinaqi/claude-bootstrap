---
name: medusa
description: Medusa headless commerce - modules, workflows, API routes, admin UI
---

# Medusa E-Commerce Skill

*Load with: base.md + typescript.md*

For building headless e-commerce with Medusa - open-source, Node.js native, fully customizable.

**Sources:** [Medusa Docs](https://docs.medusajs.com) | [API Reference](https://docs.medusajs.com/api/store) | [GitHub](https://github.com/medusajs/medusa)

---

## Why Medusa

| Feature | Benefit |
|---------|---------|
| **Open Source** | Self-host, no vendor lock-in, MIT license |
| **Node.js Native** | TypeScript, familiar stack, easy to customize |
| **Headless** | Any frontend (Next.js, Remix, mobile) |
| **Modular** | Use only what you need, extend anything |
| **Built-in Admin** | Dashboard included, customizable |

---

## Quick Start

### Prerequisites

```bash
# Required
node --version  # v20+ LTS
git --version
# PostgreSQL running locally or remote
```

### Create New Project

```bash
# Scaffold new Medusa application
npx create-medusa-app@latest my-store

# This creates:
# - Medusa backend
# - PostgreSQL database (auto-configured)
# - Admin dashboard
# - Optional: Next.js storefront

cd my-store
npm run dev
```

### Access Points

| URL | Purpose |
|-----|---------|
| `http://localhost:9000` | Backend API |
| `http://localhost:9000/app` | Admin dashboard |
| `http://localhost:8000` | Storefront (if installed) |

### Create Admin User

```bash
npx medusa user -e admin@example.com -p supersecret
```

---

## Project Structure

```
medusa-store/
├── src/
│   ├── admin/                    # Admin UI customizations
│   │   ├── widgets/              # Dashboard widgets
│   │   └── routes/               # Custom admin pages
│   ├── api/                      # Custom API routes
│   │   ├── store/                # Public storefront APIs
│   │   │   └── custom/
│   │   │       └── route.ts
│   │   └── admin/                # Admin APIs
│   │       └── custom/
│   │           └── route.ts
│   ├── jobs/                     # Scheduled tasks
│   ├── modules/                  # Custom business logic
│   ├── workflows/                # Multi-step processes
│   ├── subscribers/              # Event listeners
│   └── links/                    # Module relationships
├── .medusa/                      # Auto-generated (don't edit)
├── medusa-config.ts              # Configuration
├── package.json
└── tsconfig.json
```

---

## Configuration

### medusa-config.ts

```typescript
import { defineConfig, loadEnv } from "@medusajs/framework/utils";

loadEnv(process.env.NODE_ENV || "development", process.cwd());

export default defineConfig({
  projectConfig: {
    databaseUrl: process.env.DATABASE_URL,
    http: {
      storeCors: process.env.STORE_CORS || "http://localhost:8000",
      adminCors: process.env.ADMIN_CORS || "http://localhost:9000",
      authCors: process.env.AUTH_CORS || "http://localhost:9000",
    },
    redisUrl: process.env.REDIS_URL,
  },
  admin: {
    disable: false,
    backendUrl: process.env.MEDUSA_BACKEND_URL || "http://localhost:9000",
  },
  modules: [
    // Add custom modules here
  ],
});
```

### Environment Variables

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/medusa
REDIS_URL=redis://localhost:6379

# CORS (comma-separated for multiple origins)
STORE_CORS=http://localhost:8000
ADMIN_CORS=http://localhost:9000

# Backend URL
MEDUSA_BACKEND_URL=http://localhost:9000

# JWT Secrets
JWT_SECRET=your-super-secret-jwt-key
COOKIE_SECRET=your-super-secret-cookie-key
```

---

## Custom API Routes

### Store API (Public)

```typescript
// src/api/store/hello/route.ts
import type { MedusaRequest, MedusaResponse } from "@medusajs/framework/http";

export async function GET(
  req: MedusaRequest,
  res: MedusaResponse
) {
  res.json({
    message: "Hello from custom store API!",
  });
}

// Accessible at: GET /store/hello
```

### Admin API (Protected)

```typescript
// src/api/admin/analytics/route.ts
import type { MedusaRequest, MedusaResponse } from "@medusajs/framework/http";
import { Modules } from "@medusajs/framework/utils";

export async function GET(
  req: MedusaRequest,
  res: MedusaResponse
) {
  const orderService = req.scope.resolve(Modules.ORDER);

  const orders = await orderService.listOrders({
    created_at: {
      $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // Last 30 days
    },
  });

  const totalRevenue = orders.reduce(
    (sum, order) => sum + (order.total || 0),
    0
  );

  res.json({
    orderCount: orders.length,
    totalRevenue,
  });
}

// Accessible at: GET /admin/analytics (requires auth)
```

### Route with Parameters

```typescript
// src/api/store/products/[id]/reviews/route.ts
import type { MedusaRequest, MedusaResponse } from "@medusajs/framework/http";

export async function GET(
  req: MedusaRequest,
  res: MedusaResponse
) {
  const { id } = req.params;

  // Fetch reviews for product
  const reviews = await getReviewsForProduct(id);

  res.json({ reviews });
}

export async function POST(
  req: MedusaRequest,
  res: MedusaResponse
) {
  const { id } = req.params;
  const { rating, comment, customerId } = req.body;

  const review = await createReview({
    productId: id,
    rating,
    comment,
    customerId,
  });

  res.status(201).json({ review });
}

// Accessible at:
// GET  /store/products/:id/reviews
// POST /store/products/:id/reviews
```

### Middleware

```typescript
// src/api/middlewares.ts
import { defineMiddlewares } from "@medusajs/framework/http";
import { authenticate } from "@medusajs/framework/http";

export default defineMiddlewares({
  routes: [
    {
      matcher: "/store/protected/*",
      middlewares: [authenticate("customer", ["session", "bearer"])],
    },
    {
      matcher: "/admin/*",
      middlewares: [authenticate("user", ["session", "bearer"])],
    },
  ],
});
```

---

## Modules (Custom Business Logic)

### Create Custom Module

```typescript
// src/modules/reviews/index.ts
import { Module } from "@medusajs/framework/utils";
import ReviewModuleService from "./service";

export const REVIEW_MODULE = "reviewModuleService";

export default Module(REVIEW_MODULE, {
  service: ReviewModuleService,
});
```

```typescript
// src/modules/reviews/service.ts
import { MedusaService } from "@medusajs/framework/utils";

class ReviewModuleService extends MedusaService({}) {
  async createReview(data: CreateReviewInput) {
    // Implementation
  }

  async getProductReviews(productId: string) {
    // Implementation
  }

  async getAverageRating(productId: string) {
    // Implementation
  }
}

export default ReviewModuleService;
```

### Register Module

```typescript
// medusa-config.ts
import { REVIEW_MODULE } from "./src/modules/reviews";

export default defineConfig({
  // ...
  modules: [
    {
      resolve: "./src/modules/reviews",
      options: {},
    },
  ],
});
```

### Use Module in API

```typescript
// src/api/store/products/[id]/reviews/route.ts
import { REVIEW_MODULE } from "../../../modules/reviews";

export async function GET(req: MedusaRequest, res: MedusaResponse) {
  const { id } = req.params;
  const reviewService = req.scope.resolve(REVIEW_MODULE);

  const reviews = await reviewService.getProductReviews(id);
  const averageRating = await reviewService.getAverageRating(id);

  res.json({ reviews, averageRating });
}
```

---

## Workflows

### Define Workflow

```typescript
// src/workflows/create-order-with-notification/index.ts
import {
  createWorkflow,
  createStep,
  StepResponse,
} from "@medusajs/framework/workflows-sdk";
import { Modules } from "@medusajs/framework/utils";

const createOrderStep = createStep(
  "create-order",
  async (input: CreateOrderInput, { container }) => {
    const orderService = container.resolve(Modules.ORDER);

    const order = await orderService.createOrders(input);

    return new StepResponse(order, order.id);
  },
  // Compensation (rollback) function
  async (orderId, { container }) => {
    const orderService = container.resolve(Modules.ORDER);
    await orderService.deleteOrders([orderId]);
  }
);

const sendNotificationStep = createStep(
  "send-notification",
  async (order: Order, { container }) => {
    const notificationService = container.resolve("notificationService");

    await notificationService.send({
      to: order.email,
      template: "order-confirmation",
      data: { order },
    });

    return new StepResponse({ sent: true });
  }
);

export const createOrderWithNotificationWorkflow = createWorkflow(
  "create-order-with-notification",
  (input: CreateOrderInput) => {
    const order = createOrderStep(input);
    const notification = sendNotificationStep(order);

    return { order, notification };
  }
);
```

### Execute Workflow

```typescript
// In an API route
import { createOrderWithNotificationWorkflow } from "../../../workflows/create-order-with-notification";

export async function POST(req: MedusaRequest, res: MedusaResponse) {
  const { result } = await createOrderWithNotificationWorkflow(req.scope).run({
    input: req.body,
  });

  res.json(result);
}
```

---

## Subscribers (Event Listeners)

### Create Subscriber

```typescript
// src/subscribers/order-placed.ts
import type { SubscriberArgs, SubscriberConfig } from "@medusajs/framework";

export default async function orderPlacedHandler({
  event,
  container,
}: SubscriberArgs<{ id: string }>) {
  const orderId = event.data.id;

  console.log(`Order placed: ${orderId}`);

  // Send notification, update analytics, etc.
  const notificationService = container.resolve("notificationService");
  await notificationService.sendOrderConfirmation(orderId);
}

export const config: SubscriberConfig = {
  event: "order.placed",
};
```

### Common Events

| Event | Trigger |
|-------|---------|
| `order.placed` | New order created |
| `order.updated` | Order modified |
| `order.canceled` | Order cancelled |
| `order.completed` | Order fulfilled |
| `customer.created` | New customer registered |
| `product.created` | New product added |
| `product.updated` | Product modified |
| `inventory.updated` | Stock changed |

---

## Scheduled Jobs

```typescript
// src/jobs/sync-inventory.ts
import type { MedusaContainer } from "@medusajs/framework";

export default async function syncInventoryJob(container: MedusaContainer) {
  const inventoryService = container.resolve("inventoryService");

  console.log("Running inventory sync...");

  await inventoryService.syncFromExternalSource();

  console.log("Inventory sync complete");
}

export const config = {
  name: "sync-inventory",
  schedule: "0 */6 * * *", // Every 6 hours
};
```

---

## Admin UI Customization

### Custom Widget

```tsx
// src/admin/widgets/sales-overview.tsx
import { defineWidgetConfig } from "@medusajs/admin-sdk";
import { Container, Heading, Text } from "@medusajs/ui";

const SalesOverviewWidget = () => {
  return (
    <Container>
      <Heading level="h2">Sales Overview</Heading>
      <Text>Your custom sales data here...</Text>
    </Container>
  );
};

export const config = defineWidgetConfig({
  zone: "order.list.before", // Where to show the widget
});

export default SalesOverviewWidget;
```

### Widget Zones

| Zone | Location |
|------|----------|
| `order.list.before` | Before order list |
| `order.details.after` | After order details |
| `product.list.before` | Before product list |
| `product.details.after` | After product details |
| `customer.list.before` | Before customer list |

### Custom Admin Route

```tsx
// src/admin/routes/analytics/page.tsx
import { defineRouteConfig } from "@medusajs/admin-sdk";
import { Container, Heading } from "@medusajs/ui";
import { ChartBar } from "@medusajs/icons";

const AnalyticsPage = () => {
  return (
    <Container>
      <Heading level="h1">Analytics Dashboard</Heading>
      {/* Your analytics charts */}
    </Container>
  );
};

export const config = defineRouteConfig({
  label: "Analytics",
  icon: ChartBar,
});

export default AnalyticsPage;
```

---

## Store API (Built-in)

### Products

```typescript
// Frontend: Fetch products
const response = await fetch("http://localhost:9000/store/products");
const { products } = await response.json();

// With filters
const response = await fetch(
  "http://localhost:9000/store/products?" +
  new URLSearchParams({
    category_id: "cat_123",
    limit: "20",
    offset: "0",
  })
);
```

### Cart

```typescript
// Create cart
const { cart } = await fetch("http://localhost:9000/store/carts", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    region_id: "reg_123",
  }),
}).then(r => r.json());

// Add item
await fetch(`http://localhost:9000/store/carts/${cart.id}/line-items`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    variant_id: "variant_123",
    quantity: 1,
  }),
});

// Complete cart (create order)
const { order } = await fetch(
  `http://localhost:9000/store/carts/${cart.id}/complete`,
  { method: "POST" }
).then(r => r.json());
```

### Customer Authentication

```typescript
// Register
await fetch("http://localhost:9000/store/customers", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "customer@example.com",
    password: "password123",
    first_name: "John",
    last_name: "Doe",
  }),
});

// Login
const { token } = await fetch("http://localhost:9000/store/auth/token", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "customer@example.com",
    password: "password123",
  }),
}).then(r => r.json());

// Authenticated request
await fetch("http://localhost:9000/store/customers/me", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

---

## Payment Integration

### Stripe Setup

```bash
npm install @medusajs/payment-stripe
```

```typescript
// medusa-config.ts
export default defineConfig({
  modules: [
    {
      resolve: "@medusajs/payment-stripe",
      options: {
        apiKey: process.env.STRIPE_API_KEY,
      },
    },
  ],
});
```

### In Admin

1. Go to Settings → Regions
2. Add Stripe as payment provider
3. Configure for each region

---

## Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render

```yaml
# render.yaml
services:
  - type: web
    name: medusa-backend
    runtime: node
    plan: starter
    buildCommand: npm install && npm run build
    startCommand: npm run start
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: medusa-db
          property: connectionString
      - key: JWT_SECRET
        generateValue: true
      - key: COOKIE_SECRET
        generateValue: true

databases:
  - name: medusa-db
    plan: starter
```

### Docker

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 9000
CMD ["npm", "run", "start"]
```

---

## CLI Commands

```bash
# Development
npm run dev                    # Start dev server

# Database
npx medusa db:migrate          # Run migrations
npx medusa db:sync             # Sync schema

# Users
npx medusa user -e email -p pass  # Create admin user

# Build
npm run build                  # Build for production
npm run start                  # Start production server
```

---

## Checklist

### Setup

- [ ] PostgreSQL database configured
- [ ] Redis configured (optional but recommended)
- [ ] Admin user created
- [ ] CORS origins configured
- [ ] JWT/Cookie secrets set

### Customization

- [ ] Custom modules for business logic
- [ ] Custom API routes for frontend
- [ ] Subscribers for event handling
- [ ] Workflows for complex operations

### Deployment

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] HTTPS enabled
- [ ] Admin URL secured

---

## Anti-Patterns

- **Editing .medusa folder** - Auto-generated, will be overwritten
- **Direct database access** - Use services and modules
- **Skipping workflows for complex ops** - Workflows provide rollback
- **Hardcoding URLs** - Use environment variables
- **Ignoring TypeScript errors** - Framework relies on types
