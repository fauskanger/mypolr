from pkg_resources import get_distribution, DistributionNotFound

from mypolr import exceptions
from mypolr.polr_api import PolrApi, DEFAULT_API_ROOT

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
