---
name: ms-teams-apps
description: Microsoft Teams bots and AI agents - Claude/OpenAI, Adaptive Cards, Graph API
---

# Microsoft Teams Apps Skill

*Load with: base.md*

**Purpose:** Build AI-powered agents and apps for Microsoft Teams. Create conversational bots, message extensions, and intelligent assistants that integrate with LLMs like OpenAI and Claude.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  TEAMS APP TYPES                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  1. AI AGENTS (Bots)                                            │
│     Conversational apps powered by LLMs                         │
│     Handle messages, commands, and actions                      │
│                                                                 │
│  2. MESSAGE EXTENSIONS                                          │
│     Search external systems, insert cards into messages         │
│     Action commands with modal dialogs                          │
│                                                                 │
│  3. TABS                                                        │
│     Embedded web applications inside Teams                      │
│     Personal, channel, or meeting tabs                          │
│                                                                 │
│  4. WEBHOOKS & CONNECTORS                                       │
│     Incoming: Post messages to channels                         │
│     Outgoing: Respond to @mentions                              │
├─────────────────────────────────────────────────────────────────┤
│  SDK LANDSCAPE (2025)                                           │
│  ─────────────────────────────────────────────────────────────  │
│  Teams SDK v2: Primary SDK for Teams-only apps                  │
│  M365 Agents SDK: Multi-channel (Teams, Outlook, Copilot)       │
│  Teams Toolkit: VS Code extension for development               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Install Teams CLI

```bash
npm install -g @microsoft/teams.cli
```

### Create New Project

```bash
# TypeScript (Recommended)
npx @microsoft/teams.cli new typescript my-agent --template echo

# Python
npx @microsoft/teams.cli new python my-agent --template echo

# C#
npx @microsoft/teams.cli new csharp my-agent --template echo
```

### Project Structure

```
my-agent/
├── src/
│   ├── index.ts              # Entry point
│   ├── app.ts                # App configuration
│   └── handlers/
│       ├── message.ts        # Message handlers
│       └── commands.ts       # Command handlers
├── appPackage/
│   ├── manifest.json         # App manifest
│   ├── color.png             # App icon (192x192)
│   └── outline.png           # Outline icon (32x32)
├── .env                      # Environment variables
├── teamsapp.yml              # Teams Toolkit config
└── package.json
```

---

## App Manifest

### Basic Manifest Structure

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.17/MicrosoftTeams.schema.json",
  "manifestVersion": "1.17",
  "version": "1.0.0",
  "id": "{{APP_ID}}",
  "developer": {
    "name": "Your Company",
    "websiteUrl": "https://yourcompany.com",
    "privacyUrl": "https://yourcompany.com/privacy",
    "termsOfUseUrl": "https://yourcompany.com/terms"
  },
  "name": {
    "short": "AI Assistant",
    "full": "AI Assistant for Teams"
  },
  "description": {
    "short": "Your AI-powered assistant",
    "full": "An intelligent assistant that helps you with tasks using AI."
  },
  "icons": {
    "color": "color.png",
    "outline": "outline.png"
  },
  "accentColor": "#5558AF",
  "bots": [
    {
      "botId": "{{BOT_ID}}",
      "scopes": ["personal", "team", "groupChat"],
      "supportsFiles": false,
      "isNotificationOnly": false,
      "commandLists": [
        {
          "scopes": ["personal", "team", "groupChat"],
          "commands": [
            {
              "title": "help",
              "description": "Show available commands"
            },
            {
              "title": "ask",
              "description": "Ask the AI a question"
            }
          ]
        }
      ]
    }
  ],
  "permissions": ["identity", "messageTeamMembers"],
  "validDomains": ["*.azurewebsites.net"]
}
```

### Manifest with Message Extensions

```json
{
  "composeExtensions": [
    {
      "botId": "{{BOT_ID}}",
      "commands": [
        {
          "id": "searchQuery",
          "type": "query",
          "title": "Search",
          "description": "Search for information",
          "initialRun": true,
          "parameters": [
            {
              "name": "query",
              "title": "Search query",
              "description": "Enter your search terms",
              "inputType": "text"
            }
          ]
        },
        {
          "id": "createTask",
          "type": "action",
          "title": "Create Task",
          "description": "Create a new task",
          "fetchTask": true,
          "context": ["compose", "commandBox", "message"]
        }
      ]
    }
  ]
}
```

---

## AI Agent Development

### Basic Bot with Teams SDK v2

```typescript
// src/app.ts
import { App, HttpPlugin, DevtoolsPlugin } from '@microsoft/teams.ai';
import { OpenAIModel, ActionPlanner, PromptManager } from '@microsoft/teams.ai';

