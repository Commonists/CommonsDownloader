CommonsDownloader
=================
[![Build Status](https://secure.travis-ci.org/Commonists/CommonsDownloader.png)](http://travis-ci.org/Commonists/CommonsDownloader)

Tool to download thumbnails of files from Wikimedia Commons 


Usage
-----

This tool can be used either by passing the filenames or by using a file list.

### Using filenames ###

Just list the files we want to download.

    download_from_Wikimedia_Commons.py Example.jpg Example_ka.png

You can set the width of the thumbnail by using the `--width` argument:

    download_from_Wikimedia_Commons.py --width 50 Example.jpg Example_ka.png

### Using a file list ###

The file list must be formated as following, with one file per line, and `filename,width`:

    Example.jpg,100
    Example ka.png,80

Then use the `--list` argument:

    download_from_Wikimedia_Commons.py --list list.txt

### Setting the output folder ###

By default, the tool downloads the files in the current directory.

This can be changed using the `--output` flag with a valid path.

    download_from_Wikimedia_Commons.py Example.jpg --output some/path/


### Verbosity ###

By default, the tool does not display anything it logs (through `logging`).

You can increase the verbosity level with the `-v` flag:
use `-v` to display INFO-level messages, `-vv` for DEBUG-level messages.

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
