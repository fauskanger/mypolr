import requests
from functools import wraps


def no_raise(f):
    """Decorator/wrapper function to force return None instead of raising module exceptions.

    Exceptions that can be ignored are found in mypolr.exceptions."""
    @wraps(f)
    def new_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except MypolrError:
            pass
        return None
    return new_f


class MypolrError(Exception):
    """
    Base class for all module exceptions
    """


class DebugTempWarning(Warning, MypolrError):
    """Temporary Warning that should be removed"""
    def __init__(self):
        super(DebugTempWarning, self).__init__('This should not happen')


class CustomEndingUnavailable(ValueError, MypolrError):
    """Raised when a custom ending is in use and therefore cannot be created.

    :param str custom_ending: the custom ending that was unavailable
    """
    def __init__(self, custom_ending):
        msg = 'Custom ending already in use: {}'.format(custom_ending)
        super(CustomEndingUnavailable, self).__init__(msg)


class BadApiRequest(requests.HTTPError, MypolrError):
    """Raised when a request is malformed or otherwise is not understandable by server."""
    def __init__(self):
        msg = 'HTTP 400 Bad Request: Request malformed, or arguments do not fit the required data type.'
        super(BadApiRequest, self).__init__(msg)


class BadApiResponse(ValueError, MypolrError):
    """Raised when a response is malformed and cannot be interpreted as valid JSON."""
    def __init__(self):
        msg = 'Cannot interpret API response: invalid JSON.'
        super(BadApiResponse, self).__init__(msg)


class UnauthorizedKeyError(requests.HTTPError, MypolrError):
    """Raised when an invalid key has been used in a request.

    This refers either to:
    the API_KEY used in all endpoints, or the URL_KEY optionally used at the lookup endpoint.

    :param msg:
    :type msg:
    """
    def __init__(self, msg=None):
        msg = msg or 'API_KEY invalid or inactive.'
        super(UnauthorizedKeyError, self).__init__('HTTP 401 Unauthorized: {}'.format(msg))


class QuotaExceededError(requests.HTTPError, MypolrError):
    """Admins may assign quotas to users, and this is raised when it's exceeded and service stopped."""
    def __init__(self):
        msg = 'HTTP 403 Forbidden: quota is exceeded.'
        super(QuotaExceededError, self).__init__(msg)


class ServerOrConnectionError(requests.ConnectionError, MypolrError):
    """Raised when there is a timeout, internal server error, or any other connection error."""
    def __init__(self):
        msg = 'API cannot be reached. Check connection or server status.'
        super(ServerOrConnectionError, self).__init__(msg)
