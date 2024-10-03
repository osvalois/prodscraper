from pydantic import BaseSettings, Field
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class Settings(BaseSettings):
    # Redis configuration
    REDIS_HOST: str = Field(...)
    REDIS_PORT: int = Field(...)
    REDIS_USERNAME: str = Field(...)
    REDIS_PASSWORD: str = Field(...)
    REDIS_MAX_CONNECTIONS: int = Field(default=10)
    REDIS_SOCKET_TIMEOUT: int = Field(default=5)
    REDIS_RETRY_ON_TIMEOUT: bool = Field(default=True)
    REDIS_CACHE_EXPIRATION: int = Field(default=300)  # 5 minutes

    # API Key configuration
    API_KEY: str = Field(...)
    API_KEY_NAME: str = Field(default="X-API-Key")

    # Scraping settings
    SCRAPE_TIMEOUT: int = Field(default=30000)
    RATE_LIMIT_CALLS: int = Field(default=1)
    RATE_LIMIT_PERIOD: float = Field(default=1.0)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @property
    def redis_url(self):
        parsed_url = urlparse(self.REDIS_HOST)
        host = parsed_url.hostname or self.REDIS_HOST
        port = parsed_url.port or self.REDIS_PORT

        if self.REDIS_USERNAME and self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}@{host}:{port}/0"
        else:
            return f"redis://{host}:{port}/0"

settings = Settings()