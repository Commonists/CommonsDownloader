CommonsDownloader
=================

Tool to download thumbnails of files from Wikimedia Commons 


Usage
-----

This tool can be used either by passing the filenames or by using a file list,
which also allows to choose the thumbnail width.

### Using filenames ###

    download_from_Wikimedia_Commons.py Example.jpg Example_ka.png


### Using a file list ###

The file list must be formated as following, with one file per line, and <filename,width>:

    Example.jpg,100
    Example ka.png,80

The use the `--list` argument:

    download_from_Wikimedia_Commons.py --list list.txt


Installation
------------

Easiest way to install is to use `pip`:

    pip install git+git://github.com/JeanFred/CommonsDownloader.git#egg=CommonsDownloader

Alternatively, you can clone the repository and install it using `setuptools`:

    python setup.py install

This will install the executable script `download_from_Wikimedia_Commons.py`


License
-------
MIT license
