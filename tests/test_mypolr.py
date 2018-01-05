import requests
import responses
import pytest
import sys

from mypolr import PolrApi, DEFAULT_API_ROOT, exceptions as polr_errors



class ResponseErrorMap:
    """Maps sets of ``responses.add()``-arguments to expected exceptions.

    .. _pytest: https://docs.pytest.org
    .. _responses: https://github.com/getsentry/responses

    This works with pytest_ and responses_.

    Either pass mappings to initializer, or add them as pairs with ``add(response_args, errors)``:

    .. code-block:: python

        response_args = [
            dict(status=401, json=dict(error='please authorize')),
            dict(status=500, json=dict(error='internal error')),
            dict(body=requests.RequestException()),
            dict(body=ValueError())
        ]

        errors = [
            UnauthorizedKeyError,
            ServerOrConnectionError,
            ServerOrConnectionError,
            BadApiResponse,
        ]

        rmap = ResponseErrorMap(response_args, errors)

    which is the equivalent of doing this:

    .. code-block:: python

        rmap = ResponseErrorMap()
        rmap.add(dict(status=401, json=dict(error='please authorize')), UnauthorizedKeyError)
        rmap.add(dict(status=500, json=dict(error='internal error')), ServerOrConnectionError)
        rmap.add(dict(body=requests.RequestException()), ServerOrConnectionError)
        rmap.add(dict(body=ValueError()), BadApiResponse)


    *After* (and **only** after) mappings have been added, the ``make_error_tests()`` can be called. E.g.:

    .. code-block:: python

        rmap.make_error_tests(my_api.action, 'foo', 42, dict(user='Alice', pass='pass123'))

    This will:

     - add all ``response_args`` entries with ``responses.add(*args)``, and then

     - call the ``my_api.action()``-method with given arguments for each entry in the ``ResponseErrorMap``,
       but in a ``pytest.raises()``-context, like so:

    .. code-block:: python

        for error in self.errors:
            with pytest.raises(error):
                my_api.action('foo', 42, dict(user='Alice', pass='pass123'))


    :param response_args: list of dictionaries that will be the arguments for the given test
    :type response_args: list of dictionaries or None
    :param errors: list of exceptions that should be raised given when the corresponding response from response_args
                   is used.
    :type errors: list or None
    :param common_kwargs:
    :type common_kwargs: dict or None
    """

    def __init__(self, endpoint, response_args=None, errors=None, common_kwargs=None):
        self.endpoint = endpoint
        self.response_args = response_args or []
        self.errors = errors or []
        self.common_kwargs = common_kwargs or {}

    def add(self, response_kwargs, error):
        """

        :param response_kwargs: a dictionary of arguments to ``response.add()``
        :type response_kwargs: dict or None
        :param error: the error that pytest should expect with ``pytest.raises(error)``.
        :type error: type(Exception)
        :return: None
        """
        self.response_args.append(response_kwargs)
        self.errors.append(error)

    @responses.activate
    def make_error_tests(self, f, *args, **kwargs):
        for kws in self.response_args:
            kws.update(self.common_kwargs)
            responses.add('GET', self.endpoint, **kws)

        for error in self.errors:
            with pytest.raises(error):
                f(*args, **kwargs)


def json_action(action, result, **kwargs):
    kwargs = kwargs or {}
    kwargs.update(dict(action=action, result=result))
    return kwargs


def create_api():
    # Add trailing '/' to api_server to verify cleanup has been made
    # Don't add preceding '/' to api_root to verify cleanup has been made
    return PolrApi(api_server='https://ti.ny/', api_key=api_key, api_root='api/v2')


long_url = 'https://example.com'
api_key = 'test_key'
api = create_api()
api_server = api.api_server
api_root = api.api_root

short_url = '{}/abcd'.format(api_server)
shorten_resp = json_action('shorten', short_url)
lookup_resp = json_action('lookup', dict(long_url=long_url))


