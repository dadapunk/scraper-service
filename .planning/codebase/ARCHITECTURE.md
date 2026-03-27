# Architecture

**Analysis Date:** 2026-03-26

## Pattern Overview

**Overall:** FastAPI REST API with Scraper Plugin Architecture

**Key Characteristics:**
- Async-first design using FastAPI and asyncio
- LLM-powered extraction layer for unstructured web content
- Plugin-based scraper system with abstract base class
- Type-safe request/response via Pydantic models
- Configuration via environment variables using pydantic-settings

## Layers

**API Layer:**
- Purpose: Handle HTTP requests and responses
- Location: `main.py`
- Contains: FastAPI application with `/search` and `/health` endpoints
- Depends on: `models.py`, `scrapers/__init__.py`
- Used by: HTTP clients, external consumers

**Scraper Layer:**
- Purpose: Abstract scraper interface and concrete implementations
- Location: `scrapers/base.py`, `scrapers/supermarkets/`, `scrapers/realestate/`
- Contains: `Scraper` abstract base class, specific scraper implementations
- Depends on: `models.py`, `llm.py`, `config.py`, Crawl4AI
- Used by: API layer via `SCRAPERS` registry

**LLM Extraction Layer:**
- Purpose: Parse markdown content into structured data using LLM
- Location: `llm.py`
- Contains: `extract_products_from_markdown`, `extract_real_estate_from_markdown`
- Depends on: `config.py`, `models.py`, httpx for API calls
- Used by: Scraper implementations

**Data Layer:**
- Purpose: Define request/response schemas and domain models
- Location: `models.py`
- Contains: Pydantic models for SearchRequest, SearchResponse, SearchResult variants
- Used by: All layers

**Configuration Layer:**
- Purpose: Manage application settings via environment variables
- Location: `config.py`
- Contains: `Settings` class with pydantic-settings
- Used by: All layers needing configuration

## Data Flow

**Search Request Flow:**

1. Client sends POST to `/search` with `SearchRequest` (source, query, limit)
2. API layer validates source against `SCRAPERS` registry
3. API layer instantiates or retrieves scraper for the source
4. Scraper constructs target URL from query
5. Scraper uses Crawl4AI `AsyncWebCrawler` to fetch page and get markdown
6. Scraper calls LLM extraction function with markdown and query
7. LLM extraction layer calls external LLM API with prompt and markdown
8. LLM returns JSON, extraction layer parses into domain model
9. Results returned to API layer wrapped in `SearchResponse`
10. Client receives HTTP response

**State Management:**
- Stateless request handling - no session state
- Each request creates new crawler instance via context manager
- Configuration is singleton via `get_settings()`

## Key Abstractions

**Scraper (Abstract Base Class):**
- Purpose: Define interface for all scrapers
- Location: `scrapers/base.py`
- Pattern: Template Method / Strategy pattern
- Methods: `async search(query, limit) -> List[SearchResult]`

**Scraper Registry:**
- Purpose: Map source names to scraper instances
- Location: `scrapers/__init__.py`
- Pattern: Simple dictionary registry
- Contains: `SCRAPERS = {"bonpreu": ..., "lidl": ..., "idealista": ...}`

**LLM Extraction:**
- Purpose: Convert unstructured markdown to typed results
- Location: `llm.py`
- Pattern: Factory/fallback pattern for multiple models
- Features: Automatic fallback on quota errors

## Entry Points

**API Server:**
- Location: `main.py`
- Triggers: `uvicorn main:app` or container start
- Responsibilities: FastAPI app initialization, route registration, error handling

**Scraper Instantiation:**
- Location: `scrapers/__init__.py`
- Triggers: Module import at startup
- Responsibilities: Register all scraper instances in registry

## Error Handling

**Strategy:** Exception propagation with graceful error responses

**Patterns:**
- HTTP 400 for unknown source validation
- Error captured in `ErrorResponse` model with source and query context
- Logging via Python standard `logging` module
- LLM quota errors handled via fallback model mechanism

## Cross-Cutting Concerns

**Logging:** Python standard `logging` module, configured in `main.py`

**Validation:** Pydantic models in `models.py` provide automatic validation

**Configuration:** Centralized in `config.py` via pydantic-settings, reads from `.env`

---

*Architecture analysis: 2026-03-26*
