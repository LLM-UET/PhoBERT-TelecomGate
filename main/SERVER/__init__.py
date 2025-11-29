import sys

class HTTPException(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"HTTP {code}: {message}")

def run_server(
    input_model_dir: str | None = None,
    host=None,
    port=None,
):
    host = host or "0.0.0.0"
    port = port or 8136
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from socketserver import ThreadingMixIn

    print("Initializing Inferer for server...", file=sys.stderr)
    from ..INFER import Inferer
    inferer = Inferer(input_model_dir=input_model_dir)

    def test_segmenter():
        input = "Mình xin chào các bạn trẻ có mặt tại đây nhé!"
        print(f"Testing segmenter with input: {input}...", file=sys.stderr)
        output = inferer.segment(input)
        print(f"Segmenter test output: {output}", file=sys.stderr)
        print("Segmenter seems to be working.", file=sys.stderr)
    
    test_segmenter()

    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        """Handle requests in separate threads."""
        daemon_threads = True  # kill threads on shutdown

    class TextRPCHandler(BaseHTTPRequestHandler):
        # disable noisy logging
        def log_message(self, format, *args):
            return

        def do_POST(self):
            path = self.path
            if path == '/v1/infer':
                try:
                    self.serve_v1_infer()
                except HTTPException as e:
                    self.send_response(e.code)
                    self.end_headers()
                    self.wfile.write(e.message.encode("utf-8"))
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(str(e).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")
        
        def serve_v1_infer(self):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            # ---- your RPC handler logic goes here ----
            # response = f"Thread {threading.get_ident()} received: {body}"
            if body.strip() == "":
                raise HTTPException(400, "No input text?")
            
            response = inferer.infer(body)
            # -------------------------------------------

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

    # ========== Start the server ==========

    server = ThreadedHTTPServer((host, port), TextRPCHandler)
    print(f"Server running on {host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
