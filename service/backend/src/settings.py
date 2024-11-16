from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.shared.swagger import SwaggerSettings


__all__ = [
    'BaseConfig',
    'AppSettings',
    'Settings',
    'load_settings',
]


# Базовый класс настроек с дефолтными параметрами
class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        case_sensitive=False,
    )


# Настройки веб части приложения
class AppSettings(BaseConfig):
    title: str
    host: str
    port: int


# Настройки всего приложения
class Settings(BaseConfig):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',  # позволяет задать настройки вложенным сущностям (например, APP__HOST) 
    )


    vectorizer_path: Path
    label_encoder_path: Path
    classifier_path: Path

    app: AppSettings
    swagger: SwaggerSettings = SwaggerSettings()


# Функция для создания настроек (подгрузит данные из .env)
def load_settings() -> Settings:
    return Settings()
