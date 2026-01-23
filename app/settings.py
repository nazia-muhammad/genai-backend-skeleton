from pydantic import BaseModel
import os


class Settings(BaseModel):
    JWT_SECRET_KEY: str = "change-me-in-dev"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60


def get_settings() -> Settings:
    return Settings(
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "change-me-in-dev"),
        JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256"),
        JWT_EXPIRES_MINUTES=int(os.getenv("JWT_EXPIRES_MINUTES", "60")),
    )


settings = get_settings()
