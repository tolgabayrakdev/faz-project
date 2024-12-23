import jwt
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Union


class Helper:
    JWT_SECRET_KEY = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    @classmethod
    def generate_hash_password(cls, password: str) -> str:
        """Parolayı hash'ler."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Parolanın doğruluğunu kontrol eder."""
        return cls.generate_hash_password(plain_password) == hashed_password

    @classmethod
    def generate_access_token(cls, data: Dict[str, Union[str, int]]) -> str:
        """Access token oluşturur."""
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})

        encoded_jwt = jwt.encode(to_encode, cls.JWT_SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @classmethod
    def generate_refresh_token(cls, data: Dict[str, Union[str, int]]) -> str:
        """Refresh token oluşturur."""
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": int(expire.timestamp())})

        encoded_jwt = jwt.encode(to_encode, cls.JWT_SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @classmethod
    def decode_token(cls, token: str) -> Dict:
        """Token'ı decode eder."""
        try:
            decoded_token = jwt.decode(token, cls.JWT_SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise Exception("Token süresi dolmuş")
        except jwt.InvalidTokenError:
            raise Exception("Geçersiz token")
