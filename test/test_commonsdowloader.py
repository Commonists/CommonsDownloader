#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Unit tests."""

import unittest
import commonsdownloader


class TestCommonsDownloader(unittest.TestCase):

    """Testing methods from commonsdownloader."""

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


if __name__ == "__main__":
    unittest.main()
