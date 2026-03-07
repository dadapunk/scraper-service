import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from unittest.mock import AsyncMock, patch, MagicMock
from models import SupermarketResult

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_search_endpoint_success():
    mock_results = [SupermarketResult(title="Test", price=1.0, url="")]
    mock_scraper = MagicMock()
    mock_scraper.search = AsyncMock(return_value=mock_results)
    
    with patch("main.SCRAPERS", {"bonpreu": mock_scraper}):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/search", json={
                "source": "bonpreu",
                "query": "queso",
                "limit": 5
            })
            
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "bonpreu"
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "Test"
    assert "scraped_at" in data

@pytest.mark.asyncio
async def test_search_endpoint_unknown_source():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/search", json={
            "source": "unknown",
            "query": "queso"
        })
    assert response.status_code == 400
    assert "Unknown source" in response.json()["detail"]

@pytest.mark.asyncio
async def test_search_endpoint_scraper_error():
    mock_scraper = MagicMock()
    mock_scraper.search = AsyncMock(side_effect=Exception("Scraper failed"))
    
    with patch("main.SCRAPERS", {"bonpreu": mock_scraper}):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/search", json={
                "source": "bonpreu",
                "query": "queso"
            })
            
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Scraper failed"
    assert data["results"] == []
