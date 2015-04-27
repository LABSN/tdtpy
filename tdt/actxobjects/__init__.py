from .RPcoX import RPcoX
from .ZBUSx import ZBUSx
from .PA5x import PA5x

'''
The files in this directory were generated using makepy.  If TDT ever updates
their drivers with new methods and signatures, the files may need to be
regenerated.  To replicate the process, open up a command window and type:

>>> python -m win32com.client.makepy

A popup window with all the COM libraries available will appear.  Select the
library you want (i.e. TDevAccX) and click OK.  You'll get the following
message:

>>> python -m win32com.client.makepy
Generating to c:\Python26\lib\site-packages\win32com\gen_py\831D8AF7-7E2B-426B-A430-18E670F56C12x0x10x9.py
Building definitions from type library...
Generating...
Importing module

Pay attention to the "Generating to" path.  Find the file described and copy it
to this folder (and rename it to something more appropriate).

.. note::

    The RPcoX.py file has been modified by hand to optimize certain method calls
    (ReadTagV and ReadTagVEX).  See `Brad Buran's post` for more detail.  

.. _`Brad Buran's post`:  http://bradburan.com/2011/03/speeding-up-readtagv-and-readtagvex/
'''
