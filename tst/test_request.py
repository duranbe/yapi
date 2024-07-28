import unittest
from src.request import Request
from tst.setup import YapiTestCase

class TestRequest(YapiTestCase):

    def test_request_parse_headers(self):
        
        request_data = b'GET /test HTTP/1.1\r\n\r\n'

        request = Request(request_data)

        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.endpoint, '/test')
        self.assertEqual(request.protocol, 'HTTP/1.1')
        self.assertEqual(request.headers, {})


