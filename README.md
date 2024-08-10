# yapi    
 
![example workflow](https://github.com/duranbe/yapi/actions/workflows/test.yml/badge.svg)


## What's yapi
yapi is supposed to be a micro-web framework in Python


## Getting Started 

### Installation


### Simple Server

Create a server object, with domain and port

```python
server = Server("localhost", 1337)
```

Declare an endpoint and return a standard Response, an HTMLResponse or JsonResponse
```python
@server.endpoint(path="/test", allowed_methods=["GET"])
def test_endpoint(request: Request):
    response = Response(status=HTTP_200, headers={}, body=None)
    return response
```

Finally run it ! 

```python
if __name__ == "__main__":
    server.run()
```

Full example 

```python
import argparse

from src.response import Response
from src.request import Request
from src.server import Server
from src.response.statuses import HTTP_200

parser = argparse.ArgumentParser()
parser.add_argument("--domain", dest="domain", type=str, help="domain to run server", default="localhost")
parser.add_argument("--port", dest="port", type=int, help="port to run server", default=4221)
args = parser.parse_args()

server = Server(args.domain, args.port)

@server.endpoint(path="/test", allowed_methods=["GET"])
def test_endpoint(request: Request):
    return Response(status=HTTP_200, headers={}, body="Hello World!")


if __name__ == "__main__":
    server.run()

```

Test it with ```curl http://localhost:4221/test -i ```

For more examples checkout the sample_server is tst folder
