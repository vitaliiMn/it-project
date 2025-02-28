from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    TGBOT_TOKEN: str
    CHAT_ID: int

settings = Settings()