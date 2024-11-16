from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        extra='ignore',
        case_sensitive=False,
    )

    input_files_dir: Path = './data'

    vectorizer_path: Path
    label_encoder_path: Path
    classifier_path: Path


# Функция для создания настроек (подгрузит данные из .env)
def load_settings() -> Settings:
    return Settings()
