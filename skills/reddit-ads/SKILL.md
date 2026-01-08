---
name: reddit-ads
description: Reddit Ads API - campaigns, targeting, conversions, agentic optimization
---

# Reddit Ads API Skill

*Load with: base.md*

**Purpose:** Automate Reddit advertising campaigns using the Reddit Ads API. Create, manage, and optimize campaigns, ad groups, and ads programmatically.

---

## API Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  REDDIT ADS API HIERARCHY                                        │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Account                                                        │
│    └── Campaign (objective, budget, schedule)                   │
│         └── Ad Group (targeting, bidding, placement)            │
│              └── Ad (creative, headline, CTA)                   │
│                                                                 │
│  + Custom Audiences (customer lists, lookalikes)                │
│  + Conversions API (track events server-side)                   │
├─────────────────────────────────────────────────────────────────┤
│  BASE URL: https://ads-api.reddit.com/api/v2.0                  │
│  DOCS: https://ads-api.reddit.com/docs/                         │
│  RATE LIMIT: 1 request per second                               │
│  AUTH: OAuth 2.0 with Bearer token                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Authentication

### Step 1: Create Reddit Developer App

1. Go to https://www.reddit.com/prefs/apps/
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name:** Your app name
   - **Type:** Select `script` for server-side automation
   - **Redirect URI:** Your callback URL (e.g., `https://yourapp.com/callback`)
4. Note your **Client ID** (under app name) and **Client Secret**

### Step 2: Authorization Flow

```javascript
// Node.js OAuth2 flow
const REDDIT_CLIENT_ID = process.env.REDDIT_ADS_CLIENT_ID;
const REDDIT_CLIENT_SECRET = process.env.REDDIT_ADS_CLIENT_SECRET;
const REDIRECT_URI = 'https://yourapp.com/callback';

// Step 1: Generate authorization URL
function getAuthorizationUrl(state) {
  const scopes = 'adsread,adsedit,history';
  return `https://www.reddit.com/api/v1/authorize?` +
    `client_id=${REDDIT_CLIENT_ID}` +
    `&response_type=code` +
    `&state=${state}` +
    `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}` +
    `&duration=permanent` +
    `&scope=${scopes}`;
}

// Step 2: Exchange code for tokens
async function getAccessToken(authorizationCode) {
  const credentials = Buffer.from(
    `${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`
  ).toString('base64');

  const response = await fetch('https://www.reddit.com/api/v1/access_token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'YourApp/1.0.0'
    },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code: authorizationCode,
      redirect_uri: REDIRECT_URI
    })
  });

  return response.json();
  // Returns: { access_token, refresh_token, expires_in, scope }
}

// Step 3: Refresh token when expired
async function refreshAccessToken(refreshToken) {
  const credentials = Buffer.from(
    `${REDDIT_CLIENT_ID}:${REDDIT_CLIENT_SECRET}`
  ).toString('base64');

  const response = await fetch('https://www.reddit.com/api/v1/access_token', {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'YourApp/1.0.0'
    },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: refreshToken
    })
  });

  return response.json();
}
```

### Python OAuth2 Flow

```python
import requests
import base64
import os

REDDIT_CLIENT_ID = os.environ['REDDIT_ADS_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_ADS_CLIENT_SECRET']
REDIRECT_URI = 'https://yourapp.com/callback'
USER_AGENT = 'YourApp/1.0.0'

def get_authorization_url(state: str) -> str:
    """Generate OAuth authorization URL."""
    scopes = 'adsread,adsedit,history'
    return (
        f"https://www.reddit.com/api/v1/authorize?"
        f"client_id={REDDIT_CLIENT_ID}"
        f"&response_type=code"
        f"&state={state}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&duration=permanent"
        f"&scope={scopes}"
    )

def get_access_token(authorization_code: str) -> dict:
    """Exchange authorization code for access token."""
    credentials = base64.b64encode(
        f"{REDDIT_CLIENT_ID}:{REDDIT_CLIENT_SECRET}".encode()
    ).decode()

    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        headers={
            'Authorization': f'Basic {credentials}',
            'User-Agent': USER_AGENT
        },
        data={
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': REDIRECT_URI
        }
    )
    return response.json()

def refresh_access_token(refresh_token: str) -> dict:
    """Refresh expired access token."""
    credentials = base64.b64encode(
        f"{REDDIT_CLIENT_ID}:{REDDIT_CLIENT_SECRET}".encode()
    ).decode()

    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        headers={
            'Authorization': f'Basic {credentials}',
            'User-Agent': USER_AGENT
        },
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
    )
    return response.json()
```

### Required Scopes

| Scope | Access Level |
|-------|--------------|
| `adsread` | Read campaigns, ad groups, ads, reports |
| `adsedit` | Create/update campaigns, ad groups, ads |
| `history` | Access account history |

---

## Reddit Ads Client

### Node.js Client

```typescript
// lib/reddit-ads-client.ts
interface RedditAdsConfig {
  accessToken: string;
  accountId: string;
}

class RedditAdsClient {
  private baseUrl = 'https://ads-api.reddit.com/api/v2.0';
  private accessToken: string;
  private accountId: string;

  constructor(config: RedditAdsConfig) {
    this.accessToken = config.accessToken;
    this.accountId = config.accountId;
  }

