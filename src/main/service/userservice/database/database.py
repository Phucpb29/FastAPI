from pymongo.mongo_client import MongoClient
from config.config import *

# Connect DB
client = MongoClient(URI_DB)
try:
    client.admin.command('ping')
    db = client.userserivce
    user_repository = db[COLLECTION_USER]
    user_profile_repository = db[COLLECTION_USER_PROFILE]
except Exception as e:
    print(e)
