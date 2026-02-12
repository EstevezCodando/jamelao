import unittest

import raiz


class RaizCore(unittest.TestCase):
    def test_find_title(self):
        self.assertEqual(raiz.find_title("<div></div>"), 'Hello World')
