from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_api_key: str = ""
    embedding_model: str = "intfloat/multilingual-e5-small"
    chunk_size: int = 800
    chunk_overlap: int = 100
    data_dir: Path = Path("data/raw")
    chroma_dir: Path = Path("chroma_db")


settings = Settings()
