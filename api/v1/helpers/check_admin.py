# api/v1/helpers/check_admin.py

from flask import make_response
from api.v1.models import User

def check_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user.admin is False:
        assert False, "You are not authorized to perform this operation"
