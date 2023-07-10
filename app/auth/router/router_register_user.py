from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class RegisterUserRequest(AppModel):
    email: str
    phone: str
    password: str


class AuthorizeUserResponse(AppModel):
    access_token: str
    token_type: str = "Bearer"


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=AuthorizeUserResponse
)
def register_user(
    input: RegisterUserRequest,
    svc: Service = Depends(get_service),
) -> str:
    if svc.repository.get_user_by_email(input.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )

    svc.repository.create_user(input.dict())
    user = svc.repository.get_user_by_email(input.email)
    return AuthorizeUserResponse(
        access_token=svc.jwt_svc.create_access_token(user=user),
    )
