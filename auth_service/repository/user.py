from pydantic import EmailStr

from typing import List, overload, Union

from schemas.user import UserRole, UserToCreate

class User:

    _id_counter = 0

    def __init__(self, user: UserToCreate):
        self.id = User._generate_id()
        self.username = user.username
        self.password = user.password
        self.email = user.email
        self.oauth = user.oauth
        self.role = user.role

    @classmethod
    def _generate_id(cls):
        cls._id_counter += 1
        return cls._id_counter

class UserDB:
    users: List[User] = []

    def user_exists(self, email: EmailStr) -> bool:
        for user in self.users:
            if user.email == email:
                return True
        return False
    
    def get_user(self, identifier: Union[int, str]) -> User:
        if isinstance(identifier, int):
            if 0 <= identifier <= len(self.users):
                return self.users[identifier - 1]
        elif isinstance(identifier, str):
            for user in self.users:
                if user.email == identifier:
                    return user
        return None
    
    def create_user(self, user_form: UserToCreate) -> User:
        new_user = User(user_form)
        self.users.append(new_user)
        return new_user 

users = UserDB()