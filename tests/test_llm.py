import pytest
import httpx
import json
from unittest.mock import AsyncMock, patch, MagicMock
from llm import extract_products_from_markdown

@pytest.fixture
def mock_llm_response():
    return {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "products": [
                            {"name": "Queso", "brand": "Marca", "price": 2.99, "unit": "g", "unit_price": 14.95}
                        ]
                    })
                }
            }
        ]
    }

async def test_extract_products_success(mock_llm_response):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_llm_response,
            raise_for_status=lambda: None
        )
        
        results = await extract_products_from_markdown("some markdown", "queso")
        
        assert len(results) == 1
        assert results[0].title == "Queso"
        assert results[0].price == 2.99

async def test_extract_products_empty_json():
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"choices": [{"message": {"content": '{"products": []}'}}]},
            raise_for_status=lambda: None
        )
        
        results = await extract_products_from_markdown("some markdown", "queso")
        assert results == []

async def test_extract_products_retry_on_429(mock_llm_response):
    mock_settings = MagicMock()
    mock_settings.llm_models = ["model-1", "model-2"]
    mock_settings.llm_base_url = "http://test"
    mock_settings.llm_api_key = "key"

    with patch("llm.get_settings", return_value=mock_settings):
        with patch("httpx.AsyncClient.post") as mock_post:
            # First call returns 429, second returns success
            mock_post.side_effect = [
                MagicMock(status_code=429, text="429 quota exceeded"),
                MagicMock(
                    status_code=200,
                    json=lambda: mock_llm_response,
                    raise_for_status=lambda: None
                )
            ]
            
            results = await extract_products_from_markdown("some markdown", "queso")
            
            assert len(results) == 1
            assert mock_post.call_count == 2

async def test_extract_products_all_fail():
    mock_settings = MagicMock()
    mock_settings.llm_models = ["model-1"]
    mock_settings.llm_base_url = "http://test"
    mock_settings.llm_api_key = "key"

    with patch("llm.get_settings", return_value=mock_settings):
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=500, text="Internal Server Error")
            mock_post.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Error", request=MagicMock(), response=mock_post.return_value
            )

            with pytest.raises(httpx.HTTPStatusError):
                await extract_products_from_markdown("some markdown", "queso")


async def test_extract_products_all_quota_fail():
    mock_settings = MagicMock()
    mock_settings.llm_models = ["model-1", "model-2"]
    mock_settings.llm_base_url = "http://test"
    mock_settings.llm_api_key = "key"

    with patch("llm.get_settings", return_value=mock_settings):
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=429, text="quota exceeded")

            with pytest.raises(Exception, match="Quota exceeded"):
                await extract_products_from_markdown("some markdown", "queso")
