from os import path
from setuptools import setup
import versioneer

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

name = 'TDTPy'
version =versioneer.get_version()

setup(
    name=name,
    author='The TDTPy development team',
    author_email='bburan@alum.mit.edu',
    packages=['tdt',
              'tdt.actxobjects',
              'tdt.components',
              'tdt.device'],
    url='http://tdtpy.readthedocs.org',
    license='BSD (3-clause)',
    description='Module for communicating with TDT\'s System 3 hardware',
    long_description=long_description,
    install_requires=['pypiwin32', 'numpy'],
    package_data={'tdt': ['components/*.rcx']},
    classifiers=CLASSIFIERS,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'docs'),
        },
    },
    version=version,
    cmdclass=versioneer.get_cmdclass(),
)
