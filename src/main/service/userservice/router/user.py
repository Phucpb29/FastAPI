from fastapi import *
from model.user_profile import UserProfile
from fastapi.security import HTTPBearer
from router.authen import validate_token
from database.database import user_profile_repository
from bson import ObjectId


user = APIRouter()

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


@user.get("/user/get_profile")
def get_profile(credentials=Depends(reusable_oauth2)):
    username = validate_token(credentials)
    user__profile_data = user_profile_repository.find_one(
        {'username': username})
    if user__profile_data:
        return {
            'id': str(user__profile_data['_id']),
            'username': user__profile_data['username'],
            'address': user__profile_data['address'],
            'full_name': user__profile_data['full_name'],
            'phone_number': user__profile_data['phone_number']
        }
    else:
        return {'message': 'Plesase add your profile'}


@user.post("/user/add_profile")
def add_profile(user_profile_data: UserProfile, credentials=Depends(reusable_oauth2)):
    username = validate_token(credentials)
    user_profile_data_exist = user_profile_repository.find_one(
        {'username': username})
    if user_profile_data_exist:
        user_profile_repository.update_one(
            {'username': username},
            {'$set': {
                'full_name': user_profile_data.full_name,
                'address': user_profile_data.address,
                'phone_numner': user_profile_data.phone_number
            }}
        )
    else:
        user_profile = {
            'username': username,
            'full_name': user_profile_data.full_name,
            'address': user_profile_data.address,
            'phone_number': user_profile_data.phone_number
        }
        user_profile_repository.insert_one(user_profile)
    return {'message': 'Add profile success'}


@user.put("/user/change_profile")
def change_profile(user_profile_data: UserProfile, credentials=Depends(reusable_oauth2)):
    username = validate_token(credentials)
    user_profile_repository.update_one(
        {'username': username},
        {'$set': {
            'full_name': user_profile_data.full_name,
            'address': user_profile_data.address,
            'phone_numner': user_profile_data.phone_number
        }}
    )
    return {'message': 'Update profile success'}


@user.delete("/user/delete_profile")
def delete_profile(credentials=Depends(reusable_oauth2)):
    username = validate_token(credentials)
    # user_profile_repository.delete_one({'_id': ObjectId(id)})
    user_profile_repository.delete_one({'username': username})
    return {'message': 'Delete profile success'}