  private async request<T>(
    method: string,
    endpoint: string,
    body?: object
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await fetch(url, {
      method,
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json',
        'User-Agent': 'YourApp/1.0.0'
      },
      body: body ? JSON.stringify(body) : undefined
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Reddit Ads API Error: ${JSON.stringify(error)}`);
    }

    return response.json();
  }

  // Account
  async getAccount() {
    return this.request('GET', `/accounts/${this.accountId}`);
  }

  // Campaigns
  async getCampaigns() {
    return this.request('GET', `/accounts/${this.accountId}/campaigns`);
  }

  async getCampaign(campaignId: string) {
    return this.request('GET', `/accounts/${this.accountId}/campaigns/${campaignId}`);
  }

  async createCampaign(campaign: CampaignCreate) {
    return this.request('POST', `/accounts/${this.accountId}/campaigns`, campaign);
  }

  async updateCampaign(campaignId: string, updates: Partial<CampaignCreate>) {
    return this.request('PUT', `/accounts/${this.accountId}/campaigns/${campaignId}`, updates);
  }

  // Ad Groups
  async getAdGroups(campaignId?: string) {
    const endpoint = campaignId
      ? `/accounts/${this.accountId}/campaigns/${campaignId}/ad_groups`
      : `/accounts/${this.accountId}/ad_groups`;
    return this.request('GET', endpoint);
  }

  async getAdGroup(adGroupId: string) {
    return this.request('GET', `/accounts/${this.accountId}/ad_groups/${adGroupId}`);
  }

  async createAdGroup(adGroup: AdGroupCreate) {
    return this.request('POST', `/accounts/${this.accountId}/ad_groups`, adGroup);
  }

  async updateAdGroup(adGroupId: string, updates: Partial<AdGroupCreate>) {
    return this.request('PUT', `/accounts/${this.accountId}/ad_groups/${adGroupId}`, updates);
  }

  // Ads
  async getAds(adGroupId?: string) {
    const endpoint = adGroupId
      ? `/accounts/${this.accountId}/ad_groups/${adGroupId}/ads`
      : `/accounts/${this.accountId}/ads`;
    return this.request('GET', endpoint);
  }

  async createAd(ad: AdCreate) {
    return this.request('POST', `/accounts/${this.accountId}/ads`, ad);
  }

  async updateAd(adId: string, updates: Partial<AdCreate>) {
    return this.request('PUT', `/accounts/${this.accountId}/ads/${adId}`, updates);
  }

  // Reports
  async getReport(reportRequest: ReportRequest) {
    return this.request('POST', `/accounts/${this.accountId}/reports`, reportRequest);
  }

  // Custom Audiences
  async getCustomAudiences() {
    return this.request('GET', `/accounts/${this.accountId}/custom_audiences`);
  }

  async createCustomAudience(audience: CustomAudienceCreate) {
    return this.request('POST', `/accounts/${this.accountId}/custom_audiences`, audience);
  }
}

export default RedditAdsClient;
```

### Python Client

```python
# lib/reddit_ads_client.py
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

@dataclass
class RedditAdsConfig:
    access_token: str
    account_id: str

class RedditAdsClient:
    BASE_URL = 'https://ads-api.reddit.com/api/v2.0'

    def __init__(self, config: RedditAdsConfig):
        self.access_token = config.access_token
        self.account_id = config.account_id
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'YourApp/1.0.0'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.request(method, url, json=json)
        response.raise_for_status()
        return response.json()

    # Account
    def get_account(self) -> Dict:
        return self._request('GET', f'/accounts/{self.account_id}')

    # Campaigns
    def get_campaigns(self) -> List[Dict]:
        return self._request('GET', f'/accounts/{self.account_id}/campaigns')

    def get_campaign(self, campaign_id: str) -> Dict:
        return self._request('GET', f'/accounts/{self.account_id}/campaigns/{campaign_id}')

    def create_campaign(self, campaign: Dict) -> Dict:
        return self._request('POST', f'/accounts/{self.account_id}/campaigns', json=campaign)

    def update_campaign(self, campaign_id: str, updates: Dict) -> Dict:
        return self._request('PUT', f'/accounts/{self.account_id}/campaigns/{campaign_id}', json=updates)

    # Ad Groups
    def get_ad_groups(self, campaign_id: Optional[str] = None) -> List[Dict]:
        endpoint = (
            f'/accounts/{self.account_id}/campaigns/{campaign_id}/ad_groups'
            if campaign_id
            else f'/accounts/{self.account_id}/ad_groups'
        )
        return self._request('GET', endpoint)

    def create_ad_group(self, ad_group: Dict) -> Dict:
        return self._request('POST', f'/accounts/{self.account_id}/ad_groups', json=ad_group)

    def update_ad_group(self, ad_group_id: str, updates: Dict) -> Dict:
        return self._request('PUT', f'/accounts/{self.account_id}/ad_groups/{ad_group_id}', json=updates)

    # Ads
    def get_ads(self, ad_group_id: Optional[str] = None) -> List[Dict]:
        endpoint = (
            f'/accounts/{self.account_id}/ad_groups/{ad_group_id}/ads'
            if ad_group_id
            else f'/accounts/{self.account_id}/ads'
        )
        return self._request('GET', endpoint)

    def create_ad(self, ad: Dict) -> Dict:
        return self._request('POST', f'/accounts/{self.account_id}/ads', json=ad)

    # Reports
    def get_report(self, report_request: Dict) -> Dict:
        return self._request('POST', f'/accounts/{self.account_id}/reports', json=report_request)

    # Custom Audiences
    def get_custom_audiences(self) -> List[Dict]:
        return self._request('GET', f'/accounts/{self.account_id}/custom_audiences')

    def create_custom_audience(self, audience: Dict) -> Dict:
        return self._request('POST', f'/accounts/{self.account_id}/custom_audiences', json=audience)
```

---

## API Endpoints Reference

### Account Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{account_id}` | Get account details |
| GET | `/accounts/{account_id}/funding` | Get funding information |

### Campaign Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{account_id}/campaigns` | List all campaigns |
| GET | `/accounts/{account_id}/campaigns/{campaign_id}` | Get campaign by ID |
| POST | `/accounts/{account_id}/campaigns` | Create campaign |
| PUT | `/accounts/{account_id}/campaigns/{campaign_id}` | Update campaign |
| DELETE | `/accounts/{account_id}/campaigns/{campaign_id}` | Delete campaign |

### Ad Group Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{account_id}/ad_groups` | List all ad groups |
| GET | `/accounts/{account_id}/ad_groups/{ad_group_id}` | Get ad group by ID |
| POST | `/accounts/{account_id}/ad_groups` | Create ad group |
| PUT | `/accounts/{account_id}/ad_groups/{ad_group_id}` | Update ad group |
| DELETE | `/accounts/{account_id}/ad_groups/{ad_group_id}` | Delete ad group |

### Ad Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{account_id}/ads` | List all ads |
| GET | `/accounts/{account_id}/ads/{ad_id}` | Get ad by ID |
| POST | `/accounts/{account_id}/ads` | Create ad |
| PUT | `/accounts/{account_id}/ads/{ad_id}` | Update ad |
| DELETE | `/accounts/{account_id}/ads/{ad_id}` | Delete ad |

### Custom Audience Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts/{account_id}/custom_audiences` | List custom audiences |
| POST | `/accounts/{account_id}/custom_audiences` | Create custom audience |
| PUT | `/accounts/{account_id}/custom_audiences/{audience_id}` | Update audience |
| DELETE | `/accounts/{account_id}/custom_audiences/{audience_id}` | Delete audience |

### Report Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts/{account_id}/reports` | Generate report |

---

## Campaign Creation

### Campaign Objectives

| Objective | Use Case |
|-----------|----------|
| `BRAND_AWARENESS` | Build brand recognition and reach |
| `TRAFFIC` | Drive clicks to website/landing page |
| `CONVERSIONS` | Track and optimize for conversions |
| `VIDEO_VIEWS` | Maximize video view engagement |
| `APP_INSTALLS` | Drive mobile app installations |
| `CATALOG_SALES` | Promote product catalog items |

### Budget Types

| Type | Description |
|------|-------------|
| `DAILY` | Average daily spend (may vary slightly) |
| `LIFETIME` | Total spend over campaign duration |

### Campaign Create Example

```typescript
interface CampaignCreate {
  name: string;
  objective: 'BRAND_AWARENESS' | 'TRAFFIC' | 'CONVERSIONS' | 'VIDEO_VIEWS' | 'APP_INSTALLS';
  is_enabled: boolean;
  budget_type: 'DAILY' | 'LIFETIME';
  budget_total_amount_micros: number; // Amount in micros (1 USD = 1,000,000 micros)
  start_time: string; // ISO 8601 format
  end_time?: string; // ISO 8601 format (optional)
}

// Create a traffic campaign with $50/day budget
const campaign: CampaignCreate = {
  name: 'Q1 2025 Traffic Campaign',
  objective: 'TRAFFIC',
  is_enabled: true,
  budget_type: 'DAILY',
  budget_total_amount_micros: 50_000_000, // $50
  start_time: '2025-01-15T00:00:00Z',
  end_time: '2025-03-31T23:59:59Z'
};

const result = await client.createCampaign(campaign);
```

```python
# Python example
campaign = {
    'name': 'Q1 2025 Traffic Campaign',
    'objective': 'TRAFFIC',
    'is_enabled': True,
    'budget_type': 'DAILY',
    'budget_total_amount_micros': 50_000_000,  # $50
    'start_time': '2025-01-15T00:00:00Z',
    'end_time': '2025-03-31T23:59:59Z'
}

result = client.create_campaign(campaign)
```

---

## Ad Group Creation

### Bidding Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `LOWEST_COST` | Maximize conversions within budget | Best for most campaigns |
| `COST_CAP` | Set average CPC cap | Control cost per result |
| `MANUAL` | Set strict CPC/CPM bid | Maximum control |

### Targeting Options

| Targeting Type | Description |
|----------------|-------------|
| `communities` | Target specific subreddits |
| `interests` | Target by interest categories |
| `keywords` | Target by keyword engagement |
| `devices` | Target by device type |
| `locations` | Target by geography |
| `custom_audiences` | Target uploaded customer lists |

### Ad Group Create Example

```typescript
interface AdGroupCreate {
  name: string;
  campaign_id: string;
  is_enabled: boolean;
  bid_strategy: 'LOWEST_COST' | 'COST_CAP' | 'MANUAL';
  bid_amount_micros?: number; // For COST_CAP or MANUAL
  goal_type: 'CLICKS' | 'IMPRESSIONS' | 'CONVERSIONS';
  goal_value_micros?: number;
  targeting: {
    communities?: string[]; // Subreddit names without r/
    interests?: string[];
    keywords?: string[];
    geo_locations?: {
      countries?: string[];
      regions?: string[];
      cities?: string[];
    };
    devices?: ('DESKTOP' | 'MOBILE' | 'TABLET')[];
    custom_audience_ids?: string[];
  };
  start_time?: string;
  end_time?: string;
}

// Create ad group targeting specific subreddits
const adGroup: AdGroupCreate = {
  name: 'Tech Enthusiasts - Subreddit Targeting',
  campaign_id: 'campaign_123',
  is_enabled: true,
  bid_strategy: 'LOWEST_COST',
  goal_type: 'CLICKS',
  targeting: {
    communities: [
      'technology',
      'gadgets',
      'programming',
      'webdev',
      'startups'
    ],
    geo_locations: {
      countries: ['US', 'CA', 'GB']
    },
    devices: ['DESKTOP', 'MOBILE']
  },
  start_time: '2025-01-15T00:00:00Z'
};

const result = await client.createAdGroup(adGroup);
```

```python
# Python example
ad_group = {
    'name': 'Tech Enthusiasts - Subreddit Targeting',
    'campaign_id': 'campaign_123',
    'is_enabled': True,
    'bid_strategy': 'LOWEST_COST',
    'goal_type': 'CLICKS',
    'targeting': {
        'communities': [
            'technology',
            'gadgets',
            'programming',
            'webdev',
            'startups'
        ],
        'geo_locations': {
            'countries': ['US', 'CA', 'GB']
        },
        'devices': ['DESKTOP', 'MOBILE']
    },
    'start_time': '2025-01-15T00:00:00Z'
}

result = client.create_ad_group(ad_group)
```

---

## Ad Creation

### Ad Types

| Type | Description |
|------|-------------|
| `LINK` | Link ad with image/video |
| `TEXT` | Text-only promoted post |
| `VIDEO` | Video ad |
| `CAROUSEL` | Multiple images/cards |
| `PRODUCT` | Product catalog ad |

### Call-to-Action Options

| CTA | Use Case |
|-----|----------|
| `SHOP_NOW` | E-commerce |
| `SIGN_UP` | Lead generation |
| `LEARN_MORE` | Information |
| `DOWNLOAD` | App/content download |
| `INSTALL` | App install |
| `GET_QUOTE` | Services |
| `CONTACT_US` | B2B/Services |
| `APPLY_NOW` | Jobs/Finance |
| `BOOK_NOW` | Travel/Services |
| `WATCH_NOW` | Video content |
| `SUBSCRIBE` | Newsletters/SaaS |
| `GET_OFFER` | Promotions |
| `SEE_MENU` | Restaurants |

### Ad Create Example

```typescript
interface AdCreate {
  name: string;
  ad_group_id: string;
  is_enabled: boolean;
  type: 'LINK' | 'TEXT' | 'VIDEO' | 'CAROUSEL';
  headline: string; // Max 300 characters
  body?: string;
  url: string;
  display_url?: string;
  call_to_action: string;
  thumbnail_url?: string; // For image/video ads
  video_url?: string; // For video ads
}

// Create a link ad
const ad: AdCreate = {
  name: 'Product Launch Ad - v1',
  ad_group_id: 'ad_group_456',
  is_enabled: true,
  type: 'LINK',
  headline: 'Introducing Our Revolutionary New Product',
  body: 'Discover how our latest innovation can transform your workflow. Join 10,000+ satisfied customers.',
  url: 'https://yoursite.com/product?utm_source=reddit&utm_medium=paid',
  display_url: 'yoursite.com/product',
  call_to_action: 'LEARN_MORE',
  thumbnail_url: 'https://yoursite.com/images/ad-creative.jpg'
};

const result = await client.createAd(ad);
```

```python
# Python example
ad = {
    'name': 'Product Launch Ad - v1',
    'ad_group_id': 'ad_group_456',
    'is_enabled': True,
    'type': 'LINK',
    'headline': 'Introducing Our Revolutionary New Product',
    'body': 'Discover how our latest innovation can transform your workflow. Join 10,000+ satisfied customers.',
    'url': 'https://yoursite.com/product?utm_source=reddit&utm_medium=paid',
    'display_url': 'yoursite.com/product',
    'call_to_action': 'LEARN_MORE',
    'thumbnail_url': 'https://yoursite.com/images/ad-creative.jpg'
}

result = client.create_ad(ad)
```

---

## Conversions API

### Event Types

| Event Type | Description |
|------------|-------------|
| `PAGE_VISIT` | Page view |
| `VIEW_CONTENT` | Product/content view |
| `SEARCH` | Search action |
| `ADD_TO_CART` | Add to cart |
| `ADD_TO_WISHLIST` | Add to wishlist |
| `PURCHASE` | Completed purchase |
| `LEAD` | Lead submission |
| `SIGN_UP` | Account creation |
| `CUSTOM` | Custom event |

### Conversion Event Structure

```typescript
interface ConversionEvent {
  event_at: number; // Unix timestamp in milliseconds
  event_type: {
    tracking_type: string;
    custom_event_name?: string; // For CUSTOM type
  };
  user: {
    email?: string; // SHA256 hashed, lowercase
    phone_number?: string; // SHA256 hashed, E.164 format
    external_id?: string;
    ip_address?: string;
    user_agent?: string;
    aaid?: string; // Android Advertising ID
    idfa?: string; // iOS IDFA
  };
  event_metadata?: {
    item_count?: number;
    value_decimal?: number;
    currency?: string;
    conversion_id: string; // Unique event ID
    products?: Array<{
      id: string;
      name?: string;
      category?: string;
    }>;
  };
  click_id?: string; // Reddit click ID for attribution
}
```

### Send Conversion Events

```typescript
import crypto from 'crypto';

function hashPII(value: string): string {
  return crypto
    .createHash('sha256')
    .update(value.toLowerCase().trim())
    .digest('hex');
}

async function sendConversionEvent(
  accessToken: string,
  pixelId: string,
  event: ConversionEvent
) {
  const response = await fetch(
    `https://ads-api.reddit.com/api/v2.0/conversions/events/${pixelId}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        events: [event],
        test_mode: false // Set true for testing
      })
    }
  );

  return response.json();
}

