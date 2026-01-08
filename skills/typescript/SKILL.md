---
name: typescript
description: TypeScript strict mode with eslint and jest
---

# TypeScript Skill

*Load with: base.md*

---

## Strict Mode (Non-Negotiable)

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

---

## Project Structure

```
project/
├── src/
│   ├── core/               # Pure business logic
│   │   ├── types.ts        # Domain types/interfaces
│   │   ├── services/       # Pure functions
│   │   └── index.ts        # Public API
│   ├── infra/              # Side effects
│   │   ├── api/            # HTTP handlers
│   │   ├── db/             # Database operations
│   │   └── external/       # Third-party integrations
│   └── utils/              # Shared utilities
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
├── tsconfig.json
└── CLAUDE.md
```

---

## Tooling (Required)

```json
// package.json scripts
{
  "scripts": {
    "lint": "eslint src/ --ext .ts,.tsx",
    "typecheck": "tsc --noEmit",
    "test": "jest",
    "test:coverage": "jest --coverage",
    "format": "prettier --write 'src/**/*.ts'"
  }
}
```

```javascript
// eslint.config.js
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/explicit-function-return-type': 'error',
      'max-lines-per-function': ['error', 20],
      'max-depth': ['error', 2],
      'max-params': ['error', 3],
    }
  }
);
```

---

## Testing with Jest

```typescript
// tests/unit/services/user.test.ts
import { calculateTotal } from '../../../src/core/services/pricing';

describe('calculateTotal', () => {
  it('returns sum of item prices', () => {
    // Arrange
    const items = [{ price: 10 }, { price: 20 }];

    // Act
    const result = calculateTotal(items);

    // Assert
    expect(result).toBe(30);
  });

  it('returns zero for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('throws on invalid item', () => {
    expect(() => calculateTotal([{ invalid: 'item' }])).toThrow();
  });
});
```

---

## GitHub Actions

```yaml
name: TypeScript Quality Gate

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Lint
        run: npm run lint
        
      - name: Type Check
        run: npm run typecheck
        
      - name: Test with Coverage
        run: npm run test:coverage
        
      - name: Coverage Threshold (80%)
        run: npm run test:coverage -- --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
```

---

## Pre-Commit Hooks

Using Husky + lint-staged:

```bash
npm install -D husky lint-staged
npx husky init
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
npx tsc --noEmit
npm run test -- --onlyChanged --passWithNoTests
```

This runs on every commit:
1. ESLint + Prettier on staged files
2. Type check entire project
3. Tests for changed files only

---

## Type Patterns

### Discriminated Unions for Results
```typescript
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

function parseUser(data: unknown): Result<User> {
  // Type-safe error handling without exceptions
}
```

### Branded Types for IDs
```typescript
type UserId = string & { readonly brand: unique symbol };
type OrderId = string & { readonly brand: unique symbol };

// Can't accidentally pass UserId where OrderId expected
function getOrder(orderId: OrderId): Order { ... }
```

### Const Assertions for Literals
```typescript
const STATUSES = ['pending', 'active', 'closed'] as const;
type Status = typeof STATUSES[number]; // 'pending' | 'active' | 'closed'
```

### Zod for Runtime Validation
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

type User = z.infer<typeof UserSchema>;
```

---

## TypeScript Anti-Patterns

- ❌ `any` type - use `unknown` and narrow
- ❌ Type assertions (`as`) - use type guards
- ❌ Non-null assertions (`!`) - handle null explicitly
- ❌ `@ts-ignore` without explanation
- ❌ Enums - use const objects or union types
- ❌ Classes for data - use interfaces/types
- ❌ Default exports - use named exports
