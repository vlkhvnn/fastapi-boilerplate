from . import router
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from fastapi import Depends
from app.auth.service import Service, get_service


@router.get("/{id}/chat/getresponse")
def get_response(
    question: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> str:
    svc.repository.ensure_fit_tokens(jwt_data.user_id)
    chat_history = svc.repository.get_chat_history_by_id(jwt_data.user_id)
    response = svc.openaiService.generate_chat_response(question, chat_history)
    svc.repository.add_user_message(jwt_data.user_id, question)
    svc.repository.add_response(jwt_data.user_id, response)
    return response