from typing import Any
from fastapi import Depends, Response
from pydantic import Field
from app.auth.adapters.jwt_service import JWTData
from app.utils import AppModel
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.post("/{id}/comments")
def create_comment(
    shanyrak_id : str,
    input: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    comment_id = svc.repository.create_comment(jwt_data.user_id, shanyrak_id, input)
    if comment_id is None:
        return Response(status_code=404)
    return Response(status_code=200)