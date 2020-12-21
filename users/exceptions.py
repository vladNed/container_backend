from rest_framework.exceptions import APIException


class UserCreationException(APIException):
    status_code = 400
    default_detail = "An error occured during user creation"
    default_code = 'user_creation_error'
