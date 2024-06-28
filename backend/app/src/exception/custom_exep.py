from rest_framework.exceptions import APIException


class CustomException(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidIdentifierError(CustomException):
    """Exception raised for errors in the input identifier.

    Attributes:
        identifier -- input identifier which caused the error
        message -- explanation of the error
    """

    def __init__(self, identifier, message="Invalid identifier provided"):
        self.identifier = identifier
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.identifier} -> {self.message}'


class InvalidDataError(CustomException):
    status_code = 400
    default_detail = 'Datos inválidos'
    default_code = 'datos_invalidos'

    def __init__(self, detail=None, data=None):
        if detail is not None:
            self.detail = {
                'error': detail,
                'data': data
            }
        else:
            self.detail = {
                'error': self.default_detail,
                'data': data
            }

    def __str__(self):
        return  f'{self.detail["error"]}'
