import unittest

from raiz.remoteok import find_title


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual(find_title("<div></div>"), [])
