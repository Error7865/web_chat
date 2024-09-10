from functools import wraps
from .errors import forbidden
from ..models import User,db

def user_required(user_key):
    def check_user(func):
        @wraps(func)
        def wrap_check_user(*args, **kwargs):
            user=User.query.filter_by(user_key=user_key).first()
            if user is None:
                return forbidden('User key is not valid.')
            return func(*args, **kwargs)
        return wrap_check_user
    return check_user