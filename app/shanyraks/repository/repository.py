from typing import Any
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        data["comments"] = []
        data["media"] = []
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def update_shanyrak(self, shanyrak_id: str, user_id: str, data: dict[str, Any]) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
    
    def upload_photos(self, shanyrak_id: str, media : list[str]) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$set": {"media": media},
            },
        )
    
    def get_media(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})
    
    def delete_photo(self, shanyrak_id: str, user_id: str, photo_name: str) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            {"$pull": {"media": photo_name}}
        )
    
    def create_comment(self, user_id: str, shanyrak_id: str, content: str) -> UpdateResult:
        data = dict()
        comm_id = str(ObjectId())
        data["_id"] = comm_id
        data["content"] = content
        data["author_id"] = ObjectId(user_id)
        data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$push": {"comments": data},
            },
        )

    def get_comments(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def update_comment(self, shanyrak_id: str, comment_id: str, content: str) -> UpdateResult:
        collection = self.database["shanyraks"]
        update_query = {"$set": {"comments.$[comment].content": content}}
        array_filters = [{"comment._id": comment_id}]
        filter_query = {"_id": ObjectId(shanyrak_id)}
        return collection.update_one(filter_query, update_query, array_filters=array_filters)

    def delete_comment(self, user_id: str, shanyrak_id: str, comment_id: str) -> UpdateResult:
        collection = self.database["shanyraks"]
        update_query = {"$pull": {"comments": {"_id": comment_id}}}
        filter_query = {"_id": ObjectId(shanyrak_id), 
                        "user_id": ObjectId(user_id)}
        return collection.update_one(filter_query, update_query)