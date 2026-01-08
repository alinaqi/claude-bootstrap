---
name: ai-models
description: Latest AI models reference - Claude, OpenAI, Gemini, Eleven Labs, Replicate
---

# AI Models Reference Skill

*Load with: base.md + llm-patterns.md*

**Last Updated: December 2025**

## Philosophy

**Use the right model for the job.** Bigger isn't always better - match model capabilities to task requirements. Consider cost, latency, and accuracy tradeoffs.

## Model Selection Matrix

| Task | Recommended | Why |
|------|-------------|-----|
| Complex reasoning | Claude Opus 4.5, o3, Gemini 3 Pro | Highest accuracy |
| Fast chat/completion | Claude Haiku, GPT-4.1 mini, Gemini Flash | Low latency, cheap |
| Code generation | Claude Sonnet 4.5, Codestral, GPT-4.1 | Strong coding |
| Vision/images | Claude Sonnet, GPT-4o, Gemini 3 Pro | Multimodal |
| Embeddings | text-embedding-3-small, Voyage | Cost-effective |
| Voice synthesis | Eleven Labs v3, OpenAI TTS | Natural sounding |
| Image generation | FLUX.2, DALL-E 3, SD 3.5 | Different styles |

---

## Anthropic (Claude)

### Documentation
- **API Docs**: https://docs.anthropic.com
- **Models Overview**: https://docs.anthropic.com/en/docs/about-claude/models/overview
- **Pricing**: https://www.anthropic.com/pricing

### Latest Models (December 2025)

```typescript
const CLAUDE_MODELS = {
  // Flagship - highest capability
  opus: 'claude-opus-4-5-20251101',

  // Balanced - best for most tasks
  sonnet: 'claude-sonnet-4-5-20250929',

  // Previous generation (still excellent)
  opus4: 'claude-opus-4-20250514',
  sonnet4: 'claude-sonnet-4-20250514',

  // Fast & cheap - high volume tasks
  haiku: 'claude-haiku-3-5-20241022',
} as const;
```

### Usage
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const response = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' }
  ],
});
```

### Model Selection
```
claude-opus-4-5-20251101 (Opus 4.5)
├── Best for: Complex analysis, research, nuanced writing
├── Context: 200K tokens
├── Cost: $5/$25 per 1M tokens (input/output)
└── Use when: Accuracy matters most

claude-sonnet-4-5-20250929 (Sonnet 4.5)
├── Best for: Code, general tasks, balanced performance
├── Context: 200K tokens
├── Cost: $3/$15 per 1M tokens
└── Use when: Default choice for most applications

claude-haiku-3-5-20241022 (Haiku 3.5)
├── Best for: Classification, extraction, high-volume
├── Context: 200K tokens
├── Cost: $0.25/$1.25 per 1M tokens
└── Use when: Speed and cost matter most
```

---

## OpenAI

### Documentation
- **API Docs**: https://platform.openai.com/docs
- **Models**: https://platform.openai.com/docs/models
- **Pricing**: https://openai.com/pricing

### Latest Models (December 2025)

```typescript
const OPENAI_MODELS = {
  // GPT-5 series (latest)
  gpt5: 'gpt-5.2',
  gpt5Mini: 'gpt-5-mini',

  // GPT-4.1 series (recommended for most)
  gpt41: 'gpt-4.1',
  gpt41Mini: 'gpt-4.1-mini',
  gpt41Nano: 'gpt-4.1-nano',

  // Reasoning models (o-series)
  o3: 'o3',
  o3Pro: 'o3-pro',
  o4Mini: 'o4-mini',

  // Legacy but still useful
  gpt4o: 'gpt-4o',           // Still has audio support
  gpt4oMini: 'gpt-4o-mini',

  // Embeddings
  embeddingSmall: 'text-embedding-3-small',
  embeddingLarge: 'text-embedding-3-large',

  // Image generation
  dalle3: 'dall-e-3',
  gptImage: 'gpt-image-1',

  // Audio
  tts: 'tts-1',
  ttsHd: 'tts-1-hd',
  whisper: 'whisper-1',
} as const;
```

### Usage
```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Chat completion
const response = await openai.chat.completions.create({
  model: 'gpt-4.1',
  messages: [
    { role: 'user', content: 'Hello!' }
  ],
});

// With vision
const visionResponse = await openai.chat.completions.create({
  model: 'gpt-4.1',
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'What is in this image?' },
        { type: 'image_url', image_url: { url: 'https://...' } },
      ],
    },
  ],
});

