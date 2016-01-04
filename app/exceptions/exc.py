from flask.ext.api.exceptions import APIException


class UserExists(APIException):
    """ Raises a 406 status when username is already taken """
    status_code = 406
    detail = 'This name is already taken'


class CredentialsRequired(APIException):
    """ Raises a 202 status if user is not authorized """
    status_code = 202
    detail = 'Authenticate by POSTING to /login with your credentials'


class ValidationError(APIException):
    """ Raises exception when token is invalid """
    status_code = 406
    detail = 'Invalid Token'