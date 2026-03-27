# Requirements

## Current State

The Scraper Service is a functional brownfield project at v0.1.0. It provides a REST API for scraping supermarket and real estate data but has several issues that need addressing.

## Requirements

### Phase 1: Critical Fixes

#### R1: Fix Error Response Status Codes
- Return appropriate HTTP status codes (4xx/5xx) instead of 200 with error in body
- Use FastAPI's exception handling properly

#### R2: Add Rate Limiting
- Implement rate limiting on `/search` endpoint
- Protect against abuse of expensive scraping + LLM calls

#### R3: Add Retry Logic for Scraping
- Add retry mechanism with exponential backoff for Crawl4AI calls
- Handle transient network failures gracefully

#### R4: Fix Hardcoded Empty URLs
- Extract and return actual URLs from scraped pages
- Include source URLs in search results

### Phase 2: Stability & Performance

#### R5: Connection Pooling
- Use singleton pattern for AsyncWebCrawler
- Reduce latency and resource usage

#### R6: Add Idealista Sale Support
- Support both rental and sale property searches
- Add operation type parameter

#### R7: LLM Response Caching
- Cache LLM responses to reduce API calls
- Implement in-memory or Redis-based cache

#### R8: Request Tracing
- Add correlation IDs to trace requests
- Implement request ID middleware

### Phase 3: Testing & Documentation

#### R9: Integration Tests for Scrapers
- Add integration tests with mocked responses
- Cover all scraper classes

#### R10: Add Idealista Tests
- Create test file for Idealista scraper

#### R11: Input Validation
- Validate source parameter with Pydantic enum
- Add URL validation for SSRF prevention

### Non-Functional Requirements

- **Performance:** Response time < 5s for typical queries
- **Reliability:** 99.9% uptime target
- **Security:** No sensitive data logging, proper API key handling
- **Maintainability:** Code coverage > 70%

## Acceptance Criteria

- [ ] Error responses return proper HTTP status codes
- [ ] Rate limiting prevents abuse
- [ ] Scraping retries on transient failures
- [ ] Results include valid source URLs
- [ ] Connection pooling reduces latency
- [ ] Idealista supports both rent and sale
- [ ] LLM responses are cached
- [ ] Request tracing enables debugging
- [ ] Integration tests cover scrapers
- [ ] Source parameter is validated