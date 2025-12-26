# UI Testing Skill

*Load with: base.md + (ui-web.md or ui-mobile.md)*

## Philosophy

**If you can't see it, users can't click it.** AI-generated UI often has invisible buttons, broken layouts, and missing styles on first pass. Test visually before shipping.

## Common AI-Generated UI Bugs

```
CATCH THESE BEFORE SHIPPING:
□ Invisible buttons (no background, text same as bg)
□ Text with no contrast (gray on gray)
□ Elements outside viewport
□ Overlapping elements
□ Missing hover/focus states
□ Broken dark mode colors
□ Z-index wars (modals behind content)
□ Flex/grid items not wrapping
□ Touch targets too small (<44px)
□ Missing loading states
```

---

## Visual Verification Checklist

### After Every UI Change
```markdown
## Visual QA Checklist

### Visibility
- [ ] All buttons have visible backgrounds OR borders
- [ ] All text has sufficient contrast (4.5:1 min)
- [ ] Interactive elements have distinct hover states
- [ ] Focus rings visible on keyboard navigation

### Layout
- [ ] Content fits within viewport (no horizontal scroll)
- [ ] Elements don't overlap unexpectedly
- [ ] Spacing is consistent (8px grid)
- [ ] Responsive: check 320px, 768px, 1280px widths

### States
- [ ] Loading states show spinners/skeletons
- [ ] Empty states have helpful messages
- [ ] Error states are visible and red
- [ ] Disabled states are visually distinct (opacity)

### Dark Mode
- [ ] Text is readable on dark backgrounds
- [ ] Borders are visible
- [ ] Images/icons adapt or have fallbacks

### Accessibility
- [ ] Touch targets are 44px minimum
- [ ] Interactive elements have labels
- [ ] Color is not the only indicator
```

---

## Component Testing (React)

### Setup
```bash
npm install -D @testing-library/react @testing-library/jest-dom vitest jsdom
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    globals: true,
  },
});
```

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
```

### Test Button Visibility
```typescript
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('is visible with proper contrast', () => {
    render(<Button>Click me</Button>);

    const button = screen.getByRole('button', { name: /click me/i });

    // Button exists and is visible
    expect(button).toBeInTheDocument();
    expect(button).toBeVisible();

    // Has accessible name
    expect(button).toHaveAccessibleName('Click me');
  });

  it('has visible focus state', () => {
    render(<Button>Submit</Button>);

    const button = screen.getByRole('button');
    button.focus();

    // Check focus is applied (via class or style)
    expect(button).toHaveFocus();
    // Visual focus indicator should exist
    expect(button).toHaveClass(/focus|ring/);
  });

  it('shows loading state', () => {
    render(<Button loading>Submit</Button>);

    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    // Loading indicator should be present
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('meets minimum touch target size', () => {
    render(<Button>Tap</Button>);

    const button = screen.getByRole('button');
    const styles = window.getComputedStyle(button);

    const height = parseFloat(styles.height) +
                   parseFloat(styles.paddingTop) +
                   parseFloat(styles.paddingBottom);

    expect(height).toBeGreaterThanOrEqual(44);
  });
});
```

### Test Card Visibility
```typescript
import { render, screen } from '@testing-library/react';
import { Card } from './Card';

