from flask import request, current_app
from models import User, Session, db
from exceptions.wailer import UserExists
import jwt
import hashlib


MESSAGES = {
    "login": "You have been logged in successfully",
    "logout": "You have been logged out successfully",
    }


def register(username, password):
    """Registers a user on the bucketlist service
    """
    user = User.query.filter_by(username=username).first()
    db.session.remove()
    if user is not None:
        raise UserExists()
    else:
        user = User(username=username, password=password)
        user.save()
        return {
            "message": "You have been registered successfully",
            "more": "Continue to login to your personalized bucketlist"
        }, 201


def check_auth(username, password):
    """Checks that user credentials is valid
    """
    user = User.query.filter_by(username='john').first()
    db.session.remove()
    return user.is_valid_password(password)


def tokenize(username, password):
    """Generates a token and persists it in the database until
    user logs out
    """
    user_data = {
        'username': username,
        'password': hashlib.sha512(password).hexdigest()
    }
    user_query = User.query.filter_by(**user_data).first()
    secret_key = current_app.config.get('SECRET_KEY')
    token = jwt.encode(user_data, secret_key)
    session = Session(user_id=user_query.id, token=token)
    session.save()
    return token


def get_current_user_id():
    """Returns the current user id in the session
    """
    jwt_token = request.headers.get('Authorization')
    session = Session.query.filter_by(token=jwt_token[7:]).first()
    db.session.remove()
    return session.user_id


def logout():
    """Logs out a user from the session
    """
    jwt_token = request.headers.get('Authorization')
    session = Session.query.filter_by(token=jwt_token[7:]).first()
    Session.query.filter(Session.user_id == session.user_id).delete()
    db.session.remove()
    return True
