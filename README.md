# http_proxy
A proxy server that carries cookies for every forwarded HTTP request

* Run the proxy server
```bash
$ python proxy_server.py
Serving proxy on port 8080
```
* Test the GET method
```bash
$ curl -X GET "http://127.0.0.1:8080/?url=https://example.com"
```
* Test the POST method
```bash
$ curl -X POST -d "key=value" "http://127.0.0.1:8080/?url=https://httpbin.org/post"
```
* Press Ctrl + C to stop the server.
```bash
Shutting down the proxy server gracefully...
Proxy server has been shut down.
```
