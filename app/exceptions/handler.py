from flask.ext.api.exceptions import APIException


class UserAlreadyExists(APIException):
    """Raises a 406 status when username is already taken """
    status_code = 406
    detail = 'This name is already taken'


class CredentialsRequired(APIException):
    """Raises a 202 status if user is not authorized """
    status_code = 202
    detail = 'Credentials Required. Please authenticate by POSTING to auth/login with your credentials'


class ValidationError(APIException):
    """ Raises exception when token is invalid """
    status_code = 406
    detail = 'Invalid Token'


class NullBucketListException(APIException):
    """Raises exception when trying to edit non existing bucketlist item"""
    status_code = 404
    detail = 'No such bucketlist. You can only access an existing bucketlist'


class NullReferenceException(APIException):
    """Raises exception when trying to edit non existing bucketlist item"""
    status_code = 404
    detail = 'No such item in your bucketlist. \
        You can only edit/update existing items'
