from os import path
from setuptools import setup

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

# get the version (don't import tdt here, so dependencies are not needed)
version = None
with open(path.join('tdt', '__init__.py'), 'r') as fid:
    for line in (line.strip() for line in fid):
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'')
            break
if version is None:
    raise RuntimeError('Could not determine version')


setup(
    name=name,
    version=version,
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
    extras_require={
        'test': ['pytest'],
    },
    package_data={'tdt': ['components/*.rcx']},
    classifiers=CLASSIFIERS,
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'docs'),
        },
    }
)
