from distutils.core import setup

setup(
    name='TDTPy',
    version='0.7',
    author='Brad Buran',
    author_email='bburan@alum.mit.edu',
    packages=['tdt', 'tdt.actxobjects', 'tdt.debuggers', 'tdt.device'],
    url='http://bradburan.com/programs/tdtpy',
    license='LICENSE.txt',
    description='Module for communicating with TDT\'s System 3 hardware',
    requires=['win32com'],
    package_data={'tdt': ['components/*.rcx']}
)
