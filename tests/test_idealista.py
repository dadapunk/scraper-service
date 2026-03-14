import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from llm import extract_real_estate_from_markdown


@pytest.fixture
def mock_llm_real_estate_response():
    return {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "properties": [
                                {
                                    "title": "Apartamento en Barcelona",
                                    "price": 1200.0,
                                    "price_per_m2": 15.5,
                                    "size": 80.0,
                                    "rooms": 3,
                                    "bathrooms": 2,
                                    "location": "Barcelona, Gracia",
                                    "property_type": "apartment",
                                    "operation_type": "rent",
                                }
                            ]
                        }
                    )
                }
            }
        ]
    }


async def test_extract_real_estate_success(mock_llm_real_estate_response):
    mock_settings = MagicMock()
    mock_settings.llm_models = ["model-1"]
    mock_settings.llm_base_url = "http://test"
    mock_settings.llm_api_key = "key"

    with patch("llm.get_settings", return_value=mock_settings):
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200,
                json=lambda: mock_llm_real_estate_response,
                raise_for_status=lambda: None,
            )

            results = await extract_real_estate_from_markdown(
                "some markdown", "alquiler Barcelona"
            )

            assert len(results) == 1
            assert results[0].title == "Apartamento en Barcelona"
            assert results[0].price == 1200.0
            assert results[0].location == "Barcelona, Gracia"
            assert results[0].operation_type == "rent"


async def test_extract_real_estate_empty_json():
    mock_settings = MagicMock()
    mock_settings.llm_models = ["model-1"]
    mock_settings.llm_base_url = "http://test"
    mock_settings.llm_api_key = "key"

    with patch("llm.get_settings", return_value=mock_settings):
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = MagicMock(
                status_code=200,
                json=lambda: {
                    "choices": [{"message": {"content": '{"properties": []}'}}]
                },
                raise_for_status=lambda: None,
            )

            results = await extract_real_estate_from_markdown(
                "some markdown", "alquiler Barcelona"
            )
            assert results == []
