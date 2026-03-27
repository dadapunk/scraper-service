# Codebase Concerns

**Analysis Date:** 2026-03-26

## API Design Issues

**Inconsistent Error Response Status Code:**
- Issue: When a scraper fails, the endpoint returns an `ErrorResponse` with HTTP 200 status instead of an appropriate error code (5xx or 4xx)
- Files: `main.py` (lines 37-44)
- Impact: Clients cannot distinguish between successful responses with empty results and actual failures. The error is hidden in the response body.
- Fix approach: Return appropriate HTTP status codes (500 for scraper errors, 400 for invalid requests) instead of embedding errors in 200 responses.

**Unvalidated Source Parameter:**
- Issue: The source parameter is only checked for membership in SCRAPERS dict after being lowercased. No validation prevents potential edge cases.
- Files: `main.py` (line 23-24)
- Impact: Minor - currently only allows known sources, but error handling could be clearer.
- Fix approach: Use a Pydantic enum or literal type for source validation.

## Security Considerations

**No Input Validation for URLs:**
- Issue: User-provided query is URL-encoded and used to construct external URLs. No validation prevents potential SSRF-like behavior.
- Files: `scrapers/supermarkets/bonpreu.py` (line 13), `scrapers/supermarkets/lidl.py` (line 14), `scrapers/realestate/idealista.py` (line 27)
- Impact: Service makes HTTP requests to attacker-controlled URLs if query contains special characters or if base URL is manipulated.
- Fix approach: Validate that constructed URLs start with expected base domains before making requests.

**Hardcoded Empty URLs:**
- Issue: All search results return `url=""` - no actual URLs to the scraped items are provided
- Files: `llm.py` (line 94), `llm.py` (line 187)
- Impact: Clients cannot link back to the actual source pages
- Fix approach: Extract and return the original URLs from the scraped pages

**No Rate Limiting:**
- Issue: No rate limiting or throttling on the `/search` endpoint
- Files: `main.py`
- Impact: Service is vulnerable to abuse, especially expensive scraping + LLM calls
- Fix approach: Implement rate limiting middleware (e.g., slowapi)

**LLM API Key Exposure Risk:**
- Issue: API key is stored in environment and passed to LLM with minimal validation
- Files: `config.py`, `llm.py`
- Impact: If configuration is misconfigured or key leaks, external calls could be made
- Fix approach: Add request-time validation that API key is present and valid format

## Error Handling Gaps

**No Retry Logic for Web Scraping:**
- Issue: Only LLM calls have retry logic (for quota errors). Web scraping (Crawl4AI) has no retry mechanism.
- Files: `scrapers/supermarkets/bonpreu.py`, `scrapers/supermarkets/lidl.py`, `scrapers/realestate/idealista.py`
- Impact: Transient network failures or temporary site issues cause immediate failures
- Fix approach: Add retry logic with exponential backoff for crawler failures

**Silent Failure in Error Response:**
- Issue: When `search()` raises an exception, the error is logged but an empty result set is returned with error message
- Files: `main.py` (lines 37-44)
- Impact: Partial failures are not clearly communicated; may confuse API consumers
- Fix approach: Consider returning partial results when available, not just error or success

## Performance Bottlenecks

**No Connection Pooling:**
- Issue: Each request creates a new `AsyncWebCrawler` instance. This is expensive as it initializes browser context.
- Files: `scrapers/supermarkets/bonpreu.py` (lines 16-21), similar in lidl.py and idealista.py
- Impact: High latency per request, potential resource exhaustion under load
- Fix approach: Use a singleton pattern or connection pool for the crawler

**No LLM Response Caching:**
- Issue: Identical queries result in repeated LLM calls
- Files: `llm.py`
- Impact: Wasted API quota and latency for repeated searches
- Fix approach: Implement caching (e.g., Redis or in-memory) for LLM responses

**No Request Timeout for LLM:**
- Issue: LLM timeout is set to 60 seconds but there's no distinction between different operation types
- Files: `llm.py` (lines 47, 144)
- Impact: Long-running requests can block resources
- Fix approach: Consider different timeouts for different operations, add request queuing

## Idealista Scraper Limitations

**Hardcoded Rental Search:**
- Issue: Idealista scraper only supports rental properties (`/alquiler-viviendas/`). Sale properties not supported.
- Files: `scrapers/realestate/idealista.py` (line 27)
- Impact: Users cannot search for properties for sale
- Fix approach: Add operation type parameter (rent/sale) and construct appropriate URL path

## Testing Gaps

**No Integration Tests for Scrapers:**
- Issue: No tests that actually test the scraper classes with real or mocked HTTP responses
- Files: `tests/` - only unit tests for API and LLM
- Impact: Scrapers may fail in production without detection
- Fix approach: Add integration tests with mocked crawler responses

**No Tests for Idealista:**
- Issue: Idealista scraper has no dedicated test file
- Files: `scrapers/realestate/idealista.py`
- Impact: Changes to Idealista scraping break undetected
- Fix approach: Add test file similar to `test_bonpreu.py` and `test_lidl.py`

## Logging Concerns

**Inconsistent Logging:**
- Issue: `main.py` uses module logger, but `llm.py` imports logging inside functions for some calls
- Files: `llm.py` (lines 71-77, 168-174)
- Impact: Log entries scattered, harder to trace requests
- Fix approach: Use consistent logger configuration at module level

**No Request Tracing:**
- Issue: No request IDs or correlation IDs to trace requests through the system
- Files: `main.py`
- Impact: Difficult to debug issues in production
- Fix approach: Add request ID middleware and propagate through all operations

---

*Concerns audit: 2026-03-26*
