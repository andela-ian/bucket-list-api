from flask import make_response, jsonify, session
from functools import wraps
from models import User, db
from tools import decypher


def check_auth(username, password):
    """Checks that user credentials is valid
    """
    user = User.query.filter_by(username='john').first()
    return user.is_valid_password(password)


def authenticate():
    """Returns error message if authentication fails
    """
    message = {'message': 'Unauthorized access'}
    return make_response(jsonify(message), 401)


def requires_auth(f):
    """Enforces client authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = session['user']
        if not auth:
            return authenticate()
        elif not check_auth(auth[0], auth[1]):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def get_current_user_id():
    """Returns the current user id in the session
    """
    username, password = decypher(session['user'])
    query_result = db.session.query(User).filter(
            User.username == username,
            User.password == password).first()
    return query_result.id