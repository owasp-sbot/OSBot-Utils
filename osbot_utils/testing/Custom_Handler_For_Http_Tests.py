import json
from http.server  import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from osbot_utils.utils.Json import json_dumps_to_bytes


class Custom_Handler_For_Http_Tests(BaseHTTPRequestHandler):

    HTTP_GET_DATA_JSON   : str = '/data.json'
    HTTP_GET_HTML        : str = "<html><p>hello world</p></html>"
    HTTP_GET_IMAGE_PATH  : str = '/test.png'
    HTTP_GET_IMAGE_BYTES : bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00'
    captured_logs        : list = []
    print_logs           : bool = False

    def do_DELETE(self):
        # Assuming  data as a query string in the URL or as a form
        content_length  = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0
        data_string     = self.rfile.read(content_length).decode('utf-8')
        response_data   = {'status': 'success', 'data_received': data_string}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json_dumps_to_bytes(response_data))


    def do_GET(self):
        if self.path == self.HTTP_GET_IMAGE_PATH:
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(self.HTTP_GET_IMAGE_BYTES)
            return
        if self.path == self.HTTP_GET_DATA_JSON:
            response_data = {
                'args': {'ddd': '1', 'eee': '2'},
                'headers': {
                    'Accept': 'application/json',
                    'Accept-Encoding': 'identity',
                    'Host': 'httpbin.org',
                    'User-Agent': 'Python-urllib/3.10' ,
                    'X-Amzn-Trace-Id': 'Root=1-616b1b1e-4b0a1b1e1b1e1b1e1b1e1b1e'
                },
                'origin': 'some origin',
                'url': 'https://httpbin.org/get?ddd=1&eee=2'
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = self.HTTP_GET_HTML
        self.wfile.write(html.encode())

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Allow', 'POST')
        self.end_headers()

    def do_POST(self):
        # Calculate content length & read the data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = parse_qs(post_data)  # parse the received data

        # Create the response data structure
        response_data = {
            'args': {'ddd': '1', 'eee': '2'},  # This should match the expected args in the test
            'data': '',
            'files': {},
            'form': {key: value[0] for key, value in post_data.items()},  # Convert form data from list to single value
            'headers': {
                'Accept': self.headers['Accept'],
                'Accept-Encoding': self.headers['Accept-Encoding'],
                'Content-Length': self.headers['Content-Length'],
                'Content-Type'  : self.headers['Content-Type'],
                'Host'          : self.headers['Host'],
                'User-Agent'    : self.headers['User-Agent'],
                'X-Amzn-Trace-Id': 'Root=1-616b1b1e-4b0a1b1e1b1e1b1e1b1e1b1e'
            },
            'origin': 'some origin',
            'json': { 'json':'is here', 'a':42},
            'url': self.headers['Host'] + self.path  # Construct the URL from the Host header and path
        }

        # Send the HTTP response

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Convert the response data to JSON and write it to the response
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])                    # todo refactor into helper method (since there are a number of methods here that use this)
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = parse_qs(post_data)  # parse the received data
        response_data = {
            'args': {'ddd': '1', 'eee': '2'},  # This should match the expected args in the test
            'data': '',
            'files': {},
            'form': {key: value[0] for key, value in post_data.items()},  # Convert form data from list to single value
            'headers': { 'X-Amzn-Trace-Id': 'Root=1-616b1b1e-4b0a1b1e1b1e1b1e1b1e1b1e'},
            'origin': 'some origin',
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def log_message(self, msg_format, *args):
        log_message = "%s - - %s" % (self.address_string(), msg_format % args)
        self.captured_logs.append(log_message)
        if self.print_logs:
            print(log_message)