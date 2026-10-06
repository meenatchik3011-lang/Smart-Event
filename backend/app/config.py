from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SmartEvent"

    database_url: str = "sqlite:///./smart_event.db"

    secret_key: str = "change-this-secret-key"

    algorithm: str = "HS256"

    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()