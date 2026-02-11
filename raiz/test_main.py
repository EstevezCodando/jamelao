import unittest

import main


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual(main.find_title("<div></div>"), 'Hello World')
