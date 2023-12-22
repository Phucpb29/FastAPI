from umongo import Document, fields
from .utils import user_instance


@user_instance.register
class UserModel(Document):
    username = fields.StringField(allow_none=False)
    password = fields.StringField(allow_none=False)
    email = fields.StringField(allow_none=False)
    # active = fields.BooleanField(default=False)
