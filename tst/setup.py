import unittest


class YapiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        print("\n", unittest.TestCase.id(self))
