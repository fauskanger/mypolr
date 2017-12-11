*********
Testing
*********
.. _pytest: https://docs.pytest.org
.. _tox: https://tox.readthedocs.io
.. _tox_pytest: https://tox.readthedocs.io/en/latest/example/pytest.html
.. _tox_conda: https://fizzylogic.nl/2017/11/01/how-to-setup-tox-on-windows-with-anaconda/
.. _symlink: https://www.howtogeek.com/howto/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/

Pytest and tox
==============

This project is set up to use pytest_ and tox_, and all tests are in the */tests*-folder.

.. note:: pytest is NOT compatible with Python 3.3.

.. warning:: Using Anaconda and tox on Windows is likely to result in a "Error: InterpreterNotFound" message and fail.
             If that is the case, see :ref:`fix_conda_tox` on how to make it work.


Test in one environment
-----------------------

To run tests for the current Python environment, simply invoke pytest_ in project root,
or pass ``test`` as an option argument to ``setup.py``.

Examples:

.. code-block:: none

    C:\dev\mypolr> pytest

.. code-block:: none

    C:\dev\mypolr> python setup.py test


Multiple versions
-----------------

Tests can be run for multiple python versions in separate *virtualenv*\ s using tox_.
Its setup is defined in the *tox.ini*, and will run tests in separate environments for:

- Python 2.7
- Python 3.4
- Python 3.5
- Python 3.6

These need to be created first using ``virtualenv`` or ``conda``. (Keep reading.)

All versions
''''''''''''

To run tests in all the Python environments, simply invoke tox_ in project root
(after the Python environments are created).

Example:

.. code-block:: none

    C:\dev\mypolr> tox

Specific versions
'''''''''''''''''

To run on only a subset (or a single one) of the configured environments, you can use the ``-e ENV[,ENV,...]`` option.

E.g., to only run tests in environments with Python version 2.7 and 3.6:

.. code-block:: none

    C:\dev\mypolr>tox -e py27,py36

Read more about how to `integrate tox and pytest <tox_pytest_>`_.

.. _fix_conda_tox:

Working with Windows, conda, tox
--------------------------------

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

Fast and easy fix
'''''''''''''''''

The *tests/tox_with_conda.py*-file is a utility for making the steps above with a single call.

The ``ToxEnvMatcher``-class can be used from Python to create environments and set up the needed symlinks,
but it's also possible to use the file from command line.

Examples of use in Python:

.. code-block:: python

    my_envs = join('E:\\', 'Anaconda3', 'envs')
    tem = ToxEnvMatcher(my_envs)
    for version in '27,34,35,36'.split(','):
        tem.make(version)

Examples of use from cmd.exe:

.. code-block:: none

    E:\dev\mypolr\tests> tox_with_conda.py E:\Anaconda3\envs 27 34 35 36

Environment prefix (defaults to *py*) can be overridden with -p/--env_prefix options:

.. code-block:: python

    E:\dev\mypolr\tests> python tox_with_conda.py E:\Anaconda3\envs 27 34 35 36 -p Python


This will create new environments in ``E:\Anaconda3\envs\PythonXY`` instead of ``E:\Anaconda3\envs\pyXY``

If, for some reason you need to, it's possible to use
the ``-b``/``--base`` option to override the default base location (``C:\Python``):

.. code-block:: none

    E:\dev\mypolr\tests> tox_with_conda.py E:\Anaconda3\envs 27 34 35 36 --base D:\Python

.. note:: The *tox_with_conda.py*-file has been uploaded to a repository of its own on
          https://github.com/fauskanger/tox_with_conda and can also be installed with pip:

          .. code-block:: none

              pip install tox_with_conda

If installed with pip, then instead of

.. code-block:: none

   python tox_with_conda.py ...

use

.. code-block:: none

   python -m tox_with_conda ...

Travis CI
=========

Current build and test status:
   .. image:: https://api.travis-ci.org/fauskanger/mypolr.svg?branch=master
      :align: center
      :alt: Travis CI build and test status
      :target: https://travis-ci.org/fauskanger/mypolr

.. _travis_python: https://docs.travis-ci.com/user/languages/python/
.. _travis_mypolr: https://travis-ci.org/fauskanger/mypolr

The *.travis.yml*-file defines the `Travis CI setup <travis_python_>`_ for this project.
When new code has been pushed to the git repository, Travis CI will automatically pull the updates.
Then it will build and run tests for multiple versions of Python.
The process can be `monitored here <travis_mypolr_>`_.

.. warning:: Travis continuous integration is not a replacement for running tests locally before committing changes
             or making pull requests.