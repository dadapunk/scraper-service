# External Integrations

**Analysis Date:** 2026-03-26

## APIs & External Services

**LLM (Large Language Model):**
- Google Gemini (via OpenAI-compatible API) - Content extraction from scraped pages
  - Base URL: `https://generativelanguage.googleapis.com/v1beta/openai`
  - Default models: `gemini-2.5-flash-lite`, `gemini-2.5-flash`
  - Authentication: Bearer token via `LLM_API_KEY` environment variable
  - Implementation: `llm.py` - Uses OpenAI chat completions format
  - Fallback support: Multiple models tried sequentially on quota errors

**Web Scraping:**
- Crawl4AI - JavaScript-rendering web crawler
  - Uses Playwright under the hood
  - Configurable timeout (default: 30 seconds)
  - Headless browser mode
  - Supports: Bonpreu, Lidl, Idealista

## Data Storage

**Database:**
- None - Stateless REST API service

**File Storage:**
- Local filesystem only - No external storage service

**Caching:**
- None - No caching layer

## Authentication & Identity

**LLM API:**
- Google AI API (API Key)
  - Environment variable: `LLM_API_KEY`
  - Format: Bearer token in Authorization header

## Monitoring & Observability

**Error Tracking:**
- None - No external error tracking service

**Logs:**
- Python standard logging (`logging` module)
- Configurable log level via `LOG_LEVEL` env var
- Log output to stdout (container-compatible)

## CI/CD & Deployment

**Hosting:**
- Self-hosted on Proxmox LXC (recommended for homelab)
- Podman container support

**CI Pipeline:**
- None detected - No external CI service

**Container Registry:**
- Not applicable - Self-built images only

## Environment Configuration

**Required env vars:**
| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_BASE_URL` | LLM API endpoint | `https://generativelanguage.googleapis.com/v1beta/openai` |
| `LLM_MODEL` | LLM model(s) to use (comma-separated) | `gemini-2.5-flash-lite,gemini-2.5-flash` |
| `LLM_API_KEY` | API key for LLM service | (Google AI API key) |
| `SERVER_PORT` | Port to run the server on | `8090` |
| `LOG_LEVEL` | Logging level | `info` |
| `CRAWL4AI_TIMEOUT` | Web scraping timeout in seconds | `30` |

**Secrets location:**
- `.env` file (local development)
- Environment variables (production)

## Webhooks & Callbacks

**Incoming:**
- None - No incoming webhook endpoints

**Outgoing:**
- None - No outgoing webhooks

## Scraping Targets

**Supermarkets:**
- **Bonpreu** (`bonpreu`)
  - URL: `https://compraonline.bonpreuesclat.cat/search`
  - Data: Product name, price, unit, unit_price, brand

- **Lidl** (`lidl`)
  - Data: Product name, price, unit, unit_price, brand

**Real Estate:**
- **Idealista** (`idealista`)
  - Data: Property title, price, price_per_m2, size, rooms, bathrooms, location, property_type, operation_type

---

*Integration audit: 2026-03-26*
