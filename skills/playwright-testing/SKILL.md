---
name: playwright-testing
description: E2E testing with Playwright - Page Objects, cross-browser, CI/CD
---

# Playwright E2E Testing Skill

*Load with: base.md + [framework].md*

For end-to-end testing of web applications with Playwright - cross-browser, fast, reliable.

**Sources:** [Playwright Best Practices](https://playwright.dev/docs/best-practices) | [Playwright Docs](https://playwright.dev/docs/intro) | [Better Stack Guide](https://betterstack.com/community/guides/testing/playwright-best-practices/)

---

## Setup

### Installation

```bash
# New project
npm init playwright@latest

# Existing project
npm install -D @playwright/test
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['list'],
    process.env.CI ? ['github'] : ['line'],
  ],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    // Auth setup - runs once before all tests
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup'],
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
      dependencies: ['setup'],
    },
    // Mobile viewports
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
      dependencies: ['setup'],
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
      dependencies: ['setup'],
    },
  ],

  // Start dev server before tests
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

---

## Project Structure

```
project/
├── e2e/
│   ├── fixtures/
│   │   ├── auth.fixture.ts      # Auth fixtures
│   │   └── test.fixture.ts      # Extended test with fixtures
│   ├── pages/
│   │   ├── base.page.ts         # Base page object
│   │   ├── login.page.ts        # Login page object
│   │   ├── dashboard.page.ts    # Dashboard page object
│   │   └── index.ts             # Export all pages
│   ├── tests/
│   │   ├── auth.spec.ts         # Auth tests
│   │   ├── dashboard.spec.ts    # Dashboard tests
│   │   └── checkout.spec.ts     # Checkout flow tests
│   ├── utils/
│   │   ├── helpers.ts           # Test helpers
│   │   └── test-data.ts         # Test data factories
│   └── auth.setup.ts            # Global auth setup
├── playwright.config.ts
└── .auth/                        # Stored auth state (gitignored)
```

---

## Locator Strategy (Priority Order)

Use locators that mirror how users interact with the page:

```typescript
// ✅ BEST: Role-based (accessible, resilient)
page.getByRole('button', { name: 'Submit' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('link', { name: 'Sign up' })
page.getByRole('heading', { name: 'Welcome' })

// ✅ GOOD: User-facing text
page.getByLabel('Email address')
page.getByPlaceholder('Enter your email')
page.getByText('Welcome back')
page.getByTitle('Profile settings')

// ✅ GOOD: Test IDs (stable, explicit)
page.getByTestId('submit-button')
page.getByTestId('user-avatar')

// ⚠️ AVOID: CSS selectors (brittle)
page.locator('.btn-primary')
page.locator('#submit')

// ❌ NEVER: XPath (extremely brittle)
page.locator('//div[@class="container"]/button[1]')
```

### Chaining Locators

```typescript
// Narrow down to specific section
const form = page.getByRole('form', { name: 'Login' });
await form.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await form.getByRole('button', { name: 'Submit' }).click();

// Filter within a list
const productCard = page.getByTestId('product-card')
  .filter({ hasText: 'Pro Plan' });
await productCard.getByRole('button', { name: 'Buy' }).click();
```

---

## Page Object Model

### Base Page

```typescript
// e2e/pages/base.page.ts
import { Page, Locator } from '@playwright/test';

export abstract class BasePage {
  constructor(protected page: Page) {}

  async navigate(path: string = '/') {
    await this.page.goto(path);
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  // Common elements
  get header() {
    return this.page.getByRole('banner');
  }

  get footer() {
    return this.page.getByRole('contentinfo');
  }

  // Common actions
  async clickNavLink(name: string) {
    await this.header.getByRole('link', { name }).click();
  }
}
```

### Page Implementation

```typescript
// e2e/pages/login.page.ts
import { Page, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.navigate('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }

  async expectLoggedIn() {
    await expect(this.page).toHaveURL(/.*dashboard/);
  }
}
```

```typescript
// e2e/pages/dashboard.page.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class DashboardPage extends BasePage {
  readonly welcomeHeading: Locator;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    super(page);
    this.welcomeHeading = page.getByRole('heading', { name: /welcome/i });
    this.userMenu = page.getByTestId('user-menu');
    this.logoutButton = page.getByRole('button', { name: 'Logout' });
  }

  async goto() {
    await this.navigate('/dashboard');
  }

  async logout() {
    await this.userMenu.click();
    await this.logoutButton.click();
  }

  async expectWelcome(name: string) {
    await expect(this.welcomeHeading).toContainText(name);
  }
}
```

### Export All Pages

```typescript
// e2e/pages/index.ts
export { BasePage } from './base.page';
export { LoginPage } from './login.page';
export { DashboardPage } from './dashboard.page';
```

---

## Authentication

### Global Auth Setup

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '../.auth/user.json');

setup('authenticate', async ({ page }) => {
  // Go to login page
  await page.goto('/login');

  // Login with test credentials
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Wait for auth to complete
  await expect(page).toHaveURL(/.*dashboard/);

  // Save auth state for reuse
  await page.context().storageState({ path: authFile });
});
```

### Using Auth in Tests

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

### Tests Without Auth

```typescript
// e2e/tests/public.spec.ts
import { test } from '@playwright/test';

// Override to skip auth
test.use({ storageState: { cookies: [], origins: [] } });

test('homepage loads for anonymous users', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
});
```

---

## Writing Tests

### Basic Test Structure

```typescript
// e2e/tests/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Skip stored auth for login tests
    await page.context().clearCookies();
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');
    await loginPage.expectLoggedIn();
  });

  test('invalid credentials show error', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('wrong@example.com', 'wrongpass');
    await loginPage.expectError('Invalid email or password');
  });

  test('empty form shows validation errors', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.submitButton.click();

    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();
  });
});
```

### User Flow Tests

```typescript
// e2e/tests/checkout.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Checkout Flow', () => {
  test('complete purchase flow', async ({ page }) => {
    // 1. Browse products
    await page.goto('/products');
    await page.getByTestId('product-card')
      .filter({ hasText: 'Pro Plan' })
      .getByRole('button', { name: 'Add to cart' })
      .click();

    // 2. View cart
    await page.getByRole('link', { name: 'Cart' }).click();
    await expect(page.getByText('Pro Plan')).toBeVisible();
    await expect(page.getByTestId('cart-total')).toContainText('$29.99');

    // 3. Checkout
    await page.getByRole('button', { name: 'Checkout' }).click();

    // 4. Fill payment (use Stripe test card)
    const stripeFrame = page.frameLocator('iframe[name*="stripe"]');
    await stripeFrame.getByPlaceholder('Card number').fill('4242424242424242');
    await stripeFrame.getByPlaceholder('MM / YY').fill('12/30');
    await stripeFrame.getByPlaceholder('CVC').fill('123');

    // 5. Complete purchase
    await page.getByRole('button', { name: 'Pay now' }).click();

    // 6. Verify success
    await expect(page).toHaveURL(/.*success/);
    await expect(page.getByRole('heading', { name: 'Thank you' })).toBeVisible();
  });
});
```

---

## Assertions

### Web-First Assertions (Auto-Wait)

```typescript
// ✅ These wait and retry automatically
await expect(page.getByRole('button')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByRole('button')).toHaveText('Submit');
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveTitle(/Dashboard/);

// ❌ Avoid manual waits
await page.waitForTimeout(3000);  // NEVER do this
```

### Soft Assertions

```typescript
// Continue test even if assertion fails
await expect.soft(page.getByTestId('price')).toHaveText('$29.99');
await expect.soft(page.getByTestId('stock')).toHaveText('In Stock');

// Fail at end if any soft assertions failed
```

### Common Assertions

```typescript
// Visibility
await expect(locator).toBeVisible();
await expect(locator).toBeHidden();
await expect(locator).toBeAttached();

// Text content
await expect(locator).toHaveText('exact text');
await expect(locator).toContainText('partial');
await expect(locator).toHaveValue('input value');

// State
await expect(locator).toBeEnabled();
await expect(locator).toBeDisabled();
await expect(locator).toBeChecked();
await expect(locator).toBeFocused();

// Count
await expect(locator).toHaveCount(5);

// Page
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveTitle('Dashboard | App');
await expect(page).toHaveScreenshot('dashboard.png');
```

---

## Mocking & Network

### Mock API Responses

```typescript
test('shows error when API fails', async ({ page }) => {
  // Mock API to return error
  await page.route('**/api/users', (route) => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    });
  });

  await page.goto('/users');
  await expect(page.getByText('Failed to load users')).toBeVisible();
});

test('displays user data from API', async ({ page }) => {
  // Mock successful response
  await page.route('**/api/users', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'John Doe', email: 'john@example.com' },
        { id: 2, name: 'Jane Doe', email: 'jane@example.com' },
      ]),
    });
  });

  await page.goto('/users');
  await expect(page.getByText('John Doe')).toBeVisible();
  await expect(page.getByText('Jane Doe')).toBeVisible();
});
```

### Wait for API Calls

```typescript
test('submits form and shows success', async ({ page }) => {
  await page.goto('/contact');

  // Fill form
  await page.getByLabel('Name').fill('John');
  await page.getByLabel('Email').fill('john@example.com');
  await page.getByLabel('Message').fill('Hello!');

  // Wait for API call on submit
  const responsePromise = page.waitForResponse('**/api/contact');
  await page.getByRole('button', { name: 'Send' }).click();

  const response = await responsePromise;
  expect(response.status()).toBe(200);

  await expect(page.getByText('Message sent!')).toBeVisible();
});
```

---

## Visual Testing

```typescript
// Full page screenshot
await expect(page).toHaveScreenshot('homepage.png');

// Element screenshot
await expect(page.getByTestId('chart')).toHaveScreenshot('chart.png');

// With options
await expect(page).toHaveScreenshot('dashboard.png', {
  maxDiffPixels: 100,
  mask: [page.getByTestId('timestamp')], // Ignore dynamic content
});
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests
        run: npx playwright test --project=chromium
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

### Run Specific Tests

```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test e2e/tests/auth.spec.ts

# Run tests with tag
npx playwright test --grep @critical

# Run in headed mode (debug)
npx playwright test --headed

# Run specific browser
npx playwright test --project=chromium

# Debug mode
npx playwright test --debug

# Show HTML report
npx playwright show-report
```

---

## Test Data

### Factories

```typescript
// e2e/utils/test-data.ts
import { faker } from '@faker-js/faker';

export const createUser = (overrides = {}) => ({
  email: faker.internet.email(),
  password: faker.internet.password({ length: 12 }),
  name: faker.person.fullName(),
  ...overrides,
});

export const createProduct = (overrides = {}) => ({
  name: faker.commerce.productName(),
  price: faker.commerce.price({ min: 10, max: 100 }),
  description: faker.commerce.productDescription(),
  ...overrides,
});
```

### Environment Variables

```bash
# .env.test
BASE_URL=http://localhost:3000
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=testpassword123
```

---

## Debugging

### Trace Viewer

```typescript
// Enable in config for failures
use: {
  trace: 'on-first-retry',
}

// View traces
npx playwright show-trace trace.zip
```

### Debug Mode

```bash
# Step through test
npx playwright test --debug

# Pause at specific point
await page.pause();  // In test code
```

### VS Code Extension

Install "Playwright Test for VS Code" for:
- Run tests from editor
- Debug with breakpoints
- Pick locators visually
- Watch mode

---

## Dead Link Detection (REQUIRED)

**Every project MUST include dead link detection tests.** Run these on every deployment.

### Link Validator Test

```typescript
// e2e/tests/links.spec.ts
import { test, expect } from '@playwright/test';

const PAGES_TO_CHECK = ['/', '/about', '/pricing', '/blog', '/contact'];

test.describe('Dead Link Detection', () => {
  for (const pagePath of PAGES_TO_CHECK) {
    test(`no dead links on ${pagePath}`, async ({ page, request }) => {
      await page.goto(pagePath);

      // Get all links on the page
      const links = await page.locator('a[href]').all();
      const hrefs = await Promise.all(
        links.map(link => link.getAttribute('href'))
      );

      // Filter to internal and absolute external links
      const uniqueLinks = [...new Set(hrefs.filter(Boolean))] as string[];

      for (const href of uniqueLinks) {
        // Skip mailto, tel, and anchor links
        if (href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('#')) {
          continue;
        }

        // Build full URL
        const url = href.startsWith('http') ? href : new URL(href, page.url()).href;

        // Check link status
        const response = await request.get(url, {
          timeout: 10000,
          ignoreHTTPSErrors: true,
        });

        expect(
          response.ok(),
          `Dead link found on ${pagePath}: ${href} returned ${response.status()}`
        ).toBeTruthy();
      }
    });
  }
});
```

### Comprehensive Link Crawler

```typescript
// e2e/tests/site-links.spec.ts
import { test, expect, Page, APIRequestContext } from '@playwright/test';

interface LinkResult {
  url: string;
  status: number;
  foundOn: string;
}

async function checkAllLinks(
  page: Page,
  request: APIRequestContext,
  startUrl: string
): Promise<LinkResult[]> {
  const visited = new Set<string>();
  const results: LinkResult[] = [];
  const toVisit = [startUrl];
  const baseUrl = new URL(startUrl).origin;

  while (toVisit.length > 0) {
    const currentUrl = toVisit.pop()!;
    if (visited.has(currentUrl)) continue;
    visited.add(currentUrl);

    try {
      await page.goto(currentUrl);
      const links = await page.locator('a[href]').all();

      for (const link of links) {
        const href = await link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
          continue;
        }

        const fullUrl = href.startsWith('http') ? href : new URL(href, currentUrl).href;

        // Check link
        const response = await request.get(fullUrl, {
          timeout: 10000,
          ignoreHTTPSErrors: true,
        });

        results.push({
          url: fullUrl,
          status: response.status(),
          foundOn: currentUrl,
        });

        // Add internal links to queue
        if (fullUrl.startsWith(baseUrl) && !visited.has(fullUrl)) {
          toVisit.push(fullUrl);
        }
      }
    } catch (error) {
      results.push({
        url: currentUrl,
        status: 0,
        foundOn: 'navigation',
      });
    }
  }

  return results;
}

test('no dead links on entire site', async ({ page, request, baseURL }) => {
  const results = await checkAllLinks(page, request, baseURL!);
  const deadLinks = results.filter(r => r.status >= 400 || r.status === 0);

  if (deadLinks.length > 0) {
    console.error('Dead links found:');
    deadLinks.forEach(link => {
      console.error(`  ${link.url} (${link.status}) - found on ${link.foundOn}`);
    });
  }

  expect(deadLinks, `Found ${deadLinks.length} dead links`).toHaveLength(0);
});
```

### Image Link Validation

```typescript
// e2e/tests/images.spec.ts
import { test, expect } from '@playwright/test';

test('no broken images on homepage', async ({ page, request }) => {
  await page.goto('/');

  const images = await page.locator('img[src]').all();

  for (const img of images) {
    const src = await img.getAttribute('src');
    if (!src) continue;

    const url = src.startsWith('http') ? src : new URL(src, page.url()).href;

    // Skip data URLs
    if (url.startsWith('data:')) continue;

    const response = await request.get(url);
    expect(
      response.ok(),
      `Broken image: ${src}`
    ).toBeTruthy();

    // Verify it's actually an image
    const contentType = response.headers()['content-type'];
    expect(
      contentType?.startsWith('image/'),
      `${src} is not an image (${contentType})`
    ).toBeTruthy();
  }
});
```

### CI Integration for Link Checking

```yaml
# .github/workflows/link-check.yml
name: Link Check

on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Monday
  push:
    branches: [main]

jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install chromium
      - run: npx playwright test e2e/tests/links.spec.ts --project=chromium
        env:
          BASE_URL: ${{ secrets.PRODUCTION_URL }}
```

---

## Anti-Patterns

- **Hardcoded waits** - Use auto-waiting assertions instead
- **CSS/XPath selectors** - Use role/text/testid locators
- **Testing third-party sites** - Mock external dependencies
- **Shared state between tests** - Each test must be isolated
- **Missing awaits** - Use ESLint rule `no-floating-promises`
- **Flaky time-based tests** - Mock dates/times
- **Testing implementation details** - Test user-visible behavior
- **Huge test files** - Split by feature/page

---

## Quick Reference

```bash
# Install
npm init playwright@latest

# Run tests
npx playwright test
npx playwright test --headed
npx playwright test --project=chromium
npx playwright test --grep @smoke

# Debug
npx playwright test --debug
npx playwright show-report
npx playwright show-trace trace.zip

# Generate tests
npx playwright codegen localhost:3000
```

### Package.json Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:report": "playwright show-report",
    "test:e2e:codegen": "playwright codegen"
  }
}
```
