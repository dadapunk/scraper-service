from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    llm_base_url: str
    llm_model: str
    llm_api_key: str
    server_port: int = 8090
    log_level: str = "info"
    crawl4ai_timeout: int = 30

    @property
    def llm_models(self) -> List[str]:
        return [model.strip() for model in self.llm_model.split(",") if model.strip()]

def get_settings() -> Settings:
    return Settings()
