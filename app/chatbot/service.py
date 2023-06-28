from app.config import database
from .repository.repository import ChatBotRepository
from .adapters.openai_service import OpenAIService


class Service:
    def __init__(self):
        self.repository = ChatBotRepository(database)
        self.openaiService = OpenAIService()


def get_service():
    svc = Service()
    return svc