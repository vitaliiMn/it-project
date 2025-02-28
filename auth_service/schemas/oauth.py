from pydantic import BaseModel, EmailStr, model_validator

class YandexAuthResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str

class YandexInfoResponse(BaseModel):
    username: str
    email: EmailStr = None

    @model_validator(mode="after")
    def build_email(cls, values: "YandexInfoResponse"):
        if not values.email:
            values.email = f"{values.username}@yandex.ru"
        return values