import requests
import responses
import pytest

from mypolr import PolrApi, exceptions as polr_errors


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


    *After* (and **only** after) mappings have been added, the ``make_endpoint_tests()`` can be called. E.g.:

    .. code-block:: python

        rmap.make_endpoint_tests(my_api.action, 'foo', 42, dict(user='Alice', pass='pass123'))

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

    def __init__(self, response_args=None, errors=None, common_kwargs=None):
        self.response_args = response_args or []
        self.errors = errors or []
        self.common_kwargs = common_kwargs or {}

    def add(self, response_kwargs, error):
        """

        :param response_kwargs: a dictionary of arguments to ``response.add()``
        :type response_kwargs: list or None
        :param error: the error that pytest should expect with ``pytest.raises(error)``.
        :type error: list or None
        :return: None
        """
        self.response_args.append(response_kwargs)
        self.errors.append(error)

    def make_endpoint_tests(self, f, *args, **kwargs):
        for kws in self.response_args:
            kws.update(self.common_kwargs)
            responses.add('GET', api.api_shorten_endpoint, **kws)

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


def test_endpoint_url_building():
    assert api.api_shorten_endpoint == api_server + '/api/v2/action/shorten'
    assert api.api_lookup_endpoint == api_server + '/api/v2/action/lookup'
    # The next one is not implemented, but the endpoint should be correct anyway
    assert api.api_link_data_endpoint == api_server + '/api/v2/data/link'


@responses.activate
def test_make_requests_success():
    short_url = '{}/abcd'.format(api_server)
    json_resp = json_action('shorten', short_url)
    assert json_resp == dict(action='shorten', result=short_url)
    responses.add('GET', api.api_shorten_endpoint, json=json_resp, status=200)
    data, r = api._make_request(api.api_shorten_endpoint, dict(url=long_url))
    assert r.status_code == 200
    assert data == json_resp


@responses.activate
def test_make_request_errors():
    short_url = '{}/abcd'.format(api_server)
    json_resp = json_action('shorten', short_url)

    rmap = ResponseErrorMap()
    rmap.add(dict(status=401, json=json_resp), polr_errors.UnauthorizedKeyError)
    rmap.add(dict(status=400, json=json_resp), polr_errors.BadApiRequest)
    rmap.add(dict(status=500, json=json_resp), polr_errors.ServerOrConnectionError)
    rmap.add(dict(body=ValueError()), polr_errors.BadApiResponse)
    rmap.add(dict(body=requests.RequestException()), polr_errors.ServerOrConnectionError)

    rmap.make_endpoint_tests(api.shorten, short_url)


class TestShorten:
    @responses.activate
    def test_shorten_success(self):
        short_url = '{}/abcd'.format(api_server)
        json_data = json_action('shorten', short_url)

        responses.add('GET', api.api_shorten_endpoint, json=json_data, status=200)
        assert api.shorten(long_url) == short_url

    # @responses.activate
    # def test_shorten_fails(self):
    #     responses.add('GET', api.api_shorten_endpoint, body=, status=200)
    #     responses.add('GET', api.api_shorten_endpoint, body=, status=200)
    #
    #     with pytest.raises(requests.ConnectionError):
    #         api.shorten(long_url)
    #     with pytest.raises(requests.ConnectionError):
    #         api.shorten(long_url)

