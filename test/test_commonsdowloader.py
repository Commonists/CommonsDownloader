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

    def test_make_thumb_url_with_ampersand(self):
        """Test make_thumb_url with an ampersand character."""
        input_value = ('My_Example2&3.jpg', 100)
        expected_value = "http://commons.wikimedia.org/w/thumb.php?f=My_Example2%263.jpg&width=100"
        output = thumbnaildownload.make_thumb_url(*input_value)
        self.assertEqual(output, expected_value)

    def test_make_full_size_url(self):
        """Test make_full_size_url."""
        input_value = 'My_Example.jpg'
        expected_value = "http://commons.wikimedia.org/w/index.php?title=Special:FilePath&file=My_Example.jpg"
        output = thumbnaildownload.make_full_size_url(input_value)
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

    """Testing methods from thumbnaildownload which require connection."""

    def setUp(self):
        """Sett up the TestCase with the data files."""
        self.outputfile1 = join(dirname(__file__), 'data', 'Example-100.jpg')
        self.outputfile2 = join(dirname(__file__), 'data', 'Example-50.jpg')
        self.outputfile3 = join(dirname(__file__), 'data', 'Example.jpg')

    def test_get_thumbnail_of_file(self):
        """Test get_thumbnail_of_file."""
        values = [(('Example.jpg', 100), (self.outputfile1, 'Example.jpg')),
                  (('Example.jpg', 50), (self.outputfile2, 'Example.jpg'))]
        for (input_value, expected) in values:
            expected_value = (open(expected[0]).read(), expected[1])
            output = thumbnaildownload.get_thumbnail_of_file(*input_value)
            self.assertEqual(output, expected_value)

    def test_get_thumbnail_of_file_higher_than_possible(self):
        """Test get_thumbnail_of_file with a size larger than available."""
        input_value = ('Example.jpg', 1000)
        with self.assertRaises(thumbnaildownload.RequestedWidthBiggerThanSourceException):
            _ = thumbnaildownload.get_thumbnail_of_file(*input_value)

    def test_get_thumbnail_of_non_existing_file(self):
        """Test get_thumbnail_of_file with a non-existing file."""
        input_value = ('UnexistingExample.jpg', 100)
        with self.assertRaises(thumbnaildownload.FileDoesNotExistException):
            _ = thumbnaildownload.get_thumbnail_of_file(*input_value)

    def test_get_full_size_file(self):
        """Test get_full_size_file."""
        input_value = 'Example.jpg'
        expected_value = (open(self.outputfile3).read(), 'Example.jpg')
        output = thumbnaildownload.get_full_size_file(input_value)
        self.assertEqual(output, expected_value)

    def test_get_full_size_of_non_existing_file(self):
        """Test get_full_size_file with a non-existing file."""
        input_value = 'UnexistingExample.jpg'
        with self.assertRaises(thumbnaildownload.FileDoesNotExistException):
            _ = thumbnaildownload.get_full_size_file(input_value)


class TestCommonsDownloaderOnlineFile(unittest.TestCase):

    """Testing methods dealing with downloaded files."""

    @classmethod
    def setUpClass(cls):
        """Set up the TestCase with the data files."""
        cls.outputfile1 = join(dirname(__file__), 'data', 'Example-100.jpg')
        cls.outputfile2 = join(dirname(__file__), 'data', 'Example-50.jpg')
        cls.outputfile3 = join(dirname(__file__), 'data', 'Example.jpg')
        cls.tmpdir1 = tempfile.mkdtemp()
        cls.tmpdir2 = tempfile.mkdtemp()
        cls.tmpdir3 = tempfile.mkdtemp()
        values = [('Example.jpg', cls.tmpdir1, 100),
                  ('Example.jpg', cls.tmpdir2, 50),
                  ('Example.jpg', cls.tmpdir3, 1000)]
        cls.outputs = [thumbnaildownload.download_file(*input_value)
                       for input_value in values]
        cls.expected = [cls.outputfile1, cls.outputfile2, cls.outputfile3]

    def test_paths_in_download_file(self):
        """Test if download_file return the expected values."""
        expected_paths = [join(self.tmpdir1, 'Example.jpg'),
                          join(self.tmpdir2, 'Example.jpg'),
                          join(self.tmpdir3, 'Example.jpg')]
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

    def test_download_file_with_non_existing_file(self):
        """Test download_file with a non-existing file."""
        input_value = ('UnexistingExample.jpg', 100)
        with self.assertRaises(thumbnaildownload.FileDoesNotExistException):
            _ = thumbnaildownload.download_file(input_value[0], self.tmpdir1, width=input_value[1])


if __name__ == "__main__":
    unittest.main()
