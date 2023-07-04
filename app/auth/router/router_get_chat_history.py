from . import router
from fastapi import Depends
from typing import List
from app.auth.service import Service, get_service
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.get("users/{id}/chat")
def get_chat(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> List[dict[str, str]]:
    response = svc.repository.get_chat_history_by_id(jwt_data.user_id)
    return response