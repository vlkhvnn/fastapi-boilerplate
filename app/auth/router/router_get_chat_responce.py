from . import router
from fastapi import Depends
from app.auth.service import Service, get_service
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data


@router.get("/chat/getresponse")
def get_response(
    question: str,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> str:
    svc.repository.add_user_message(jwt_data.user_id, question)
    chat_history = svc.repository.get_chat_history_by_id(jwt_data.user_id)
    response = svc.openaiService.generate_chat_response(question, chat_history)
    svc.repository.add_response(jwt_data.user_id, response)
    return response