// Configure the AI model
const model = new OpenAIModel({
  azureApiKey: process.env.AZURE_OPENAI_API_KEY!,
  azureDefaultDeployment: process.env.AZURE_OPENAI_DEPLOYMENT!,
  azureEndpoint: process.env.AZURE_OPENAI_ENDPOINT!,
  // Or use OpenAI directly:
  // apiKey: process.env.OPENAI_API_KEY!,
  // defaultModel: 'gpt-4'
});

// Configure prompts
const prompts = new PromptManager({
  promptsFolder: './src/prompts'
});

// Create action planner
const planner = new ActionPlanner({
  model,
  prompts,
  defaultPrompt: 'chat'
});

// Create the app
const app = new App({
  plugins: [
    new HttpPlugin(),
    new DevtoolsPlugin()
  ],
  ai: {
    planner
  }
});

// Handle messages
app.on('message', async (context, state) => {
  // AI automatically handles the conversation
  // The planner uses the 'chat' prompt to generate responses
});

// Handle specific commands
app.message('/help', async (context, state) => {
  await context.sendActivity({
    type: 'message',
    text: 'Available commands:\n- /help - Show this message\n- /ask [question] - Ask me anything'
  });
});

// Start the app
app.start();
```

### Prompt Configuration

```yaml
# src/prompts/chat/config.json
{
  "schema": 1.1,
  "description": "AI Assistant for Teams",
  "type": "completion",
  "completion": {
    "model": "gpt-4",
    "max_tokens": 1000,
    "temperature": 0.7,
    "top_p": 1
  }
}
```

```text
# src/prompts/chat/skprompt.txt
You are an AI assistant for Microsoft Teams. You help users with their questions and tasks.

Current conversation:
{{$history}}

User: {{$input}}
Assistant:
```

---

## Integrating Claude/Anthropic

### Claude-Powered Teams Bot

```typescript
// src/claude-bot.ts
import { App, HttpPlugin } from '@microsoft/teams.ai';
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY!
});

const app = new App({
  plugins: [new HttpPlugin()]
});

// Conversation history store
const conversations = new Map<string, Anthropic.MessageParam[]>();

app.on('message', async (context, state) => {
  const userId = context.activity.from.id;
  const userMessage = context.activity.text;

  // Get or initialize conversation history
  if (!conversations.has(userId)) {
    conversations.set(userId, []);
  }
  const history = conversations.get(userId)!;

  // Add user message to history
  history.push({ role: 'user', content: userMessage });

  // Show typing indicator
  await context.sendActivity({ type: 'typing' });

  try {
    // Call Claude API
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      system: `You are an AI assistant integrated into Microsoft Teams.
        Help users with their questions and tasks.
        Be concise and helpful. Use markdown formatting when appropriate.
        Current user: ${context.activity.from.name}`,
      messages: history
    });

    const assistantMessage = response.content[0].type === 'text'
      ? response.content[0].text
      : '';

    // Add assistant response to history
    history.push({ role: 'assistant', content: assistantMessage });

    // Keep history manageable (last 20 messages)
    if (history.length > 20) {
      history.splice(0, history.length - 20);
    }

    // Send response
    await context.sendActivity({
      type: 'message',
      text: assistantMessage
    });

  } catch (error) {
    console.error('Claude API error:', error);
    await context.sendActivity({
      type: 'message',
      text: 'Sorry, I encountered an error processing your request.'
    });
  }
});

