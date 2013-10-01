# -=- encoding: latin-1 -=-

"""Download files from Wikimedia Commons"""

import os
import urllib2
import logging


DEFAULT_WIDTH = 100


def clean_up_filename(file_name):
    """Return the cleaned-up file title."""
    return file_name.strip().replace(' ', '_')


def make_thumb_url(image_name, width):
    """Return the URL to the thumbnail of the file, at the given width."""
    base_url = "http://commons.wikimedia.org/w/thumb.php?f=%s&width=%s"
    return base_url % (image_name, width)


def make_thumbnail_name(image_name, extension):
    """Return name of the downloaded thumbnail, based on the extension."""
    file_name, _ = os.path.splitext(image_name)
    return file_name + '.' + extension


def get_thumbnail_of_file(image_name, width):
    """Return the file contents of the thumbnail of the given file."""
    hdr = {'User-Agent': 'Python urllib2'}
    url = make_thumb_url(image_name, width)
    req = urllib2.Request(url, headers=hdr)
    try:
        logging.debug("Retrieving %s" % url)
        opened = urllib2.urlopen(req)
        extension = opened.headers.subtype
        return opened.read(), make_thumbnail_name(image_name, extension)
    except urllib2.HTTPError, e:
        raise Exception(e.fp.read())


def download_file(image_name, output_path, width=DEFAULT_WIDTH):
    """Download a given Wikimedia Commons file."""
    image_name = clean_up_filename(image_name)
    logging.info("Downloading %s with width %s", image_name, width)
    contents, output_file_name = get_thumbnail_of_file(image_name, width)
    output_file_path = os.path.join(output_path, output_file_name)
    with open(output_file_path, 'wb') as f:
        logging.debug("Writing as %s" % output_file_path)
        f.write(contents)
    return output_file_path
