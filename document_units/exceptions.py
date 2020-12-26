from rest_framework.exceptions import APIException
from rest_framework import status


class InvalidFormatData(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Given document format data is invalid'
    default_code = 'invalid_format_data'
