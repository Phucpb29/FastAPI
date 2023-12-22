from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserProfileRequest(BaseModel):
    full_name: str | None = Field(default=None)
    address: str | None = Field(default=None, max_length=50)
    phone_number: str | None = Field(
        default=None, min_length=10, max_length=11)
