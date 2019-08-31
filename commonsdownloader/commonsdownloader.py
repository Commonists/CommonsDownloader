#!/usr/bin/python
# -=- encoding: latin-1 -=-

"""Download files from Wikimedia Commons."""

import os
import logging
import argparse
from commonsdownloader.thumbnaildownload import download_file, DownloadException

from itertools import zip_longest


def get_category_files_from_api(category_name):
    """Yield the file names of a category by querying the MediaWiki API."""
    import mwclient
    site = mwclient.Site('commons.wikimedia.org')
    category = site.Categories[category_name]
    return (x.page_title for x in category.members(namespace=6))


def download_from_category(category_name, output_path, width):
    """Download files of a given category."""
    file_names = get_category_files_from_api(category_name)
    files_to_download = zip_longest(file_names, [], fillvalue=width)
    download_files_if_not_in_manifest(files_to_download, output_path)


def get_files_from_textfile(textfile_handler):
    """Yield the file names and widths by parsing a text file handler."""
    for line in textfile_handler:
        line = line.rstrip()
        try:
            (image_name, width) = line.rsplit(',', 1)
            width = int(width)
        except ValueError:
            image_name = line
            width = None
        yield (image_name, width)


def download_from_file_list(file_list, output_path):
    """Download files from a given textfile list."""
    files_to_download = get_files_from_textfile(file_list)
    download_files_if_not_in_manifest(files_to_download, output_path)


def get_files_from_arguments(files, width):
    """Yield the file names and chosen width."""
    return zip_longest(files, [], fillvalue=width)


def download_from_files(files, output_path, width):
    """Download files from a given file list."""
    files_to_download = get_files_from_arguments(files, width)
    download_files_if_not_in_manifest(files_to_download, output_path)


def get_local_manifest_path(output_path):
    """Return the path to the local downloading manifest."""
    return os.path.join(output_path, '.manifest')


def read_local_manifest(output_path):
    """Return the contents of the local manifest, as a dictionary."""
    local_manifest_path = get_local_manifest_path(output_path)
    try:
        with open(local_manifest_path, 'r') as f:
            manifest = dict(get_files_from_textfile(f))
            logging.debug('Retrieving %s elements from manifest', len(manifest))
            return manifest
    except IOError:
        logging.debug('No local manifest at %s', local_manifest_path)
        return {}


def is_file_in_manifest(file_name, width, manifest):
    """Whether the given file, in its given width, is in manifest."""
    return (manifest.get(file_name, '-1') == width)


def write_file_to_manifest(file_name, width, manifest_fh):
    """Write the given file in manifest."""
    manifest_fh.write("%s,%s\n" % (file_name, str(width)))
    logging.debug("Wrote file %s to manifest", file_name)


def download_files_if_not_in_manifest(files_iterator, output_path):
    """Download the given files to the given path, unless in manifest."""
    local_manifest = read_local_manifest(output_path)
    with open(get_local_manifest_path(output_path), 'a') as manifest_fh:
        for (file_name, width) in files_iterator:
            if is_file_in_manifest(file_name, width, local_manifest):
                logging.info('Skipping file %s', file_name)
                continue
            try:
                download_file(file_name, output_path, width=width)
                write_file_to_manifest(file_name, width, manifest_fh)
            except DownloadException as e:
                logging.error("Could not download %s: %s", file_name, e.message)


class Folder(argparse.Action):

    """An argparse action for directories."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Overriding call action."""
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            msg = "Folder:{0} is not a valid path".format(prospective_dir)
            raise argparse.ArgumentTypeError(msg)
        else:
            setattr(namespace, self.dest, prospective_dir)


def main():
    """Main method, entry point of the script."""
    from argparse import ArgumentParser
    description = "Download a bunch of thumbnails from Wikimedia Commons"
    parser = ArgumentParser(description=description)
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument("-l", "--list", metavar="LIST",
                              dest="file_list",
                              type=argparse.FileType('r'),
                              help='A list of files <filename,width>')
    source_group.add_argument("-c", "--category", metavar="CATEGORY",
                              dest="category_name",
                              type=str,
                              help='A category name (without prefix)')
    parser.add_argument("files", nargs='*',
                        metavar="FILES",
                        help='A list of filenames')
    parser.add_argument("-o", "--output", metavar="FOLDER",
                        dest="output_path",
                        action=Folder,
                        default=os.getcwd(),
                        help='The directory to download the files to')
    parser.add_argument("-w", "--width",
                        dest="width",
                        type=int,
                        default=100,
                        help='The width of the thumbnail (default: 100)')
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-v",
                                 action="count",
                                 dest="verbose",
                                 default=1,
                                 help="Verbosity level. -v for DEBUG")
    verbosity_group.add_argument("-q", "--quiet",
                                 action="store_const",
                                 dest="verbose",
                                 const=0,
                                 help="To silence the INFO messages")
    args = parser.parse_args()
    logging_map = {0: logging.WARNING,
                   1: logging.INFO,
                   2: logging.DEBUG}
    logging_level = logging_map.get(args.verbose, logging.DEBUG)
    logging.basicConfig(level=logging_level)
    logging.info("Starting")

    if args.file_list:
        download_from_file_list(args.file_list, args.output_path)
    elif args.category_name:
        download_from_category(args.category_name, args.output_path, args.width)
    elif args.files:
        download_from_files(args.files, args.output_path, args.width)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
