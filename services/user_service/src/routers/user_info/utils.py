from fastapi import HTTPException
from bson.objectid import ObjectId
from constants.success_log import reponse_success_log, reponse_success_log_object
from src.models.user_profile import UserProfile
from src.schemas.user_request import UserProfileRequest
from src.schemas.user_response import UserProfileResponse


class UserServiceHandle():
    @classmethod
    async def get_profile(self, current_user):
        user_profile = await UserProfile.find_one({'user_id': ObjectId(current_user)})
        if user_profile is None:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        user_profile_response = UserProfileResponse(
            full_name=user_profile['full_name'],
            address=user_profile['address'],
            phone_number=user_profile['phone_number']
        )
        return reponse_success_log_object(200, 'data', user_profile_response)

    @classmethod
    async def create_profile(self, user_profile_data: UserProfileRequest, current_user):
        await self.create_or_update(self, user_profile_data, current_user)
        return reponse_success_log(200, 'Success')

    @classmethod
    async def update_profile(self, user_profile_data: UserProfileRequest, current_user):
        await self.create_or_update(self, user_profile_data, current_user)
        return reponse_success_log(200, 'Success')

    @classmethod
    async def delete_profile(self, current_user):
        user_profile = await UserProfile.find_one({'user_id': ObjectId(current_user)})
        if user_profile is None:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        UserProfile.collection.delete_one(
            {'_id': ObjectId(user_profile.id)})
        return reponse_success_log(200, 'Success')

    async def create_or_update(self, user_profile_data: UserProfileRequest, current_user):
        address = user_profile_data.address
        full_name = user_profile_data.full_name
        phone_number = user_profile_data.phone_number

        await UserProfile.collection.update_one(
            {'user_id': ObjectId(current_user)},
            {'$set': {
                'user_id': ObjectId(current_user),
                'address': address,
                'full_name': full_name,
                'phone_number': phone_number
            }}, upsert=True)
