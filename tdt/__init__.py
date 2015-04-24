import logging

# Although Python 2.7+ has a logging.NullHandler class available, we should at
# least maintain backwards-compatibility with Python 2.6 so that
# ReadTheDocs.org can generate our autodocumentation.


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

from .dsp_project import DSPProject
from .dsp_process import DSPProcess
from .dsp_circuit import DSPCircuit
from .dsp_buffer import DSPBuffer
from .dsp_error import DSPError