// Embeddings
const embedding = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: 'Your text here',
});
```

### Model Selection
```
o3 / o3-pro
├── Best for: Math, coding, complex multi-step reasoning
├── Context: 200K tokens
├── Cost: Premium pricing
└── Use when: Hardest problems, need chain-of-thought

gpt-4.1
├── Best for: General tasks, coding, instruction following
├── Context: 1M tokens (!)
├── Cost: Lower than GPT-4o
└── Use when: Default choice, replaces GPT-4o

gpt-4.1-mini / gpt-4.1-nano
├── Best for: High-volume, cost-sensitive
├── Context: 1M tokens
├── Cost: Very low
└── Use when: Simple tasks at scale

o4-mini
├── Best for: Fast reasoning at low cost
├── Context: 200K tokens
├── Cost: Budget reasoning
└── Use when: Need reasoning but cost-conscious
```

---

## Google (Gemini)

### Documentation
- **API Docs**: https://ai.google.dev/docs
- **Models**: https://ai.google.dev/gemini-api/docs/models/gemini
- **Pricing**: https://ai.google.dev/pricing

### Latest Models (December 2025)

```typescript
const GEMINI_MODELS = {
  // Gemini 3 (Latest)
  gemini3Pro: 'gemini-3-pro-preview',
  gemini3ProImage: 'gemini-3-pro-image-preview',
  gemini3Flash: 'gemini-3-flash-preview',

  // Gemini 2.5 (Stable)
  gemini25Pro: 'gemini-2.5-pro',
  gemini25Flash: 'gemini-2.5-flash',
  gemini25FlashLite: 'gemini-2.5-flash-lite',

  // Specialized
  gemini25FlashTTS: 'gemini-2.5-flash-preview-tts',
  gemini25FlashAudio: 'gemini-2.5-flash-native-audio-preview-12-2025',

  // Previous generation
  gemini2Flash: 'gemini-2.0-flash',
} as const;
```

### Usage
```typescript
import { GoogleGenerativeAI } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

const result = await model.generateContent('Hello!');
const response = result.response.text();

// With vision
const visionModel = genAI.getGenerativeModel({ model: 'gemini-2.5-pro' });
const imagePart = {
  inlineData: {
    data: base64Image,
    mimeType: 'image/jpeg',
  },
};
const result = await visionModel.generateContent(['Describe this:', imagePart]);
```

### Model Selection
```
gemini-3-pro-preview
├── Best for: "Best model in the world for multimodal"
├── Context: 2M tokens
├── Cost: Premium
└── Use when: Need absolute best quality

gemini-2.5-pro
├── Best for: State-of-the-art thinking, complex tasks
├── Context: 2M tokens
├── Cost: $1.25/$5 per 1M tokens
└── Use when: Long context, complex reasoning

gemini-2.5-flash
├── Best for: Fast, balanced performance
├── Context: 1M tokens
├── Cost: $0.075/$0.30 per 1M tokens
└── Use when: Speed and cost matter

gemini-2.5-flash-lite
├── Best for: Ultra-fast, lowest cost
├── Context: 1M tokens
├── Cost: $0.04/$0.15 per 1M tokens
└── Use when: High volume, simple tasks
```

---

## Eleven Labs (Voice)

### Documentation
- **API Docs**: https://elevenlabs.io/docs
- **Models**: https://elevenlabs.io/docs/models
- **Pricing**: https://elevenlabs.io/pricing

### Latest Models (December 2025)

```typescript
const ELEVENLABS_MODELS = {
  // Latest - highest quality (alpha)
  v3: 'eleven_v3',

  // Production ready
  multilingualV2: 'eleven_multilingual_v2',
  turboV2_5: 'eleven_turbo_v2_5',

  // Ultra-low latency
  flashV2_5: 'eleven_flash_v2_5',
  flashV2: 'eleven_flash_v2', // English only
} as const;
```

### Usage
```typescript
import { ElevenLabsClient } from 'elevenlabs';

const elevenlabs = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY,
});

// Text to speech
const audio = await elevenlabs.textToSpeech.convert('voice-id', {
  text: 'Hello, world!',
  model_id: 'eleven_turbo_v2_5',
  voice_settings: {
    stability: 0.5,
    similarity_boost: 0.75,
  },
});

// Stream audio (for real-time)
const audioStream = await elevenlabs.textToSpeech.convertAsStream('voice-id', {
  text: 'Streaming audio...',
  model_id: 'eleven_flash_v2_5',
});
```

### Model Selection
```
eleven_v3 (Alpha)
├── Best for: Highest quality, emotional range
├── Latency: ~1s+ (not for real-time)
├── Languages: 74
└── Use when: Quality over speed, pre-rendered

