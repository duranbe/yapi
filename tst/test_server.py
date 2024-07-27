from tst.setup import YapiTestCase
from urllib.request import urlopen
from subprocess import Popen


class TestServer(YapiTestCase):
    def setUp(self) -> None:
        self.process = Popen(["python3", "-m", "tst.sample_server"])

    def test_simple_connectivity_check(self):
        url = "http://127.0.0.1:4221"

        with urlopen(url) as response:
            self.assertEqual(response.getcode(), 200)

    def tearDown(self):
        self.process.kill()
        self.process.wait()
