from scrapers.base import Scraper
from models import RealEstateResult
from typing import List
from crawl4ai import AsyncWebCrawler
from llm import extract_real_estate_from_markdown
from config import get_settings
from urllib.parse import quote_plus


class IdealistaScraper(Scraper):
    BASE_URL = "https://www.idealista.com"

    async def search(self, query: str, limit: int = 10) -> List[RealEstateResult]:
        """
        Search for real estate properties on Idealista.

        Args:
            query: Search query, can be a location (city/neighborhood) or more complex query
            limit: Maximum number of results to return

        Returns:
            List of RealEstateResult objects
        """
        # For now, assume query is a location/city
        # Build URL for rental properties in the specified location
        location = quote_plus(query)
        url = f"{self.BASE_URL}/alquiler-viviendas/{location}/"

        settings = get_settings()

        async with AsyncWebCrawler(
            headless=True,
            timeout=settings.crawl4ai_timeout,
            browser_args=["--no-sandbox", "--disable-dev-shm-usage"],
        ) as crawler:
            result = await crawler.arun(url=url)

            markdown = result.markdown

            # Extract real estate listings using LLM
            properties = await extract_real_estate_from_markdown(markdown, query)

            return properties[:limit]
