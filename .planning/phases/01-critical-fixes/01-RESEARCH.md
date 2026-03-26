# Phase 1: Critical Fixes - Research

**Researched:** 2026-03-26
**Status:** Ready for planning

## Research Questions

1. **How to implement rate limiting in FastAPI?**
2. **How to add retry logic with exponential backoff for async operations?**
3. **How to extract URLs from Crawl4AI results?**

---

## Finding 1: FastAPI Rate Limiting with SlowAPI

### Library Selection
- **Chosen:** SlowAPI (`slowapi`) — de facto standard for FastAPI rate limiting
- **Alternative considered:** custom middleware (more complex, less tested)

### Implementation Approach

**Installation:**
```bash
uv add slowapi
```

**Setup Pattern (from Context7):**
```python
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

# Add exception handler for rate limit exceeded
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

**Usage on Endpoints:**
```python
@app.post("/search")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def search(request: Request, ...):
    # Note: route decorator must be ABOVE limit decorator
    pass
```

### Configuration Options

| Limit | Description |
|-------|-------------|
| `"5/minute"` | 5 requests per minute |
| `"100/hour"` | 100 requests per hour |
| `"1000/day"` | 1000 requests per day |
| `"10/minute", "100/hour"` | Multiple limits (AND logic) |

### Key Functions
- `get_remote_address` — Use client IP (default)
- Custom: `get_api_key(request)` — Rate limit by API key header
- Custom: `get_user_id(request)` — Rate limit by authenticated user

---

## Finding 2: Async Retry Logic with Tenacity

### Library Selection
- **Chosen:** Tenacity (`tenacity`) — battle-tested, supports async
- **Alternative:** Custom asyncio retry (more code, less features)

### Implementation Approach

**Installation:**
```bash
uv add tenacity
```

**Basic Pattern (from Context7):**
```python
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
async def async_operation():
    # Exponential backoff: 2^1=2s, 2^2=4s, 2^3=8s, then capped at 10s
    pass
```

### Configuration Options

| Parameter | Description |
|-----------|-------------|
| `multiplier` | Base multiplier for 2^x (default: 1) |
| `min` | Minimum wait in seconds (default: 4) |
| `max` | Maximum wait in seconds (default: 10) |
| `stop=stop_after_attempt(N)` | Max attempts before giving up |
| `retry_on=retry_if_exception_type(...)` | Which exceptions trigger retry |

### Complete Example
```python
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((ConnectionError, TimeoutError))
)
async def crawl_with_retry(url: str) -> CrawlResult:
    async with AsyncWebCrawler() as crawler:
        return await crawler.arun(url=url)
```

---

## Finding 3: URL Extraction from Crawl4AI Results

### CrawlResult Object Structure

From Context7 documentation, the `CrawlResult` object contains:
```python
result.success        # bool - crawl success status
result.url            # str - original URL
result.status_code    # int - HTTP status
result.markdown       # obj - markdown content (raw_markdown, fit_markdown)
result.links          # dict - internal and external links
result.media          # dict - images, videos, audio
result.error_message  # str - error details if failed
```

### Extracting Links

```python
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url=url)
    
    if result.success:
        # Internal links (same domain)
        internal_links = result.links.get("internal", [])
        
        # External links (different domain)
        external_links = result.links.get("external", [])
        
        # Each link is a dict with:
        # { "href": "...", "text": "...", "title": "...", "context": "...", "domain": "..." }
```

### URL Extraction Strategy

To fix the hardcoded empty URLs (R4), the scrapers should:

1. **Pass the crawl result to LLM extraction** — Include URLs from `result.links` in the extraction prompt
2. **Parse URLs from markdown** — If LLM doesn't extract URLs, extract from result.links
3. **Match results to URLs** — Use position/index to correlate LLM results with URLs

**Implementation pattern:**
```python
async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
    # ... crawl ...
    result = await crawler.arun(url=url)
    
    # Extract internal links for product URLs
    internal_links = result.links.get("internal", [])
    
    # Pass to LLM or post-process to assign URLs to results
    products = await extract_products_from_markdown(markdown, query, internal_links)
    
    # If LLM doesn't return URLs, map results to links by position
    for i, product in enumerate(products):
        if not product.url and i < len(internal_links):
            product.url = internal_links[i]["href"]
    
    return products[:limit]
```

---

## Architecture Recommendations

### Phase 1 Implementation Plan

1. **Error Response (R1)** — Already mostly correct in main.py, but exception handler returns 200 with ErrorResponse. Change to raise HTTPException for 5xx errors.

2. **Rate Limiting (R2)** — Add SlowAPI to main.py with `@limiter.limit("10/minute")` on `/search` endpoint

3. **Retry Logic (R3)** — Wrap AsyncWebCrawler calls in scrapers with tenacity retry decorator

4. **URL Extraction (R4)** — Extract URLs from `result.links` and pass to LLM or post-process results

### Dependencies to Add

```toml
# pyproject.toml additions
dependencies = [
    "slowapi>=0.1.0",
    "tenacity>=8.0.0",
]
```

---

## Validation Architecture

For Nyquist validation, the plans should include verification criteria:

| Requirement | Verification |
|-------------|---------------|
| R1: Error status codes | Test: `curl -X POST /search -d '{}'` returns 422 or 500, not 200 |
| R2: Rate limiting | Test: Send 11 requests in 1 minute, 11th returns 429 |
| R3: Retry logic | Test: Simulate transient failure, verify 3 retry attempts |
| R4: URL extraction | Test: Search returns results with non-empty `url` field |

---

*Research completed: 2026-03-26*