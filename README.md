# Scraper Service

## Overview

Scraper Service is a Python-based web scraping microservice built with FastAPI and Crawl4AI. It provides a REST API to scrape product data from various online sources, with a focus on supermarket product search.

## Features

- **FastAPI REST API** for easy integration
- **Crawl4AI** for scraping JavaScript-heavy single-page applications (SPAs)
- **LLM integration** for intelligent content extraction using OpenAI-compatible APIs (e.g., Google's Gemini)
- **Multi-source support**: currently supports Bonpreu supermarket, Lidl supermarket, and Idealista real estate

## Quick Start

### Installation

```bash
cd scraper-service
uv sync
```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   ```env
   LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
   LLM_MODEL=gemini-2.0-flash,gemini-2.0-flash-lite
   LLM_API_KEY=your-api-key-here
   SERVER_PORT=8090
   LOG_LEVEL=info
   CRAWL4AI_TIMEOUT=30
   ```

### Running the Service

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8090 --reload
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:8090/health
```

#### Search Products
```bash
curl -X POST http://localhost:8090/search \
  -H "Content-Type: application/json" \
  -d '{
    "source": "bonpreu",
    "query": "queso manchego",
    "limit": 10
  }'
```

#### Search Real Estate
```bash
curl -X POST http://localhost:8090/search \
  -H "Content-Type: application/json" \
  -d '{
    "source": "idealista",
    "query": "Barcelona",
    "limit": 10
  }'
```

## Development

### Dependencies

- Python 3.12+
- FastAPI 0.104.1+
- Uvicorn 0.24.0+
- Crawl4AI 0.4.0+
- httpx 0.27.0+
- pydantic 2.5.0+
- pydantic-settings 2.1.0+

### Project Structure

```
scraper-service/
├── main.py                 # FastAPI application and endpoints
├── config.py              # Configuration management (pydantic-settings)
├── models.py              # Pydantic models for request/response
├── llm.py                 # LLM client for content extraction
├── scrapers/
│   ├── base.py           # Abstract base scraper class
│   ├── __init__.py       # Scraper registry
│   ├── supermarkets/
│   │   ├── bonpreu.py    # Bonpreu supermarket scraper
│   │   └── lidl.py       # Lidl supermarket scraper
│   └── realestate/
│       └── idealista.py  # Idealista real estate scraper
├── pyproject.toml        # Dependency management with uv
├── .env.example          # Example configuration
├── Containerfile         # Podman container build file
└── scraper-service.container # Systemd quadlet service file
```

## Deployment

### Proxmox LXC (recomendado para homelab)

El servicio corre como proceso systemd directamente en un LXC — el LXC ya provee el aislamiento necesario, no hace falta contenedor adicional.

Ver `docs/proxmox-lxc-deploy.md` para la guía completa.

Resumen rápido:
```bash
# En el LXC
cd /opt/scraper-service
uv sync
uv run playwright install chromium
systemctl enable --now scraper-service
```

### Health Check

```bash
systemctl status scraper-service
curl http://localhost:8090/health
```

## Adding New Scrapers

To add support for a new source:

1. Create a new scraper class in `scrapers/` (e.g., `scrapers/supermarkets/mercadona.py`)
2. Implement the `Scraper` interface from `scrapers/base.py`
3. Add the new scraper to the registry in `scrapers/__init__.py`

## License

MIT
