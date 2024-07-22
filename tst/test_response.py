import unittest

from src.response.response import Response 

class TestResponse(unittest.TestCase):

    def setUp(self):
        self.response = Response(status="200 OK", headers={},body="sample body text")

    def test_make_response(self):
        expected_response = "HTTP/1.1 200 OK\r\nContent-Length: 16\r\n\r\n\r\nsample body text"
        self.assertEqual(expected_response, self.response._response)




if __name__ == '__main__':
    unittest.main()
