import jwt
from smtplib import SMTP
from config.config import *
from fastapi import HTTPException, BackgroundTasks
from email.mime.text import MIMEText
from ssl import create_default_context
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.models.user_model import UserModel
from constants.success_log import reponse_success_log
from src.schemas.user_request import UserLogin, UserRegister
from bson import ObjectId


pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


class AuthenticateHandler():

    @classmethod
    async def login(self, user_login_data: UserLogin):
        username = user_login_data.username
        user = await UserModel.find_one({'username': username})
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        hash_password = user['password']
        password_request = user_login_data.password
        is_match_password = self.verify_password(
            password_request, hash_password)
        if is_match_password is False:
            raise HTTPException(
                status_code=403,
                detail="Password doesn't match"
            )

        access_token = self.generate_access_token(username)
        return reponse_success_log(200, 'data', access_token)

    @classmethod
    async def register(self, user_register_data: UserRegister, background_tasks: BackgroundTasks):
        username = user_register_data.username
        user = await UserModel.find_one({'username': username})
        if user:
            raise HTTPException(
                status_code=400,
                detail="User is exsit",
                headers={"WWW-Authenticate": "Bearer"}
            )

        email = user_register_data.email
        password = user_register_data.password
        hash_password = self.generate_hash_password(password)

        try:
            # send email register for user
            background_tasks.add_task(self.send_mail_register, email)

            # write log register in file log
            background_tasks.add_task(
                self.write_log_register, username, datetime.now())

            user_model = UserModel(
                username=username,
                password=hash_password,
                email=email
            )
            # await user_model.commit()
            return reponse_success_log(200, 'Success')
        except:
            raise HTTPException(
                status_code=500,
                detail="Server error exception",
                headers={"WWW-Authenticate": "Bearer"}
            )

    # Function verify active user from email
    # @classmethod
    # async def active_user(current_user: str):
    #     user = UserModel.collection.find_one({'_id': ObjectId(current_user)})
    #     if user is None:
    #         raise HTTPException(
    #             status_code=401,
    #             detail='No matching user'
    #         )

    #     user['active'] = True
    #     user.commint()

    # =============================== Token ===============================

    def generate_hash_password(password_request):
        return pwd_context.hash(password_request)

    def verify_password(password_request: str, hash_password: str):
        return pwd_context.verify(password_request, hash_password)

    def generate_access_token(username):
        expire = datetime.utcnow() + timedelta(int(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode = {
            "exp": expire, "username": username
        }
        encoded_jwt = jwt.encode(
            to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
        return encoded_jwt

    # =============================== Tasks background ===============================
    async def write_log_register(username, date):
        file_direct = './src/log/register.log'
        with open(file_direct, mode='w', encoding='utf-8') as file_log_register:
            content = f'New user has register: {username} {date} \n'
            file_log_register.write(content)

    async def send_mail_register(email):
        try:
            msg = MIMEText('Register success', "html")
            msg['Subject'] = 'Notify register from FastAPI demo'
            msg['From'] = EMAIL_FULL_NAME
            msg['To'] = email

            with SMTP(HOST, PORT) as server:
                server.ehlo()
                server.starttls(context=create_default_context())
                server.ehlo()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
                server.quit
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)
