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

    def tearDown(self):
        self.process.kill()
        self.process.wait()
        logging.info("Sample Server with pid %d has been terminated", self.process.pid)
