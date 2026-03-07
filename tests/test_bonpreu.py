import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from scrapers.supermarkets.bonpreu import BonpreuScraper
from models import SupermarketResult
import os

@pytest.fixture
def bonpreu_markdown():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "bonpreu_markdown.txt")
    with open(fixture_path, "r") as f:
        return f.read()

@pytest.mark.asyncio
async def test_bonpreu_search_success(bonpreu_markdown):
    scraper = BonpreuScraper()
    query = "queso manchego"
    
    # Mock products returned by LLM
    mock_products = [
        SupermarketResult(title="Queso 1", price=3.49, url=""),
        SupermarketResult(title="Queso 2", price=4.99, url=""),
    ]
    
    with patch("scrapers.supermarkets.bonpreu.AsyncWebCrawler") as mock_crawler_class:
        # Set up the mock for the context manager
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler
        
        # Mock crawler.arun to return an object with markdown attribute
        mock_result = MagicMock()
        mock_result.markdown = bonpreu_markdown
        mock_crawler.arun = AsyncMock(return_value=mock_result)
        
        with patch("scrapers.supermarkets.bonpreu.extract_products_from_markdown", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_products
            
            results = await scraper.search(query, limit=1)
            
            mock_crawler.arun.assert_called_once()
            mock_extract.assert_called_once_with(bonpreu_markdown, query)
            
            # Check limit
            assert len(results) == 1
            assert results[0].title == "Queso 1"

@pytest.mark.asyncio
async def test_bonpreu_search_empty():
    scraper = BonpreuScraper()
    
    with patch("scrapers.supermarkets.bonpreu.AsyncWebCrawler") as mock_crawler_class:
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler
        
        mock_result = MagicMock()
        mock_result.markdown = ""
        mock_crawler.arun = AsyncMock(return_value=mock_result)
        
        with patch("scrapers.supermarkets.bonpreu.extract_products_from_markdown", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = []
            
            results = await scraper.search("something")
            assert results == []
