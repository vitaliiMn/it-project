from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    HASH_ALGORITHM: str

    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str

    CLIENT_SECRET: str
    CLIENT_ID: str

settings = Settings()