def test_endpoint_url_building():
    assert api.api_shorten_endpoint == api_server + '/api/v2/action/shorten'
    assert api.api_lookup_endpoint == api_server + '/api/v2/action/lookup'
    # The next one is not implemented, but the endpoint should be correct anyway
    assert api.api_link_data_endpoint == api_server + '/api/v2/data/link'


class TestMakeRequest:
    @responses.activate
    def test_success(self):
        assert shorten_resp == dict(action='shorten', result=short_url)
        responses.add('GET', api.api_shorten_endpoint, json=shorten_resp, status=200)
        data, r = api._make_request(api.api_shorten_endpoint, dict(url=long_url))
        assert r.status_code == 200
        assert data == shorten_resp

    def test_errors(self):
        # Use dummy endpoint as _make_requests is sensitive
        # to endpoints with regards to raising errors
        endpoint = 'https://ti.ny/dummy/fails'

        rmap = ResponseErrorMap(endpoint)
        rmap.add(dict(status=401, json=shorten_resp), polr_errors.UnauthorizedKeyError)
        rmap.add(dict(status=400, json=shorten_resp), polr_errors.BadApiRequest)
        rmap.add(dict(status=500, json=shorten_resp), polr_errors.ServerOrConnectionError)
        rmap.add(dict(body='this is not JSON'), polr_errors.BadApiResponse)
        rmap.add(dict(body=ValueError()), polr_errors.BadApiResponse)
        rmap.add(dict(body=requests.RequestException()), polr_errors.ServerOrConnectionError)

        rmap.make_error_tests(api._make_request, endpoint, {})


class TestShorten:
    @responses.activate
    def test_success(self):
        responses.add('GET', api.api_shorten_endpoint, json=shorten_resp, status=200)
        assert api.shorten(long_url) == short_url
        assert api.shorten(long_url, 'custom') == short_url
        assert api.shorten(long_url, 'custom', True) == short_url
        assert api.shorten(long_url, is_secret=True) == short_url

    def test_errors(self):
        rmap = ResponseErrorMap(api.api_shorten_endpoint)
        rmap.add(dict(status=400, json=shorten_resp), polr_errors.BadApiRequest)
        rmap.add(dict(status=403, json=shorten_resp), polr_errors.QuotaExceededError)
        rmap.make_error_tests(api.shorten, long_url, custom_ending=None, is_secret=False)

        rmap = ResponseErrorMap(api.api_shorten_endpoint)
        rmap.add(dict(status=400, json=shorten_resp), polr_errors.CustomEndingUnavailable)
        rmap.make_error_tests(api.shorten, long_url, custom_ending='someCustomEnding', is_secret=False)


class TestLookup:
    @responses.activate
    def test_success(self):
        responses.add('GET', api.api_lookup_endpoint, json=lookup_resp, status=200)
        assert api.lookup(long_url).get('long_url') == long_url
        assert api.lookup(long_url, 'a_secret').get('long_url') == long_url

    @responses.activate
    def test_not_found(self):
        responses.add('GET', api.api_lookup_endpoint, json={}, status=404)
        assert api.lookup(short_url) is False

    def test_errors(self):
        rmap = ResponseErrorMap(api.api_lookup_endpoint)
        rmap.add(dict(status=401, json=lookup_resp), polr_errors.UnauthorizedKeyError)
        rmap.make_error_tests(api.lookup, short_url, url_key='a_secret')


class TestCliArgs:
    def test_parser(self):
        from mypolr import is_cli_supported

        if not is_cli_supported:
            # Skip tests for old versions for which CLI usage is not supported
            return

        from mypolr.cli import get_args as _get_args

        none_kws = 'url server key custom'.split()
        bool_kws = 'version secret lookup save clear'.split()
        flags_true = ['--{}'.format(kw) for kw in bool_kws]

        args = _get_args([])
        assert args.api_root == DEFAULT_API_ROOT

        for kw in bool_kws:
            assert kw in args
            assert getattr(args, kw) is False

        for kw in none_kws:
            assert kw in args
            assert getattr(args, kw) is None

        args = _get_args(flags_true)
        for kw in bool_kws:
            assert kw in args
            assert getattr(args, kw) is True
