# Phase 1: Critical Fixes - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning
**Source:** /gsd-plan-phase via REQUIREMENTS.md + ROADMAP.md

<domain>
## Phase Boundary

Phase 1 addresses critical reliability and API correctness issues in the existing v0.1.0 scraper service:

1. **Error Response Status Codes** - Fix the API to return proper HTTP 4xx/5xx status codes instead of 200 with error in body
2. **Rate Limiting** - Add protection against abuse of expensive scraping + LLM operations
3. **Retry Logic** - Add exponential backoff for transient Crawl4AI failures
4. **Hardcoded Empty URLs** - Extract and return actual source URLs from scraped pages

</domain>

<decisions>
## Implementation Decisions

### R1: Error Response Status Codes
- **Locked Decision:** API endpoints MUST return proper HTTP status codes (4xx for client errors, 5xx for server errors)
- **Locked Decision:** Use FastAPI's exception handling mechanism (HTTPException, APIException)
- **Decision ID:** D-01

### R2: Rate Limiting
- **Locked Decision:** Implement rate limiting on `/search` endpoint
- **Locked Decision:** Use `slowapi` library for FastAPI rate limiting
- **Decision ID:** D-02

### R3: Retry Logic for Scraping
- **Locked Decision:** Add retry mechanism with exponential backoff for Crawl4AI calls
- **Locked Decision:** Handle transient network failures gracefully with appropriate exceptions
- **Decision ID:** D-03

### R4: Fix Hardcoded Empty URLs
- **Locked Decision:** Results MUST include valid source URLs from scraped pages
- **Locked Decision:** URLs must be extracted from the actual scraped content, not hardcoded
- **Decision ID:** D-04

### the agent's Discretion
- Implementation approach for error handling (which exceptions to use, how to structure error responses)
- Rate limiting thresholds and configuration (requests per minute/hour)
- Retry parameters (max retries, initial delay, max delay, backoff factor)
- How to extract URLs from each source (Bonpreu, Lidl, Idealista) - may differ per scraper

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Existing Code Patterns
- `main.py` — FastAPI app structure, current endpoint implementation
- `models.py` — Pydantic models for request/response (SearchRequest, SearchResponse, SearchResult)
- `scrapers/base.py` — Abstract Scraper base class
- `scrapers/__init__.py` — Scraper registry (SCRAPERS dict)

### Configuration
- `config.py` — Settings class structure
- `.env.example` — Environment variable template

### Architecture
- `.planning/codebase/ARCHITECTURE.md` — Full architecture documentation

</canonical_refs>

<specifics>
## Specific Ideas

### Error Handling Pattern
- Use `HTTPException(status_code=400, detail="...")` for client errors
- Use `HTTPException(status_code=500, detail="...")` for server errors
- Return `ErrorResponse` model in body when appropriate

### Rate Limiting Options
- `slowapi` is already in stack (referenced in ROADMAP)
- Consider: 10 requests/minute, 100 requests/hour as starting points

### Retry Pattern
- Use `tenacity` library or custom asyncio retry logic
- Exponential backoff: start with 1s, max 30s, factor 2

### URL Extraction
- Each scraper constructs URLs - ensure they're returned in results
- Check how search results are constructed in each scraper

</specifics>

<deferred>
## Deferred Ideas

- None — Phase 1 scope is fixed by requirements

</deferred>

---

*Phase: 01-critical-fixes*
*Context gathered: 2026-03-26*