# Phase 02: Mercadona Scraper - Context

**Date:** 2026-03-26

## Decisions (Locked - Do Not Change)

### D1: Scraping Approach
- **Use Crawl4AI** with standard headless browser (same as Bonpreu/Lidl)
- Don't attempt custom anti-bot solutions without testing first

### D2: URL Pattern
- **Algolia API** (not HTML scraping): `https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_vlc1_es/query`
- This is what Mercadona's frontend actually uses
- Alternative: scrape `https://tienda.mercadona.es/buscar?q={query}` for fallback
- Region: Default to Valencia (`vlc1`) - can be made configurable later

### D3: Data Model
- **Reuse `SupermarketResult`** from `models.py`
- Fields: `title`, `price`, `unit`, `unit_price`, `brand`, `url`

### D4: LLM Extraction
- **Reuse existing prompt** in `llm.py:extract_products_from_markdown`
- It's already in Spanish and handles supermarket products

### D5: File Location
- **Create:** `scrapers/supermarkets/mercadona.py`
- **Add to:** `scrapers/__init__.py` registry
- **Add tests:** `tests/test_mercadona.py`

## the agent's Discretion (Research & Recommend)

### Gray Areas to Resolve

1. **Algolia API key** - Is it public or needs extraction from frontend?
   - Research: Check if API is accessible without auth
   - If blocked: Fall back to HTML scraping of search page

2. **Postal code requirement** - Mercadona results depend on location
   - Option A: Use default Valencia region
   - Option B: Accept postal_code parameter in search
   - Recommend: Start with default, add parameter in Phase 2

3. **Anti-bot challenges** - Mercadona may block headless browsers
   - Test with standard Crawl4AI first
   - If blocked: Add stealth browser args (user-agent, etc.)

## Deferred Ideas (Out of Scope)

- Postal code selection UI
- Product category filtering
- Price history tracking
- Multiple region support

## Implementation Notes

Based on research:
- Mercadona uses Algolia for product search (like the GitHub gist shows)
- API endpoint: `https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_vlc1_es/query`
- Product URLs: `https://tienda.mercadona.es/product/{id}/{slug}`
- Image URLs: `https://prod-mercadona.imgix.net/images/...`

This means we have TWO options:
1. **Direct API** - Call Algolia directly (may need API key)
2. **HTML scraping** - Use Crawl4AI on `/buscar?q={query}`

Recommendation: Try HTML scraping first (matches existing pattern), fall back to API if needed.