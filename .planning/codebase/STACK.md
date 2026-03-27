# Technology Stack

**Analysis Date:** 2026-03-26

## Languages

**Primary:**
- Python 3.12+ - Core application language
- Markdown - Content extraction format from scraped pages

## Runtime

**Environment:**
- Python 3.12+ (minimum version specified in `pyproject.toml`)

**Package Manager:**
- uv - Modern Python package manager
- Lockfile: `uv.lock` present

## Frameworks

**Core:**
- FastAPI 0.104.1+ - REST API framework
- Uvicorn 0.24.0+ - ASGI server (with standard extras)

**Testing:**
- pytest 7.4+ - Test framework
- pytest-asyncio 0.23+ - Async test support
- pytest-mock 3.12+ - Mocking utilities

**Web Scraping:**
- Crawl4AI 0.4.0+ - JavaScript-rendering web crawler

**HTTP Client:**
- httpx 0.27.0+ - Async HTTP client for LLM API calls

**Data Validation:**
- pydantic 2.5.0+ - Data modeling
- pydantic-settings 2.1.0+ - Settings management

**Configuration:**
- python-dotenv 1.0.0+ - Environment variable loading

## Key Dependencies

**Production:**
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.104.1 | REST API framework |
| uvicorn[standard] | >=0.24.0 | ASGI server |
| crawl4ai | >=0.4.0 | Web scraping with JS rendering |
| httpx | >=0.27.0 | HTTP client for LLM calls |
| pydantic | >=2.5.0 | Data validation |
| pydantic-settings | >=2.1.0 | Settings from environment |
| python-dotenv | >=1.0.0 | Load .env files |

**Development:**
| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.4 | Test framework |
| pytest-asyncio | >=0.23 | Async test support |
| pytest-mock | >=3.12 | Mock utilities |
| httpx | >=0.27 | Test HTTP client |

## Configuration

**Environment:**
- Configuration via `pydantic-settings` from `.env` file
- `.env.example` provides template

**Build:**
- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Locked dependency versions
- `Containerfile` - Podman container build

## Platform Requirements

**Development:**
- Python 3.12+
- uv package manager
- Browser (for Crawl4AI - Playwright-based)

**Production:**
- Podman container (via `Containerfile`)
- Systemd service (via `scraper-service.container`)
- Proxmox LXC deployment supported

---

*Stack analysis: 2026-03-26*
