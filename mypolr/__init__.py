import requests
from functools import wraps

import mypolr.exceptions as errors


def no_raise(f):
    """Decorator/wrapper function to force return None instead of raising module exceptions.

    Exceptions that can be ignored are found in mypolr.exceptions."""
    @wraps(f)
    def new_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except errors.MypolrError:
            pass
        return None
    return new_f


class UrlShorter:
    """
    Url shorter instance that stores server and API key

    :param str api_server: The url to your server with Polr Project installed.
    :param str api_key: The API key associated with an user on server.
    :param str api_root: API root endpoint.
    """
    def __init__(self, api_server, api_key, api_root='/api/v2/', ):
        self.api_root = api_server + api_root
        self.api_shorten_endpoint = self.api_root + 'action/shorten'
        self.api_lookup_endpoint = self.api_root + 'action/lookup'
        self.api_link_data_endpoint = self.api_root + 'data/link'
        self.api_key = api_key
        self._base_params = {
            'key': self.api_key,
            'response_type': 'json'
        }

    def _make_request(self, endpoint, params):
        """
        Prepares the request and catches common errors and returns tuple of data and the request response.

        Read more about error codes: https://docs.polrproject.org/en/latest/developer-guide/api/#http-error-codes

        :param endpoint: full endpoint url
        :type endpoint: str
        :param params: parameters for the given endpoint
        :type params: dict
        :return: Tuple of response data, and the response instance
        :rtype: dict, requests.Response
        :raises: requests.HTTPError if API_KEY is invalid (or inactive),
        """
        params = {
            **self._base_params,
            **params
        }
        try:
            r = requests.get(endpoint, params)
            data = r.json()
            if r.status_code == 401 and not endpoint.endswith('lookup'):
                raise errors.UnauthorizedKeyError
            elif r.status_code == 400 and not endpoint.endswith('shorten'):
                raise errors.BadApiRequest
            elif r.status_code == 500:
                raise errors.ServerOrConnectionError
            return data, r
        except ValueError:
            raise errors.BadApiResponse
        except requests.RequestException:
            raise errors.ServerOrConnectionError

    def shorten(self, long_url, custom_ending=None, is_secret=False):
        """
        Creates a short url if valid, else returns None

        :param str long_url: The url to shorten.
        :param str or None custom_ending: The custom url to create if available.
        :param bool is_secret: if not public, it's secret
        :return: a short link
        :rtype: str
        """
        params = {
            'url': long_url,
            'is_secret': 'true' if is_secret else 'false',
            'custom_encoding': custom_ending
        }
        data, r = self._make_request(self.api_shorten_endpoint, params)
        if r.status_code == 400:
            if custom_ending is not None:
                raise errors.CustomEndingUnavailable(custom_ending)
            raise errors.BadApiRequest
        elif r.status_code == 403:
            raise errors.QuotaExceededError
        action = data.get('action')
        short_url = data.get('result')
        if action == 'shorten' and short_url is not None:
            return short_url
        raise errors.DebugTempWarning  # TODO: remove after testing

    def lookup(self, url_ending, url_key=None):
        """
        Looks up the url_ending to obtain the full url if it exists.

        If it exists, the API will return with the destination of that URL. Se

        :param url_key: optional URL ending key for lookups against secret URLs
        :type url_key: str or None
        :param str url_ending:
        :return: Url mapped to the url_ending or None if not existing
        :rtype: str or None
        """
        params = {
            'url_ending': url_ending,
            'url_key': url_key
        }
        data, r = self._make_request(self.api_lookup_endpoint, params)
        if r.status_code == 401:
            if url_key is not None:
                raise errors.UnauthorizedKeyError('given url_key is not valid for secret lookup.')
            raise errors.UnauthorizedKeyError
        elif r.status_code == 404:
            return None  # no url found in lookup
        action = data.get('action')
        full_url = data.get('result')
        if action == 'lookup' and full_url is not None:
            return full_url
        raise errors.DebugTempWarning  # TODO: remove after testing

    @no_raise
    def shorten_no_raise(self, *args, **kwargs):
        """
        Calls UrlShorter.shorten(*args, **kwargs) but returns None instead of raising module errors.
        """
        return self.shorten(*args, **kwargs)

    @no_raise
    def lookup_no_raise(self, *args, **kwargs):
        """
        Calls UrlShorter.lookup(*args, **kwargs) but returns None instead of raising module errors.
        """
        return self.lookup(*args, **kwargs)
