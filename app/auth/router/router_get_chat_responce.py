from . import router
from fastapi import Depends
from app.auth.service import Service, get_service


@router.get("/chat/getresponse")
def get_response(
    chat_history: str,
    question: str,
    svc: Service = Depends(get_service),
) -> str:
    response = svc.openaiService.generate_chat_response(question, chat_history)
    return response