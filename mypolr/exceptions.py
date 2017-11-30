import requests


class DebugTempWarning(Warning):
    """Temporary Warning that should be removed"""
    def __init__(self):
        super(DebugTempWarning, self).__init__('This should not happen')


class CustomEndingUnavailable(ValueError):
    """Raised when a custom ending is in use and therefore cannot be created.

    :param str custom_ending: the custom ending that was unavailable
    """
    def __init__(self, custom_ending):
        msg = 'Custom ending already in use: {}'.format(custom_ending)
        super(CustomEndingUnavailable, self).__init__(msg)


class BadApiRequest(requests.HTTPError):
    """Raised when a request is malformed or otherwise is not understandable by server."""
    def __init__(self):
        msg = 'HTTP 400 Bad Request: Request malformed, or arguments do not fit the required data type.'
        super(BadApiRequest, self).__init__(msg)


class UnauthorizedKeyError(requests.HTTPError):
    """Raised when an invalid key has been used in a request.

    This refers either to:
    the API_KEY used in all endpoints, or the URL_KEY optionally used at the lookup endpoint.

    :param msg:
    :type msg:
    """
    def __init__(self, msg=None):
        msg = msg or 'API_KEY invalid or inactive.'
        super(UnauthorizedKeyError, self).__init__('HTTP 401 Unauthorized: {}'.format(msg))


class QuotaExceededError(requests.HTTPError):
    """Admins may assign quotas to users, and this is raised when it's exceeded and service stopped."""
    def __init__(self):
        msg = 'HTTP 403 Forbidden: quota is exceeded.'
        super(QuotaExceededError, self).__init__(msg)
