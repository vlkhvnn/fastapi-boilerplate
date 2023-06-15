from pydantic import BaseSettings
from app.config import database
from .repository.repository import ShanyrakRepository
from .adapters.s3_service import S3Service
from .adapters.here_service import HereService


class Config(BaseSettings):
    HERE_API_KEY: str


class Service:
    def __init__(self):
        config = Config()        
        self.repository = ShanyrakRepository(database)
        self.s3_service = S3Service()
        self.here_service = HereService(config.HERE_API_KEY)


def get_service():
    svc = Service()
    return svc