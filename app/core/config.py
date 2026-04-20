from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    PASSWORD_HASED_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"   #loads .env file

settings = Settings()