# Testing Patterns

**Analysis Date:** 2026-03-26

## Test Framework

**Runner:**
- pytest 7.4+
- Config: `pyproject.toml` with `[tool.pytest.ini_options]`
- Async support: pytest-asyncio 0.23+

**Assertion Library:**
- pytest built-in assertions
- Pydantic model validation

**Run Commands:**
```bash
pytest                    # Run all tests
pytest tests/             # Run tests in specific directory
pytest -v                # Verbose output
pytest --asyncio-mode=auto  # Auto-detect async tests (default in config)
```

## Test File Organization

**Location:**
- `tests/` directory at project root
- Co-located with source code (not alongside modules)

**Naming:**
- `test_*.py` - pytest auto-discovery pattern
- Examples: `test_api.py`, `test_llm.py`, `test_bonpreu.py`, `test_models.py`

**Test Discovery:**
- Python path configured in `pyproject.toml`: `pythonpath = ["."]`
- Matches standard pytest conventions

## Test Structure

**Suite Organization:**
```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.mark.asyncio
async def test_function_name():
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...
```

**Patterns:**
- Uses `@pytest.mark.asyncio` for async test functions
- Setup via fixtures (`@pytest.fixture`) for reusable test data
- Teardown via context manager cleanup or fixture scope

**Example from `tests/test_bonpreu.py`:**
```python
@pytest.fixture
def bonpreu_markdown():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "bonpreu_markdown.txt")
    with open(fixture_path, "r") as f:
        return f.read()

@pytest.mark.asyncio
async def test_bonpreu_search_success(bonpreu_markdown):
    scraper = BonpreuScraper()
    query = "queso manchego"
    
    mock_products = [...]
    
    with patch("scrapers.supermarkets.bonpreu.AsyncWebCrawler") as mock_crawler_class:
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler
        # ...
        results = await scraper.search(query, limit=1)
        assert len(results) == 1
```

## Mocking

**Framework:** `unittest.mock` (standard library)
- `MagicMock` for sync mocks
- `AsyncMock` for async mocks
- `patch` decorator for module-level mocking

**Patterns:**
```python
# Mock class as context manager (async with)
mock_crawler = AsyncMock()
mock_crawler_class.return_value.__aenter__.return_value = mock_crawler

# Mock method returns
mock_result = MagicMock()
mock_result.markdown = bonpreu_markdown
mock_crawler.arun = AsyncMock(return_value=mock_result)

# Patch function at import location
with patch("scrapers.supermarkets.bonpreu.extract_products_from_markdown", new_callable=AsyncMock) as mock_extract:
    mock_extract.return_value = mock_products
```

**What to Mock:**
- External HTTP calls (LLM API, web scraping)
- AsyncWebCrawler class
- Third-party service responses

**What NOT to Mock:**
- Pydantic models (use real instances for validation tests)
- Configuration with valid test values

## Fixtures and Factories

**Test Data:**
- Fixtures stored in `tests/fixtures/` directory
- Example: `tests/fixtures/bonpreu_markdown.txt`

**Location:**
```
tests/
├── fixtures/
│   └── bonpreu_markdown.txt
├── test_api.py
├── test_llm.py
├── test_bonpreu.py
└── ...
```

**Usage:**
```python
@pytest.fixture
def bonpreu_markdown():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "bonpreu_markdown.txt")
    with open(fixture_path, "r") as f:
        return f.read()
```

## Coverage

**Requirements:** None enforced
**View Coverage:** No coverage command configured

## Test Types

**Unit Tests:**
- Test individual components in isolation
- Mock all external dependencies
- Examples: `test_models.py` (Pydantic validation), `test_config.py` (settings), `test_llm.py` (LLM extraction logic)

**Integration Tests:**
- Test API endpoints with mocked scrapers
- Test async flow with crawler mocks
- Example: `test_api.py` uses `httpx.AsyncClient` with FastAPI app transport

**Smoke Tests:**
- Manual integration test: `tests/smoke_test.py`
- Requires service running on port 8090
- Run: `python tests/smoke_test.py`

## Common Patterns

**Async Testing:**
```python
@pytest.mark.asyncio
async def test_function():
    result = await async_function()
    assert result == expected
```

**Error Testing:**
```python
async def test_error_handling():
    with pytest.raises(httpx.HTTPStatusError):
        await function_that_throws()

# Test error response (not exception)
async def test_search_endpoint_scraper_error():
    with patch("main.SCRAPERS", {"bonpreu": mock_scraper}):
        response = await ac.post("/search", json={...})
    assert response.status_code == 200  # Returns ErrorResponse, not 500
    assert "error" in response.json()
```

**Mock Settings:**
```python
def test_config_single_model():
    settings = Settings(
        llm_base_url="http://localhost:8000",
        llm_model="gemini-2.0-flash",
        llm_api_key="test-key"
    )
    assert settings.llm_models == ["gemini-2.0-flash"]
```

## Test Files Inventory

| File | Purpose |
|------|---------|
| `tests/test_api.py` | FastAPI endpoints: `/health`, `/search` |
| `tests/test_llm.py` | LLM extraction, retry logic, quota handling |
| `tests/test_bonpreu.py` | BonpreuScraper search integration |
| `tests/test_lidl.py` | LidlScraper search integration |
| `tests/test_idealista.py` | IdealistaScraper tests (present) |
| `tests/test_models.py` | Pydantic model validation and serialization |
| `tests/test_config.py` | Settings configuration parsing |
| `tests/smoke_test.py` | Manual integration test (requires running service) |

---

*Testing analysis: 2026-03-26*