// Clear conversation command
app.message('/clear', async (context, state) => {
  const userId = context.activity.from.id;
  conversations.delete(userId);
  await context.sendActivity('Conversation cleared. Starting fresh!');
});

app.start();
```

### Claude with Tools/Function Calling

```typescript
// src/claude-agent.ts
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

// Define tools the agent can use
const tools: Anthropic.Tool[] = [
  {
    name: 'search_knowledge_base',
    description: 'Search the company knowledge base for information',
    input_schema: {
      type: 'object' as const,
      properties: {
        query: {
          type: 'string',
          description: 'The search query'
        }
      },
      required: ['query']
    }
  },
  {
    name: 'create_task',
    description: 'Create a new task in the task management system',
    input_schema: {
      type: 'object' as const,
      properties: {
        title: { type: 'string', description: 'Task title' },
        description: { type: 'string', description: 'Task description' },
        assignee: { type: 'string', description: 'Person to assign the task to' },
        due_date: { type: 'string', description: 'Due date in YYYY-MM-DD format' }
      },
      required: ['title']
    }
  },
  {
    name: 'get_calendar',
    description: 'Get calendar events for a user',
    input_schema: {
      type: 'object' as const,
      properties: {
        user: { type: 'string', description: 'User email or name' },
        days: { type: 'number', description: 'Number of days to look ahead' }
      },
      required: ['user']
    }
  }
];

// Tool implementations
async function executeTools(toolName: string, toolInput: any): Promise<string> {
  switch (toolName) {
    case 'search_knowledge_base':
      // Implement your search logic
      return `Found 3 results for "${toolInput.query}":\n1. Document A\n2. Document B\n3. Document C`;

    case 'create_task':
      // Implement task creation (e.g., call Microsoft Graph API)
      return `Task created: "${toolInput.title}"`;

    case 'get_calendar':
      // Implement calendar lookup
      return `Calendar for ${toolInput.user}: 2 meetings today`;

    default:
      return 'Unknown tool';
  }
}

// Agent loop with tool use
async function runAgent(userMessage: string): Promise<string> {
  let messages: Anthropic.MessageParam[] = [
    { role: 'user', content: userMessage }
  ];

  while (true) {
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      system: 'You are a helpful Teams assistant. Use tools when needed to help users.',
      tools,
      messages
    });

    // Check if we need to use tools
    if (response.stop_reason === 'tool_use') {
      const toolResults: Anthropic.MessageParam[] = [];

      for (const content of response.content) {
        if (content.type === 'tool_use') {
          const result = await executeTools(content.name, content.input);
          toolResults.push({
            role: 'user',
            content: [{
              type: 'tool_result',
              tool_use_id: content.id,
              content: result
            }]
          });
        }
      }

      messages.push({ role: 'assistant', content: response.content });
      messages.push(...toolResults);
      continue;
    }

    // Return final text response
    const textContent = response.content.find(c => c.type === 'text');
    return textContent?.text || 'No response';
  }
}
```

---

## Adaptive Cards

### Basic Adaptive Card

```typescript
// src/cards/welcome-card.ts
import { CardFactory } from 'botbuilder';

