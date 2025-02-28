from config import settings

from repository.user import users, User
from repository.history import histories

from passlib.context import CryptContext

from pydantic import EmailStr

from schemas.user import RegisterForm, UserToCreate, UserRole, LoginForm
from schemas.jwt import TokenResponse

from services.producer import producer
from services.jwt import token_service

class UserService:

    ALGORITHM = settings.HASH_ALGORITHM

    def __init__(self):
        self.password_context = CryptContext(schemes=[self.ALGORITHM])

    def hash_password(self, password: str) -> str:
        return self.password_context.hash(password)
    
    def verify_password(self, entered_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(entered_password, hashed_password)
    
    async def check_exists_user(self, email: EmailStr) -> bool:
        return users.user_exists(email=email)
    
    async def create_user(self, user_form: RegisterForm, oauth: bool, role: UserRole) -> User:
        if await self.check_exists_user(user_form.email):
            return None
        new_user_form = UserToCreate(username=user_form.username,
                                password=self.hash_password(user_form.password) if user_form.password else None,
                                email=user_form.email,
                                role=role,
                                oauth=oauth)
        new_user = users.create_user(new_user_form)
        await producer.send_message(new_user.username)
        return new_user
    
    async def check_user_password(self, user_form: LoginForm) -> User:
        user = users.get_user(identifier=user_form.email)
        if user:
            if self.verify_password(user_form.password, user.password):
                return user
            return None
        return None
    
    async def auth_user_default(self, user_form: LoginForm) -> TokenResponse:
        user = await self.check_user_password(user_form)

        if not user:
            return None
        
        histories.create_history(user.id)

        access_token = token_service.create_access_token(user_id=user.id, role=user.role)
        refresh_token = token_service.create_refresh_token(user_id=user.id, role=user.role)
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    async def auth_user_oauth(self, email: EmailStr) -> TokenResponse:
        user = users.get_user(email)
        histories.create_history(user.id)

        access_token = token_service.create_access_token(user_id=user.id, role=user.role)
        refresh_token = token_service.create_refresh_token(user_id=user.id, role=user.role)
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    async def get_user_history(self, access_token: str, user_id: int) -> list:
        token_data = token_service.decode_token(access_token)
        if token_data.role == UserRole.admin or token_data.id == user_id:
            return histories.get_user_history(user_id)
        return None
            



user_service = UserService()