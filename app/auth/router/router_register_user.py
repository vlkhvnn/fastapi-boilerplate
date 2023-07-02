from fastapi import Depends, HTTPException, status

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class RegisterUserRequest(AppModel):
    email: str
    phone: str
    password: str


@router.post(
    "/users", status_code=status.HTTP_201_CREATED
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

    return input.email
