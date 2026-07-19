"""
Configuración central de la aplicación.
Lee variables de entorno con valores por defecto seguros para desarrollo.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    APP_NAME: str = "English Learning Platform"
    ENV: str = "development"  # development | production

    # Base de datos
    # Dev: SQLite local. Prod: se sobreescribe con una URL de PostgreSQL
    # (ej: postgresql://user:pass@host:5432/dbname)
    DATABASE_URL: str = "sqlite:///./app.db"

    # Seguridad / JWT
    SECRET_KEY: str = "change-this-secret-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    FRONTEND_ORIGIN: str = "http://localhost:5173"


settings = Settings()
