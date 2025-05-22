import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_TITLE: str = os.getenv("APP_TITLE", "app-service-python")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "app-service-python")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    APP_ENV: str = os.getenv("APP_ENV", "DEVELOPMENT").upper()

    IS_DEVELOPMENT: bool = os.getenv("APP_ENV", "DEVELOPMENT").upper() == "DEVELOPMENT"

    WEB_SERVER_HOST: str = os.getenv("WEB_SERVER_HOST", "0.0.0.0")
    WEB_SERVER_PORT: int = int(os.getenv("WEB_SERVER_PORT", "8000"))

    WEB_SERVER_CORS_ORIGINS: list[str] = os.getenv(
        "WEB_SERVER_CORS_ORIGINS", "*"
    ).split(",")
    WEB_SERVER_CORS_CREDENTIALS: bool = (
        os.getenv("WEB_SERVER_CORS_CREDENTIALS", "false").lower() == "true"
    )
    WEB_SERVER_CORS_METHODS: list[str] = os.getenv(
        "WEB_SERVER_CORS_METHODS", "*"
    ).split(",")
    WEB_SERVER_CORS_HEADERS: list[str] = os.getenv(
        "WEB_SERVER_CORS_HEADERS", "*"
    ).split(",")

    WEB_SERVER_TRUSTED_HOSTS: list[str] = os.getenv(
        "WEB_SERVER_TRUSTED_HOSTS", "*"
    ).split(",")
    WEB_SERVER_ENFORCE_HTTPS: bool = (
        os.getenv("WEB_SERVER_ENFORCE_HTTPS", "false").lower() == "true"
    )

    AI_GOOGLE_GEMINI_API_KEY: str = os.getenv("AI_GOOGLE_GEMINI_API_KEY", "")
    AI_GOOGLE_GEMINI_MODEL: str = os.getenv("AI_GOOGLE_GEMINI_MODEL", "gemini-2.0-flash")



settings = Settings()