describe('Card', () => {
  it('renders content visibly', () => {
    render(
      <Card>
        <h2>Title</h2>
        <p>Description</p>
      </Card>
    );

    expect(screen.getByText('Title')).toBeVisible();
    expect(screen.getByText('Description')).toBeVisible();
  });

  it('has visible border or shadow', () => {
    const { container } = render(<Card>Content</Card>);
    const card = container.firstChild as HTMLElement;
    const styles = window.getComputedStyle(card);

    // Card should have visual boundary
    const hasBorder = styles.borderWidth !== '0px';
    const hasShadow = styles.boxShadow !== 'none';
    const hasBg = styles.backgroundColor !== 'transparent';

    expect(hasBorder || hasShadow || hasBg).toBe(true);
  });
});
```

### Test Form Inputs
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TextField } from './TextField';

describe('TextField', () => {
  it('shows label visibly', () => {
    render(<TextField label="Email" />);

    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByText('Email')).toBeVisible();
  });

  it('shows error state visibly', () => {
    render(<TextField label="Email" error="Invalid email" />);

    const input = screen.getByLabelText('Email');
    const error = screen.getByText('Invalid email');

    expect(error).toBeVisible();
    expect(input).toHaveAttribute('aria-invalid', 'true');
  });

  it('has visible focus state', async () => {
    const user = userEvent.setup();
    render(<TextField label="Name" />);

    const input = screen.getByLabelText('Name');
    await user.click(input);

    expect(input).toHaveFocus();
    // Should have visual focus indicator
  });

  it('placeholder is visible but lighter', () => {
    render(<TextField label="Search" placeholder="Type to search..." />);

    const input = screen.getByPlaceholderText('Type to search...');
    expect(input).toBeVisible();
  });
});
```

---

## Visual Regression Testing

### Playwright Screenshots
```bash
npm install -D @playwright/test
npx playwright install
```

```typescript
// e2e/visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage matches snapshot', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png');
  });

  test('buttons are visible', async ({ page }) => {
    await page.goto('/');

    // Check all buttons have visible boundaries
    const buttons = page.locator('button');
    const count = await buttons.count();

    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      await expect(button).toBeVisible();

      // Verify button has content
      const text = await button.textContent();
      const hasIcon = await button.locator('svg').count() > 0;
      expect(text?.trim() || hasIcon).toBeTruthy();
    }
  });

  test('no horizontal overflow', async ({ page }) => {
    await page.goto('/');

    const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
    const viewportWidth = await page.evaluate(() => window.innerWidth);

    expect(bodyWidth).toBeLessThanOrEqual(viewportWidth);
  });

  test('dark mode renders correctly', async ({ page }) => {
    await page.goto('/');
    await page.emulateMedia({ colorScheme: 'dark' });

    await expect(page).toHaveScreenshot('homepage-dark.png');
  });

  test.describe('responsive', () => {
    const viewports = [
      { width: 320, height: 568, name: 'mobile' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 1280, height: 800, name: 'desktop' },
    ];

    for (const vp of viewports) {
      test(`renders at ${vp.name}`, async ({ page }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto('/');
        await expect(page).toHaveScreenshot(`homepage-${vp.name}.png`);
      });
    }
  });
});
```

### Playwright Config
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  snapshotDir: './e2e/snapshots',
  updateSnapshots: 'missing',
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.05, // 5% tolerance
    },
  },
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: true,
  },
});
```

---

## Storybook for Component Isolation

### Setup
```bash
npx storybook@latest init
```

### Component Story
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'ghost'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

// Default state - MUST be visible
export const Primary: Story = {
  args: {
    children: 'Click me',
    variant: 'primary',
  },
};

// All variants for visual comparison
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  ),
};

// States
export const States: Story = {
  render: () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <Button>Default</Button>
      <Button disabled>Disabled</Button>
      <Button loading>Loading</Button>
    </div>
  ),
};

// Dark mode
export const DarkMode: Story = {
  parameters: {
    backgrounds: { default: 'dark' },
  },
  render: () => (
    <div className="dark" style={{ padding: '2rem' }}>
      <Button variant="primary">Dark Mode</Button>
    </div>
  ),
};
```

### Visual Testing with Chromatic
```bash
npm install -D chromatic
npx chromatic --project-token=<token>
```

---

## Accessibility Testing

### axe-core Integration
```bash
npm install -D @axe-core/react axe-core
```

```typescript
// src/test/axe-setup.ts
import { configureAxe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

export const axe = configureAxe({
  rules: {
    // Require visible focus indicators
    'focus-indicator': { enabled: true },
    // Color contrast
    'color-contrast': { enabled: true },
  },
});
```

