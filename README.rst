********
Overview
********

This package, `mypolr`, is a simple python package for creating short links using the
`Polr Project <https://polrproject.org>`_'s REST
`API <https://docs.polrproject.org/en/latest/developer-guide/api/>`_.

Documentation and User Guide:
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

