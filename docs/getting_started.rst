Installing
==========

The easiest install method is to use Python's pip tool.  First, let's make sure
that it's installed (PythonXY and Enthought's Python Distribution do not come
with this tool by default)::

    c:\\> easy_install pip

Once it's installed, install a copy of Mercurial (Hg) if you haven't already.
The source code for TDTPy is managed via the Mercurial distributed version
control system and pip requires the Hg binary to checkout a copy of TDTPy::

    c:\\> pip install mercurial

.. note::

    Installing Mercurial from source requires a working compiler.  If the above
    command fails with the error message, "unable to find vcvarsall.bat", you
    need to install a compiler.  On Windows, you can install Microsoft Visual
    Studio 2008 Express (the `version of Visual Studio`_ is important).
    Alternatively, it may be much easier to just install the TortoiseHg_
    binaries

.. _TortoiseHg: http://tortoisehg.bitbucket.org/
.. _version of Visual Studio: http://slacy.com/blog/2010/09/python-unable-to-find-vcvarsall-bat

Now, install TDTPy::

    c:\\> pip install hg+http://bitbucket.org/bburan/tdtpy#egg=tdt

To install a local copy of TDTPy that you can edit::

    c:\\> pip install -e hg+http://bitbucket.org/bburan/tdtpy#egg=tdt

Or, using the more verbose syntax::

    c:\\> hg clone http://bitbucket.org/bburan/tdtpy tdtpy
    c:\\> cd tdtpy
    c:\\> python setup.py install