eleven_turbo_v2_5
├── Best for: Balanced quality and speed
├── Latency: ~250-300ms
├── Languages: 32
└── Use when: Good quality with reasonable latency

eleven_flash_v2_5
├── Best for: Real-time, conversational AI
├── Latency: <75ms
├── Languages: 32
└── Use when: Live voice agents, chatbots
```

---

## Replicate

### Documentation
- **API Docs**: https://replicate.com/docs
- **Models**: https://replicate.com/explore
- **Pricing**: https://replicate.com/pricing

### Popular Models (December 2025)

```typescript
const REPLICATE_MODELS = {
  // FLUX.2 (Latest - November 2025)
  flux2Pro: 'black-forest-labs/flux-2-pro',
  flux2Flex: 'black-forest-labs/flux-2-flex',
  flux2Dev: 'black-forest-labs/flux-2-dev',

  // FLUX.1 (Still excellent)
  flux11Pro: 'black-forest-labs/flux-1.1-pro',
  fluxKontext: 'black-forest-labs/flux-kontext', // Image editing
  fluxSchnell: 'black-forest-labs/flux-schnell',

  // Video
  stableVideo4D: 'stability-ai/sv4d-2.0',

  // Audio
  musicgen: 'meta/musicgen',

  // LLMs (if needed outside main providers)
  llama: 'meta/llama-3.2-90b-vision',
} as const;
```

### Usage
```typescript
import Replicate from 'replicate';

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

// Image generation with FLUX.2
const output = await replicate.run('black-forest-labs/flux-2-pro', {
  input: {
    prompt: 'A serene mountain landscape at sunset',
    aspect_ratio: '16:9',
    output_format: 'webp',
  },
});

// Image editing with Kontext
const edited = await replicate.run('black-forest-labs/flux-kontext', {
  input: {
    image: 'https://...',
    prompt: 'Change the sky to sunset colors',
  },
});
```

### Model Selection
```
flux-2-pro
├── Best for: Highest quality, up to 4MP
├── Speed: ~6s
├── Cost: $0.015 + per megapixel
└── Use when: Professional quality needed

flux-2-flex
├── Best for: Fine details, typography
├── Speed: ~22s
├── Cost: $0.06 per megapixel
└── Use when: Need precise control

flux-2-dev (Open source)
├── Best for: Fast generation
├── Speed: ~2.5s
├── Cost: $0.012 per megapixel
└── Use when: Speed over quality

flux-kontext
├── Best for: Image editing with text
├── Speed: Variable
├── Cost: Per run
└── Use when: Edit existing images
```

---

## Stability AI

### Documentation
- **API Docs**: https://platform.stability.ai/docs/api-reference
- **Models**: https://stability.ai/stable-image
- **Pricing**: https://platform.stability.ai/pricing

### Latest Models (December 2025)

```typescript
const STABILITY_MODELS = {
  // Image generation
  sd35Large: 'sd3.5-large',
  sd35LargeTurbo: 'sd3.5-large-turbo',
  sd3Medium: 'sd3-medium',

  // Video
  sv4d: 'sv4d-2.0', // Stable Video 4D 2.0

  // Upscaling
  upscale: 'esrgan-v1-x2plus',
} as const;
```

### Usage
```typescript
const response = await fetch(
  'https://api.stability.ai/v2beta/stable-image/generate/sd3',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${process.env.STABILITY_API_KEY}`,
    },
    body: JSON.stringify({
      prompt: 'A futuristic city at night',
      output_format: 'webp',
      aspect_ratio: '16:9',
      model: 'sd3.5-large',
    }),
  }
);
```

---

## Mistral AI

### Documentation
- **API Docs**: https://docs.mistral.ai
- **Models**: https://docs.mistral.ai/getting-started/models
- **Pricing**: https://mistral.ai/technology/#pricing

### Latest Models (December 2025)

```typescript
const MISTRAL_MODELS = {
  // Flagship
  large: 'mistral-large-latest',  // Points to 2411

  // Medium tier
  medium: 'mistral-medium-2505',  // Medium 3

  // Small/Fast
  small: 'mistral-small-2506',    // Small 3.2

  // Code specialized
  codestral: 'codestral-2508',
  devstral: 'devstral-medium-2507',

  // Reasoning (Magistral)
  magistralMedium: 'magistral-medium-2507',
  magistralSmall: 'magistral-small-2507',

  // Audio
  voxtral: 'voxtral-small-2507',

  // OCR
  ocr: 'mistral-ocr-2505',
} as const;
```

### Usage
```typescript
import MistralClient from '@mistralai/mistralai';

const client = new MistralClient(process.env.MISTRAL_API_KEY);

const response = await client.chat({
  model: 'mistral-large-latest',
  messages: [{ role: 'user', content: 'Hello!' }],
});

// Code completion with Codestral
const codeResponse = await client.chat({
  model: 'codestral-2508',
  messages: [{ role: 'user', content: 'Write a Python function to...' }],
});
```

### Model Selection
```
mistral-large-latest (123B params)
├── Best for: Complex reasoning, knowledge tasks
├── Context: 128K tokens
└── Use when: Need high capability

codestral-2508
├── Best for: Code generation, 80+ languages
├── Speed: 2.5x faster than predecessor
└── Use when: Code-focused tasks

magistral-medium-2507
├── Best for: Multi-step reasoning
├── Specialty: Transparent chain-of-thought
└── Use when: Need reasoning traces
```

---

## Voyage AI (Embeddings)

### Documentation
- **API Docs**: https://docs.voyageai.com
- **Models**: https://docs.voyageai.com/docs/embeddings
- **Pricing**: https://www.voyageai.com/pricing

### Latest Models (December 2025)

```typescript
const VOYAGE_MODELS = {
  // General purpose
  large2: 'voyage-large-2',
  large2Instruct: 'voyage-large-2-instruct',

  // Code specialized
  code2: 'voyage-code-2',
  code3: 'voyage-code-3',

  // Multilingual
  multilingual2: 'voyage-multilingual-2',

  // Domain specific
  law2: 'voyage-law-2',
  finance2: 'voyage-finance-2',
} as const;
```

### Usage
```typescript
const response = await fetch('https://api.voyageai.com/v1/embeddings', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.VOYAGE_API_KEY}`,
  },
  body: JSON.stringify({
    model: 'voyage-code-3',
    input: ['Your code to embed'],
  }),
});