// Example: Track a purchase
const purchaseEvent: ConversionEvent = {
  event_at: Date.now(),
  event_type: {
    tracking_type: 'PURCHASE'
  },
  user: {
    email: hashPII('customer@example.com'),
    ip_address: '192.168.1.1',
    user_agent: 'Mozilla/5.0...'
  },
  event_metadata: {
    conversion_id: 'order_12345',
    value_decimal: 99.99,
    currency: 'USD',
    item_count: 2,
    products: [
      { id: 'SKU001', name: 'Product A', category: 'Electronics' },
      { id: 'SKU002', name: 'Product B', category: 'Electronics' }
    ]
  },
  click_id: 'reddit_click_id_from_url' // From rdt_cid parameter
};

await sendConversionEvent(accessToken, 'pixel_123', purchaseEvent);
```

```python
import hashlib
import time
import requests

def hash_pii(value: str) -> str:
    """SHA256 hash PII data."""
    return hashlib.sha256(value.lower().strip().encode()).hexdigest()

def send_conversion_event(
    access_token: str,
    pixel_id: str,
    events: list[dict],
    test_mode: bool = False
) -> dict:
    """Send conversion events to Reddit."""
    response = requests.post(
        f'https://ads-api.reddit.com/api/v2.0/conversions/events/{pixel_id}',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={
            'events': events,
            'test_mode': test_mode
        }
    )
    response.raise_for_status()
    return response.json()

