from pydantic import BaseModel
from bson import ObjectId


class UserProfile(BaseModel):
    full_name: str
    address: str
    phone_number: str
