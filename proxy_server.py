import http.server
import socketserver
import urllib.parse
import http.client
import threading
import signal
import sys


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    cookies = {}

    def forward_request(self, method):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        target_url = query_params.get("url", [None])[0]

        if not target_url:
            self.send_error(400, "Missing 'url' query parameter")
            return

        target_parsed = urllib.parse.urlparse(target_url)
        target_host = target_parsed.hostname
        target_path = target_parsed.path or "/"
        target_port = target_parsed.port or (443 if target_parsed.scheme == "https" else 80)
        target_scheme = target_parsed.scheme

        print(f"Target URL: {target_url}")

        try:
            if target_scheme == "https":
                connection = http.client.HTTPSConnection(target_host, target_port)
            else:
                connection = http.client.HTTPConnection(target_host, target_port)

            headers = dict(self.headers)
            if target_host in self.cookies:
                headers["Cookie"] = "; ".join(self.cookies[target_host])

            body = None
            if method == "POST":
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length) if content_length > 0 else None

            connection.request(method, target_path, body=body, headers=headers)
            response = connection.getresponse()

            self.send_response(response.status)
            for header, value in response.getheaders():
                if header.lower() == "set-cookie":
                    if target_host not in self.cookies:
                        self.cookies[target_host] = []
                    self.cookies[target_host].append(value.split(";")[0])
                self.send_header(header, value)
            self.end_headers()

            self.wfile.write(response.read())
        except Exception as e:
            print(f"Error during request: {e}")
            self.send_error(500, f"Proxy error: {e}")
        finally:
            connection.close()

    def do_GET(self):
        self.forward_request("GET")

    def do_POST(self):
        self.forward_request("POST")


class GracefulTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

    def shutdown(self):
        self._BaseServer__shutdown_request = True
        super().shutdown()


def start_server():
    PORT = 8080
    httpd = GracefulTCPServer(("", PORT), ProxyHandler)

    def handle_signal(signal_num, frame):
        print("\nShutting down the proxy server gracefully...")
        threading.Thread(target=stop_server, args=(httpd,)).start()

    def stop_server(server):
        server.shutdown()
        server.server_close()
        print("Proxy server has been shut down.")

    signal.signal(signal.SIGINT, handle_signal)
    print(f"Serving proxy on port {PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nProxy server stopped.")
