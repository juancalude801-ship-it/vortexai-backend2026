from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = "dev"
    APP_NAME: str = "VortexAI Wholesale"
    BASE_URL: str = "http://localhost:8080"

    DATABASE_URL: str

    RENTCAST_API_KEY: str = ""
    RENTCAST_BASE_URL: str = "https://api.rentcast.io/v1"

    BREVO_API_KEY: str = ""
    BREVO_SENDER_EMAIL: str = ""
    BREVO_SENDER_NAME: str = "VortexAI Deals"
    REPORT_EMAIL: str = ""

    MARKETS: str = "Dallas,TX"
    AUTORUN_ENABLED: bool = True
    AUTORUN_INTERVAL_SECONDS: int = 900
    MIN_SCORE_TO_BLAST: int = 75

    DEAL_ROOM_SECRET: str = Field(default="change_me")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
