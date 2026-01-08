---
name: woocommerce
description: WooCommerce REST API - products, orders, customers, webhooks
---

# WooCommerce Development Skill

*Load with: base.md + (typescript.md or python.md)*

For integrating with WooCommerce stores via REST API - products, orders, customers, webhooks, and custom extensions.

**Sources:** [WooCommerce REST API](https://woocommerce.github.io/woocommerce-rest-api-docs/) | [Developer Docs](https://developer.woocommerce.com/docs/)

---

## Prerequisites

### Store Requirements

```bash
# WooCommerce store must have:
# 1. WordPress with WooCommerce plugin installed
# 2. HTTPS enabled (required for API auth)
# 3. Permalinks set to anything except "Plain"
#    WordPress Admin → Settings → Permalinks → Post name (recommended)
```

### Generate API Keys

1. Go to **WooCommerce → Settings → Advanced → REST API**
2. Click **Add key**
3. Set Description, User (admin), and Permissions (Read/Write)
4. Click **Generate API key**
5. Copy **Consumer Key** and **Consumer Secret** (shown only once)

---

## API Basics

### Base URL

```
https://your-store.com/wp-json/wc/v3/
```

### Authentication

```typescript
// Node.js - Basic Auth (recommended)
const WooCommerceRestApi = require("@woocommerce/woocommerce-rest-api").default;

const api = new WooCommerceRestApi({
  url: "https://your-store.com",
  consumerKey: process.env.WC_CONSUMER_KEY,
  consumerSecret: process.env.WC_CONSUMER_SECRET,
  version: "wc/v3"
});
```

```python
# Python
from woocommerce import API

wcapi = API(
    url="https://your-store.com",
    consumer_key=os.environ["WC_CONSUMER_KEY"],
    consumer_secret=os.environ["WC_CONSUMER_SECRET"],
    version="wc/v3"
)
```

### Query String Auth (Fallback)

```bash
# Only use if Basic Auth fails (some hosting configurations)
curl https://your-store.com/wp-json/wc/v3/products \
  ?consumer_key=ck_xxx&consumer_secret=cs_xxx
```

---

## Installation

### Node.js

```bash
npm install @woocommerce/woocommerce-rest-api
```

```typescript
// lib/woocommerce.ts
import WooCommerceRestApi from "@woocommerce/woocommerce-rest-api";

const api = new WooCommerceRestApi({
  url: process.env.WC_STORE_URL!,
  consumerKey: process.env.WC_CONSUMER_KEY!,
  consumerSecret: process.env.WC_CONSUMER_SECRET!,
  version: "wc/v3",
  queryStringAuth: false, // Set true for HTTP (dev only)
});

export default api;
```

### Python

```bash
pip install woocommerce
```

```python
# lib/woocommerce.py
import os
from woocommerce import API

wcapi = API(
    url=os.environ["WC_STORE_URL"],
    consumer_key=os.environ["WC_CONSUMER_KEY"],
    consumer_secret=os.environ["WC_CONSUMER_SECRET"],
    version="wc/v3",
    timeout=30
)
```

---

## Products

### List Products

```typescript
// Node.js
async function getProducts(page = 1, perPage = 20) {
  const response = await api.get("products", {
    page,
    per_page: perPage,
    status: "publish",
  });
  return response.data;
}

// With filters
async function searchProducts(search: string, category?: number) {
  const response = await api.get("products", {
    search,
    category: category || undefined,
    orderby: "popularity",
    order: "desc",
  });
  return response.data;
}
```

```python
# Python
def get_products(page=1, per_page=20):
    response = wcapi.get("products", params={
        "page": page,
        "per_page": per_page,
        "status": "publish"
    })
    return response.json()
```

### Get Single Product

```typescript
async function getProduct(productId: number) {
  const response = await api.get(`products/${productId}`);
  return response.data;
}
```

### Create Product

```typescript
async function createProduct(data: ProductInput) {
  const response = await api.post("products", {
    name: data.name,
    type: "simple", // simple, variable, grouped, external
    regular_price: data.price.toString(),
    description: data.description,
    short_description: data.shortDescription,
    categories: data.categoryIds.map(id => ({ id })),
    images: data.images.map(url => ({ src: url })),
    manage_stock: true,
    stock_quantity: data.stockQuantity,
    status: "publish",
  });
  return response.data;
}
```

### Update Product

```typescript
async function updateProduct(productId: number, data: Partial<ProductInput>) {
  const response = await api.put(`products/${productId}`, data);
  return response.data;
}

// Update stock only
async function updateStock(productId: number, quantity: number) {
  const response = await api.put(`products/${productId}`, {
    stock_quantity: quantity,
  });
  return response.data;
}
```

### Delete Product

```typescript
async function deleteProduct(productId: number, force = false) {
  // force: true = permanent delete, false = move to trash
  const response = await api.delete(`products/${productId}`, {
    force,
  });
  return response.data;
}
```

### Variable Products

```typescript
// Create variable product
async function createVariableProduct(data: VariableProductInput) {
  // 1. Create product with type "variable"
  const product = await api.post("products", {
    name: data.name,
    type: "variable",
    attributes: [
      {
        name: "Size",
        visible: true,
        variation: true,
        options: ["Small", "Medium", "Large"],
      },
      {
        name: "Color",
        visible: true,
        variation: true,
        options: ["Red", "Blue"],
      },
    ],
  });

  // 2. Create variations
  for (const variant of data.variants) {
    await api.post(`products/${product.data.id}/variations`, {
      regular_price: variant.price.toString(),
      stock_quantity: variant.stock,
      attributes: [
        { name: "Size", option: variant.size },
        { name: "Color", option: variant.color },
      ],
    });
  }

  return product.data;
}

// Get variations
async function getVariations(productId: number) {
  const response = await api.get(`products/${productId}/variations`);
  return response.data;
}
```

---

## Orders

### List Orders

```typescript
async function getOrders(params: OrderQueryParams = {}) {
  const response = await api.get("orders", {
    page: params.page || 1,
    per_page: params.perPage || 20,
    status: params.status || "any", // pending, processing, completed, etc.
    after: params.after, // ISO date string
    before: params.before,
  });
  return response.data;
}

// Get recent orders
async function getRecentOrders(days = 7) {
  const after = new Date();
  after.setDate(after.getDate() - days);

  const response = await api.get("orders", {
    after: after.toISOString(),
    orderby: "date",
    order: "desc",
  });
  return response.data;
}
```

### Get Single Order

```typescript
async function getOrder(orderId: number) {
  const response = await api.get(`orders/${orderId}`);
  return response.data;
}
```

### Create Order

```typescript
async function createOrder(data: OrderInput) {
  const response = await api.post("orders", {
    payment_method: "stripe",
    payment_method_title: "Credit Card",
    set_paid: false,
    billing: {
      first_name: data.customer.firstName,
      last_name: data.customer.lastName,
      email: data.customer.email,
      phone: data.customer.phone,
      address_1: data.billing.address1,
      city: data.billing.city,
      state: data.billing.state,
      postcode: data.billing.postcode,
      country: data.billing.country,
    },
    shipping: {
      first_name: data.customer.firstName,
      last_name: data.customer.lastName,
      address_1: data.shipping.address1,
      city: data.shipping.city,
      state: data.shipping.state,
      postcode: data.shipping.postcode,
      country: data.shipping.country,
    },
    line_items: data.items.map(item => ({
      product_id: item.productId,
      variation_id: item.variationId,
      quantity: item.quantity,
    })),
    shipping_lines: [
      {
        method_id: "flat_rate",
        method_title: "Flat Rate",
        total: data.shippingCost.toString(),
      },
    ],
  });
  return response.data;
}
```

### Update Order Status

```typescript
async function updateOrderStatus(orderId: number, status: OrderStatus) {
  const response = await api.put(`orders/${orderId}`, {
    status, // pending, processing, on-hold, completed, cancelled, refunded, failed
  });
  return response.data;
}

// Add order note
async function addOrderNote(orderId: number, note: string, customerNote = false) {
  const response = await api.post(`orders/${orderId}/notes`, {
    note,
    customer_note: customerNote, // true = visible to customer
  });
  return response.data;
}
```

### Order Statuses

| Status | Description |
|--------|-------------|
| `pending` | Awaiting payment |
| `processing` | Payment received, awaiting fulfillment |
| `on-hold` | Awaiting action (stock, payment confirmation) |
| `completed` | Order fulfilled |
| `cancelled` | Cancelled by admin or customer |
| `refunded` | Refunded |
| `failed` | Payment failed |

---

## Customers

### List Customers

```typescript
async function getCustomers(params: CustomerQueryParams = {}) {
  const response = await api.get("customers", {
    page: params.page || 1,
    per_page: params.perPage || 20,
    role: "customer",
    orderby: "registered_date",
    order: "desc",
  });
  return response.data;
}

// Search customers
async function searchCustomers(email: string) {
  const response = await api.get("customers", {
    email,
  });
  return response.data;
}
```

### Create Customer

```typescript
async function createCustomer(data: CustomerInput) {
  const response = await api.post("customers", {
    email: data.email,
    first_name: data.firstName,
    last_name: data.lastName,
    username: data.email.split("@")[0],
    billing: {
      first_name: data.firstName,
      last_name: data.lastName,
      email: data.email,
      phone: data.phone,
      address_1: data.address1,
      city: data.city,
      state: data.state,
      postcode: data.postcode,
      country: data.country,
    },
    shipping: {
      // Same as billing or different
    },
  });
  return response.data;
}
```

### Update Customer

```typescript
async function updateCustomer(customerId: number, data: Partial<CustomerInput>) {
  const response = await api.put(`customers/${customerId}`, data);
  return response.data;
}
```

---

## Webhooks

### Create Webhook

```typescript
async function createWebhook(topic: string, deliveryUrl: string) {
  const response = await api.post("webhooks", {
    name: `Webhook for ${topic}`,
    topic, // order.created, order.updated, product.created, etc.
    delivery_url: deliveryUrl,
    status: "active",
    secret: process.env.WC_WEBHOOK_SECRET,
  });
  return response.data;
}
```

### Webhook Topics

| Topic | Trigger |
|-------|---------|
| `order.created` | New order placed |
| `order.updated` | Order status/details changed |
| `order.deleted` | Order deleted |
| `product.created` | New product created |
| `product.updated` | Product updated |
| `product.deleted` | Product deleted |
| `customer.created` | New customer registered |
| `customer.updated` | Customer updated |
| `coupon.created` | New coupon created |

### Verify Webhook Signature

```typescript
// Express.js webhook handler
import crypto from "crypto";

function verifyWooCommerceWebhook(req: Request): boolean {
  const signature = req.headers["x-wc-webhook-signature"] as string;
  const payload = JSON.stringify(req.body);

  const expectedSignature = crypto
    .createHmac("sha256", process.env.WC_WEBHOOK_SECRET!)
    .update(payload)
    .digest("base64");

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}

// Route handler
app.post("/webhooks/woocommerce", (req, res) => {
  if (!verifyWooCommerceWebhook(req)) {
    return res.status(401).json({ error: "Invalid signature" });
  }

  const topic = req.headers["x-wc-webhook-topic"];
  const payload = req.body;

  switch (topic) {
    case "order.created":
      handleNewOrder(payload);
      break;
    case "order.updated":
      handleOrderUpdate(payload);
      break;
    // ... other topics
  }

  res.status(200).json({ received: true });
});
```

```python
# Python/Flask webhook handler
import hmac
import hashlib
import base64

@app.route("/webhooks/woocommerce", methods=["POST"])
def woocommerce_webhook():
    signature = request.headers.get("X-WC-Webhook-Signature")
    payload = request.get_data()

    expected = base64.b64encode(
        hmac.new(
            os.environ["WC_WEBHOOK_SECRET"].encode(),
            payload,
            hashlib.sha256
        ).digest()
    ).decode()

    if not hmac.compare_digest(signature, expected):
        return {"error": "Invalid signature"}, 401

    topic = request.headers.get("X-WC-Webhook-Topic")
    data = request.json

    if topic == "order.created":
        handle_new_order(data)
    elif topic == "order.updated":
        handle_order_update(data)

    return {"received": True}, 200
```

---

## Categories & Tags

### List Categories

```typescript
async function getCategories() {
  const response = await api.get("products/categories", {
    per_page: 100,
    orderby: "name",
  });
  return response.data;
}

// Create category
async function createCategory(name: string, parentId?: number) {
  const response = await api.post("products/categories", {
    name,
    parent: parentId || 0,
  });
  return response.data;
}
```

### List Tags

```typescript
async function getTags() {
  const response = await api.get("products/tags", {
    per_page: 100,
  });
  return response.data;
}
```

---

## Coupons

### Create Coupon

```typescript
async function createCoupon(data: CouponInput) {
  const response = await api.post("coupons", {
    code: data.code,
    discount_type: data.type, // percent, fixed_cart, fixed_product
    amount: data.amount.toString(),
    individual_use: true,
    exclude_sale_items: false,
    minimum_amount: data.minimumAmount?.toString(),
    maximum_amount: data.maximumAmount?.toString(),
    usage_limit: data.usageLimit,
    usage_limit_per_user: 1,
    date_expires: data.expiresAt, // ISO date string
  });
  return response.data;
}
```

---

## Reports

### Sales Report

```typescript
async function getSalesReport(period = "month") {
  const response = await api.get("reports/sales", {
    period, // day, week, month, year
  });
  return response.data;
}

// Top sellers
async function getTopSellers(period = "month") {
  const response = await api.get("reports/top_sellers", {
    period,
  });
  return response.data;
}
```

---

## Pagination

### Handle Large Datasets

```typescript
async function getAllProducts() {
  const allProducts = [];
  let page = 1;
  const perPage = 100;

  while (true) {
    const response = await api.get("products", {
      page,
      per_page: perPage,
    });

    allProducts.push(...response.data);

    // Check headers for total pages
    const totalPages = parseInt(response.headers["x-wp-totalpages"]);
    if (page >= totalPages) break;

    page++;
  }

  return allProducts;
}
```

### Pagination Headers

| Header | Description |
|--------|-------------|
| `X-WP-Total` | Total number of items |
| `X-WP-TotalPages` | Total number of pages |

---

## Error Handling

```typescript
import WooCommerceRestApi from "@woocommerce/woocommerce-rest-api";

async function safeApiCall<T>(
  operation: () => Promise<{ data: T }>
): Promise<T> {
  try {
    const response = await operation();
    return response.data;
  } catch (error: any) {
    if (error.response) {
      // API returned an error
      const { status, data } = error.response;

      switch (status) {
        case 400:
          throw new Error(`Bad request: ${data.message}`);
        case 401:
          throw new Error("Invalid API credentials");
        case 404:
          throw new Error("Resource not found");
        case 429:
          // Rate limited - wait and retry
          await new Promise(r => setTimeout(r, 5000));
          return safeApiCall(operation);
        default:
          throw new Error(`API error: ${data.message}`);
      }
    }
    throw error;
  }
}

// Usage
const products = await safeApiCall(() => api.get("products"));
```

---

## Environment Variables

```bash
# .env
WC_STORE_URL=https://your-store.com
WC_CONSUMER_KEY=ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WC_CONSUMER_SECRET=cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WC_WEBHOOK_SECRET=your_webhook_secret
```

Add to `credentials.md`:
```python
'WC_CONSUMER_KEY': r'ck_[a-f0-9]{40}',
'WC_CONSUMER_SECRET': r'cs_[a-f0-9]{40}',
```

---

## Checklist

### Before Integration

- [ ] WooCommerce plugin installed and activated
- [ ] HTTPS enabled on store
- [ ] Permalinks set to non-Plain setting
- [ ] API keys generated with appropriate permissions
- [ ] Webhook secret configured

### Security

- [ ] API keys stored in environment variables
- [ ] Webhook signatures verified
- [ ] HTTPS used for all API calls
- [ ] Rate limiting handled

### Testing

- [ ] Test API connection
- [ ] Test product CRUD operations
- [ ] Test order creation/updates
- [ ] Test webhook delivery
- [ ] Test pagination for large datasets

---

## Anti-Patterns

- **Plain permalinks** - API won't work without pretty permalinks
- **HTTP in production** - Always use HTTPS
- **Ignoring rate limits** - WooCommerce may throttle requests
- **Large single requests** - Use pagination for bulk operations
- **Storing keys in code** - Use environment variables
- **Skipping webhook verification** - Always verify signatures
