from importlib.metadata import version, PackageNotFoundError
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .dsp_project import DSPProject
from .dsp_process import DSPProcess
from .dsp_circuit import DSPCircuit
from .dsp_buffer import DSPBuffer
from .dsp_error import DSPError

try:
    __version__ = version("mne_bids_pipeline")
except PackageNotFoundError:
    # package is not installed
    pass
