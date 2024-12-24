from fastapi import APIRouter, Depends, Response
from ..database import get_db
from ..repository.user_repository import UserRepository
from ..service.auth_service import AuthService
from ..util.helper import Helper
from ..security.authenticated_user import authenticated_user
from ..schema.auth_schema import LoginRequest, RegisterRequest
from sqlalchemy.orm import Session


router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    helper = Helper()
    return AuthService(user_repository=user_repository, helper=helper)


@router.post("/login")
async def login(
    response: Response,
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    result = auth_service.login(request.email, request.password)

    response.set_cookie(key="access_token", value=result["access_token"], httponly=True)
    response.set_cookie(
        key="refresh_token", value=result["refresh_token"], httponly=True
    )

    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
    }


@router.post("/register", status_code=201)
async def register(
    user: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register(user)


@router.get("/private")
async def private(current_user: dict = Depends(authenticated_user)):
    return {"message": f"Hello {current_user['username']}"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logout successful"}
