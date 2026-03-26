# Roadmap

## Project: Scraper Service

**Type:** Brownfield microservice improvement  
**Current:** v0.1.0 - Functional but has critical issues

---

## Phase 1: Critical Fixes

**Duration:** 1-2 days  
**Goal:** Fix critical API and reliability issues

### Tasks

1. **T1:** Fix error response status codes - Return proper HTTP 4xx/5xx instead of 200 with error body
2. **T2:** Add rate limiting - Use slowapi or similar to protect expensive operations
3. **T3:** Add retry logic for scraping - Implement exponential backoff for Crawl4AI calls
4. **T4:** Fix hardcoded empty URLs - Extract actual URLs from scraped pages

### Verification
- Error responses return appropriate status codes
- Rate limiting triggers after threshold
- Transient failures retry automatically
- Results contain valid source URLs

---

## Phase 2: Stability & Performance

**Duration:** 2-3 days  
**Goal:** Improve performance and add missing features

### Tasks

5. **T5:** Connection pooling - Singleton AsyncWebCrawler to reduce latency
6. **T6:** Add Idealista sale support - Add operation type (rent/sale) parameter
7. **T7:** LLM response caching - Cache responses in memory
8. **T8:** Request tracing - Add correlation IDs via middleware

### Verification
- Response time < 5s for typical queries
- Both rent and sale searches work
- Repeated queries hit cache
- Request IDs appear in logs

---

## Phase 3: Testing & Polish

**Duration:** 1-2 days  
**Goal:** Complete testing coverage and input validation

### Tasks

9. **T9:** Integration tests for scrapers - Add mocked HTTP response tests
10. **T10:** Add Idealista tests - Create test file
11. **T11:** Input validation - Pydantic enum for sources, URL validation

### Verification
- All scrapers have tests
- >70% code coverage
- Source parameter validated at request level

---

## Summary

| Phase | Tasks | Duration |
|-------|-------|----------|
| 1 - Critical | 4 | 1-2 days |
| 2 - Stability | 4 | 2-3 days |
| 3 - Testing | 3 | 1-2 days |
| **Total** | **11** | **4-7 days** |

---

## Next Step

Run `/gsd-plan-phase 1` to begin executing Phase 1 tasks.