---
name: llm-patterns
description: AI-first application patterns, LLM testing, prompt management
---

# LLM Patterns Skill

*Load with: base.md + [language].md*

For AI-first applications where LLMs handle logical operations.

---

## Core Principle

**LLM for logic, code for plumbing.**

Use LLMs for:
- Classification, extraction, summarization
- Decision-making with natural language reasoning
- Content generation and transformation
- Complex conditional logic that would be brittle in code

Use traditional code for:
- Data validation (Zod/Pydantic)
- API routing and HTTP handling
- Database operations
- Authentication/authorization
- Orchestration and error handling

---

## Project Structure

```
project/
├── src/
│   ├── core/
│   │   ├── prompts/           # Prompt templates
│   │   │   ├── classify.ts
│   │   │   └── extract.ts
│   │   ├── llm/               # LLM client and utilities
│   │   │   ├── client.ts      # LLM client wrapper
│   │   │   ├── schemas.ts     # Response schemas (Zod)
│   │   │   └── index.ts
│   │   └── services/          # Business logic using LLM
│   ├── infra/
│   └── ...
├── tests/
│   ├── unit/
│   ├── integration/
│   └── llm/                   # LLM-specific tests
│       ├── fixtures/          # Saved responses for deterministic tests
│       ├── evals/             # Evaluation test suites
│       └── mocks/             # Mock LLM responses
└── _project_specs/
    └── prompts/               # Prompt specifications
```

---

## LLM Client Pattern

### Typed LLM Wrapper
```typescript
// core/llm/client.ts
import Anthropic from '@anthropic-ai/sdk';
import { z } from 'zod';

const client = new Anthropic();

interface LLMCallOptions<T> {
  prompt: string;
  schema: z.ZodSchema<T>;
  model?: string;
  maxTokens?: number;
}

export async function llmCall<T>({
  prompt,
  schema,
  model = 'claude-sonnet-4-20250514',
  maxTokens = 1024,
}: LLMCallOptions<T>): Promise<T> {
  const response = await client.messages.create({
    model,
    max_tokens: maxTokens,
    messages: [{ role: 'user', content: prompt }],
  });

  const text = response.content[0].type === 'text'
    ? response.content[0].text
    : '';

  // Parse and validate response
  const parsed = JSON.parse(text);
  return schema.parse(parsed);
}
```

### Structured Outputs
```typescript
// core/llm/schemas.ts
import { z } from 'zod';

export const ClassificationSchema = z.object({
  category: z.enum(['support', 'sales', 'feedback', 'other']),
  confidence: z.number().min(0).max(1),
  reasoning: z.string(),
});

export type Classification = z.infer<typeof ClassificationSchema>;
```

---

## Prompt Patterns

### Template Functions
```typescript
// core/prompts/classify.ts
export function classifyTicketPrompt(ticket: string): string {
  return `Classify this support ticket into one of these categories:
- support: Technical issues or help requests
- sales: Pricing, plans, or purchase inquiries
- feedback: Suggestions or complaints
- other: Anything else

Respond with JSON:
{
  "category": "...",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}

Ticket:
${ticket}`;
}
```

### Prompt Versioning
```typescript
// core/prompts/index.ts
export const PROMPTS = {
  classify: {
    v1: classifyTicketPromptV1,
    v2: classifyTicketPromptV2,  // improved accuracy
    current: classifyTicketPromptV2,
  },
} as const;
```

---

## Testing LLM Calls

### 1. Unit Tests with Mocks (Fast, Deterministic)
```typescript
// tests/llm/mocks/classify.mock.ts
export const mockClassifyResponse = {
  category: 'support',
  confidence: 0.95,
  reasoning: 'User is asking for help with login',
};

// tests/unit/services/ticket.test.ts
import { classifyTicket } from '../../../src/core/services/ticket';
import { mockClassifyResponse } from '../../llm/mocks/classify.mock';

// Mock the LLM client
vi.mock('../../../src/core/llm/client', () => ({
  llmCall: vi.fn().mockResolvedValue(mockClassifyResponse),
}));

describe('classifyTicket', () => {
  it('returns classification for ticket', async () => {
    const result = await classifyTicket('I cannot log in');

    expect(result.category).toBe('support');
    expect(result.confidence).toBeGreaterThan(0.9);
  });
});
```

