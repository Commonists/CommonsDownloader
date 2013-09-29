#!/usr/bin/python
# -*- coding: latin-1 -*-

"""Setup script"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities'
]
py_modules = ['commonsdownloader']
scripts = ['download_from_Wikimedia_Commons.py']
requires = ['argparse']

setup(
      name='CommonsDownloader',
      version=0.1,
      author='Jean-Frédéric',
      author_email='JeanFred@github',
      url='http://github.com.org/JeanFred/CommonsDownloader',
      description='Download thumbnails from Wikimedia Commons',
      long_description=open('README.md').read(),
      license='MIT',
      py_modules=py_modules,
      scripts=scripts,
      install_requires=requires,
      classifiers=classifiers
)
