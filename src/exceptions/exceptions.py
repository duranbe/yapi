

class ContentLengthNotMatchingException(BaseException):
    """
    Exception when Content-Length headers does not match body length
    """

    def __str__(self):
        return "Length in Content-Length header does not match length of body"
