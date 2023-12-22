from fastapi import APIRouter, Depends, BackgroundTasks
from src.utils.common_utils import get_current_user
from constants.success_log import reponse_success_log
from src.schemas.user_request import UserLogin, UserRegister
from src.routers.authenticate.utils import AuthenticateHandler

rooter = APIRouter(prefix='/auth', tags=['Authenticate'])


@rooter.post("/login")
async def login(user_login_data: UserLogin):
    resposne = await AuthenticateHandler.login(user_login_data)
    return resposne


@rooter.post("/register")
async def register(user_register_data: UserRegister, background_tasks: BackgroundTasks):
    resposne = await AuthenticateHandler.register(user_register_data, background_tasks)
    return resposne

# API verify active user from email
# @rooter.get('/active')
# async def active(current_user: str = Depends(get_current_user)):
#     await AuthenticateHandler.active_user(current_user)
#     return reponse_success_log(200, 'Success')


@rooter.get("/whoami")
def whoami(current_user: str = Depends(get_current_user)):
    return reponse_success_log(200, 'Success')
