from flask import request, current_app
from functools import wraps
from models import User, Session, db
from flask.ext.api.exceptions import AuthenticationFailed
import jwt


MESSAGES = {
    "login": "You have been logged in successfully",
    "logout": "You have been logged out successfully",
    }


def check_auth(username, password):
    """Checks that user credentials is valid
    """
    user = User.query.filter_by(username='john').first()
    return user.is_valid_password(password)


def tokenize(username, password):
    """Generates a token and persists it in the database until
    user logs out
    """
    user_data = {'username': username, 'password': password}
    user_query = User.query.filter_by(**user_data).first()
    secret_key = current_app.config.get('SECRET_KEY')
    token = jwt.encode(user_data, secret_key)
    session = Session(user_id=user_query.id, token=token)
    db.session.add(session)
    db.session.commit()
    return token


def requires_auth(f):
    """Enforces client authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            jwt_token = request.headers.get('Authorization')
            session = Session.query.filter_by(token=jwt_token[7:]).first()
        except:
            raise AuthenticationFailed()
        if not session:
            return AuthenticationFailed()
        return f(*args, **kwargs)
    return decorated


def get_current_user_id():
    """Returns the current user id in the session
    """
    jwt_token = request.headers.get('Authorization')
    session = Session.query.filter_by(token=jwt_token[7:]).first()
    return session.user_id


def logout():
    """Logs out a user from the session
    """
    jwt_token = request.headers.get('Authorization')
    session = Session.query.filter_by(token=jwt_token[7:]).first()
    Session.query.filter(Session.user_id == session.user_id).delete()
    return True
