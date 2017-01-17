from flask import g
from flask_httpauth import HTTPTokenAuth
from app import database


auth = HTTPTokenAuth('token')


@auth.verify_token
def verify_token(token):
    g.user = None
    user = database.get_user(token=token)
    if user is not None:
        g.user = user
        return True
    return False
