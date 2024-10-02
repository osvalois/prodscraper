from pydantic import BaseSettings, Field
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class Settings(BaseSettings):
    # Redis configuration
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_USERNAME: str = Field(default="")
    REDIS_PASSWORD: str = Field(default="")
    REDIS_DB: int = Field(default=0)
    REDIS_MAX_CONNECTIONS: int = Field(default=10)
    REDIS_SOCKET_TIMEOUT: int = Field(default=5)
    REDIS_RETRY_ON_TIMEOUT: bool = Field(default=True)

    # MongoDB configuration
    MONGODB_URL: str = Field(default="mongodb://localhost:27017/default_db")
    MONGODB_MAX_POOL_SIZE: int = Field(default=100)
    MONGODB_MIN_POOL_SIZE: int = Field(default=0)
    MONGODB_MAX_IDLE_TIME_MS: int = Field(default=10000)

    # JWT configuration
    JWT_SECRET: str = Field(default="your-secret-key")
    JWT_ALGORITHM: str = Field(default="HS256")

    # API Key configuration
    API_KEY: str = Field(...)
    API_KEY_NAME: str = Field(default="X-API-Key")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @property
    def redis_url(self):
        parsed_url = urlparse(self.REDIS_HOST)
        host = parsed_url.hostname or self.REDIS_HOST
        port = parsed_url.port or self.REDIS_PORT

        if self.REDIS_USERNAME and self.REDIS_PASSWORD:
            return f"redis://{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}@{host}:{port}/{self.REDIS_DB}"
        else:
            return f"redis://{host}:{port}/{self.REDIS_DB}"

    @property
    def mongodb_database(self):
        parsed_url = urlparse(self.MONGODB_URL)
        return parsed_url.path.lstrip('/') or 'default_db'

settings = Settings()