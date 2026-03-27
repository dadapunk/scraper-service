# Coding Conventions

**Analysis Date:** 2026-03-26

## Naming Patterns

**Files:**
- snake_case: `test_api.py`, `bonpreu.py`, `llm.py`
- Module names use descriptive nouns: `bonpreu.py`, `idealista.py`, `models.py`

**Classes:**
- PascalCase: `BonpreuScraper`, `LidlScraper`, `IdealistaScraper`, `SearchRequest`
- Base class prefix: `Scraper` (base class), specific scrapers inherit and add name

**Functions:**
- snake_case: `get_settings()`, `extract_products_from_markdown()`, `search()`
- Async functions prefixed with `async`: `async def search(...)`

**Variables:**
- snake_case: `bonpreu_markdown`, `mock_scraper`, `mock_results`
- Constants: UPPER_SNAKE_CASE for configuration constants

**Types:**
- Pydantic models: PascalCase in `models.py`
- Type hints: Use Python typing module (`List`, `Optional`, `dict`)

## Code Style

**Formatting:**
- Tool: Black (inferred from Python project conventions, no explicit config)
- Settings in `pyproject.toml` not fully configured for formatting

**Linting:**
- Tool: Ruff (`.ruff_cache` directory present in project)
- No explicit `ruff.toml` or ruff config in `pyproject.toml` found

**General Style:**
- 4-space indentation
- Python 3.12+ features used (type hinting, match statements optional)
- Single blank lines between top-level definitions
- No trailing whitespace

## Import Organization

**Order:**
1. Standard library: `from abc`, `from typing`, `from datetime`
2. Third-party: `from fastapi`, `from pydantic`, `from crawl4ai`, `from httpx`
3. Local: `from config`, `from models`, `from scrapers.*`

**Example from `llm.py`:**
```python
import json
import httpx
from typing import List
from config import get_settings
from models import SupermarketResult, RealEstateResult
```

**No path aliases used** - imports use relative module paths

## Error Handling

**Patterns:**
- Use Pydantic for validation: `ValidationError` caught by framework
- HTTP errors via FastAPI: `HTTPException(status_code=400, detail=...)`
- LLM quota errors handled explicitly: custom `_is_quota_error()` function with fallback retry logic in `llm.py`
- Generic exception handling in API endpoint returns `ErrorResponse` instead of raising

**Example from `main.py`:**
```python
except Exception as e:
    logger.error(f"Error scraping {source} for query '{query}': {e}")
    return ErrorResponse(...)
```

## Logging

**Framework:** Python `logging` module
- Basic config in `main.py`: `logging.basicConfig(level=logging.INFO)`
- Named logger: `logger = logging.getLogger(__name__)`
- Error logging with context: `logger.error(f"Error scraping {source}...")`

**Patterns:**
- Use for unexpected errors only
- No debug/info logging in happy path

## Comments

**When to Comment:**
- Docstrings on public classes and methods
- Inline comments for complex logic or workarounds
- Explain non-obvious behavior (e.g., LLM fallback logic)

**Docstrings Style:**
- Google-style for classes (e.g., `IdealistaScraper.search`)
- Simple inline for straightforward methods

**Example from `idealista.py`:**
```python
async def search(self, query: str, limit: int = 10) -> List[RealEstateResult]:
    """
    Search for real estate properties on Idealista.

    Args:
        query: Search query, can be a location (city/neighborhood) or more complex query
        limit: Maximum number of results to return

    Returns:
        List of RealEstateResult objects
    """
```

## Function Design

**Size:** Keep functions focused and under 50 lines where possible
- `search()` in scrapers handles single responsibility
- LLM extraction functions split into product vs real estate variants

**Parameters:**
- Use type hints on all parameters
- Default values for optional parameters (`limit: int = 10`)
- Keyword arguments used in test assertions for clarity

**Return Values:**
- Always annotated with return types
- Use Pydantic models for structured returns

## Module Design

**Exports:**
- Single level exports via `__init__.py` (e.g., `SCRAPERS` dict)
- No `__all__` declarations
- Classes and functions exported directly

**Barrel Files:**
- `scrapers/__init__.py` aggregates all scrapers into single `SCRAPERS` dict
- No deep barrel file patterns

## Class Design

**Base Classes:**
- `Scraper` abstract base in `scrapers/base.py` using ABC
- Abstract method: `async def search(...)` 
- Concrete scrapers inherit and implement

**Inheritance Pattern:**
```python
class BonpreuScraper(Scraper):
    async def search(self, query: str, limit: int = 10) -> List[SupermarketResult]:
        ...
```

## Configuration

**Environment:**
- Use Pydantic `BaseSettings` in `config.py`
- Load from `.env` file: `SettingsConfigDict(env_file=".env")`
- Required env vars: `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY`
- Optional: `SERVER_PORT` (default 8090), `LOG_LEVEL` (default info), `CRAWL4AI_TIMEOUT` (default 30)

## Async/Await Patterns

**HTTP Clients:**
- Use `httpx.AsyncClient` for LLM API calls
- Use `crawl4ai.AsyncWebCrawler` as context manager

**Testing:**
- Mark async tests with `@pytest.mark.asyncio`
- Use `pytest-asyncio` for async test support
- Config in `pyproject.toml`: `asyncio_mode = "auto"`

---

*Convention analysis: 2026-03-26*