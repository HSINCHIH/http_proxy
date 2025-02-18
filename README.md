# http_proxy
A proxy server that forwards HTTP and WebSocket requests while preserving cookies.

* Install the necessary packages.
```bash
$ brew install node
$ npm install http-proxy-middleware express
```
* Start the server, and stop it using [Ctrl + C] to terminate the process.
```bash
$ node proxy.js
```
* Modify the proxy server configuration if needed.
```javascript
// proxy.js
const targetUrl = 'http://example.com';
const PORT = 8080;
```
