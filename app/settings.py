from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI SQLALCHEMY CRUD"
    PROJECT_VERSION: str = "v0.0.1"
    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*3
    ALGORITHM: str = "HS256"
    # SECRET_KEY: str = os.urandom(12).hex()
    SECRET_KEY: str = "13cd6d096247d567f4723da4"

settings = Settings()

