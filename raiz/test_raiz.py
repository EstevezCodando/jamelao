import unittest

import raiz


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual(raiz.find_title("<div></div>"), [])
