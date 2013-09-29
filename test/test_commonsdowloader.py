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


if __name__ == "__main__":
    unittest.main()
