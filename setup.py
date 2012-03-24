from distutils.core import setup
from os import path

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    #'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Topic :: Scientific/Engineering',
    'Topic :: System :: Hardware',
    'License :: OSI Approved :: GNU General Public License (GPL)'
]

here = path.dirname(path.abspath(__file__))
with open(path.join(here, 'readme.rst')) as f:
    long_description = f.read().strip()

long_description += '''

Source code: http://bitbucket.org/bburan/tdtpy

Documentation: http://tdtpy.readthedocs.org

'''

setup(
    name='TDTPy',
    version='0.7',
    author='Brad Buran',
    author_email='bburan@alum.mit.edu',
    packages=['tdt', 'tdt.actxobjects', 'tdt.debuggers', 'tdt.device'],
    url='http://bradburan.com/programs/tdtpy',
    license='GPLv3',
    description='Module for communicating with TDT\'s System 3 hardware',
    long_description=long_description,
    requires=['win32com'],
    package_data={'tdt': ['components/*.rcx']},
    classifiers=CLASSIFIERS,
)
