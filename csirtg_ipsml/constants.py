from ._version import get_versions
__version__ = get_versions()['version']
VERSION = __version__
del get_versions
import sys

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

PYVERSION = 2
if sys.version_info > (3,):
    PYVERSION = 3