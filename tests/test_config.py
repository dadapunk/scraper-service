import os
import pytest
from pydantic import ValidationError

# Set mandatory env vars before importing anything that might trigger Settings instantiation
os.environ["LLM_BASE_URL"] = "http://localhost:8000"
os.environ["LLM_MODEL"] = "test-model"
os.environ["LLM_API_KEY"] = "test-key"

from config import Settings

def test_config_single_model():
    settings = Settings(
        llm_base_url="http://localhost:8000",
        llm_model="gemini-2.0-flash",
        llm_api_key="test-key"
    )
    assert settings.llm_models == ["gemini-2.0-flash"]

def test_config_multiple_models():
    settings = Settings(
        llm_base_url="http://localhost:8000",
        llm_model="gemini-2.0-flash, gemini-2.0-flash-lite ",
        llm_api_key="test-key"
    )
    assert settings.llm_models == ["gemini-2.0-flash", "gemini-2.0-flash-lite"]

def test_config_default_port():
    settings = Settings(
        llm_base_url="http://localhost:8000",
        llm_model="test-model",
        llm_api_key="test-key"
    )
    assert settings.server_port == 8090

def test_config_missing_required_vars(monkeypatch):
    # We need to clear env vars to test validation error
    # but Settings might have already loaded from .env if it exists
    # BaseSettings allows passing values to constructor to override
    with pytest.raises(ValidationError):
        # Trying to instantiate without required fields
        Settings(llm_base_url=None, llm_model=None, llm_api_key=None)
