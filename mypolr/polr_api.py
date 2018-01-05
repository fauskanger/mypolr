"""
This file defines the main component of the Mypolr package: the :class:`PolrApi` class.
"""
import requests

from mypolr import exceptions

DEFAULT_API_ROOT = '/api/v2/'


class PolrApi:
    """
    Url shorter instance that stores server and API key

    :param str api_server: The url to your server with Polr Project installed.
    :param str api_key: The API key associated with a user on the server.
    :param str api_root: API root endpoint.
    """
    def __init__(self, api_server, api_key, api_root=DEFAULT_API_ROOT):
        # Clean url and paths
        api_root = api_root if api_root.startswith('/') else '/{}'.format(api_root)
        api_root = api_root if api_root.endswith('/') else '{}/'.format(api_root)
        api_server = api_server if not api_server.endswith('/') else api_server[:-1]
        # Use cleaned up urls
        self.api_server = api_server
        self.api_root = api_root
        # Endpoint paths
        self.api_base = self.api_server + self.api_root
        self.api_shorten_endpoint = self.api_base + 'action/shorten'
        self.api_lookup_endpoint = self.api_base + 'action/lookup'
        self.api_link_data_endpoint = self.api_base + 'data/link'
        # API params
        self.api_key = api_key
        self._base_params = {
            'key': self.api_key,
            'response_type': 'json'
        }

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.api_base)

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
        """
        # params = {
        #     **self._base_params,  # Mind order to allow params to overwrite base params
        #     **params
        # }
        full_params = self._base_params.copy()
        full_params.update(params)
        try:
            r = requests.get(endpoint, full_params)
            data = r.json()
            if r.status_code == 401 and not endpoint.endswith('lookup'):
                raise exceptions.UnauthorizedKeyError
            elif r.status_code == 400 and not endpoint.endswith('shorten'):
                raise exceptions.BadApiRequest
            elif r.status_code == 500:
                raise exceptions.ServerOrConnectionError
            return data, r
        except ValueError as e:
            raise exceptions.BadApiResponse(e)
        except requests.RequestException:
            raise exceptions.ServerOrConnectionError

    def shorten(self, long_url, custom_ending=None, is_secret=False):
        """
        Creates a short url if valid, else returns None

        :param str long_url: The url to shorten.
        :param custom_ending: The custom url to create if available.
        :type custom_ending: str or None
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
                raise exceptions.CustomEndingUnavailable(custom_ending)
            raise exceptions.BadApiRequest
        elif r.status_code == 403:
            raise exceptions.QuotaExceededError
        action = data.get('action')
        short_url = data.get('result')
        if action == 'shorten' and short_url is not None:
            return short_url
        raise exceptions.DebugTempWarning  # TODO: remove after testing

    def _get_ending(self, lookup_url):
        """
        Returns the short url ending from a short url or an short url ending.

        Example:
         - Given `<your Polr server>/5N3f8`, return `5N3f8`.
         - Given `5N3f8`, return `5N3f8`.

        :param lookup_url: A short url or short url ending
        :type lookup_url: str
        :return: The url ending
        :rtype: str
        """
        if lookup_url.startswith(self.api_server):
            return lookup_url[len(self.api_server) + 1:]
        return lookup_url

    def lookup(self, lookup_url, url_key=None):
        """
        Looks up the url_ending to obtain information about the short url.

        If it exists, the API will return a dictionary with information, including
        the long_url that is the destination of the given short url URL.


        The lookup object looks like something like this:

        .. code-block:: python

            {
                'clicks': 42,
                'created_at':
                    {
                        'date': '2017-12-03 00:40:45.000000',
                        'timezone': 'UTC',
                        'timezone_type': 3
                    },
                'long_url': 'https://stackoverflow.com/questions/tagged/python',
                'updated_at':
                    {
                        'date': '2017-12-24 13:37:00.000000',
                        'timezone': 'UTC',
                        'timezone_type': 3
                    }
            }

        :param str lookup_url: An url ending or full short url address
        :param url_key: optional URL ending key for lookups against secret URLs
        :type url_key: str or None
        :return: Lookup dictionary containing, among others things, the long url; or None if not existing
        :rtype: dict or None
        """
        url_ending = self._get_ending(lookup_url)
        params = {
            'url_ending': url_ending,
            'url_key': url_key
        }
        data, r = self._make_request(self.api_lookup_endpoint, params)
        if r.status_code == 401:
            if url_key is not None:
                raise exceptions.UnauthorizedKeyError('given url_key is not valid for secret lookup.')
            raise exceptions.UnauthorizedKeyError
        elif r.status_code == 404:
            return False  # no url found in lookup
        action = data.get('action')
        full_url = data.get('result')
        if action == 'lookup' and full_url is not None:
            return full_url
        raise exceptions.DebugTempWarning  # TODO: remove after testing

    @exceptions.no_raise
    def shorten_no_raise(self, *args, **kwargs):
        """Calls `PolrApi.shorten(*args, **kwargs)` but returns `None` instead of raising module errors."""
        return self.shorten(*args, **kwargs)

    @exceptions.no_raise
    def lookup_no_raise(self, *args, **kwargs):
        """Calls `PolrApi.lookup(*args, **kwargs)` but returns `None` instead of raising module errors."""
        return self.lookup(*args, **kwargs) or False
