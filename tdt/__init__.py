import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .dsp_project import DSPProject
from .dsp_process import DSPProcess
from .dsp_circuit import DSPCircuit
from .dsp_buffer import DSPBuffer
from .dsp_error import DSPError

try:
    from importlib.metadata import version
    __version__ = version("TDTPy")
except Exception:
    # Catch a generic exception which will handle both PackageNotFoundError and
    # ImportError (attempting to catch PackageNotFoundError is a bit tricky if
    # importlib.metadata is not available).
    try:
        from .version import __version__
    except ImportError:
        # package is not installed. probably some munging of Python path going
        # on here.
        __version__ = '0.0.0'
