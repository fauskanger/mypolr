********
Overview
********

``mypolr`` is a simple python package for creating short links using the
`Polr Project <https://polrproject.org>`_'s REST
`API <https://docs.polrproject.org/en/latest/developer-guide/api/>`_.

Documentation:
    https://mypolr.readthedocs.io

GitHub:
    https://github.com/fauskanger/mypolr

Clone source:
    ``git clone git://github.com/fauskanger/mypolr.git``

.. note:: **Disclaimer:** This package, `mypolr`, is not affiliated with the Polr Project.


Requirements
============

Polr Project
------------
To use `mypolr`, you need a valid API key to a server with the Polr Project installed.

You can obtain the API key by logging in to your Polr site and navigate to `<polr project root>/admin#developer`.

Python
------

There is only one requirement:

- the awesome HTTP library `requests` (`Documentation <http://python-requests.org>`_).

When installing with `pip` or `conda` this will be installed automatically (if not already installed).

Tested on Python 3.6, but should work with version 3.3 and newer.


Installation
============

Coming soon
------------

**NOTE**: The `mypolr` package is *not yet* uploaded to `pip` or `conda`.

With `pip`:
    ``pip install mypolr``

With `conda`:
    ``conda install mypolr``


Usage
=====

.. code-block:: python

    from mypolr import UrlShorter

    # Replace with your values
    server_url = 'polr.example.com'
    api_key = '1234567890abcdef'

    # Example url to shorten
    long_url = 'https://some.long.example.com/long/url'

    # Create UrlShorter instance
    url_shorter = UrlShorter(server_url, api_key)

    # Use
    shorted_url = url_shorter.get_shorturl(long_url)
    custom_url = url_shorter.get_shorturl(long_url, custom='myurl')
    secret_url = url_shorter.get_shorturl(long_url, is_secret=True)


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

