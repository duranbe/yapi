from src.request import Request
from tst.setup import YapiTestCase


class TestRequest(YapiTestCase):
    def test_request_parse_headers(self):
        request_data = b"GET /test HTTP/1.1\r\nAccept-Encoding: gzip\r\n\r\n"

        request = Request(request_data)

        self.assertEqual(request.method, "GET")
        self.assertEqual(request.endpoint, "/test")
        self.assertEqual(request.protocol, "HTTP/1.1")
        self.assertEqual(request.headers, {"Accept-Encoding": "gzip"})
        self.assertEqual(request.body, "")


    def test_request_parse_headers_and_url(self):
            request_data = b"POST /test/test/test HTTP/1.1\r\nAccept-Encoding: gzip\r\n\r\nbody"

            request = Request(request_data)

            self.assertEqual(request.method, "POST")
            self.assertEqual(request.endpoint, "/test/test/test")
            self.assertEqual(request.protocol, "HTTP/1.1")
            self.assertEqual(request.headers, {"Accept-Encoding": "gzip"})
            self.assertEqual(request.body, "body")