export function createWelcomeCard(userName: string) {
  return CardFactory.adaptiveCard({
    type: 'AdaptiveCard',
    $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
    version: '1.5',
    body: [
      {
        type: 'TextBlock',
        text: `Welcome, ${userName}!`,
        size: 'Large',
        weight: 'Bolder'
      },
      {
        type: 'TextBlock',
        text: 'I\'m your AI assistant. How can I help you today?',
        wrap: true
      },
      {
        type: 'ActionSet',
        actions: [
          {
            type: 'Action.Submit',
            title: 'Get Started',
            data: { action: 'getStarted' }
          },
          {
            type: 'Action.Submit',
            title: 'View Help',
            data: { action: 'help' }
          }
        ]
      }
    ]
  });
}
```

### AI Response Card with Actions

```typescript
// src/cards/ai-response-card.ts
export function createAIResponseCard(
  question: string,
  answer: string,
  sources?: string[]
) {
  return {
    type: 'AdaptiveCard',
    $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
    version: '1.5',
    body: [
      {
        type: 'Container',
        style: 'emphasis',
        items: [
          {
            type: 'TextBlock',
            text: 'Your Question',
            size: 'Small',
            weight: 'Bolder'
          },
          {
            type: 'TextBlock',
            text: question,
            wrap: true
          }
        ]
      },
      {
        type: 'Container',
        items: [
          {
            type: 'TextBlock',
            text: 'AI Response',
            size: 'Small',
            weight: 'Bolder'
          },
          {
            type: 'TextBlock',
            text: answer,
            wrap: true
          }
        ]
      },
      ...(sources && sources.length > 0 ? [{
        type: 'Container',
        items: [
          {
            type: 'TextBlock',
            text: 'Sources',
            size: 'Small',
            weight: 'Bolder'
          },
          ...sources.map(source => ({
            type: 'TextBlock',
            text: `• ${source}`,
            size: 'Small'
          }))
        ]
      }] : [])
    ],
    actions: [
      {
        type: 'Action.Submit',
        title: '👍 Helpful',
        data: { action: 'feedback', value: 'positive' }
      },
      {
        type: 'Action.Submit',
        title: '👎 Not Helpful',
        data: { action: 'feedback', value: 'negative' }
      },
      {
        type: 'Action.Submit',
        title: 'Ask Follow-up',
        data: { action: 'followUp' }
      }
    ]
  };
}
```

### Form Card for User Input

```typescript
// src/cards/task-form-card.ts
export function createTaskFormCard() {
  return {
    type: 'AdaptiveCard',
    $schema: 'http://adaptivecards.io/schemas/adaptive-card.json',
    version: '1.5',
    body: [
      {
        type: 'TextBlock',
        text: 'Create New Task',
        size: 'Large',
        weight: 'Bolder'
      },
      {
        type: 'Input.Text',
        id: 'taskTitle',
        label: 'Task Title',
        isRequired: true,
        placeholder: 'Enter task title'
      },
      {
        type: 'Input.Text',
        id: 'taskDescription',
        label: 'Description',
        isMultiline: true,
        placeholder: 'Enter task description'
      },
      {
        type: 'Input.ChoiceSet',
        id: 'priority',
        label: 'Priority',
        choices: [
          { title: 'High', value: 'high' },
          { title: 'Medium', value: 'medium' },
          { title: 'Low', value: 'low' }
        ],
        value: 'medium'
      },
      {
        type: 'Input.Date',
        id: 'dueDate',
        label: 'Due Date'
      }
    ],
    actions: [
      {
        type: 'Action.Submit',
        title: 'Create Task',
        data: { action: 'createTask' }
      },
      {
        type: 'Action.Submit',
        title: 'Cancel',
        data: { action: 'cancel' }
      }
    ]
  };
}
```

---

## Microsoft Graph Integration

### Setup Graph Client

```typescript
// src/graph/client.ts
import { Client } from '@microsoft/microsoft-graph-client';
import { TokenCredentialAuthenticationProvider } from '@microsoft/microsoft-graph-client/authProviders/azureTokenCredentials';
import { ClientSecretCredential } from '@azure/identity';

export function createGraphClient() {
  const credential = new ClientSecretCredential(
    process.env.AZURE_TENANT_ID!,
    process.env.AZURE_CLIENT_ID!,
    process.env.AZURE_CLIENT_SECRET!
  );

  const authProvider = new TokenCredentialAuthenticationProvider(credential, {
    scopes: ['https://graph.microsoft.com/.default']
  });

  return Client.initWithMiddleware({ authProvider });
}
```

### Common Graph Operations

```typescript
// src/graph/operations.ts
import { Client } from '@microsoft/microsoft-graph-client';

export class GraphOperations {
  constructor(private client: Client) {}

  // Get user profile
  async getUserProfile(userId: string) {
    return this.client.api(`/users/${userId}`).get();
  }

