from scrapers.base import Scraper
from models import SupermarketResult
from typing import List
from crawl4ai import AsyncWebCrawler
from llm import extract_products_from_markdown
from config import get_settings
from urllib.parse import quote_plus


class LidlScraper(Scraper):
    BASE_URL = "https://www.lidl.es/q/search"

    async def search(self, query: str, limit: int = 10) -> List[SupermarketResult]:
        url = f"{self.BASE_URL}?q={quote_plus(query)}"
        settings = get_settings()

        async with AsyncWebCrawler(
            headless=True,
            timeout=settings.crawl4ai_timeout,
            browser_args=["--no-sandbox", "--disable-dev-shm-usage"],
        ) as crawler:
            result = await crawler.arun(url=url)
            markdown = result.markdown
            products = await extract_products_from_markdown(markdown, query)
            return products[:limit]