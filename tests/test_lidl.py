import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from scrapers.supermarkets.lidl import LidlScraper
from models import SupermarketResult


@pytest.mark.asyncio
async def test_lidl_search_success():
    scraper = LidlScraper()
    query = "test query"
    
    # Mock products returned by LLM
    mock_products = [
        SupermarketResult(title="Product 1", price=1.99, url=""),
        SupermarketResult(title="Product 2", price=2.99, url=""),
    ]
    
    with patch("scrapers.supermarkets.lidl.AsyncWebCrawler") as mock_crawler_class:
        # Set up the mock for the context manager
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler
        
        # Mock crawler.arun to return an object with markdown attribute
        mock_result = MagicMock()
        mock_result.markdown = "Test markdown with products"
        mock_crawler.arun = AsyncMock(return_value=mock_result)
        
        with patch("scrapers.supermarkets.lidl.extract_products_from_markdown", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_products
            
            results = await scraper.search(query)
            
            mock_crawler.arun.assert_called_once()
            mock_extract.assert_called_once_with("Test markdown with products", query)
            
            # Check results
            assert len(results) == 2
            assert results[0].title == "Product 1"
            assert results[0].price == 1.99
            assert results[1].title == "Product 2"
            assert results[1].price == 2.99


@pytest.mark.asyncio
async def test_lidl_search_empty():
    scraper = LidlScraper()
    
    with patch("scrapers.supermarkets.lidl.AsyncWebCrawler") as mock_crawler_class:
        mock_crawler = AsyncMock()
        mock_crawler_class.return_value.__aenter__.return_value = mock_crawler
        
        mock_result = MagicMock()
        mock_result.markdown = ""
        mock_crawler.arun = AsyncMock(return_value=mock_result)
        
        with patch("scrapers.supermarkets.lidl.extract_products_from_markdown", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = []
            
            results = await scraper.search("nonexistent product")
            assert results == []