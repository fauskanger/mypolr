********
Overview
********

.. after-travis-ci-image
.. before-introduction-links

.. _docs: https://mypolr.readthedocs.io
.. _travis_ci: https://travis-ci.org/fauskanger/mypolr
.. _pypi_new: https://pypi.org/project/mypolr/
.. _pypi_legacy: https://pypi.python.org/pypi/mypolr
.. _pypi: pypi_new_
.. _conda: https://anaconda.org/fauskanger/mypolr

This package, `mypolr`, is a python package to easily create and manage short links using the
`Polr Project <https://polrproject.org>`_'s REST
`API <https://docs.polrproject.org/en/latest/developer-guide/api/>`_ that also has CLI support.

User Guide and documentation:
    https://mypolr.readthedocs.io

GitHub:
    https://github.com/fauskanger/mypolr

Clone source:
    ``git clone git://github.com/fauskanger/mypolr.git``

PyPI:
    ``pip install mypolr`` [ `PyPI.org <pypi_new_>`_ | `Legacy <pypi_legacy_>`_ ]

.. after-introduction-links

-----

+--------------+------------------------------------------------------------------------------------------------------+
|  Project     | .. image:: https://img.shields.io/pypi/pyversions/mypolr.svg                                         |
|              |    :align: left                                                                                      |
|              |    :alt: Python versions supported                                                                   |
|              |    :target: pypi_                                                                                |
|              |                                                                                                      |
|              | .. image:: https://img.shields.io/github/license/fauskanger/mypolr.svg                               |
|              |    :align: left                                                                                      |
|              |    :alt: LICENCE                                                                                     |
|              |    :target: https://github.com/fauskanger/mypolr/blob/master/LICENSE                                 |
|              +------------------------------------------------------------------------------------------------------+
|              | .. image:: https://img.shields.io/github/tag/fauskanger/mypolr.svg                                   |
|              |    :align: left                                                                                      |
|              |    :alt: Latest git tag                                                                              |
|              |    :target: https://github.com/fauskanger/mypolr/tags                                                |
|              |                                                                                                      |
|              | .. image:: https://img.shields.io/pypi/v/mypolr.svg                                                  |
|              |    :align: left                                                                                      |
|              |    :alt: PyPI version                                                                                |
|              |    :target: pypi_                                                                                |
|              |                                                                                                      |
|              | .. image:: https://img.shields.io/conda/v/fauskanger/mypolr.svg                                      |
|              |    :align: left                                                                                      |
|              |    :alt: conda version                                                                               |
|              |    :target: conda_                                                                                   |
+--------------+------------------------------------------------------------------------------------------------------+
| Git          | .. image:: https://img.shields.io/github/last-commit/fauskanger/mypolr.svg                           |
|              |    :align: left                                                                                      |
|              |    :alt: Last commit                                                                                 |
|              |    :target: https://github.com/fauskanger/mypolr/commits                                             |
|              |                                                                                                      |
|              | .. image:: https://img.shields.io/github/issues/fauskanger/mypolr.svg                                |
|              |    :align: left                                                                                      |
|              |    :alt: Open issues                                                                                 |
|              |    :target: https://github.com/fauskanger/mypolr/issues                                              |
|              |                                                                                                      |
|              | .. image:: https://img.shields.io/github/issues-closed/fauskanger/mypolr.svg                         |
|              |    :align: left                                                                                      |
|              |    :alt: Close issues                                                                                |
|              |    :target: https://github.com/fauskanger/mypolr/issues                                              |
|              +------------------------------------------------------------------------------------------------------+
|              | .. image:: https://img.shields.io/github/languages/code-size/fauskanger/mypolr.svg                   |
|              |    :align: left                                                                                      |
|              |    :alt: Repo size                                                                                   |
|              |    :target: https://github.com/fauskanger/mypolr                                                     |
|              |                                                                                                      |
|              | .. image:: https://img.shields.io/github/repo-size/fauskanger/mypolr.svg                             |
|              |    :align: left                                                                                      |
|              |    :alt: Repo size                                                                                   |
|              |    :target: https://github.com/fauskanger/mypolr                                                     |
+--------------+------------------------------------------------------------------------------------------------------+
| Statuses     | .. image:: https://img.shields.io/pypi/status/mypolr.svg                                             |
|              |    :align: left                                                                                      |
|              |    :alt: Status                                                                                      |
|              |    :target: pypi_                                                                                |
|              |                                                                                                      |
|              | .. image:: https://readthedocs.org/projects/mypolr/badge/?version=latest                             |
|              |    :align: left                                                                                      |
|              |    :alt: ReadTheDocs.io build status                                                                 |
|              |    :target: https://mypolr.readthedocs.io/en/latest                                                  |
|              |                                                                                                      |
|              | .. image:: https://api.travis-ci.org/fauskanger/mypolr.svg?branch=master                             |
|              |    :align: left                                                                                      |
|              |    :alt: Travis CI build and test status                                                             |
|              |    :target: https://travis-ci.org/fauskanger/mypolr                                                  |
|              |                                                                                                      |
|              | .. image:: https://img.shields.io/pypi/wheel/mypolr.svg                                              |
|              |    :align: left                                                                                      |
|              |    :alt: Wheel support                                                                               |
|              |    :target: pypi_                                                                                |
+--------------+------------------------------------------------------------------------------------------------------+


Requirements
============

Polr Project
------------

Documentation:
    https://polrproject.org

To use `mypolr`, you need a valid API key to a server with the Polr Project installed.

You can obtain the API key by logging in to your Polr site and navigate to `<polr project root>/admin#developer`.

.. before-polr-affiliation-disclaimer

.. note:: **Disclaimer:** This package, `mypolr`, is not affiliated with the Polr Project.

.. after-polr-affiliation-disclaimer

Python
------

There is only one requirement:

- ``requests``, an awesome HTTP library. (`Documentation <http://python-requests.org>`_).

When installing with `pip` or `conda` this will be installed automatically (if not already installed).

Tested on Python 2.7, 3.4+, but should also work with version 3.3.


Installation
============

With `pip`:
    ``pip install mypolr``

With `conda`:
    ``conda install -c fauskanger mypolr``

ToBeDone
========
- Add ``:raises:`` docstring fields to methods/docs.
- Implement the ``/data/link``-endpoint if necessary.


License
=======
This project is licensed under the `MIT Licence <https://github.com/fauskanger/mypolr/blob/master/LICENSE>`_.
(See link for details.)

.. personal_epilogue:

Epilogue
========
This project has served several purposes:

#. Have a tool to easily utilize the Polr Project API from Python.
#. Be an exercise in packaging and distributing Python modules (with `pip` and `conda`).
#. Be an exercise in reStructuredText, Sphinx documentation, and ReadTheDocs.
#. Be an exercise in testing Python along best practices and conventions.
