"""Настройки сервиса заказов."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = "orders"
    
    # URL для подключения к базе данных (ОБЯЗАТЕЛЬНО!)
    database_url: str = "sqlite:///./orders.db"

    # Куда ходить за проверкой клиента
    accounts_url: str = "http://localhost:8001"
    
    # Таймаут для запросов к сервису клиентов
    accounts_timeout_seconds: float = 2.0


settings = Settings()