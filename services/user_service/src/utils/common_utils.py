import jwt
from config.config import *
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from src.models.user_model import UserModel

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


async def get_current_user(credentials=Depends(reusable_oauth2)):
    # parse token get payload
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[
        SECURITY_ALGORITHM], verify=True, detached_payload=True)

    # get username from payload
    username = payload.get('username')
    user = await UserModel.find_one({'username': username})
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return str(user.id)
