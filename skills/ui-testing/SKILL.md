---
name: ui-testing
description: Visual testing - catch invisible buttons, broken layouts, contrast
---

# UI Verification Skill

*Load with: ui-web.md or ui-mobile.md*

## Purpose

Quick verification that generated UI meets accessibility standards. Run these checks after creating any new UI components.

---

## Pre-Flight Checklist

### Before Shipping ANY UI:

```markdown
## Visibility Check
- [ ] All buttons have visible background OR border
- [ ] No text is same color as its background
- [ ] All text meets 4.5:1 contrast ratio
- [ ] Ghost/text buttons have visible borders

## Touch/Click Targets
- [ ] All buttons are minimum 44px height
- [ ] Icon buttons are minimum 44x44px
- [ ] Adequate spacing between clickable elements

## States
- [ ] Hover states visible (web)
- [ ] Pressed states visible (mobile)
- [ ] Focus rings on keyboard navigation
- [ ] Disabled states visually distinct (opacity 0.5)
- [ ] Loading states show indicators

## Dark Mode (if applicable)
- [ ] Text readable on dark backgrounds
- [ ] Borders visible in dark mode
- [ ] No gray-400 text on dark backgrounds

## Responsive (web)
- [ ] No horizontal scroll on mobile (320px)
- [ ] Content readable at all breakpoints
- [ ] Touch targets adequate on mobile
```

---

## Quick Contrast Check

### Use Browser DevTools
```
1. Right-click element → Inspect
2. In Styles panel, click on color value
3. Look for contrast ratio display
4. Must show ✓ for AA compliance (4.5:1 for text)
```

### Online Tools
- https://webaim.org/resources/contrastchecker/
- https://coolors.co/contrast-checker

### Tailwind Safe Combinations

```
LIGHT MODE (on white bg):
✓ text-gray-900  (#111827) = 16:1
✓ text-gray-800  (#1F2937) = 12:1
✓ text-gray-700  (#374151) = 9:1
✓ text-gray-600  (#4B5563) = 6:1
✗ text-gray-500  (#6B7280) = 4.6:1 (barely)
✗ text-gray-400  (#9CA3AF) = 2.6:1 (FAILS)

DARK MODE (on gray-900 bg):
✓ text-white     (#FFFFFF) = 16:1
✓ text-gray-100  (#F3F4F6) = 13:1
✓ text-gray-200  (#E5E7EB) = 11:1
✓ text-gray-300  (#D1D5DB) = 8:1
✗ text-gray-400  (#9CA3AF) = 5:1 (barely)
✗ text-gray-500  (#6B7280) = 3:1 (FAILS)
```

---

## Common Fixes

### Invisible Button
```tsx
// PROBLEM: No visible boundary
<button className="text-gray-500">Click</button>

// FIX: Add background OR border
<button className="bg-gray-100 text-gray-900 px-4 py-3 rounded-lg">
  Click
</button>
// OR
<button className="border border-gray-300 text-gray-700 px-4 py-3 rounded-lg">
  Click
</button>
```

### Low Contrast Text
```tsx
// PROBLEM: Light gray on white
<p className="text-gray-400">Secondary text</p>

// FIX: Use darker gray
<p className="text-gray-600">Secondary text</p>
```

### Missing Focus State
```tsx
// PROBLEM: Focus removed without replacement
<button className="outline-none">Submit</button>

// FIX: Add visible focus ring
<button className="outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">
  Submit
</button>
```

### Small Touch Target
```tsx
// PROBLEM: Too small for fingers
<button className="p-1 text-sm">×</button>

// FIX: Minimum 44px
<button className="w-11 h-11 flex items-center justify-center">×</button>
```

### Dark Mode Broken
```tsx
// PROBLEM: Same colors in both modes
<p className="text-gray-400">Text</p>

// FIX: Adjust for dark mode
<p className="text-gray-600 dark:text-gray-300">Text</p>
```

---

## Automated Checks (Optional)

### ESLint Plugin
```bash
npm install -D eslint-plugin-jsx-a11y
```

```json
// .eslintrc
{
  "extends": ["plugin:jsx-a11y/recommended"]
}
```

### Playwright Quick Test
```typescript
// e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('no accessibility violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

---

## When to Use Full Testing

Add comprehensive visual testing (Playwright screenshots, Storybook) when:
- Building a component library
- Multiple developers on UI
- Frequent UI changes
- Design system enforcement needed

For solo projects or MVPs, the checklist above is sufficient.
