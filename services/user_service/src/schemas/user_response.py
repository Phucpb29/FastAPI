from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    full_name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    email: str | None = None
