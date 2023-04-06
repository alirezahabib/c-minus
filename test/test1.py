import unittest

from Compiler import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
        SymbolTable()


if __name__ == '__main__':
    unittest.main()

