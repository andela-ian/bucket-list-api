from flask.ext.api.exceptions import APIException


class UserExists(APIException):
    status_code = 406
    detail = 'This username is in use.'
