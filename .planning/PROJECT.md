# Scraper Service

## Project Overview

**Type:** Brownfield microservice  
**Status:** Operational (v0.1.0)  
**Stack:** Python 3.12+, FastAPI, Crawl4AI, LLM extraction  
**Deployment:** Proxmox LXC / systemd

Web scraping microservice with REST API for extracting product and real estate data from multiple online sources. Built on FastAPI with Crawl4AI for JavaScript rendering and LLM-based intelligent content extraction.

## Problem Space

- Scrape supermarket product data (prices, availability, promotions)
- Scrape real estate listings (properties, prices, details)
- Handle JavaScript-heavy SPAs that require browser rendering
- Extract structured data from unstructured HTML using LLM

## Key Features

1. **REST API** - FastAPI-based HTTP endpoints for search operations
2. **Multi-source support** - Bonpreu, Lidl (supermarkets), Idealista (real estate)
3. **LLM extraction** - OpenAI-compatible API (Google Gemini) for intelligent parsing
4. **Crawl4AI integration** - Headless browser rendering for SPA scraping
5. **Pluggable scrapers** - Abstract base class with registry pattern

## Tech Stack

- Python 3.12+
- FastAPI 0.104.1+
- Crawl4AI 0.4.0+
- httpx 0.27.0+
- pydantic 2.5.0+
- pytest (testing)

## Sources

- Bonpreu supermarket
- Lidl supermarket
- Idealista real estate

## Context

This is an existing brownfield project that was analyzed via `/gsd-map-codebase`. The codebase map is available in `.planning/codebase/`.