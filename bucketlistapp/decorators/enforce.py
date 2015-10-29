from flask import request
from functools import wraps
from ..models import Session, BucketList, BucketListItem, db
from flask.ext.api.exceptions import AuthenticationFailed, PermissionDenied, \
    NotFound
from auth import get_current_user_id

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
            session = Session.query.filter_by(token=jwt_token[7:]).first()
            db.session.remove()
        except:
            raise AuthenticationFailed()
        if not session:
            return AuthenticationFailed()
        return f(*args, **kwargs)
    return decorated
