#!/usr/bin/python
# -=- encoding: latin-1 -=-

"""Download files from Wikimedia Commons"""

import os
import logging
import argparse
from commonsdownloader import download_file


def get_file_names_from_textfile(textfile_handler):
    """Yield the file names and widths by parsing a given text fileahandler."""
    for line in textfile_handler:
        line = line.rstrip()
        try:
            (image_name, width) = line.split(',')
        except ValueError:
            image_name = line
            width = None
        yield (image_name, width)


class Folder(argparse.Action):

    """An argparse action for directories."""

    def __call__(self, parser, namespace, values, option_string=None):
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
    parser.add_argument("files",
                        nargs='*',
                        metavar="FILES",
                        help='A list of filenames')
    parser.add_argument("-l", "--list", metavar="LIST",
                        dest="file_list",
                        type=argparse.FileType('r'),
                        help='A list of files <filename,width>')
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
    parser.add_argument("-v",
                        action="count",
                        dest="verbose",
                        default=0,
                        help="Verbosity level. -v for INFO, -vv for DEBUG")
    args = parser.parse_args()
    logging_map = {0: logging.WARNING,
                   1: logging.INFO,
                   2: logging.DEBUG}
    logging.basicConfig(level=logging_map[args.verbose])
    logging.info("Starting")

    if args.file_list:
        for (file_name, width) in get_file_names_from_textfile(args.file_list):
            download_file(file_name, args.output_path, width=width)
    elif args.files:
        for file_name in args.files:
            download_file(file_name, args.output_path, width=args.width)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
