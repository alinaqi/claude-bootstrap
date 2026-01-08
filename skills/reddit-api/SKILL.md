---
name: reddit-api
description: Reddit API with PRAW (Python) and Snoowrap (Node.js)
---

# Reddit API Skill

*Load with: base.md + [language].md*

For integrating Reddit data into applications - fetching posts, comments, subreddits, and user data.

**Sources:** [Reddit API Docs](https://www.reddit.com/dev/api/) | [OAuth2 Wiki](https://github.com/reddit-archive/reddit/wiki/oauth2) | [PRAW Docs](https://praw.readthedocs.io/)

---

## Setup

### 1. Create Reddit App

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name**: Your app name
   - **App type**:
     - `script` - For personal use / bots you control
     - `web app` - For server-side apps with user auth
     - `installed app` - For mobile/desktop apps
   - **Redirect URI**: `http://localhost:8000/callback` (for dev)
4. Note your `client_id` (under app name) and `client_secret`

### 2. Environment Variables

```bash
# .env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=YourApp/1.0 by YourUsername
REDDIT_USERNAME=your_username        # For script apps only
REDDIT_PASSWORD=your_password        # For script apps only
```

**User-Agent Format**: `<platform>:<app_id>:<version> (by /u/<username>)`

---

## Rate Limits

| Tier | Limit | Notes |
|------|-------|-------|
| OAuth authenticated | 100 QPM | Per OAuth client ID |
| Non-authenticated | Blocked | Must use OAuth |

- Limits averaged over 10-minute window
- Include `User-Agent` header to avoid blocks
- Respect `X-Ratelimit-*` response headers

---

## Python: PRAW (Recommended)

### Installation

```bash
pip install praw
# or
uv add praw
```

### Script App (Personal Use / Bots)

```python
import praw
from pydantic_settings import BaseSettings

class RedditSettings(BaseSettings):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    reddit_username: str
    reddit_password: str

    class Config:
        env_file = ".env"

settings = RedditSettings()

reddit = praw.Reddit(
    client_id=settings.reddit_client_id,
    client_secret=settings.reddit_client_secret,
    user_agent=settings.reddit_user_agent,
    username=settings.reddit_username,
    password=settings.reddit_password,
)

# Verify authentication
print(f"Logged in as: {reddit.user.me()}")
```

### Read-Only (No User Auth)

```python
import praw

reddit = praw.Reddit(
    client_id="your_client_id",
    client_secret="your_client_secret",
    user_agent="YourApp/1.0 by YourUsername",
)

# Read-only mode - can browse, can't post/vote
reddit.read_only = True
```

### Common Operations

```python
# Get subreddit posts
subreddit = reddit.subreddit("python")

# Hot posts
for post in subreddit.hot(limit=10):
    print(f"{post.title} - {post.score} upvotes")

# New posts
for post in subreddit.new(limit=10):
    print(post.title)

# Search posts
for post in subreddit.search("pydantic", limit=5):
    print(post.title)

# Get specific post
submission = reddit.submission(id="abc123")
print(submission.title)
print(submission.selftext)

# Get comments
submission.comments.replace_more(limit=0)  # Flatten comment tree
for comment in submission.comments.list():
    print(f"{comment.author}: {comment.body[:100]}")
```

### Posting & Voting (Requires Auth)

```python
# Submit text post
subreddit = reddit.subreddit("test")
submission = subreddit.submit(
    title="Test Post",
    selftext="This is the body of my post."
)

# Submit link post
submission = subreddit.submit(
    title="Check this out",
    url="https://example.com"
)

# Vote
submission.upvote()
submission.downvote()
submission.clear_vote()

# Comment
submission.reply("Great post!")

# Reply to comment
comment = reddit.comment(id="xyz789")
comment.reply("I agree!")
```

### Streaming (Real-time)

```python
# Stream new posts
for post in reddit.subreddit("python").stream.submissions():
    print(f"New post: {post.title}")
    # Process post...

# Stream new comments
for comment in reddit.subreddit("python").stream.comments():
    print(f"New comment by {comment.author}: {comment.body[:50]}")
```

### User Data

```python
# Get user info
user = reddit.redditor("spez")
print(f"Karma: {user.link_karma + user.comment_karma}")

# User's posts
for post in user.submissions.new(limit=5):
    print(post.title)

# User's comments
for comment in user.comments.new(limit=5):
    print(comment.body[:100])
```

---

## TypeScript / Node.js: Snoowrap

### Installation

```bash
npm install snoowrap
# or
pnpm add snoowrap
```

### Setup

```typescript
import Snoowrap from "snoowrap";

const reddit = new Snoowrap({
  userAgent: "YourApp/1.0 by YourUsername",
  clientId: process.env.REDDIT_CLIENT_ID!,
  clientSecret: process.env.REDDIT_CLIENT_SECRET!,
  username: process.env.REDDIT_USERNAME!,
  password: process.env.REDDIT_PASSWORD!,
});

// Configure rate limiting
reddit.config({
  requestDelay: 1000,  // 1 second between requests
  continueAfterRatelimitError: true,
});
```

### Common Operations

```typescript
// Get hot posts from subreddit
const posts = await reddit.getSubreddit("typescript").getHot({ limit: 10 });
posts.forEach((post) => {
  console.log(`${post.title} - ${post.score} upvotes`);
});

// Search posts
const results = await reddit.getSubreddit("programming").search({
  query: "typescript",
  sort: "relevance",
  time: "month",
  limit: 10,
});

// Get specific post
const submission = await reddit.getSubmission("abc123").fetch();
console.log(submission.title);

// Get comments
const comments = await submission.comments.fetchAll();
comments.forEach((comment) => {
  console.log(`${comment.author.name}: ${comment.body.slice(0, 100)}`);
});
```

### Posting

```typescript
// Submit text post
const post = await reddit.getSubreddit("test").submitSelfpost({
  title: "Test Post",
  text: "This is the body.",
});

// Submit link
const linkPost = await reddit.getSubreddit("test").submitLink({
  title: "Check this out",
  url: "https://example.com",
});

// Vote and comment
await post.upvote();
await post.reply("Great post!");
```

---

## Direct API (No Library)

### Python with httpx

```python
import httpx
import base64
from pydantic import BaseModel

class RedditClient:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.access_token: str | None = None
        self.client = httpx.AsyncClient()

    async def authenticate(self) -> None:
        """Get application-only OAuth token."""
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        response = await self.client.post(
            "https://www.reddit.com/api/v1/access_token",
            headers={
                "Authorization": f"Basic {auth}",
                "User-Agent": self.user_agent,
            },
            data={
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]

    async def get_posts(self, subreddit: str, sort: str = "hot", limit: int = 10) -> list[dict]:
        """Get posts from a subreddit."""
        if not self.access_token:
            await self.authenticate()

        response = await self.client.get(
            f"https://oauth.reddit.com/r/{subreddit}/{sort}",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": self.user_agent,
            },
            params={"limit": limit},
        )
        response.raise_for_status()
        return [post["data"] for post in response.json()["data"]["children"]]

    async def close(self) -> None:
        await self.client.aclose()


# Usage
async def main():
    client = RedditClient(
        client_id="your_id",
        client_secret="your_secret",
        user_agent="YourApp/1.0",
    )
    try:
        posts = await client.get_posts("python", limit=5)
        for post in posts:
            print(f"{post['title']} - {post['score']} upvotes")
    finally:
        await client.close()
```

### TypeScript with fetch

```typescript
interface RedditPost {
  title: string;
  score: number;
  url: string;
  selftext: string;
  author: string;
  created_utc: number;
}

class RedditClient {
  private accessToken: string | null = null;

  constructor(
    private clientId: string,
    private clientSecret: string,
    private userAgent: string
  ) {}

  async authenticate(): Promise<void> {
    const auth = Buffer.from(`${this.clientId}:${this.clientSecret}`).toString("base64");

    const response = await fetch("https://www.reddit.com/api/v1/access_token", {
      method: "POST",
      headers: {
        Authorization: `Basic ${auth}`,
        "User-Agent": this.userAgent,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "grant_type=client_credentials",
    });

    const data = await response.json();
    this.accessToken = data.access_token;
  }

  async getPosts(subreddit: string, sort = "hot", limit = 10): Promise<RedditPost[]> {
    if (!this.accessToken) await this.authenticate();

    const response = await fetch(
      `https://oauth.reddit.com/r/${subreddit}/${sort}?limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
          "User-Agent": this.userAgent,
        },
      }
    );

    const data = await response.json();
    return data.data.children.map((child: any) => child.data);
  }
}
```

---

## OAuth2 Web Flow (User Authorization)

For apps where users log in with their Reddit account:

```python
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import httpx
import secrets

