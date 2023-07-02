from datetime import datetime
from typing import Optional, List
from bson.objectid import ObjectId
from pymongo.database import Database
from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "username": user["username"],
            "phonenumber": user["phonenumber"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
            "chat_history": []
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_phonenumber(self, phonenumber: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "phonenumber": phonenumber,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )
    
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
    
    def delete_first_message_from_chat(self, user_id: str):
        self.database["users"].update_one({"_id": ObjectId(user_id)}, {"$pop": {"chat_history": -1}})

    def ensure_fit_tokens(self, user_id: str):
        if self.calculate_chat_size(user_id) > 10:
            self.delete_first_message_from_chat(user_id)
            self.delete_first_message_from_chat(user_id)

    def calculate_chat_size(self, user_id: str):
        document = self.database["users"].find_one({"_id": ObjectId(user_id)})
        if document:
            chat_history = document.get("chat_history", [])
            return len(chat_history)
        else:
            return 0


