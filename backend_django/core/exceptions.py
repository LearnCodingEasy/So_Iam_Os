from rest_framework.exceptions import APIException


class CoreAPIException(APIException):
    """
    Base exception for So_Iam_OS core errors.
    """

    status_code = 400
    default_detail = "A core application error occurred."
    default_code = "core_error"


class ResourceNotFoundException(CoreAPIException):
    """
    Raised when a shared resource cannot be found.
    """

    status_code = 404
    default_detail = "The requested resource was not found."
    default_code = "resource_not_found"


class InvalidOperationException(CoreAPIException):
    """
    Raised when an operation is not allowed.
    """

    status_code = 400
    default_detail = "This operation is not allowed."
    default_code = "invalid_operation"