app = FastAPI()
state_store: dict[str, bool] = {}

REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "http://localhost:8000/callback"

@app.get("/login")
async def login():
    state = secrets.token_urlsafe(16)
    state_store[state] = True

    auth_url = (
        f"https://www.reddit.com/api/v1/authorize"
        f"?client_id={REDDIT_CLIENT_ID}"
        f"&response_type=code"
        f"&state={state}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&duration=permanent"
        f"&scope=identity read submit vote"
    )
    return RedirectResponse(auth_url)

@app.get("/callback")
async def callback(code: str, state: str):
    if state not in state_store:
        return {"error": "Invalid state"}
    del state_store[state]

    # Exchange code for token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"User-Agent": "YourApp/1.0"},
        )

    tokens = response.json()
    # Store tokens securely, associate with user session
    return {"access_token": tokens["access_token"][:10] + "..."}
```

---

## Available Scopes

| Scope | Description |
|-------|-------------|
| `identity` | Access username and signup date |
| `read` | Access posts and comments |
| `submit` | Submit links and comments |
| `vote` | Upvote/downvote content |
| `edit` | Edit posts and comments |
| `history` | Access voting history |
| `subscribe` | Manage subreddit subscriptions |
| `mysubreddits` | Access subscribed subreddits |
| `privatemessages` | Access private messages |
| `save` | Save/unsave content |

Full list: https://www.reddit.com/api/v1/scopes

---

## Project Structure

```
project/
├── src/
│   ├── reddit/
│   │   ├── __init__.py
│   │   ├── client.py         # Reddit client wrapper
│   │   ├── models.py         # Pydantic models for posts/comments
│   │   └── scraper.py        # Data collection logic
│   └── main.py
├── .env
└── pyproject.toml
```

---

## Pydantic Models

```python
from pydantic import BaseModel
from datetime import datetime

