from pydantic import BaseModel, EmailStr

from enum import Enum

class UserRole(str, Enum):
    regular = "regular"
    admin = "admin"

class RegisterForm(BaseModel):
    username: str
    password: str = None
    email: EmailStr

class UserToCreate(BaseModel):
    username: str
    password: str | None
    email: EmailStr
    role: UserRole
    oauth: bool

class LoginForm(BaseModel):
    email: EmailStr
    password: str

class OAuthForm(BaseModel):
    username: str
    email: EmailStr