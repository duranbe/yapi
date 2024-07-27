import unittest
import logging
import re


class YapiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().handlers[0].setFormatter(
            logging.Formatter("\n%(levelname)s:%(message)s")
        )
        current_test = unittest.TestCase.id(self)
        test_name = re.sub(r"^.*?\.", "", current_test)
        logging.info(test_name)

    def assertInUrllibHeaders(self, header_value, urllib_headers):
        for header in urllib_headers:
            if header[0] == header_value:
                return

        raise AssertionError(f"{header_value} not found in {urllib_headers}")