const { data } = await response.json();
const embedding = data[0].embedding;
```

---

## Quick Reference

### Cost Comparison (per 1M tokens, approx.)

| Provider | Cheap | Mid | Premium |
|----------|-------|-----|---------|
| Anthropic | $0.25 (Haiku) | $3 (Sonnet 4.5) | $5 (Opus 4.5) |
| OpenAI | $0.15 (4.1-nano) | $2 (4.1) | $15+ (o3) |
| Google | $0.04 (Flash-lite) | $0.08 (Flash) | $1.25 (Pro) |
| Mistral | $0.25 (Small) | $2.70 (Medium) | $8 (Large) |

### Best For Each Task

```
Reasoning/Analysis    → Claude Opus 4.5, o3, Gemini 3 Pro
Code Generation       → Claude Sonnet 4.5, Codestral 2508, GPT-4.1
Fast Responses        → Claude Haiku, GPT-4.1-mini, Gemini Flash
Long Context          → Gemini 2.5 Pro (2M), GPT-4.1 (1M), Claude (200K)
Vision                → GPT-4.1, Claude Sonnet, Gemini 3 Pro
Embeddings            → Voyage code-3, text-embedding-3-small
Voice Synthesis       → Eleven Labs v3/flash, OpenAI TTS
Image Generation      → FLUX.2 Pro, DALL-E 3, SD 3.5
Video Generation      → Stable Video 4D 2.0, Runway
Image Editing         → FLUX Kontext, gpt-image-1
```

### Environment Variables Template
```bash
# .env.example (NEVER commit actual keys)

# LLMs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
MISTRAL_API_KEY=...

# Media
ELEVENLABS_API_KEY=...
REPLICATE_API_TOKEN=r8_...
STABILITY_API_KEY=sk-...

# Embeddings
VOYAGE_API_KEY=pa-...
```

### Model Update Checklist
```
When models update:
□ Check official changelog/blog
□ Update model ID strings
□ Test with existing prompts
□ Compare output quality
□ Check pricing changes
□ Update context limits if changed
```

---

## Sources

- [Anthropic Models](https://docs.anthropic.com/en/docs/about-claude/models/overview)
- [OpenAI Models](https://platform.openai.com/docs/models)
- [OpenAI o3 Announcement](https://openai.com/index/introducing-o3-and-o4-mini/)
- [GPT-4.1 Announcement](https://openai.com/index/gpt-4-1/)
- [Google Gemini Models](https://ai.google.dev/gemini-api/docs/models/gemini)
- [Eleven Labs Models](https://elevenlabs.io/docs/models)
- [Replicate FLUX.2](https://replicate.com/blog/run-flux-2-on-replicate)
- [Mistral Models](https://docs.mistral.ai/getting-started/models)
- [Voyage AI](https://docs.voyageai.com)
