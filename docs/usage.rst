******************
User Guide
******************


Quick Example
=============
Here is an incomplete example. See `Advanced Usage`_ below for a more detailed description.

.. before-usage-example

.. code-block:: python

    from mypolr import PolrApi, exceptions

    # Replace with your values
    server_url = 'polr.example.com'
    api_key = '1234567890abcdef'

    # Example url to shorten
    long_url = 'https://some.long.example.com/long/url'

    # Create PolrApi instance
    api = PolrApi(server_url, api_key)

    # Make short urls
    shorted_url = api.shorten(long_url)
    custom_url = api.shorten(long_url, custom=CUSTOM_ENDING)

    # Given a short url ending, find full url and stats:
    lookup_dict = api.lookup(SHORT_URL_ENDING)
    full_url = lookup_dict.get('long_url')
    n_clicks = lookup_dict.get('clicks')

    # Secret urls have an additional key after the short url ending
    # E.g the format <polr root folder> / SHORT_URL_ENDING / URL_KEY:
    secret_url = api.shorten(long_url, is_secret=True)
    # Secret lookups require url_key:
    secret_lookup = api.lookup('aTiny2', url_key='secret_key')

.. after-usage-example

.. before-advanced-example
.. _advanced-example:

Advanced Usage
==============
This example is more thorough, and covers the various errors and edge cases you might encounter with the Polr Project
API.

The following examples assume the Polr Project is installed on a server at `https://ti.ny`,
and that a valid API_KEY is stored in a submodule ``auth.secrets``.

Set up API
----------
This is how the API would be set up given the aforementioned (and arbitrary) assumptions:


.. code-block:: python

    from mypolr import PolrApi, exceptions
    from auth.secrets import api_key

    # Example url to shorten
    long_url = 'https://stackoverflow.com/questions/tagged/python'

    # Your api server url
    server_url = 'https://ti.ny'

    # Create PolrApi instance
    api = PolrApi(server_url, api_key)


Shorten long URLs
-----------------

Given a long url, the ``PolrApi.shorten()``-method produces a short url on the form ``https://ti.ny / URL_ENDING``:

.. code-block:: python

    try:
        # Generate a short url with automatic mapping
        automatic_url = api.shorten(long_url)
        # Generate a short url with the ending 'soPython'
        custom_url = api.shorten(long_url, custom_ending='soPython')

        print(automatic_url)    # E.g. https://ti.ny/5N3f8
        print(custom_url)       # E.g. https://ti.ny/soPython
    except exceptions.UnauthorizedKeyError:
        print('API_KEY invalid or inactive.')
    except exceptions.CustomEndingUnavailable:
        print('Custom ending is already in use: choose another.')
    except exceptions.QuotaExceededError:
        print('User account associated with API_KEY has exceeded their quota.')
    except exceptions.ServerOrConnectionError:
        print('Check server and/or connection status.')
    except exceptions.BadApiRequest:
        print('Something was wrong with the request to server.')
    except exceptions.BadApiResponse:
        print('Response from server was not valid JSON.')

Lookup short URLs
-----------------
The ``PolrApi.lookup()``-method accepts either a short url ending, or a full short url, and returns ``False`` if no
url is found, or returns a dictionary of info about the link.

.. code-block:: python

    try:
        # Lookup short url to get info
        url_info = api.lookup('https://ti.ny/soPython')
        url_info = api.lookup('soPython')
        if url_info is False:
            print('No url found with that ending.')
        else:
            print('Full url is: {}'.format(url_info.get('long_url')))
    except exceptions.UnauthorizedKeyError:
        print('API_KEY invalid or inactive.')
    except exceptions.ServerOrConnectionError:
        print('Check server and/or connection status.')
    except exceptions.BadApiRequest:
        print('Something was wrong with the request to server.')
    except exceptions.BadApiResponse:
        print('Response from server was not valid JSON.')

Lookup result
'''''''''''''
Response of a successful lookup results in a dictionary á la something like this:

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
                'date': '2017-12-03 00:40:45.000000',
                'timezone': 'UTC',
                'timezone_type': 3
            }
    }


Secret URLS
-----------

Secret urls are made with the form ``https://ti.ny / URL_ENDING / URL_KEY``.
The additional part, URL_KEY, is required as a parameter when doing lookup of secret urls.

.. code-block:: python

    # Working with secret urls
    secret_long_url = 'https://stackoverflow.com/questions/tagged/cryptography'

    # Can still use both automatic or custom mapping
    secret_url = api.shorten(secret_long_url, is_secret=True)
    secret_custom_url = api.shorten(secret_long_url, custom_ending='soSecret', is_secret=True)

    print(secret_url)           # E.g. https://ti.ny/gztns/bXL2
    print(secret_custom_url)    # E.g. https://ti.ny/soSecret/F3iH

    try:
        secret_url_info = api.lookup('soPython', url_key='F3iH')
    except exceptions.UnauthorizedKeyError:
        print('Your URL_KEY is wrong, or the API_KEY is invalid.')

.. note:: The ``exceptions.UnauthorizedKeyError`` should be caught `in addition to` the
          others in the ``PolrApi.lookup()`` example above.

Ignoring Errors
---------------
By applying the ``mypolr.exceptions.no_raise_(f)`` decorator, the
``PolrApi.shorten_no_raise()`` and ``PolrApi.lookup_no_raise()``
will act as their corresponing normal methods,
but will return ``None`` instead of raising **module** exceptions upon errors.

The ``PolrApi.lookup_no_raise()``-method still returns ``False`` when no lookup is found.

.. code-block:: python

    # Use the _no_raise-methods to return None instead of exceptions as above
    short_url = api.shorten_no_raise(long_url)
    url_info = api.lookup_no_raise('soPython')

    if short_url is None:
        print('There was an error with the url shortening process.')

    if url_info is False:
        print('No url with that ending')
    elif url_info is None:
        print('There was an error with the url lookup process.')

.. warning:: Even though using the `\*_no_raise`-methods allows for easy check of failure/success,
             there is no feedback on what went wrong upon failure.

.. note:: The `\*_no_raise`-methods will still raise *other* exceptions, and
          **ONLY** errors derived from ``mypolr.exception.MypolrError`` will instead return ``None``.

.. after-advanced-example
