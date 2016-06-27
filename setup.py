from distutils.core import setup
from os import path
import numpy  # noqa; a requirement, but *don't* have pip try to install it
try:
    import setuptools  # noqa, setuptools namespace
except Exception:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: System :: Hardware',
    'License :: OSI Approved'
]

here = path.dirname(path.abspath(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read().strip()

long_description += '''

Source code: http://github.com/LABSN/tdtpy

Documentation: http://tdtpy.readthedocs.org

'''

setup(
    name='TDTPy',
    version='0.8.dev0',
    author='Brad Buran',
    author_email='bburan@alum.mit.edu',
    packages=['tdt',
              'tdt.actxobjects',
              'tdt.components',
              'tdt.device'],
    url='http://tdtpy.readthedocs.org',
    license='BSD (3-clause)',
    description='Module for communicating with TDT\'s System 3 hardware',
    long_description=long_description,
    install_requires=['six', 'pypiwin32'],
    package_data={'tdt': ['components/*.rcx']},
    classifiers=CLASSIFIERS,
)
