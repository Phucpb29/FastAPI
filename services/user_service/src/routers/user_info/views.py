from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from src.schemas.user_request import UserProfileRequest
from src.routers.user_info.utils import UserServiceHandle
from src.utils.common_utils import get_current_user


rooter = APIRouter(prefix="/user_profile", tags=['User Profile'])

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


@rooter.get("/get_profile")
async def get_profile(current_user: str = Depends(get_current_user)):
    response = await UserServiceHandle.get_profile(current_user)
    return response


@rooter.post("/create_profile")
async def create_profile(user_profile_data: UserProfileRequest, current_user: str = Depends(get_current_user)):
    response = await UserServiceHandle.create_profile(user_profile_data, current_user)
    return response


@rooter.post("/change_profile")
async def update_profile(user_profile_data: UserProfileRequest, current_user: str = Depends(get_current_user)):
    response = await UserServiceHandle.update_profile(user_profile_data, current_user)
    return response


@rooter.delete("/delete_profile")
async def delete_profile(current_user: str = Depends(get_current_user)):
    response = await UserServiceHandle.delete_profile(current_user)
    return response
