from bson.objectid import ObjectId
from pymongo.database import Database
from typing import List


class ChatBotRepository:
    def __init__(self, database: Database):
        self.database = database
    
    def get_chat_history_by_id(self, user_id: str) -> List[dict[str, str]]:
        data = self.database["users"].find_one({"_id": ObjectId(user_id)})
        return data["chat_history"]

    def add_user_message(self, user_id: str, user_message: str):
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$push": {"chat_history": {'role': 'user', 'content': user_message}}
            },
        )

    def add_response(self, user_id: str, response: str):
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$push": {"chat_history": {'role': 'assistant', 'content': response}}
            },
        )