  // Get user's calendar events
  async getCalendarEvents(userId: string, days: number = 7) {
    const startDate = new Date().toISOString();
    const endDate = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString();

    return this.client
      .api(`/users/${userId}/calendarView`)
      .query({
        startDateTime: startDate,
        endDateTime: endDate
      })
      .select('subject,start,end,location')
      .orderby('start/dateTime')
      .get();
  }

  // Send email
  async sendEmail(
    fromUserId: string,
    to: string,
    subject: string,
    body: string
  ) {
    return this.client.api(`/users/${fromUserId}/sendMail`).post({
      message: {
        subject,
        body: { contentType: 'HTML', content: body },
        toRecipients: [{ emailAddress: { address: to } }]
      }
    });
  }

  // Create Teams meeting
  async createMeeting(
    userId: string,
    subject: string,
    startTime: string,
    endTime: string,
    attendees: string[]
  ) {
    return this.client.api(`/users/${userId}/onlineMeetings`).post({
      subject,
      startDateTime: startTime,
      endDateTime: endTime,
      participants: {
        attendees: attendees.map(email => ({
          upn: email,
          role: 'attendee'
        }))
      }
    });
  }

  // Post message to channel
  async postToChannel(teamId: string, channelId: string, message: string) {
    return this.client
      .api(`/teams/${teamId}/channels/${channelId}/messages`)
      .post({
        body: { content: message }
      });
  }
}
```

---

## Authentication

### SSO with Teams SDK

```typescript
// src/auth.ts
import { App } from '@microsoft/teams.ai';

const app = new App({
  // ... other config
});

app.on('message', async ({ userGraph, isSignedIn, send, signin }) => {
  // Check if user is signed in
  if (!isSignedIn) {
    // Initiate sign-in flow
    await signin();
    return;
  }

  // User is signed in, access Graph API
  const me = await userGraph.call({
    method: 'GET',
    path: '/me'
  });

  await send(`Hello, ${me.displayName}!`);
});
```

### Manual OAuth Flow

```typescript
// src/auth/oauth.ts
import { OAuthPrompt, OAuthPromptSettings } from 'botbuilder-dialogs';

const oauthSettings: OAuthPromptSettings = {
  connectionName: process.env.OAUTH_CONNECTION_NAME!,
  text: 'Please sign in to continue',
  title: 'Sign In',
  timeout: 300000 // 5 minutes
};

// In your dialog
async function handleAuth(context, state) {
  const tokenResponse = await context.adapter.getUserToken(
    context,
    oauthSettings.connectionName
  );

  if (!tokenResponse?.token) {
    // No token, show sign-in card
    await context.sendActivity({
      attachments: [
        CardFactory.oauthCard(
          oauthSettings.connectionName,
          oauthSettings.title,
          oauthSettings.text
        )
      ]
    });
    return null;
  }

  return tokenResponse.token;
}
```

---

## RAG (Retrieval-Augmented Generation)

### Vector Search with Azure AI Search

```typescript
// src/rag/azure-search.ts
import { SearchClient, AzureKeyCredential } from '@azure/search-documents';

const searchClient = new SearchClient(
  process.env.AZURE_SEARCH_ENDPOINT!,
  process.env.AZURE_SEARCH_INDEX!,
  new AzureKeyCredential(process.env.AZURE_SEARCH_KEY!)
);

export async function searchKnowledgeBase(
  query: string,
  topK: number = 5
): Promise<string[]> {
  const results = await searchClient.search(query, {
    top: topK,
    select: ['content', 'title', 'source'],
    queryType: 'semantic',
    semanticConfiguration: 'default'
  });

  const documents: string[] = [];
  for await (const result of results.results) {
    documents.push(`${result.document.title}: ${result.document.content}`);
  }

  return documents;
}
```

### RAG-Enhanced Claude Response

```typescript
// src/rag/claude-rag.ts
import Anthropic from '@anthropic-ai/sdk';
import { searchKnowledgeBase } from './azure-search';

const anthropic = new Anthropic();

