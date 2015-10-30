from flask.ext.api.exceptions import APIException


class UserExists(APIException):
    """Raise a 406 malformed when the username is in use
    """
    status_code = 406
    detail = 'This username is in use.'


class CredentialsRequired(APIException):
    """Raises a 202 accepted when the user first accesses GET /login
    """
    status_code = 202
    detail = "Make a POST to '/login' with your credentials to begin a session"


class ValidationError(APIException):
    """Raises a token is not valid when the token can't be matched to a user record
    """
    status_code = 406
    detail = 'Invalid token'
