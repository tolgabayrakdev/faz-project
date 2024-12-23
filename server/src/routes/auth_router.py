from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from ..service.auth_service import AuthService
from ..database import get_db
from ..schema.auth_schema import LoginRequest, RegisterRequest

router = APIRouter()


@router.post("/login")
async def login(
    request: LoginRequest, response: Response, db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    result = auth_service.login(request.email, request.password)

    response.set_cookie(key="access_token", value=result["access_token"], httponly=True)
    response.set_cookie(
        key="refresh_token", value=result["refresh_token"], httponly=True
    )

    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
    }


@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.register(request.model_dump())


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Successfully logged out"}
