# Codebase Structure

**Analysis Date:** 2026-03-26

## Directory Layout

```
scraper-service/
├── main.py                    # FastAPI application entry point
├── config.py                  # Settings via pydantic-settings
├── models.py                  # Pydantic request/response models
├── llm.py                     # LLM extraction functions
├── pyproject.toml             # Project configuration
├── Containerfile              # Docker container build
├── .env.example              # Environment template
├── README.md                 # Project documentation
├── scrapers/                  # Scraper implementations
│   ├── __init__.py           # Scraper registry (SCRAPERS dict)
│   ├── base.py               # Abstract Scraper base class
│   ├── supermarkets/        # Supermarket scrapers
│   │   ├── __init__.py
│   │   ├── bonpreu.py        # Bonpreu scraper
│   │   └── lidl.py           # Lidl scraper
│   └── realestate/           # Real estate scrapers
│       └── idealista.py     # Idealista scraper
├── tests/                    # Test suite
│   ├── test_api.py
│   ├── test_models.py
│   ├── test_config.py
│   ├── test_llm.py
│   ├── test_bonpreu.py
│   ├── test_lidl.py
│   ├── test_idealista.py
│   ├── smoke_test.py
│   └── fixtures/             # Test fixtures
│       └── bonpreu_markdown.txt
└── .planning/codebase/       # Planning documents (this repo)
```

## Directory Purposes

**Root (`/scraper-service`):**
- Purpose: Application entry points and core configuration
- Contains: main.py, config.py, models.py, llm.py
- Key files: `pyproject.toml`, `Containerfile`

**`scrapers/`:**
- Purpose: All web scraping implementations
- Contains: Abstract base class, concrete scrapers by category
- Key files: `scrapers/__init__.py`, `scrapers/base.py`

**`scrapers/supermarkets/`:**
- Purpose: Supermarket product scrapers
- Contains: Bonpreu and Lidl scraper implementations
- Files: `bonpreu.py`, `lidl.py`

**`scrapers/realestate/`:**
- Purpose: Real estate listing scrapers
- Contains: Idealista scraper implementation
- Files: `idealista.py`

**`tests/`:**
- Purpose: Unit and integration tests
- Contains: Test files mirroring source module structure, test fixtures
- Files: test_api.py, test_llm.py, test_bonpreu.py, etc.

**`.planning/codebase/`:**
- Purpose: Architecture and planning documentation
- Contains: This analysis document

## Key File Locations

**Entry Points:**
- `main.py`: FastAPI app initialization, routes: `/health`, `/search`

**Configuration:**
- `config.py`: Settings class with pydantic-settings
- `pyproject.toml`: Project metadata and dependencies
- `.env.example`: Template for required environment variables

**Core Logic:**
- `llm.py`: LLM extraction functions for products and real estate
- `models.py`: Pydantic models for requests, responses, and domain objects

**Testing:**
- `tests/`: Test files co-located by functionality
- `tests/fixtures/`: Test data files

## Naming Conventions

**Files:**
- Python modules: `snake_case.py` (e.g., `bonpreu.py`, `idealista.py`)
- Test files: `test_<module>.py` (e.g., `test_llm.py`)
- Config: `snake_case` (e.g., `config.py`, `models.py`)

**Directories:**
- Python packages: `snake_case` (e.g., `scrapers/`, `supermarkets/`)
- Categories: Descriptive (e.g., `supermarkets/`, `realestate/`)

**Classes:**
- PascalCase for classes (e.g., `BonpreuScraper`, `IdealistaScraper`)
- Abstract base: `Scraper`

**Variables/Functions:**
- snake_case (e.g., `extract_products_from_markdown`, `SCRAPERS`)

## Where to Add New Code

**New Scraper:**
- Implementation: `scrapers/<category>/<source>.py`
- Register in: `scrapers/__init__.py` add to `SCRAPERS` dict

**New Request/Response Model:**
- Location: `models.py`
- Add new Pydantic class extending `SearchResult` or base types

**New Test:**
- Location: `tests/test_<module>.py`
- Fixtures: `tests/fixtures/`

**New LLM Extraction Function:**
- Location: `llm.py`
- Follow existing pattern: system prompt + extraction function + fallback handling

## Special Directories

**`.venv/`:**
- Purpose: Python virtual environment
- Generated: Yes (by uv)
- Committed: No (in .gitignore)

**`.pytest_cache/`:**
- Purpose: Pytest cache
- Generated: Yes
- Committed: No

**`.ruff_cache/`:**
- Purpose: Ruff linter cache
- Generated: Yes
- Committed: No

---

*Structure analysis: 2026-03-26*
