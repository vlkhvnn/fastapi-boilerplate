from datetime import datetime
from typing import Optional, List
from pymongo.results import UpdateResult
from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
            "phone": user["phone"],
            "name": user["name"],
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

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
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
    
    def add_to_favourites(self, user_id: str, shanyrak_id: str) -> UpdateResult:
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$push": {"favourites": shanyrak_id},
            },
        )
    
    def get_favourites(self, user_id: str) -> List[dict[str, str]]:
        document = self.database["users"].find_one(
            {"_id": ObjectId(user_id)},
            {"favourites": 1}
        )
        if document:
            favourites = document.get("favourites", [])
            return favourites
        else:
            return []

    def delete_favourite(self, shanyrak_id: str, user_id: str) -> UpdateResult:
        return self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"favourites": shanyrak_id}}
        )

    def add_avatar(self, url: str, user_id: str) -> UpdateResult:
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$set": {"avatar_url": url}}
        )
    
    def delete_avatar(self, user_id: str) -> UpdateResult:
        return self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            update={"$set": {"avatar_url": ""}}
        )
    
