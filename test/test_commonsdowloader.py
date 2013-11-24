#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Unit tests."""

from os.path import dirname, join, exists
import unittest
import tempfile
from commonsdownloader import thumbnaildownload


class TestCommonsDownloaderOffline(unittest.TestCase):

    """Testing methods from thumbnaildownload which do not require connection."""

    def test_clean_up_filename(self):
        """Test clean_up_filename."""
        values = [('Example.jpg', 'Example.jpg'),
                  ('Example.jpg ', 'Example.jpg'),
                  (' Example.jpg', 'Example.jpg'),
                  ('My Example.jpg', 'My_Example.jpg')]
        for (input_value, expected_value) in values:
            self.assertEqual(thumbnaildownload.clean_up_filename(input_value),
                             expected_value)

    def test_make_thumb_url(self):
        """Test make_thumb_url."""
        input_value = ('My_Example.jpg', 100)
        expected_value = "http://commons.wikimedia.org/w/thumb.php?f=My_Example.jpg&width=100"
        output = thumbnaildownload.make_thumb_url(*input_value)
        self.assertEqual(output, expected_value)

    def test_clean_extension(self):
        """Test clean_extension."""
        values = [('jpg', 'jpg'),
                  ('png', 'png'),
                  ('jpeg', 'jpg')]
        for (input_value, expected_value) in values:
            self.assertEqual(thumbnaildownload.clean_extension(input_value),
                             expected_value)

    def test_make_thumbnail_name(self):
        """Test make_thumbnail_name."""
        input_value = ('Example.svg', 'png')
        expected_value = "Example.png"
        output = thumbnaildownload.make_thumbnail_name(*input_value)
        self.assertEqual(output, expected_value)


class TestCommonsDownloaderOnline(unittest.TestCase):

    """Testing methods from thumbnaildownload which require connection"""

    def setUp(self):
        """Sett up the TestCase with the data files."""
        self.outputfile1 = join(dirname(__file__), 'data', 'Example-100.jpg')
        self.outputfile2 = join(dirname(__file__), 'data', 'Example-50.jpg')

    def test_get_thumbnail_of_file(self):
        """Test get_thumbnail_of_file."""
        values = [(('Example.jpg', 100), (self.outputfile1, 'Example.jpeg')),
                  (('Example.jpg', 50), (self.outputfile2, 'Example.jpeg'))]
        for (input_value, expected) in values:
            expected_value = (open(expected[0]).read(), expected[1])
            output = thumbnaildownload.get_thumbnail_of_file(*input_value)
            self.assertEqual(output, expected_value)

    def test_get_thumbnail_of_file_error(self):
        """Test get_thumbnail_of_file with a bad input"""
        input_value = ('UnexistingExample.jpg', 100)
        with self.assertRaises(Exception):
           output = thumbnaildownload.get_thumbnail_of_file(*input_value)


class TestCommonsDownloaderOnlineFile(unittest.TestCase):

    """Testing methods deadling with downloaded files"""

    @classmethod
    def setUpClass(cls):
        """Set up the TestCase with the data files."""
        cls.outputfile1 = join(dirname(__file__), 'data', 'Example-100.jpg')
        cls.outputfile2 = join(dirname(__file__), 'data', 'Example-50.jpg')
        cls.tmpdir1 = tempfile.mkdtemp()
        cls.tmpdir2 = tempfile.mkdtemp()
        values = [('Example.jpg', cls.tmpdir1, 100),
                  ('Example.jpg', cls.tmpdir2, 50)]
        cls.outputs = [thumbnaildownload.download_file(*input_value)
                        for input_value in values]
        cls.expected = [cls.outputfile1, cls.outputfile2]

    def test_paths_in_download_file(self):
        """Test if download_file return the expected values."""
        expected_paths = [join(self.tmpdir1, 'Example.jpeg'),
                          join(self.tmpdir2, 'Example.jpeg')]
        self.assertListEqual(self.outputs, expected_paths)

    def test_paths_exists_in_download_file(self):
        """Test if download_file has actually downloaded anything."""
        for output_file in self.outputs:
            self.assertTrue(exists(output_file))

    def test_files_are_ok_in_download_file(self):
        """Test if download_file has downloaded the right files."""
        for (output_file, expected_file) in zip(self.outputs, self.expected):
            output_contents = open(output_file, 'r').read()
            expected_contents = open(expected_file, 'r').read()
            self.assertEquals(output_contents, expected_contents)


if __name__ == "__main__":
    unittest.main()
