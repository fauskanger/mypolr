*********
Testing
*********
.. _pytest: https://docs.pytest.org
.. _tox: https://tox.readthedocs.io
.. _tox_pytest: https://tox.readthedocs.io/en/latest/example/pytest.html

This project is set up to use pytest_ and tox_, and all tests are in the */tests*-folder.

Current environment
===================

To run tests for the current Python environment, simply invoke pytest_ in project root.

Example:

.. code-block:: batch

    C:\dev\mypolr> pytest


Multiple versions
=================

Tests can be run for multiple python versions in separate *virtualenv*\ s using tox_.
It's setup is defined in the *tox.ini*, and will install separate environments for:

- Python 2.7
- Python 3.3
- Python 3.4
- Python 3.5
- Python 3.6

To run tests in all the Python environments, simply invoke tox_ in project root.

Example:

.. code-block:: batch

    C:\dev\mypolr> tox

Read more about how to `integrate tox and pytest <tox_pytest_>`_.