export async function getRAGResponse(userQuery: string): Promise<string> {
  // 1. Search knowledge base
  const relevantDocs = await searchKnowledgeBase(userQuery);

  // 2. Build context
  const context = relevantDocs.join('\n\n---\n\n');

  // 3. Generate response with context
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    system: `You are a helpful assistant for Teams. Answer questions based on the provided context.
If the context doesn't contain relevant information, say so and provide a general response.
Always cite your sources when using information from the context.`,
    messages: [
      {
        role: 'user',
        content: `Context:\n${context}\n\nQuestion: ${userQuery}`
      }
    ]
  });

  return response.content[0].type === 'text' ? response.content[0].text : '';
}
```

---

## Deployment

### Azure Bot Service Setup

```bash
# Create resource group
az group create --name rg-teams-bot --location eastus

# Create App Service plan
az appservice plan create \
  --name asp-teams-bot \
  --resource-group rg-teams-bot \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name my-teams-bot \
  --resource-group rg-teams-bot \
  --plan asp-teams-bot \
  --runtime "NODE:18-lts"

# Create Bot Channels Registration
az bot create \
  --resource-group rg-teams-bot \
  --name my-teams-bot \
  --kind registration \
  --endpoint https://my-teams-bot.azurewebsites.net/api/messages \
  --sku F0

# Enable Teams channel
az bot msteams create \
  --name my-teams-bot \
  --resource-group rg-teams-bot
```

### Environment Variables

```bash
# .env
# Azure Bot
BOT_ID=your-bot-id
BOT_PASSWORD=your-bot-password
BOT_TENANT_ID=your-tenant-id

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4

# Or OpenAI
OPENAI_API_KEY=sk-xxx

# Or Anthropic
ANTHROPIC_API_KEY=sk-ant-xxx

# Microsoft Graph
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id

# Azure AI Search (for RAG)
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_KEY=your-key
AZURE_SEARCH_INDEX=knowledge-base
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3978

