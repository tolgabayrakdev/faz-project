from fastapi import HTTPException
from ..model import User
from ..util.helper import Helper
from ..repository.user_repository import UserRepository
from ..schema.auth_schema import RegisterRequest


class AuthService:

    def __init__(self, user_repository: UserRepository, helper: Helper):
        self.user_repository = user_repository
        self.helper = helper

    def _validate_user(self, user: User | None, password: str):
        if not user or not self.helper.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    def login(self, email: str, password: str):
        user = self.user_repository.get_user_by_email(email)
        self._validate_user(user, password)
        if user is not None:
            return {
                "access_token": self.helper.generate_access_token({"user_id": user.id}),
                "refresh_token": self.helper.generate_refresh_token(
                    {"user_id": user.id}
                ),
            }
        else:
            raise HTTPException(status_code=404, detail="User not found")

    def register(self, user_data: RegisterRequest):
        if self.user_repository.get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        if self.user_repository.get_user_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="Username already registered")

        user = User(
            email=user_data.email,
            username=user_data.username,
            password=self.helper.generate_hash_password(user_data.password),
        )
        return self.user_repository.create_user(user)
