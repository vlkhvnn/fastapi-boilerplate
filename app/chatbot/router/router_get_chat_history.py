from . import router
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from fastapi import Depends
from app.chatbot.service import Service, get_service


@router.get("/{id}/chat_history")
def get_response(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    chat_history = svc.repository.get_chat_history_by_id(jwt_data.user_id)
    return chat_history