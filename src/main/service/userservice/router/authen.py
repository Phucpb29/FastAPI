import jwt
from fastapi import *
from config.config import *
from datetime import datetime, timedelta
from model.user_model import UserModel
from model.user_profile import UserProfile
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from database.database import user_repository, user_profile_repository
from smtplib import SMTP
from ssl import create_default_context
from email.mime.text import MIMEText


authen = APIRouter()


reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


@authen.get('/register')
def register_user(username: str, password: str, email: str, background_tasks: BackgroundTasks):
    user_exsit = user_repository.find_one(
        {'username': username}, {'delete': False})
    if user_exsit:
        return {'Message': 'User is exist in system'}
    hash_password = generate_hash_password(password)
    user = {
        'username': username,
        'password': hash_password,
        'email': email,
        'delete': False
    }
    background_tasks.add_task(send_mail_register, email)
    background_tasks.add_task(write_log_register, username, datetime.now())
    user_repository.insert_one(user)
    return {'message': 'Success'}


def generate_hash_password(password):
    return pwd_context.hash(password)


async def write_log_register(username, date):
    with open('./log/register.log', mode='a') as log_file:
        content = f'New user has register: {username} {date} \n'
        log_file.write(content)


async def send_mail_register(email):
    try:
        msg = MIMEText('Register success', "html")
        msg['Subject'] = 'Notify register from FastAPI demo'
        msg['From'] = EMAIL_USER
        msg['To'] = email

        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=create_default_context())
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


def create_profile_default(username: str):
    user_profile_data = {
        'username': username,
        'full_name': 'default_fullname',
        'address': 'default_address',
        'phone_number': '0938697503'
    }
    user_profile_repository.insert_one(user_profile_data)


@authen.get('/login')
def login(username: str, password: str):
    user_data: UserModel = user_repository.find_one(
        {'username': username}, {'delete': False})
    if user_data:
        hash_password = user_data['password']
        is_match_password = verify_password(password, hash_password)
        if is_match_password:
            return {'token': generate_access_token(user_data['username'])}
        else:
            return {'message': 'Wrong information'}
    else:
        raise HTTPException(status_code=404, detail="User not found")


def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)


def generate_access_token(username):
    expire = datetime.utcnow() + timedelta(int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,
                             algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


@authen.get('/validate_token')
def validate_token(credentials=Depends(reusable_oauth2)):
    return validate_token(credentials)


def validate_token(credentials):
    payload = jwt.decode(credentials.credentials,
                         SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
    expired = payload.get('exp')
    if datetime.fromtimestamp(expired) < datetime.now():
        raise HTTPException(status_code=403, detail="Token expired")
    return payload.get('username')