# Example: Track a purchase
purchase_event = {
    'event_at': int(time.time() * 1000),
    'event_type': {
        'tracking_type': 'PURCHASE'
    },
    'user': {
        'email': hash_pii('customer@example.com'),
        'ip_address': '192.168.1.1',
        'user_agent': 'Mozilla/5.0...'
    },
    'event_metadata': {
        'conversion_id': 'order_12345',
        'value_decimal': 99.99,
        'currency': 'USD',
        'item_count': 2,
        'products': [
            {'id': 'SKU001', 'name': 'Product A', 'category': 'Electronics'},
            {'id': 'SKU002', 'name': 'Product B', 'category': 'Electronics'}
        ]
    },
    'click_id': 'reddit_click_id_from_url'
}

result = send_conversion_event(access_token, 'pixel_123', [purchase_event])
```

### Important Notes

- Events must occur within **last 7 days** to be processed
- Maximum **500 events per batch** request
- Include `click_id` when available for better attribution
- Use `test_mode: true` for testing without affecting campaigns

---

## Custom Audiences

### Audience Types

| Type | Description |
|------|-------------|
| `CUSTOMER_LIST` | Upload hashed emails/phone/MAIDs |
| `WEBSITE_VISITORS` | Pixel-based retargeting |
| `LOOKALIKE` | Similar to source audience |

### Create Customer List Audience

```typescript
interface CustomAudienceCreate {
  name: string;
  type: 'CUSTOMER_LIST';
  description?: string;
  users: Array<{
    email_sha256?: string;
    maid_sha256?: string; // Mobile Advertising ID
  }>;
}

// Create audience from customer emails
const audience: CustomAudienceCreate = {
  name: 'High Value Customers Q4 2024',
  type: 'CUSTOMER_LIST',
  description: 'Customers with LTV > $500',
  users: customerEmails.map(email => ({
    email_sha256: hashPII(email)
  }))
};

const result = await client.createCustomAudience(audience);
```

### Minimum Audience Size

- **1,000 matched users** minimum to be usable for targeting
- Match rates displayed as ranges for privacy

---

## Reporting

### Report Request

```typescript
interface ReportRequest {
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  level: 'ACCOUNT' | 'CAMPAIGN' | 'AD_GROUP' | 'AD';
  metrics: string[];
  dimensions?: string[];
  filters?: {
    campaign_ids?: string[];
    ad_group_ids?: string[];
  };
}

// Get campaign performance report
const report = await client.getReport({
  start_date: '2025-01-01',
  end_date: '2025-01-31',
  level: 'CAMPAIGN',
  metrics: [
    'impressions',
    'clicks',
    'spend',
    'ctr',
    'cpc',
    'conversions',
    'conversion_rate',
    'cpa'
  ],
  dimensions: ['date']
});
```

### Available Metrics

| Metric | Description |
|--------|-------------|
| `impressions` | Total impressions |
| `clicks` | Total clicks |
| `spend` | Total spend (in account currency) |
| `ctr` | Click-through rate |
| `cpc` | Cost per click |
| `cpm` | Cost per 1,000 impressions |
| `conversions` | Total conversions |
| `conversion_rate` | Conversions / Clicks |
| `cpa` | Cost per acquisition |
| `video_views` | Video view count |
| `video_completions` | Videos watched to completion |

---

## Environment Variables

```bash
# .env
REDDIT_ADS_CLIENT_ID=your_client_id
REDDIT_ADS_CLIENT_SECRET=your_client_secret
REDDIT_ADS_ACCOUNT_ID=t2_xxxxx
REDDIT_ADS_ACCESS_TOKEN=your_access_token
REDDIT_ADS_REFRESH_TOKEN=your_refresh_token
REDDIT_ADS_PIXEL_ID=your_pixel_id
```

---

## Best Practices

### Campaign Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  RECOMMENDED STRUCTURE                                          │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Campaign (by objective/product line)                           │
│  ├── Ad Group: Subreddit Targeting - Tech                      │
│  │   ├── Ad: Headline A + Image 1                              │
│  │   └── Ad: Headline B + Image 1                              │
│  ├── Ad Group: Subreddit Targeting - Business                  │
│  │   ├── Ad: Headline A + Image 1                              │
│  │   └── Ad: Headline B + Image 1                              │
│  └── Ad Group: Interest Targeting - Entrepreneurs              │
│      ├── Ad: Headline A + Image 2                              │
│      └── Ad: Headline B + Image 2                              │
│                                                                 │
│  • Separate ad groups by targeting type                         │
│  • Test 2-3 ad variations per ad group                          │
│  • Use clear naming conventions                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Naming Conventions

```
Campaign:  [Objective] - [Product/Brand] - [Date Range]
           Example: TRAFFIC - ProductX - Q1-2025

