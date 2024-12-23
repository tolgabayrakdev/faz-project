from sqlalchemy.orm import Session
from ..model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        """ID ile kullanıcıyı getirir."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Email ile kullanıcıyı getirir."""
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: User) -> User:
        """Yeni bir kullanıcı oluşturur."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        """Kullanıcıyı siler."""
        self.db.delete(user)
        self.db.commit()
