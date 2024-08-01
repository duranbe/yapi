from urllib.error import HTTPError
from tst.setup import YapiTestCase
from urllib.request import urlopen
from subprocess import Popen
import time
import logging

SERVER_START_WAIT_TIME = 0.1


class TestServer(YapiTestCase):
    def setUp(self) -> None:
        self.process = Popen(["python3", "-m", "tst.sample_server"])
        time.sleep(SERVER_START_WAIT_TIME)
        logging.info("Sample Server started with pid : %d", self.process.pid)

    def test_simple_connectivity_check(self):
        url = "http://localhost:4221/test"
        with urlopen(url) as response:
            self.assertEqual(response.getcode(), 200)
            self.assertInUrllibHeaders("Content-Length", response.info()._headers)
            self.assertEqual(response.read().decode(), "test")

    def test_404_not_found(self):
        url = "http://localhost:4221/doesnotexist"

        with self.assertRaises(HTTPError) as error:
            urlopen(url)
        self.assertEqual("HTTP Error 404: Not Found", str(error.exception))

        url = "http://localhost:4221/test"

        with urlopen(url) as response:
            self.assertEqual(response.getcode(), 200)
            self.assertInUrllibHeaders("Content-Length", response.info()._headers)
            self.assertEqual(response.read().decode(), "test")

    def test_405_not_found(self):
        url = "http://localhost:4221/test"

        with self.assertRaises(HTTPError) as error:
            urlopen(url, data=b"test")
        self.assertEqual("HTTP Error 405: Method Not Allowed", str(error.exception))

    def tearDown(self):
        self.process.kill()
        self.process.wait()
        logging.info("Sample Server with pid %d has been terminated", self.process.pid)
