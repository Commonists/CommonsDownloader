#!/usr/bin/python
# -*- coding: latin-1 -*-

"""Setup script."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import commonsdownloader
    version = commonsdownloader.__version__
except ImportError:
    version = 'Undefined'


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities'
]
packages = ['commonsdownloader']
requires = ['argparse', 'mwclient', 'six']
entry_points = {
        'console_scripts': [
            'download_from_Wikimedia_Commons = commonsdownloader.commonsdownloader:main',
            ]
        }

setup(
      name='CommonsDownloader',
      version=version,
      author='Jean-Frédéric',
      author_email='JeanFred@github',
      url='http://github.com/Commonists/CommonsDownloader',
      description='Download thumbnails from Wikimedia Commons',
      long_description=open('README.md').read(),
      license='MIT',
      packages=packages,
      entry_points=entry_points,
      install_requires=requires,
      classifiers=classifiers
)
