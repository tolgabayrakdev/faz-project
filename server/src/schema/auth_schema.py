from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class RegisterResponse(BaseModel):
    username: str
    email: str
