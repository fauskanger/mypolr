"""
This package, `mypolr <https://github.com/fauskanger/mypolr>`_, is a python package to
easily create and manage short links using the
`Polr Project <https://docs.polrproject.org>`_'s REST
`API <https://docs.polrproject.org/en/latest/developer-guide/api/>`_. Mypolr also has CLI support.

Main components are:

- :class:`PolrApi` class in `mypolr/polr_api.py`
- :class:`MypolrError`-based exceptions in `mypolr/exceptions.py`
- :class:`MypolrCli` class in `mypolr/__main__.py` for practical CLI usage

Tests are located in `mypolr/tests/`.

Licensed under
`MIT License <https://github.com/fauskanger/mypolr/blob/master/LICENSE>`_.
See also the `LICENSE`-file in root folder.

"""
import sys
from pkg_resources import get_distribution, DistributionNotFound

from mypolr import exceptions
from mypolr.polr_api import PolrApi, DEFAULT_API_ROOT

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

# Determines whether CLI-tests should run, and if CLI-usage is allowed
is_cli_supported = sys.version_info.major == 3 and sys.version_info.minor >= 3
