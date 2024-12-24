from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..model import User
from ..util.helper import Helper
from ..repository.user_repository import UserRepository


class AuthService:

    def __init__(self, user_repository: UserRepository, helper: Helper):
        self.user_repository = user_repository
        self.helper = helper

    def login(self, email: str, password: str):
        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not self.helper.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "access_token": self.helper.generate_access_token({"user_id": user.id}),
            "refresh_token": self.helper.generate_refresh_token({"user_id": user.id}),
        }
