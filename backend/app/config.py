from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mongo_uri: str = Field(default="mongodb://localhost:27017", alias="MONGO_URI")
    mongo_db_name: str = Field(default="dispatcher", alias="MONGO_DB_NAME")

    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")

    allowed_origins: str = Field(default="http://localhost:5173", alias="ALLOWED_ORIGINS")

    average_speed_mph: float = Field(default=55.0, alias="AVERAGE_SPEED_MPH")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()