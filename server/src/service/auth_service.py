from ..repository.user_repository import UserRepository
from ..util.helper import Helper
from ..model import User
from fastapi import HTTPException
from sqlalchemy.orm import Session


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.helper = Helper()

    def login(self, email: str, password: str):
        user = self.user_repository.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not self.helper.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = self.helper.generate_access_token({"user_id": user.id})
        refresh_token = self.helper.generate_refresh_token({"user_id": user.id})

        return {"access_token": access_token, "refresh_token": refresh_token}

    def register(self, data: dict):
        user = self.user_repository.get_user_by_email(data["email"])
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        hashed_password = self.helper.generate_hash_password(data["password"])
        user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password,)
        try:
            self.user_repository.create_user(user)
            return {"message": "User created successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
