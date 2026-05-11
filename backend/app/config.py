from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Nairobi Designer Agent"
    secret_key: str = "change-this-to-a-random-secret-string"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "sqlite+aiosqlite:///./designer_agent.db"

    # OpenAI
    openai_api_key: Optional[str] = None

    # Apify (discovery)
    apify_api_key: Optional[str] = None
    scan_interval_hours: int = 6
    lead_score_threshold: int = 70

    # SendGrid (outreach)
    sendgrid_api_key: Optional[str] = None
    sender_email: Optional[str] = None
    sender_name: str = "Your Name — Graphic Designer"

    # Stripe
    stripe_secret_key: Optional[str] = None
    stripe_publishable_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None

    # M-Pesa
    mpesa_consumer_key: Optional[str] = None
    mpesa_consumer_secret: Optional[str] = None
    mpesa_shortcode: Optional[str] = None
    mpesa_passkey: Optional[str] = None
    mpesa_environment: str = "sandbox"
    mpesa_callback_url: Optional[str] = None

    # Admin
    admin_token: str = ""

    # SEO
    seo_interval_hours: int = 168
    seo_batch_size: int = 50

    # Frontend
    frontend_url: str = "http://localhost:3000"


settings = Settings()