### 2. Fixture Tests (Deterministic, Tests Parsing)
```typescript
// tests/llm/fixtures/classify.fixtures.json
{
  "support_ticket": {
    "input": "I can't reset my password",
    "expected_category": "support",
    "raw_response": "{\"category\":\"support\",\"confidence\":0.98,\"reasoning\":\"Password reset is a support issue\"}"
  }
}

// tests/llm/classify.fixture.test.ts
import fixtures from './fixtures/classify.fixtures.json';
import { ClassificationSchema } from '../../src/core/llm/schemas';

describe('Classification Response Parsing', () => {
  Object.entries(fixtures).forEach(([name, fixture]) => {
    it(`parses ${name} correctly`, () => {
      const parsed = JSON.parse(fixture.raw_response);
      const result = ClassificationSchema.parse(parsed);

      expect(result.category).toBe(fixture.expected_category);
    });
  });
});
```

### 3. Evaluation Tests (Slow, Run in CI nightly)
```typescript
// tests/llm/evals/classify.eval.test.ts
import { classifyTicket } from '../../../src/core/services/ticket';

const TEST_CASES = [
  { input: 'How much does the pro plan cost?', expected: 'sales' },
  { input: 'The app crashes when I click save', expected: 'support' },
  { input: 'You should add dark mode', expected: 'feedback' },
  { input: 'What time is it in Tokyo?', expected: 'other' },
];

describe('Classification Accuracy (Eval)', () => {
  // Skip in regular CI, run nightly
  const runEvals = process.env.RUN_LLM_EVALS === 'true';

  it.skipIf(!runEvals)('achieves >90% accuracy on test set', async () => {
    let correct = 0;

    for (const testCase of TEST_CASES) {
      const result = await classifyTicket(testCase.input);
      if (result.category === testCase.expected) correct++;
    }

    const accuracy = correct / TEST_CASES.length;
    expect(accuracy).toBeGreaterThan(0.9);
  }, 60000); // 60s timeout for LLM calls
});
```

---

## GitHub Actions for LLM Tests

```yaml
# .github/workflows/quality.yml (add to existing)
jobs:
  quality:
    # ... existing steps ...

    - name: Run Tests (with LLM mocks)
      run: npm run test:coverage

  llm-evals:
    runs-on: ubuntu-latest
    # Run nightly or on-demand
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run LLM Evals
        run: npm run test:evals
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          RUN_LLM_EVALS: 'true'
```

---

## Cost & Performance Tracking

```typescript
// core/llm/client.ts - add tracking
interface LLMMetrics {
  model: string;
  inputTokens: number;
  outputTokens: number;
  latencyMs: number;
  cost: number;
}

export async function llmCallWithMetrics<T>(
  options: LLMCallOptions<T>
): Promise<{ result: T; metrics: LLMMetrics }> {
  const start = Date.now();

  const response = await client.messages.create({...});

  const metrics: LLMMetrics = {
    model: options.model,
    inputTokens: response.usage.input_tokens,
    outputTokens: response.usage.output_tokens,
    latencyMs: Date.now() - start,
    cost: calculateCost(response.usage, options.model),
  };

  // Log or send to monitoring
  console.log('[LLM]', metrics);

  return { result: parsed, metrics };
}
```

---

## LLM Anti-Patterns

- ❌ Hardcoded prompts in business logic - use prompt templates
- ❌ No schema validation on LLM responses - always use Zod
- ❌ Testing with live LLM calls in CI - use mocks for unit tests
- ❌ No cost tracking - monitor token usage
- ❌ Ignoring latency - LLM calls are slow, design for async
- ❌ No fallback for LLM failures - handle timeouts and errors
- ❌ Prompts without version control - track prompt changes
- ❌ No evaluation suite - measure accuracy over time
- ❌ Using LLM for deterministic logic - use code for validation, auth, math
- ❌ Giant monolithic prompts - compose smaller focused prompts
