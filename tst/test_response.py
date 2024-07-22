import unittest

from src.exceptions.exceptions import ContentLengthNotMatchingException
from src.response.response import Response


class TestResponse(unittest.TestCase):
    def test_make_response(self):
        response = Response(status="200 OK", headers={}, body="sample body text")
        expected_response = (
            "HTTP/1.1 200 OK\r\nContent-Length: 16\r\n\r\n\r\nsample body text"
        )
        self.assertEqual(expected_response, response._response)

    def test_incorrect_content_length_throws_exception(self):
        self.assertRaises(
            ContentLengthNotMatchingException,
            Response,
            "200 OK",
            {"Content-Length": 0},
            "test",
        )


if __name__ == "__main__":
    unittest.main()
