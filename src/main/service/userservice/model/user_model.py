from pydantic import BaseModel
from bson import ObjectId


class UserModel(BaseModel):
    _id: str
    username: str
    password: str
    email: str