class RedditPost(BaseModel):
    id: str
    title: str
    author: str
    subreddit: str
    score: int
    upvote_ratio: float
    url: str
    selftext: str
    created_utc: datetime
    num_comments: int
    is_self: bool

    @classmethod
    def from_praw(cls, submission) -> "RedditPost":
        return cls(
            id=submission.id,
            title=submission.title,
            author=str(submission.author),
            subreddit=submission.subreddit.display_name,
            score=submission.score,
            upvote_ratio=submission.upvote_ratio,
            url=submission.url,
            selftext=submission.selftext,
            created_utc=datetime.fromtimestamp(submission.created_utc),
            num_comments=submission.num_comments,
            is_self=submission.is_self,
        )

class RedditComment(BaseModel):
    id: str
    author: str
    body: str
    score: int
    created_utc: datetime
    parent_id: str
    is_submitter: bool
```

---

## Anti-Patterns

- **No User-Agent** - Reddit blocks requests without proper User-Agent
- **Ignoring rate limits** - Respect 100 QPM, check `X-Ratelimit-*` headers
- **Storing credentials in code** - Use environment variables
- **Not handling `MoreComments`** - Use `replace_more()` in PRAW
- **Polling instead of streaming** - Use `.stream` for real-time data
- **No error handling** - Handle 429 (rate limit), 403 (forbidden), 404 (not found)

---

## Quick Reference

```bash
# PRAW installation
pip install praw

# Snoowrap installation
npm install snoowrap

# Test authentication
python -c "import praw; r = praw.Reddit(...); print(r.user.me())"
```

### Endpoints

| Operation | Endpoint |
|-----------|----------|
| Auth token | `POST https://www.reddit.com/api/v1/access_token` |
| API requests | `https://oauth.reddit.com/...` |
| Subreddit posts | `GET /r/{subreddit}/{sort}` |
| Submission | `GET /comments/{id}` |
| User info | `GET /user/{username}/about` |
| Submit post | `POST /api/submit` |
| Vote | `POST /api/vote` |
