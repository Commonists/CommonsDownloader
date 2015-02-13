CommonsDownloader
=================
[![Build Status](https://travis-ci.org/Commonists/CommonsDownloader.svg?branch=master)](https://travis-ci.org/Commonists/CommonsDownloader)
[![Coverage Status](https://coveralls.io/repos/Commonists/CommonsDownloader/badge.svg?branch=master)](https://coveralls.io/r/Commonists/CommonsDownloader?branch=master)
[![Code Health](https://landscape.io/github/Commonists/CommonsDownloader/master/landscape.svg?style=flat)](https://landscape.io/github/Commonists/CommonsDownloader/master)
[![Documentation Status](https://readthedocs.org/projects/commonsdownloader/badge/?version=latest)](https://readthedocs.org/projects/commonsdownloader/?badge=latest)
[![Pypi](https://img.shields.io/pypi/v/CommonsDownloader.svg?style=flat)](https://pypi.python.org/pypi/CommonsDownloader)
[![License](https://img.shields.io/pypi/l/CommonsDownloader.svg?style=flat)](http://opensource.org/licenses/MIT)

Tool to download thumbnails of files from Wikimedia Commons 


Usage
-----

This tool can be used either by passing the filenames, a category or by using a file list.


### Using filenames ###

Just list the files we want to download.

    download_from_Wikimedia_Commons Example.jpg Example_ka.png


### Using a category ###

Just list the files we want to download.

    download_from_Wikimedia_Commons --category Example_images


### Using a file list ###

The file list must be formated as following, with one file per line, and `filename,width`:

    Example.jpg,100
    Example ka.png,80

Then use the `--list` argument:

    download_from_Wikimedia_Commons --list list.txt


### Setting the output folder ###

By default, the tool downloads the files in the current directory.

This can be changed using the `--output` flag with a valid path.

    download_from_Wikimedia_Commons Example.jpg --output some/path/


### Setting the default width

You can set the width of the thumbnail by using the `--width` argument:

    download_from_Wikimedia_Commons Example.jpg --width 50


### Verbosity ###

By default, the tool display basic information its logs (through `logging`).

You can adjust the verbosity level with the `-v` and `-q` flags:
use `-v` to display DEBUG-level messages, `-q` to silence INFO-level messages.


Installation
------------

Easiest way to install is to use `pip` from the Python Package Index:

    pip install CommonsDownloader

Alternatively, you can clone the repository and install it using `setuptools`:

    python setup.py install

This will install the executable script `download_from_Wikimedia_Commons`
