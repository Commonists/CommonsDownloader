#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Unit tests."""

from os.path import dirname, join
from StringIO import StringIO
import unittest
from commonsdownloader import commonsdownloader


class TestCommonsDownloaderExecutable(unittest.TestCase):

    """Testing methods from commonsdownloader executable."""

    def setUp(self):
        """Set up the TestCase with the data files."""
        self.example_file = join(dirname(__file__), 'data', 'example_file.txt')

    def test_get_files_from_textfile(self):
        """Test get_files_from_textfile."""
        with open(self.example_file, 'r') as f:
            output = list(commonsdownloader.get_files_from_textfile(f))
        expected_value = [('Example.jpg', 100),
                          ('Example rotated 90 left.jpg', None)]
        self.assertEqual(output, expected_value)

    def test_get_files_from_arguments(self):
        """Test get_files_from_arguments."""
        files_input = ['A', 'B', 'C']
        output = list(commonsdownloader.get_files_from_arguments(files_input, 100))
        expected_value = [('A', 100), ('B', 100), ('C', 100)]
        self.assertEqual(output, expected_value)

    def test_get_local_cache_path(self):
        """Test get_local_cache_path."""
        output = commonsdownloader.get_local_cache_path('output')
        expected_value = 'output/.cache'
        self.assertEqual(output, expected_value)

    def test_write_file_to_cache(self):
        fh = StringIO()
        commonsdownloader.write_file_to_cache('Example.jpg', 100, fh)
        output = fh.getvalue()
        expected_value = 'Example.jpg,100\n'
        self.assertEqual(output, expected_value)

if __name__ == "__main__":
    unittest.main()
