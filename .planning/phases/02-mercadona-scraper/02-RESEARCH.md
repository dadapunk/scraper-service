# Phase 2: Mercadona Scraper - Research

**Researched:** 2026-03-26
**Status:** Ready for planning

## Research Questions

1. **How to scrape Mercadona product search results?**
2. **What is the website structure and anti-bot considerations?**
3. **How to map existing patterns to Mercadona implementation?**

---

## Finding 1: Mercadona Website Structure

### Primary URL Pattern
- **Search endpoint:** `https://tienda.mercadona.es/buscar?q={query}`
- **Product detail:** `https://tienda.mercadona.es/product/{id}/{slug}`
- **Image CDN:** `https://prod-mercadona.imgix.net/images/...`

### Key Observations from Research

1. **HTML Search Results** — The search page renders products in HTML that can be parsed
2. **JavaScript-Rendered** — Uses client-side rendering (requires Crawl4AI for JS execution)
3. **Postal Code Dependency** — Results depend on user's selected store/zone
   - Default: Use a Valencia postal code (e.g., 46001) as fallback
   - Future: Could accept postal_code parameter in search request
4. **Product URLs Available** — Each result links to product detail page

### Anti-Bot Considerations

From existing Mercadona scrapers (GitHub research):
- Uses standard headless Chrome typically works
- May need to set custom User-Agent
- Cookie consent modal may appear (Crawl4AI can handle)

---

## Finding 2: Implementation Pattern

### Reuse Existing Supermarket Scrapers

**Pattern from Bonpreu/Lidl:**
```python
# scrapers/supermarkets/bonpreu.py
class BonpreuScraper(Scraper):
    async def search(self, query: str, limit: int = 10) -> List[SupermarketResult]:
        # 1. Build search URL
        url = f"https://tienda.bonpreuescat.es/buscar?q={quote(query)}"
        
        # 2. Crawl with Crawl4AI
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
        
        # 3. Extract with LLM
        products = await extract_products_from_markdown(result.markdown, query)
        
        # 4. Map to results
        return [SupermarketResult(...) for product in products[:limit]]
```

### Apply to Mercadona

```python
# scrapers/supermarkets/mercadona.py
class MercadonaScraper(Scraper):
    async def search(self, query: str, limit: int = 10) -> List[SupermarketResult]:
        # Use same pattern as Bonpreu/Lidl
        url = f"https://tienda.mercadona.es/buscar?q={quote(query)}"
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                # Crawl4AI options for Mercadona
                wait_for="css:.product-grid",  # Wait for products to load
                js_code="""() => {
                    // Accept cookies if modal appears
                    const btn = document.querySelector('[data-testid="accept-cookies"]');
                    if (btn) btn.click();
                }"""
            )
        
        products = await extract_products_from_markdown(result.markdown, query)
        return [SupermarketResult(...) for product in products[:limit]]
```

---

## Finding 3: LLM Extraction

### Reuse Existing Prompt

From `llm.py:extract_products_from_markdown`:
- Already handles Spanish supermarket products
- Extracts: title, price, unit, unit_price, brand
- We need to add: url field extraction

### URL Extraction Strategy

1. **From Crawl4AI links:**
```python
# After crawl, get internal links
internal_links = result.links.get("internal", [])
product_links = [l for l in internal_links if '/product/' in l.get('href', '')]

# Map to LLM results by position
for i, product in enumerate(products):
    if i < len(product_links):
        product.url = product_links[i]['href']
```

2. **Alternative:** Update LLM prompt to extract share_url from HTML

---

## Finding 4: Integration Points

### Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `scrapers/supermarkets/mercadona.py` | Create | Mercadona scraper class |
| `scrapers/__init__.py` | Modify | Add to SCRAPERS registry |
| `scrapers/supermarkets/__init__.py` | Modify | Export MercadonaScraper |
| `tests/test_mercadona.py` | Create | Test file (per Phase 3 tasks) |
| `models.py` | Check | Ensure SupermarketResult has url field |

### Registry Update

```python
# scrapers/__init__.py
SCRAPERS: dict[str, type[Scraper]] = {
    "bonpreu": BonpreuScraper,
    "lidl": LidlScraper,
    "idealista": IdealistaScraper,
    "mercadona": MercadonaScraper,  # ADD THIS
}
```

---

## Implementation Recommendations

### Task Breakdown

1. **Create Mercadona scraper** — Implement `MercadonaScraper` following Bonpreu pattern
2. **Add to registry** — Update `scrapers/__init__.py`
3. **Test integration** — Verify `/search?source=mercadona&q=leche` works

### Key Decisions for Discretion

1. **Postal code handling** — Default to Valencia (46001), don't require as parameter
2. **Cookie handling** — Let Crawl4AI handle or add JS to accept
3. **Error handling** — Reuse existing patterns from Bonpreu/Lidl

---

## Validation Architecture

For Nyquist validation, plans should include:

| Verification | Method |
|--------------|--------|
| Mercadona scraper loads | Test: `curl -X POST /search -d '{"source":"mercadona","query":"leche"}'` returns results |
| Products have URLs | Test: Response contains products with non-empty `url` field |
| Error handling works | Test: Invalid query returns proper error (not 200 with error) |

---

*Research completed: 2026-03-26*