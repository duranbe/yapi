from tst.setup import YapiTestCase
from urllib.request import urlopen
from subprocess import Popen
import os
import time
import logging

SERVER_START_WAIT_TIME = 1

class TestServer(YapiTestCase):
    def setUp(self) -> None:
        self.process = Popen(["python3", "-m", "tst.sample_server"])
        time.sleep(SERVER_START_WAIT_TIME)
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().handlers[0].setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
        logging.debug("Sample Server started with pid : %d",self.process.pid)
       
    def test_simple_connectivity_check(self):
        url = "http://localhost:4221"

        with urlopen(url) as response:
            self.assertEqual(response.getcode(), 200)
        

    def tearDown(self):

        self.process.kill()
        self.process.wait()
        logging.debug("Sample Server with pid terminated : %d",self.process.pid)
