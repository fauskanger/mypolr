********
Overview
********

This package, `mypolr`, is a simple python package for creating short links using the
`Polr Project <https://polrproject.org>`_'s REST
`API <https://docs.polrproject.org/en/latest/developer-guide/api/>`_.

Documentation:
    https://mypolr.readthedocs.io

GitHub:
    https://github.com/fauskanger/mypolr

Clone source:
    ``git clone git://github.com/fauskanger/mypolr.git``

Requirements
============

Polr Project
------------

Documentation:
    https://polrproject.org

To use `mypolr`, you need a valid API key to a server with the Polr Project installed.

You can obtain the API key by logging in to your Polr site and navigate to `<polr project root>/admin#developer`.

.. note:: **Disclaimer:** This package, `mypolr`, is not affiliated with the Polr Project.

Python
------

There is only one requirement:

- ``requests``, an awesome HTTP library. (`Documentation <http://python-requests.org>`_).

When installing with `pip` or `conda` this will be installed automatically (if not already installed).

Tested on Python 3.6, but should work with version 3.3 and newer.


Installation
============

With `pip`:
    ``pip install mypolr``


Coming soon
------------
**NOTE**: The `mypolr` package is *not yet* uploaded to `conda`.

With `conda`:
    ``conda install mypolr``


Usage
=====

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

License
=======
This project is licensed under the `MIT Licence <https://github.com/fauskanger/mypolr/blob/master/LICENSE>`_.
(See link for details.)


Epilogue
========
This project has served several purposes:

#. To easily utilize the Polr Project API with Python.
#. Be an exercise in packaging and distributing Python modules (with `pip` and `conda`).
#. Be an exercise in reStructuredText, Sphinx documentation, and ReadTheDocs.

