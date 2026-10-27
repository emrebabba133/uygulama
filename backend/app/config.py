import os


class Settings:
    database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./tdmp.db")
    # Dev-only default; production must set JWT_SECRET.
    jwt_secret: str = os.environ.get("JWT_SECRET", "dev-only-change-me-dev-only-change-me")
    jwt_minutes: int = int(os.environ.get("JWT_MINUTES", "60"))


settings = Settings()
