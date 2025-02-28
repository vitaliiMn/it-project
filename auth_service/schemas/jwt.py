from pydantic import BaseModel

from datetime import datetime

from schemas.user import UserRole

class TokenData(BaseModel):
    exp: datetime
    id: int
    role: UserRole

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
