import os
from dotenv import load_dotenv

load_dotenv()

# Db config
URI_DB = os.environ.get('URI')
COLLECTION_USER = os.environ.get('COLLECTION_USER')
COLLECTION_USER_PROFILE = os.environ.get('COLLECTION_USER_PROFILE')

# Config token
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURITY_ALGORITHM = os.environ.get('SECURITY_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get(
    'ACCESS_TOKEN_EXPIRE_MINUTES')


# Email config
HOST = os.environ.get('HOST_MAIL')
PORT = os.environ.get('PORT_MAIL')
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
