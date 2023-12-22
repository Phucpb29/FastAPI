from config.config import *
from databases.mongo_database import get_umongo_instance

user_instance = get_umongo_instance(
    'mongodb://admin:admin@172.27.230.33:27017/?authMechanism=DEFAULT', 'user')