CMD ["node", "dist/index.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  teams-bot:
    build: .
    ports:
      - "3978:3978"
    environment:
      - BOT_ID=${BOT_ID}
      - BOT_PASSWORD=${BOT_PASSWORD}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
```

### Teams Toolkit Deployment

```bash
# Login to Azure
npx teamsfx account login azure

# Provision resources
npx teamsfx provision --env dev

# Deploy
npx teamsfx deploy --env dev

# Publish to Teams
npx teamsfx publish --env dev
```

---

## Testing

### Local Testing with ngrok

```bash
# Start ngrok tunnel
ngrok http 3978

# Update manifest with ngrok URL
# Bot endpoint: https://xxxx.ngrok.io/api/messages
```

### Teams Toolkit Local Debug

```bash
# Start local debugging (opens Teams with your app)
npx teamsfx preview --local
```

### Unit Testing

```typescript
// tests/bot.test.ts
import { TestAdapter, TurnContext } from 'botbuilder';
import { createWelcomeCard } from '../src/cards/welcome-card';

describe('Bot Tests', () => {
  let adapter: TestAdapter;

  beforeEach(() => {
    adapter = new TestAdapter();
  });

  test('should respond to hello', async () => {
    await adapter
      .send('hello')
      .assertReply((activity) => {
        expect(activity.text).toContain('Hello');
      });
  });

  test('should create welcome card', () => {
    const card = createWelcomeCard('John');
    expect(card.content.body[0].text).toContain('John');
  });
});
```

---

## Best Practices

### Conversation Design

```
┌─────────────────────────────────────────────────────────────────┐
│  CONVERSATION UX GUIDELINES                                     │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  1. GREET INTELLIGENTLY                                         │
│     - Welcome new users with onboarding card                    │
│     - Return users get quick access to recent actions           │
│                                                                 │
│  2. HANDLE ERRORS GRACEFULLY                                    │
│     - Never show stack traces to users                          │
│     - Provide clear recovery options                            │
│     - Log errors for debugging                                  │
│                                                                 │
│  3. USE CARDS FOR RICH CONTENT                                  │
│     - Adaptive Cards for forms and structured data              │
│     - Hero Cards for simple actions                             │
│     - Keep cards concise and actionable                         │
│                                                                 │
│  4. TYPING INDICATORS                                           │
│     - Show typing for long operations                           │
│     - Provide progress updates for very long tasks              │
│                                                                 │
│  5. CONTEXT AWARENESS                                           │
│     - Remember conversation history                             │
│     - Personalize based on user preferences                     │
│     - Respect team/channel context                              │
└─────────────────────────────────────────────────────────────────┘
```

### Security Checklist

- [ ] Validate all incoming messages
- [ ] Use App-Only auth for Graph API when possible
- [ ] Never log sensitive user data
- [ ] Implement rate limiting
- [ ] Use managed identity in Azure
- [ ] Rotate secrets regularly
- [ ] Enable audit logging

### Performance Tips

| Tip | Description |
|-----|-------------|
| Cache Graph tokens | Token refresh is expensive |
| Stream long responses | Use typing indicator + chunked responses |
| Index knowledge base | Pre-embed documents for RAG |
| Use connection pooling | Reuse HTTP connections |
| Compress payloads | Gzip large card responses |

---

## Project Templates

### AI Assistant Template

```typescript
// Complete AI assistant with Claude
import { App, HttpPlugin } from '@microsoft/teams.ai';
import Anthropic from '@anthropic-ai/sdk';
import { createWelcomeCard } from './cards/welcome-card';
import { createAIResponseCard } from './cards/ai-response-card';

const anthropic = new Anthropic();
const app = new App({ plugins: [new HttpPlugin()] });
const conversations = new Map<string, Anthropic.MessageParam[]>();

// Welcome new users
app.conversationUpdate('membersAdded', async (context) => {
  for (const member of context.activity.membersAdded || []) {
    if (member.id !== context.activity.recipient.id) {
      await context.sendActivity({
        attachments: [createWelcomeCard(member.name || 'User')]
      });
    }
  }
});

// Handle messages
app.on('message', async (context) => {
  const userId = context.activity.from.id;
  const userMessage = context.activity.text;

  // Initialize or get conversation
  if (!conversations.has(userId)) {
    conversations.set(userId, []);
  }
  const history = conversations.get(userId)!;
  history.push({ role: 'user', content: userMessage });

  // Show typing
  await context.sendActivity({ type: 'typing' });

  // Get AI response
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    system: 'You are a helpful Teams assistant.',
    messages: history
  });

  const answer = response.content[0].type === 'text'
    ? response.content[0].text
    : '';

  history.push({ role: 'assistant', content: answer });

  // Send rich card response
  await context.sendActivity({
    attachments: [{
      contentType: 'application/vnd.microsoft.card.adaptive',
      content: createAIResponseCard(userMessage, answer)
    }]
  });
});

// Handle card actions
app.on('adaptiveCard/action', async (context) => {
  const action = context.activity.value?.action;

  switch (action) {
    case 'feedback':
      // Log feedback
      console.log('Feedback:', context.activity.value);
      await context.sendActivity('Thanks for your feedback!');
      break;
    case 'followUp':
      await context.sendActivity('What would you like to know more about?');
      break;
  }
});

app.start();
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Bot not responding | Endpoint unreachable | Check ngrok/Azure URL in manifest |
| Auth failures | Token expired/invalid | Refresh OAuth connection |
| Cards not rendering | Invalid schema | Validate at adaptivecards.io/designer |
| Graph 403 errors | Missing permissions | Check app registration permissions |
| Slow responses | API latency | Add typing indicator, consider streaming |

---

## Resources

- [Teams SDK Documentation](https://microsoft.github.io/teams-sdk/)
- [Teams Platform Docs](https://learn.microsoft.com/en-us/microsoftteams/platform/)
- [Adaptive Cards Designer](https://adaptivecards.io/designer/)
- [Microsoft Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Teams Toolkit](https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/teams-toolkit-fundamentals)
- [Bot Framework Emulator](https://github.com/Microsoft/BotFramework-Emulator)
