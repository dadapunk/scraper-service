from models import SearchRequest, SupermarketResult, SearchResponse
from datetime import datetime, UTC
import json

def test_search_request_defaults():
    req = SearchRequest(source="bonpreu", query="queso")
    assert req.limit == 10

def test_supermarket_result_inheritance():
    # SupermarketResult should have fields from SearchResult
    res = SupermarketResult(
        title="Test Product",
        url="http://example.com",
        price=1.99
    )
    assert res.title == "Test Product"
    assert res.url == "http://example.com"
    assert res.price == 1.99

def test_supermarket_result_optional_fields():
    res = SupermarketResult(
        title="Test Product",
        url="http://example.com",
        price=1.99,
        brand=None,
        unit=None
    )
    assert res.brand is None
    assert res.unit is None

def test_search_response_serialization():
    now = datetime.now(UTC)
    res = SupermarketResult(title="P1", url="U1", price=1.0)
    resp = SearchResponse(
        source="test",
        query="q",
        results=[res],
        scraped_at=now
    )
    
    # Check if scraped_at is serialized correctly (ISO8601)
    json_data = resp.model_dump_json()
    data = json.loads(json_data)
    assert "scraped_at" in data
    # Pydantic 2 serializes datetime to ISO8601 string in JSON
    assert isinstance(data["scraped_at"], str)
    assert data["scraped_at"].startswith(str(now.year))
