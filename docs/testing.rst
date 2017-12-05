*********
Testing
*********
.. _pytest: https://docs.pytest.org
.. _tox: https://tox.readthedocs.io
.. _tox_pytest: https://tox.readthedocs.io/en/latest/example/pytest.html
.. _tox_conda: https://fizzylogic.nl/2017/11/01/how-to-setup-tox-on-windows-with-anaconda/
.. _symlink: https://www.howtogeek.com/howto/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/

This project is set up to use pytest_ and tox_, and all tests are in the */tests*-folder.

.. note:: pytest is NOT compatible with Python 3.3.

.. warning:: Using Anaconda and tox on Windows is likely to result in a "Error: InterpreterNotFound" message and fail.
             If that is the case, see the `section below <fix_conda_tox_>`_ on how to make it work.


Test in one environment
=======================

To run tests for the current Python environment, simply invoke pytest_ in project root,
or pass ``test`` as an option argument to ``setup.py``.

Examples:

.. code-block:: none

    C:\dev\mypolr> pytest

.. code-block:: none

    C:\dev\mypolr> python setup.py test


Multiple versions
=================

Tests can be run for multiple python versions in separate *virtualenv*\ s using tox_.
It's setup is defined in the *tox.ini*, and will run tests in separate environments for:

- Python 2.7
- Python 3.4
- Python 3.5
- Python 3.6

These need to be created first using ``virtualenv`` or ``conda``. (Keep reading.)

All versions
------------

To run tests in all the Python environments, simply invoke tox_ in project root
(after the Python environments are created).

Example:

.. code-block:: none

    C:\dev\mypolr> tox

Specific versions
-----------------

To run on only a subset (or a single one) of the configured environments, you can use the ``-e ENV[,ENV,...]`` option.

E.g., to only run tests in environments with Python version 2.7 and 3.6:

.. code-block:: none

    C:\dev\mypolr>tox -e py27,py36

Read more about how to `integrate tox and pytest <tox_pytest_>`_.

.. _fix_conda_tox:

Working with Windows, conda, tox
================================

.. note::

    Using ``tox`` and ``conda`` (miniconda or Anaconda) is at first glance **not a good match**,
    or at least on Windows.
    Tox expects to work from a *virtualenv* and not a *conda environment*.
    However, it's possible with a few, simple steps:

    Read the tips below
    if you're using conda to manage Python environments **and**
    have problems with ``InterpreterNotFound``\ -errors when attempting to run tox.

To use tox and conda on Windows, the following recommendations apply:

#. For `tox to find your environments <tox_conda_>`_, consider to **either**:

   - Install environments in ``C:\PythonXY``, where X and Y is major and minor version, respectively; **or**
   - Make a symlink_ from ``C:\PythonXY`` to your real path.
     E.g.: ``mklink /J C:\Python27 C:\Anaconda3\envs\myPy27env``

#. In the environment where you call tox:
   install ``virtualenv`` with conda and *not with pip*.
   This seems to work well with Anaconda.

Tips 1:
    Use the ``--prefix, -p``-option to define the location of new environments:

    - Use ``conda install -p C:\PythonXY python=X.Y`` to create an environment called ``PythonXY``
      in the location ``C:\PythonXY``. (No symlink creation is needed.)

    - Use ``conda install -p C:\path\to\myenv python=X.Y`` to create an environment called ``myenv``
      in the location ``C:\path\to\myenv``. (Symlinks should be made.)

Tips 2:
    Add the ``--yes`` option to prevent conda from asking confirmation upon creating environments.

Tips 3:
    If your Anaconda installation is on a different drive than C, e.g. *E:\\Anaconda3\\*,
    then environments will be installed in the *E:\\Anaconda3\\envs\\*-directory if your
    current working drive is E.
    This allows you to create envs in the same drive as the rest of Anaconda without the need to use
    the ``--prefix`` option.

