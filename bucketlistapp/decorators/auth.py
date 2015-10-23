from flask import request, current_app
from functools import wraps
from models import User, Session, BucketList, BucketListItem, db
from flask.ext.api.exceptions import AuthenticationFailed, PermissionDenied, \
    NotFound
from ..exceptions.wailer import UserExists
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
        db.session.add(user)
        db.session.commit()
        db.session.remove()
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
    db.session.add(session)
    db.session.commit()
    db.session.remove()
    return token


def belongs_to_user(f):
    """Enforces model ownership by user
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        bucketlist_id = kwargs.get('id')
        bucketlist = BucketList.query.get(int(bucketlist_id))
        db.session.remove()
        if bucketlist.created_by != get_current_user_id():
            raise PermissionDenied()
        return f(*args, **kwargs)
    return decorated


def belongs_to_bucketlist(f):
    """Enforces bucketlistitem ownership by bucketlist
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        bucketlist_id = kwargs.get('id')
        bucketlistitem_id = kwargs.get('item_id')
        bucketlistitem = BucketListItem.query.get(int(bucketlistitem_id))
        db.session.remove()
        if bucketlistitem:
            try:
                assert bucketlistitem.bucketlist_id == int(bucketlist_id)
            except:
                raise NotFound()
        kwargs['bucketlistitem'] = bucketlistitem
        return f(*args, **kwargs)
    return decorated


def requires_auth(f):
    """Enforces client authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            jwt_token = request.headers.get('Authorization')
            session = Session.query.filter_by(token=jwt_token[7:]).first()
            db.session.remove()
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
