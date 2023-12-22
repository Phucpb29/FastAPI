from umongo import Document, fields
from .utils import user_instance


@user_instance.register
class UserProfile(Document):
    user_id = fields.ObjectIdField()
    full_name = fields.StringField(allow_none=False)
    address = fields.StringField(allow_none=False)
    phone_number = fields.StringField(allow_none=False)