Ad Group:  [Targeting Type] - [Audience Description]
           Example: Subreddits - Tech Enthusiasts

Ad:        [Headline Type] - [Creative Version]
           Example: Problem-Solution - Image-A
```

### Rate Limiting

- **1 request per second** limit
- Implement exponential backoff for retries
- Batch operations where possible

```typescript
async function rateLimitedRequest<T>(
  fn: () => Promise<T>,
  retries = 3
): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try {
      await new Promise(resolve => setTimeout(resolve, 1000)); // 1 second delay
      return await fn();
    } catch (error: any) {
      if (error.status === 429 && i < retries - 1) {
        const delay = Math.pow(2, i) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## Complete Workflow Example

```typescript
// Full campaign creation workflow
async function createRedditAdCampaign(
  client: RedditAdsClient,
  config: {
    campaignName: string;
    dailyBudget: number;
    targetSubreddits: string[];
    headline: string;
    body: string;
    landingUrl: string;
    imageUrl: string;
  }
) {
  // 1. Create Campaign
  const campaign = await client.createCampaign({
    name: config.campaignName,
    objective: 'TRAFFIC',
    is_enabled: false, // Start paused for review
    budget_type: 'DAILY',
    budget_total_amount_micros: config.dailyBudget * 1_000_000,
    start_time: new Date().toISOString()
  });

  console.log(`Created campaign: ${campaign.id}`);

  // 2. Create Ad Group with targeting
  const adGroup = await client.createAdGroup({
    name: `${config.campaignName} - Subreddit Targeting`,
    campaign_id: campaign.id,
    is_enabled: true,
    bid_strategy: 'LOWEST_COST',
    goal_type: 'CLICKS',
    targeting: {
      communities: config.targetSubreddits,
      geo_locations: { countries: ['US'] },
      devices: ['DESKTOP', 'MOBILE']
    }
  });

  console.log(`Created ad group: ${adGroup.id}`);

  // 3. Create Ad
  const ad = await client.createAd({
    name: `${config.campaignName} - Ad v1`,
    ad_group_id: adGroup.id,
    is_enabled: true,
    type: 'LINK',
    headline: config.headline,
    body: config.body,
    url: config.landingUrl,
    call_to_action: 'LEARN_MORE',
    thumbnail_url: config.imageUrl
  });

  console.log(`Created ad: ${ad.id}`);

  return { campaign, adGroup, ad };
}

// Usage
const result = await createRedditAdCampaign(client, {
  campaignName: 'Product Launch - Jan 2025',
  dailyBudget: 50, // $50/day
  targetSubreddits: ['technology', 'gadgets', 'programming'],
  headline: 'Introducing the Future of Development',
  body: 'Join 50,000+ developers using our tool to ship faster.',
  landingUrl: 'https://yoursite.com?utm_source=reddit',
  imageUrl: 'https://yoursite.com/ad-image.jpg'
});
```

---

## Testing

### Test Checklist

- [ ] OAuth flow completes successfully
- [ ] Token refresh works before expiry
- [ ] Campaign creates with correct budget
- [ ] Ad group targeting is applied correctly
- [ ] Ad creative displays properly
- [ ] Conversion events tracked (use test_mode)
- [ ] Reports return expected metrics
- [ ] Rate limiting handled gracefully
- [ ] Error responses handled properly

### Mock API for Development

```typescript
// test/mocks/reddit-ads-mock.ts
import { rest } from 'msw';

export const redditAdsMocks = [
  rest.post('https://www.reddit.com/api/v1/access_token', (req, res, ctx) => {
    return res(ctx.json({
      access_token: 'mock_access_token',
      refresh_token: 'mock_refresh_token',
      expires_in: 3600,
      scope: 'adsread adsedit history'
    }));
  }),

  rest.get('https://ads-api.reddit.com/api/v2.0/accounts/:accountId', (req, res, ctx) => {
    return res(ctx.json({
      id: req.params.accountId,
      name: 'Test Account',
      currency: 'USD'
    }));
  }),

  rest.post('https://ads-api.reddit.com/api/v2.0/accounts/:accountId/campaigns', (req, res, ctx) => {
    return res(ctx.json({
      id: 'campaign_mock_123',
      ...req.body
    }));
  })
];
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid/expired token | Refresh access token |
| `403 Forbidden` | Account not whitelisted | Contact Reddit Ads support |
| `429 Too Many Requests` | Rate limit exceeded | Implement backoff, slow down |
| `400 Bad Request` | Invalid payload | Check required fields, data types |
| `Audience too small` | < 1,000 matched users | Add more users to audience |

---

---

## Agentic Optimization Service

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENTIC REDDIT ADS OPTIMIZER                                   │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  Scheduler  │───▶│  Analyzer   │───▶│  Optimizer  │         │
│  │  (Cron)     │    │  (AI/LLM)   │    │  (Actions)  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  Fetch      │    │  Decide     │    │  Execute    │         │
│  │  Reports    │    │  Strategy   │    │  Changes    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
│  Loop: Every 4-6 hours                                          │
│  Actions: Pause losers, scale winners, adjust bids, rotate ads  │
└─────────────────────────────────────────────────────────────────┘
```

### Background Service (Node.js)

```typescript
// services/reddit-ads-optimizer.ts
import Anthropic from '@anthropic-ai/sdk';
import { CronJob } from 'cron';
import RedditAdsClient from '../lib/reddit-ads-client';

interface OptimizationConfig {
  accountId: string;
  accessToken: string;
  refreshToken: string;
  // Thresholds
  minCTR: number;           // Pause ads below this CTR (e.g., 0.005 = 0.5%)
  maxCPA: number;           // Pause ads above this CPA
  minImpressions: number;   // Min impressions before decisions (e.g., 1000)
  budgetScaleFactor: number; // Scale winning ad groups by this factor (e.g., 1.5)
  // Optimization settings
  optimizationGoal: 'CLICKS' | 'CONVERSIONS' | 'ROAS';
  checkIntervalHours: number;
}

interface PerformanceData {
  campaignId: string;
  adGroupId: string;
  adId: string;
  impressions: number;
  clicks: number;
  spend: number;
  conversions: number;
  ctr: number;
  cpc: number;
  cpa: number;
  roas: number;
}

class RedditAdsOptimizerService {
  private client: RedditAdsClient;
  private anthropic: Anthropic;
  private config: OptimizationConfig;
  private cronJob: CronJob | null = null;

  constructor(config: OptimizationConfig) {
    this.config = config;
    this.client = new RedditAdsClient({
      accessToken: config.accessToken,
      accountId: config.accountId
    });
    this.anthropic = new Anthropic();
  }

  // Start the background optimization service
  start() {
    const cronSchedule = `0 */${this.config.checkIntervalHours} * * *`;

    this.cronJob = new CronJob(cronSchedule, async () => {
      console.log(`[${new Date().toISOString()}] Running optimization cycle...`);
      await this.runOptimizationCycle();
    });

    this.cronJob.start();
    console.log(`Reddit Ads Optimizer started. Running every ${this.config.checkIntervalHours} hours.`);
  }

  stop() {
    if (this.cronJob) {
      this.cronJob.stop();
      console.log('Reddit Ads Optimizer stopped.');
    }
  }

  // Main optimization cycle
  async runOptimizationCycle() {
    try {
      // 1. Fetch performance data
      const performanceData = await this.fetchPerformanceData();

      // 2. Analyze with AI agent
      const recommendations = await this.analyzeWithAgent(performanceData);

      // 3. Execute optimizations
      await this.executeOptimizations(recommendations);

      // 4. Log results
      await this.logOptimizationResults(recommendations);

    } catch (error) {
      console.error('Optimization cycle failed:', error);
      await this.sendAlert('Optimization cycle failed', error);
    }
  }

  // Fetch last 24h performance data
  private async fetchPerformanceData(): Promise<PerformanceData[]> {
    const endDate = new Date();
    const startDate = new Date(endDate.getTime() - 24 * 60 * 60 * 1000);

    const report = await this.client.getReport({
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
      level: 'AD',
      metrics: [
        'impressions', 'clicks', 'spend', 'conversions',
        'ctr', 'cpc', 'cpa', 'conversion_value'
      ]
    });

    return report.data.map((row: any) => ({
      campaignId: row.campaign_id,
      adGroupId: row.ad_group_id,
      adId: row.ad_id,
      impressions: row.impressions,
      clicks: row.clicks,
      spend: row.spend,
      conversions: row.conversions || 0,
      ctr: row.ctr,
      cpc: row.cpc,
      cpa: row.cpa || 0,
      roas: row.conversion_value ? row.conversion_value / row.spend : 0
    }));
  }

  // AI-powered analysis and decision making
  private async analyzeWithAgent(data: PerformanceData[]): Promise<OptimizationRecommendation[]> {
    const prompt = `You are a Reddit Ads optimization agent. Analyze the following campaign performance data and recommend specific actions.

## Performance Data (Last 24 Hours)
${JSON.stringify(data, null, 2)}

## Optimization Configuration
- Goal: ${this.config.optimizationGoal}
- Min CTR threshold: ${this.config.minCTR * 100}%
- Max CPA threshold: $${this.config.maxCPA}
- Min impressions for decisions: ${this.config.minImpressions}
- Budget scale factor for winners: ${this.config.budgetScaleFactor}x

## Your Task
Analyze each ad/ad group and recommend ONE action per item:
1. PAUSE - Poor performers (low CTR, high CPA, no conversions after sufficient impressions)
2. SCALE - Winners (high CTR, low CPA, good ROAS) - increase budget
3. ADJUST_BID - Moderate performers - suggest bid adjustment
4. KEEP - Insufficient data or acceptable performance
5. ROTATE_CREATIVE - Good targeting but ad fatigue (declining CTR over time)

Return a JSON array of recommendations:
[
  {
    "adId": "string",
    "adGroupId": "string",
    "action": "PAUSE|SCALE|ADJUST_BID|KEEP|ROTATE_CREATIVE",
    "reason": "Brief explanation",
    "newBidMicros": number (optional, for ADJUST_BID),
    "budgetMultiplier": number (optional, for SCALE)
  }
]

Be aggressive with pausing poor performers to protect budget. Be conservative with scaling (only clear winners).`;

    const response = await this.anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4096,
      messages: [{ role: 'user', content: prompt }]
    });

    const content = response.content[0];
    if (content.type !== 'text') throw new Error('Unexpected response type');

    // Extract JSON from response
    const jsonMatch = content.text.match(/\[[\s\S]*\]/);
    if (!jsonMatch) throw new Error('No JSON found in response');

    return JSON.parse(jsonMatch[0]);
  }

  // Execute the AI recommendations
  private async executeOptimizations(recommendations: OptimizationRecommendation[]) {
    for (const rec of recommendations) {
      try {
        switch (rec.action) {
          case 'PAUSE':
            await this.client.updateAd(rec.adId, { is_enabled: false });
            console.log(`Paused ad ${rec.adId}: ${rec.reason}`);
            break;

          case 'SCALE':
            const adGroup = await this.client.getAdGroup(rec.adGroupId);
            const currentBudget = adGroup.budget_total_amount_micros;
            const newBudget = Math.round(currentBudget * (rec.budgetMultiplier || this.config.budgetScaleFactor));
            await this.client.updateAdGroup(rec.adGroupId, {
              budget_total_amount_micros: newBudget
            });
            console.log(`Scaled ad group ${rec.adGroupId} budget to ${newBudget / 1_000_000}: ${rec.reason}`);
            break;

          case 'ADJUST_BID':
            if (rec.newBidMicros) {
              await this.client.updateAdGroup(rec.adGroupId, {
                bid_amount_micros: rec.newBidMicros
              });
              console.log(`Adjusted bid for ${rec.adGroupId} to ${rec.newBidMicros / 1_000_000}: ${rec.reason}`);
            }
            break;

          case 'ROTATE_CREATIVE':
            // Flag for creative refresh (implement your creative rotation logic)
            console.log(`Creative rotation needed for ${rec.adId}: ${rec.reason}`);
            await this.flagForCreativeRefresh(rec.adId);
            break;

          case 'KEEP':
            // No action needed
            break;
        }
      } catch (error) {
        console.error(`Failed to execute ${rec.action} for ${rec.adId}:`, error);
      }
    }
  }

  private async flagForCreativeRefresh(adId: string) {
    // Implement: Add to queue, notify team, or auto-generate new creative
  }

  private async logOptimizationResults(recommendations: OptimizationRecommendation[]) {
    const summary = {
      timestamp: new Date().toISOString(),
      totalRecommendations: recommendations.length,
      actions: {
        paused: recommendations.filter(r => r.action === 'PAUSE').length,
        scaled: recommendations.filter(r => r.action === 'SCALE').length,
        bidAdjusted: recommendations.filter(r => r.action === 'ADJUST_BID').length,
        creativeRotation: recommendations.filter(r => r.action === 'ROTATE_CREATIVE').length,
        kept: recommendations.filter(r => r.action === 'KEEP').length
      }
    };
    console.log('Optimization Summary:', JSON.stringify(summary, null, 2));
    // Store in database for historical analysis
  }

  private async sendAlert(subject: string, error: any) {
    // Implement: Send email/Slack notification
  }
}

interface OptimizationRecommendation {
  adId: string;
  adGroupId: string;
  action: 'PAUSE' | 'SCALE' | 'ADJUST_BID' | 'KEEP' | 'ROTATE_CREATIVE';
  reason: string;
  newBidMicros?: number;
  budgetMultiplier?: number;
}

export default RedditAdsOptimizerService;
```

### Background Service (Python)

```python
# services/reddit_ads_optimizer.py
import anthropic
import schedule
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from lib.reddit_ads_client import RedditAdsClient, RedditAdsConfig

class OptimizationAction(Enum):
    PAUSE = "PAUSE"
    SCALE = "SCALE"
    ADJUST_BID = "ADJUST_BID"
    KEEP = "KEEP"
    ROTATE_CREATIVE = "ROTATE_CREATIVE"

@dataclass
class OptimizationConfig:
    account_id: str
    access_token: str
    refresh_token: str
    min_ctr: float = 0.005  # 0.5%
    max_cpa: float = 50.0
    min_impressions: int = 1000
    budget_scale_factor: float = 1.5
    optimization_goal: str = "CONVERSIONS"
    check_interval_hours: int = 4

@dataclass
class PerformanceData:
    campaign_id: str
    ad_group_id: str
    ad_id: str
    impressions: int
    clicks: int
    spend: float
    conversions: int
    ctr: float
    cpc: float
    cpa: float
    roas: float

@dataclass
class OptimizationRecommendation:
    ad_id: str
    ad_group_id: str
    action: OptimizationAction
    reason: str
    new_bid_micros: Optional[int] = None
    budget_multiplier: Optional[float] = None

class RedditAdsOptimizerService:
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.client = RedditAdsClient(RedditAdsConfig(
            access_token=config.access_token,
            account_id=config.account_id
        ))
        self.anthropic = anthropic.Anthropic()
        self._running = False

    def start(self):
        """Start the background optimization service."""
        self._running = True

        # Schedule optimization runs
        schedule.every(self.config.check_interval_hours).hours.do(
            self.run_optimization_cycle
        )

        print(f"Reddit Ads Optimizer started. Running every {self.config.check_interval_hours} hours.")

        # Run immediately on start
        self.run_optimization_cycle()

        # Keep running
        while self._running:
            schedule.run_pending()
            time.sleep(60)

    def stop(self):
        """Stop the optimization service."""
        self._running = False
        print("Reddit Ads Optimizer stopped.")

    def run_optimization_cycle(self):
        """Main optimization cycle."""
        print(f"[{datetime.now().isoformat()}] Running optimization cycle...")

        try:
            # 1. Fetch performance data
            performance_data = self._fetch_performance_data()

            # 2. Analyze with AI agent
            recommendations = self._analyze_with_agent(performance_data)

            # 3. Execute optimizations
            self._execute_optimizations(recommendations)

            # 4. Log results
            self._log_optimization_results(recommendations)

        except Exception as e:
            print(f"Optimization cycle failed: {e}")
            self._send_alert("Optimization cycle failed", str(e))

    def _fetch_performance_data(self) -> List[PerformanceData]:
        """Fetch last 24h performance data."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        report = self.client.get_report({
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'level': 'AD',
            'metrics': [
                'impressions', 'clicks', 'spend', 'conversions',
                'ctr', 'cpc', 'cpa', 'conversion_value'
            ]
        })

        return [
            PerformanceData(
                campaign_id=row['campaign_id'],
                ad_group_id=row['ad_group_id'],
                ad_id=row['ad_id'],
                impressions=row['impressions'],
                clicks=row['clicks'],
                spend=row['spend'],
                conversions=row.get('conversions', 0),
                ctr=row['ctr'],
                cpc=row['cpc'],
                cpa=row.get('cpa', 0),
                roas=row.get('conversion_value', 0) / row['spend'] if row['spend'] > 0 else 0
            )
            for row in report.get('data', [])
        ]

    def _analyze_with_agent(self, data: List[PerformanceData]) -> List[OptimizationRecommendation]:
        """AI-powered analysis and decision making."""

        prompt = f"""You are a Reddit Ads optimization agent. Analyze the following campaign performance data and recommend specific actions.

## Performance Data (Last 24 Hours)
{json.dumps([vars(d) for d in data], indent=2)}

## Optimization Configuration
- Goal: {self.config.optimization_goal}
- Min CTR threshold: {self.config.min_ctr * 100}%
- Max CPA threshold: ${self.config.max_cpa}
- Min impressions for decisions: {self.config.min_impressions}
- Budget scale factor for winners: {self.config.budget_scale_factor}x

## Your Task
Analyze each ad/ad group and recommend ONE action per item:
1. PAUSE - Poor performers (low CTR, high CPA, no conversions after sufficient impressions)
2. SCALE - Winners (high CTR, low CPA, good ROAS) - increase budget
3. ADJUST_BID - Moderate performers - suggest bid adjustment
4. KEEP - Insufficient data or acceptable performance
5. ROTATE_CREATIVE - Good targeting but ad fatigue (declining CTR over time)

Return a JSON array of recommendations:
[
  {{
    "ad_id": "string",
    "ad_group_id": "string",
    "action": "PAUSE|SCALE|ADJUST_BID|KEEP|ROTATE_CREATIVE",
    "reason": "Brief explanation",
    "new_bid_micros": number (optional, for ADJUST_BID),
    "budget_multiplier": number (optional, for SCALE)
  }}
]

Be aggressive with pausing poor performers to protect budget. Be conservative with scaling (only clear winners)."""

        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text

        # Extract JSON from response
        import re
        json_match = re.search(r'\[[\s\S]*\]', content)
        if not json_match:
            raise ValueError("No JSON found in response")

        recommendations_data = json.loads(json_match.group())

        return [
            OptimizationRecommendation(
                ad_id=r['ad_id'],
                ad_group_id=r['ad_group_id'],
                action=OptimizationAction(r['action']),
                reason=r['reason'],
                new_bid_micros=r.get('new_bid_micros'),
                budget_multiplier=r.get('budget_multiplier')
            )
            for r in recommendations_data
        ]

    def _execute_optimizations(self, recommendations: List[OptimizationRecommendation]):
        """Execute the AI recommendations."""
        for rec in recommendations:
            try:
                if rec.action == OptimizationAction.PAUSE:
                    self.client.update_ad(rec.ad_id, {'is_enabled': False})
                    print(f"Paused ad {rec.ad_id}: {rec.reason}")

                elif rec.action == OptimizationAction.SCALE:
                    ad_group = self.client.get_ad_group(rec.ad_group_id)
                    current_budget = ad_group['budget_total_amount_micros']
                    multiplier = rec.budget_multiplier or self.config.budget_scale_factor
                    new_budget = int(current_budget * multiplier)
                    self.client.update_ad_group(rec.ad_group_id, {
                        'budget_total_amount_micros': new_budget
                    })
                    print(f"Scaled ad group {rec.ad_group_id} budget to ${new_budget / 1_000_000}: {rec.reason}")

                elif rec.action == OptimizationAction.ADJUST_BID:
                    if rec.new_bid_micros:
                        self.client.update_ad_group(rec.ad_group_id, {
                            'bid_amount_micros': rec.new_bid_micros
                        })
                        print(f"Adjusted bid for {rec.ad_group_id}: {rec.reason}")

                elif rec.action == OptimizationAction.ROTATE_CREATIVE:
                    print(f"Creative rotation needed for {rec.ad_id}: {rec.reason}")
                    self._flag_for_creative_refresh(rec.ad_id)

            except Exception as e:
                print(f"Failed to execute {rec.action} for {rec.ad_id}: {e}")

    def _flag_for_creative_refresh(self, ad_id: str):
        """Flag ad for creative refresh."""
        # Implement: Add to queue, notify team, or auto-generate new creative
        pass

    def _log_optimization_results(self, recommendations: List[OptimizationRecommendation]):
        """Log optimization results."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_recommendations': len(recommendations),
            'actions': {
                'paused': len([r for r in recommendations if r.action == OptimizationAction.PAUSE]),
                'scaled': len([r for r in recommendations if r.action == OptimizationAction.SCALE]),
                'bid_adjusted': len([r for r in recommendations if r.action == OptimizationAction.ADJUST_BID]),
                'creative_rotation': len([r for r in recommendations if r.action == OptimizationAction.ROTATE_CREATIVE]),
                'kept': len([r for r in recommendations if r.action == OptimizationAction.KEEP]),
            }
        }
        print(f"Optimization Summary: {json.dumps(summary, indent=2)}")

    def _send_alert(self, subject: str, error: str):
        """Send alert notification."""
        # Implement: Send email/Slack notification
        pass


# Entry point for running as background service
if __name__ == "__main__":
    import os

    config = OptimizationConfig(
        account_id=os.environ['REDDIT_ADS_ACCOUNT_ID'],
        access_token=os.environ['REDDIT_ADS_ACCESS_TOKEN'],
        refresh_token=os.environ['REDDIT_ADS_REFRESH_TOKEN'],
        min_ctr=0.005,
        max_cpa=50.0,
        min_impressions=1000,
        budget_scale_factor=1.5,
        optimization_goal="CONVERSIONS",
        check_interval_hours=4
    )

    optimizer = RedditAdsOptimizerService(config)
    optimizer.start()
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "services/reddit_ads_optimizer.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  reddit-ads-optimizer:
    build: .
    container_name: reddit-ads-optimizer
    restart: unless-stopped
    environment:
      - REDDIT_ADS_CLIENT_ID=${REDDIT_ADS_CLIENT_ID}
      - REDDIT_ADS_CLIENT_SECRET=${REDDIT_ADS_CLIENT_SECRET}
      - REDDIT_ADS_ACCOUNT_ID=${REDDIT_ADS_ACCOUNT_ID}
      - REDDIT_ADS_ACCESS_TOKEN=${REDDIT_ADS_ACCESS_TOKEN}
      - REDDIT_ADS_REFRESH_TOKEN=${REDDIT_ADS_REFRESH_TOKEN}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Optimization Strategies

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENTIC OPTIMIZATION STRATEGIES                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PERFORMANCE-BASED PAUSING                                   │
│     ─────────────────────────────────────────────────────────  │
│     IF impressions > 1000 AND ctr < 0.3% → PAUSE               │
│     IF impressions > 500 AND conversions = 0 → PAUSE           │
│     IF cpa > 2x target → PAUSE                                  │
│                                                                 │
│  2. WINNER SCALING                                              │
│     ─────────────────────────────────────────────────────────  │
│     IF ctr > 1% AND cpa < target AND conversions > 5           │
│     → SCALE budget by 1.5x                                      │
│     Cap at 3x original budget to manage risk                    │
│                                                                 │
│  3. BID OPTIMIZATION                                            │
│     ─────────────────────────────────────────────────────────  │
│     IF position low AND ctr good → INCREASE bid 10-20%         │
│     IF cpa high but converting → DECREASE bid 10-15%           │
│                                                                 │
│  4. CREATIVE FATIGUE DETECTION                                  │
│     ─────────────────────────────────────────────────────────  │
│     IF ctr declining 3 consecutive days → ROTATE_CREATIVE      │
│     IF frequency > 3 → ROTATE_CREATIVE                          │
│                                                                 │
│  5. BUDGET REALLOCATION                                         │
│     ─────────────────────────────────────────────────────────  │
│     Move budget from paused ads to scaled winners              │
│     Maintain total daily budget cap                             │
└─────────────────────────────────────────────────────────────────┘
```

### Advanced: Multi-Agent Optimization

```typescript
// services/multi-agent-optimizer.ts
import Anthropic from '@anthropic-ai/sdk';

interface AgentRole {
  name: string;
  systemPrompt: string;
}

const AGENTS: AgentRole[] = [
  {
    name: 'Performance Analyst',
    systemPrompt: `You analyze Reddit Ads performance data. Identify:
    - Top performers (high CTR, low CPA, good ROAS)
    - Poor performers (low CTR, high CPA, no conversions)
    - Trends (improving, declining, stable)
    Output structured analysis with confidence scores.`
  },
  {
    name: 'Budget Strategist',
    systemPrompt: `You optimize budget allocation across campaigns.
    Given performance analysis, recommend:
    - Budget increases for winners (max 50% increase)
    - Budget decreases for losers
    - Reallocation between ad groups
    Protect total budget while maximizing ROI.`
  },
  {
    name: 'Creative Director',
    systemPrompt: `You evaluate ad creative performance.
    Identify ads with:
    - Creative fatigue (declining engagement)
    - High potential but poor execution
    - A/B test winners
    Recommend creative refreshes and new variations.`
  },
  {
    name: 'Risk Manager',
    systemPrompt: `You ensure optimization safety.
    Review recommendations and flag:
    - Overly aggressive scaling
    - Insufficient data for decisions
    - Budget concentration risk
    - Compliance concerns
    Approve, modify, or reject recommendations.`
  }
];

class MultiAgentOptimizer {
  private anthropic: Anthropic;

  constructor() {
    this.anthropic = new Anthropic();
  }

  async runAgentPipeline(performanceData: any) {
    let context = { performanceData };

    // Run agents in sequence, each building on previous output
    for (const agent of AGENTS) {
      const response = await this.anthropic.messages.create({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 4096,
        system: agent.systemPrompt,
        messages: [{
          role: 'user',
          content: `Previous context:\n${JSON.stringify(context, null, 2)}\n\nProvide your analysis and recommendations.`
        }]
      });

      context = {
        ...context,
        [agent.name.toLowerCase().replace(' ', '_')]: response.content[0]
      };
    }

    return context;
  }
}
```

### Monitoring Dashboard Data

```typescript
// api/optimization-stats.ts
interface OptimizationStats {
  period: string;
  totalOptimizations: number;
  actionBreakdown: {
    paused: number;
    scaled: number;
    bidAdjusted: number;
    creativeRotated: number;
  };
  performanceImpact: {
    ctrChange: number;
    cpaChange: number;
    roasChange: number;
    spendEfficiency: number;
  };
  budgetSaved: number;
  revenueIncreased: number;
}

async function getOptimizationStats(
  startDate: Date,
  endDate: Date
): Promise<OptimizationStats> {
  // Query optimization logs and performance data
  // Calculate before/after metrics
  // Return aggregated stats
}
```

---

## Resources

- [Reddit Ads API Docs](https://ads-api.reddit.com/docs/)
- [Reddit Developer Portal](https://www.reddit.com/prefs/apps/)
- [Reddit Ads Help Center](https://business.reddithelp.com/s/article/Reddit-Ads-API)
- [OAuth2 Documentation](https://www.reddit.com/dev/api/oauth/)