```typescript
// Component.test.tsx
import { render } from '@testing-library/react';
import { axe } from './axe-setup';
import { Button } from './Button';

describe('Button accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Playwright Accessibility
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('page has no accessibility violations', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

---

## Mobile Testing (React Native)

### Detox E2E
```bash
npm install -D detox
```

```typescript
// e2e/visual.test.ts
describe('Visual Tests', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('buttons are visible and tappable', async () => {
    await expect(element(by.id('primary-button'))).toBeVisible();
    await element(by.id('primary-button')).tap();
  });

  it('takes screenshot for comparison', async () => {
    await device.takeScreenshot('home-screen');
  });
});
```

### React Native Testing Library
```typescript
import { render, screen } from '@testing-library/react-native';
import { Button } from './Button';

describe('Button', () => {
  it('renders with visible text', () => {
    render(<Button title="Submit" onPress={() => {}} />);

    expect(screen.getByText('Submit')).toBeVisible();
  });

  it('has accessible role', () => {
    render(<Button title="Submit" onPress={() => {}} />);

    expect(screen.getByRole('button')).toBeTruthy();
  });
});
```

---

## CI Integration

### GitHub Actions
```yaml
# .github/workflows/visual-tests.yml
name: Visual Tests

on: [push, pull_request]

jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run component tests
        run: npm test

      - name: Run visual tests
        run: npx playwright test

      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diff
          path: e2e/snapshots/
```

---

## Quick Verification Script

```typescript
// scripts/verify-ui.ts
/**
 * Quick UI verification - run after generating new components
 * npx tsx scripts/verify-ui.ts
 */

import { chromium } from 'playwright';

async function verifyUI() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('http://localhost:3000');

  const issues: string[] = [];

  // Check for invisible buttons
  const buttons = await page.locator('button').all();
  for (const button of buttons) {
    const box = await button.boundingBox();
    if (!box || box.width === 0 || box.height === 0) {
      issues.push(`Invisible button: ${await button.textContent()}`);
    }
    if (box && box.height < 44) {
      issues.push(`Small touch target: ${await button.textContent()} (${box.height}px)`);
    }
  }

  // Check for horizontal overflow
  const overflow = await page.evaluate(() => {
    return document.body.scrollWidth > window.innerWidth;
  });
  if (overflow) {
    issues.push('Page has horizontal overflow');
  }

  // Check for low contrast text (basic check)
  const lowContrast = await page.evaluate(() => {
    const elements = document.querySelectorAll('*');
    const issues: string[] = [];
    elements.forEach(el => {
      const style = window.getComputedStyle(el);
      const color = style.color;
      const bg = style.backgroundColor;
      // Very basic: flag if text is very light gray
      if (color.includes('rgb(200') || color.includes('rgb(210')) {
        issues.push(el.textContent?.slice(0, 30) || 'unknown');
      }
    });
    return issues;
  });

  if (lowContrast.length > 0) {
    issues.push(`Potential low contrast: ${lowContrast.join(', ')}`);
  }

  await browser.close();

  if (issues.length > 0) {
    console.log('❌ UI Issues Found:');
    issues.forEach(issue => console.log(`  - ${issue}`));
    process.exit(1);
  } else {
    console.log('✅ UI verification passed');
  }
}

verifyUI();
```

---

## Anti-Patterns

```
NEVER:
✗ Ship UI without viewing it in browser
✗ Use color as only indicator (red = error)
✗ Assume dark mode works without testing
✗ Skip focus state testing
✗ Ignore mobile viewport testing
✗ Trust AI-generated UI blindly

ALWAYS:
✓ View every new component in browser
✓ Test with keyboard navigation
✓ Check both light and dark mode
✓ Verify touch targets on mobile
✓ Run accessibility checks
✓ Take screenshots for regression
```
