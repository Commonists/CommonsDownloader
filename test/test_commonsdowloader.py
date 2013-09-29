#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Unit tests."""

from os.path import dirname, join
import unittest
import commonsdownloader


class TestCommonsDownloaderOffline(unittest.TestCase):

    """Testing methods from commonsdownloader which do not require connection."""

    def test_clean_up_filename(self):
        """Test clean_up_filename."""
        values = [('Example.jpg', 'Example.jpg'),
                  ('Example.jpg ', 'Example.jpg'),
                  (' Example.jpg', 'Example.jpg'),
                  ('My Example.jpg', 'My_Example.jpg')]
        for (input_value, expected_value) in values:
            self.assertEqual(commonsdownloader.clean_up_filename(input_value),
                             expected_value)

    def test_make_thumb_url(self):
        """Test make_thumb_url."""
        input_value = ('My_Example.jpg', 100)
        expected_value = "http://commons.wikimedia.org/w/thumb.php?f=My_Example.jpg&width=100"
        output = commonsdownloader.make_thumb_url(*input_value)
        self.assertEqual(output, expected_value)

    def test_make_thumbnail_name(self):
        """Test make_thumbnail_name."""
        input_value = ('Example.svg', 'png')
        expected_value = "Example.png"
        output = commonsdownloader.make_thumbnail_name(*input_value)
        self.assertEqual(output, expected_value)


class TestCommonsDownloaderOnline(unittest.TestCase):

    """Testing methods from commonsdownloader which require connection"""

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
            output = commonsdownloader.get_thumbnail_of_file(*input_value)
            self.assertEqual(output, expected_value)

    def test_get_thumbnail_of_file_error(self):
        """Test get_thumbnail_of_file with a bad input"""
        input_value = ('UnexistingExample.jpg', 100)
        with self.assertRaises(Exception):
           output = commonsdownloader.get_thumbnail_of_file(*input_value)

if __name__ == "__main__":
    unittest.main()
