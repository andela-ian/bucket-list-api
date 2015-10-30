from flask import request, current_app
from functools import wraps
from ..models import Session, BucketList, BucketListItem, db, User
from flask.ext.api.exceptions import AuthenticationFailed, PermissionDenied, \
    NotFound
from ..exceptions.wailer import ValidationError
from ..auth import get_current_user_id
from flask.ext.sqlalchemy import sqlalchemy as S
import jwt


MESSAGES = {
    "login": "You have been logged in successfully",
    "logout": "You have been logged out successfully",
    }


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
            secret_key = current_app.config.get('SECRET_KEY')
            try:
                decoded_jwt = jwt.decode(jwt_token[7:], secret_key)
            except jwt.ExpiredSignatureError:
                raise PermissionDenied('Your token has expired! Please login.')
            User.query.filter_by(
                username=decoded_jwt['username'],
                password=decoded_jwt['password']).one()
            if not Session.query.filter_by(token=jwt_token[7:]):
                raise AuthenticationFailed()
        except (S.orm.exc.MultipleResultsFound, S.orm.exc.NoResultFound):
            raise ValidationError()
        return f(*args, **kwargs)
    return decorated
