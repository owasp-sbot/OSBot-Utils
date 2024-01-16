import json
from http.server import BaseHTTPRequestHandler
from pprint import pprint
from unittest import TestCase
from urllib.parse import parse_qs

from osbot_utils.utils.Objects import obj_info

from osbot_utils.utils.Json import json_dumps_to_bytes
from osbot_utils.testing.Temp_Web_Server import Temp_Web_Server
from osbot_utils.utils.Files import temp_file, file_not_exists, file_exists, file_bytes, file_size, file_create_bytes, \
    file_delete
from osbot_utils.utils.Http import DELETE, POST, GET, GET_json, DELETE_json, GET_bytes, GET_bytes_to_file, \
    dns_ip_address, port_is_open, port_is_not_open, current_host_online, POST_json, OPTIONS, PUT_json, \
    is_port_open, wait_for_port, current_host_offline


# note: with the use of Custom_Handler_For_Http_Tests this test went from 10 seconds + to 17 ms :)
#       which is massive since the total test execution went from 15 seconds to 5 seconds

class test_Http(TestCase):
    expected_logs   : list = []
    local_host      : str
    local_port      : int
    local_url       : str
    temp_web_server : Temp_Web_Server
    url_png         : str

    @classmethod
    def add_expected_log(cls, method='GET', path='/', status_code=200):
        log_message = f'127.0.0.1 - - "{method} {path} HTTP/1.1" {status_code} -'
        cls.expected_logs.append(log_message)

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_web_server = Temp_Web_Server(http_handler=Custom_Handler_For_Http_Tests)
        cls.temp_web_server.start()
        cls.local_url      = cls.temp_web_server.url()
        cls.local_host     = cls.temp_web_server.host
        cls.local_port     = cls.temp_web_server.port
        cls.url_png        = cls.temp_web_server.url(Custom_Handler_For_Http_Tests.HTTP_GET_IMAGE_PATH)
        cls.headers        = {"Accept": "application/json"}
        cls.data           = "aaa=42&bbb=123"
        cls.data_json      = {"aaa": 42, "bbb": "123"}
        assert cls.temp_web_server.GET() == Custom_Handler_For_Http_Tests.HTTP_GET_HTML
        cls.add_expected_log()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_web_server.stop()
        assert cls.temp_web_server.http_handler.captured_logs == cls.expected_logs

    def test__setUp(self):
        assert self.temp_web_server.server_port_open() is True
        assert self.local_url  == f'http://127.0.0.1:{self.local_port}'
        assert self.local_host == '127.0.0.1'
        assert self.local_port  > 20000
        assert self.headers    == {'Accept': 'application/json', 'Content-Type': 'application/json'}
        assert self.data       == "aaa=42&bbb=123"
        assert self.data_json  == {"aaa": 42, "bbb": "123"}


    def test_current_host_online(self):
        url_to_use = self.local_url
        assert current_host_online(url_to_use=url_to_use                    ) is True
        assert current_host_online(url_to_use='http://111-2222-3333-abc.com') is False
        self.add_expected_log('HEAD')

    def test_current_host_offline(self):
        url_to_use = self.local_url
        assert current_host_offline(url_to_use=url_to_use                    ) is False
        assert current_host_offline(url_to_use='http://111-2222-3333-abc.com') is True
        self.add_expected_log('HEAD')

    def test_is_port_open__port_is_open__port_is_not_open(self):
        host    = 'localhost'
        port    = self.local_port
        host_ip = dns_ip_address(host)
        timeout = 0.10

        assert host_ip == self.local_host
        assert is_port_open    (host=host   , port=port    , timeout=timeout) is True
        assert is_port_open    (host=host_ip, port=port    , timeout=timeout) is True
        assert is_port_open    (host=host   , port=port+1  , timeout=timeout) is False
        assert is_port_open    (host=host_ip, port=port+1  , timeout=timeout) is False

        assert port_is_open    (port=port   , host=host    , timeout=timeout) is True
        assert port_is_open    (port=port   , host=host_ip , timeout=timeout) is True
        assert port_is_open    (port=port+1 , host=host    , timeout=timeout) is False
        assert port_is_open    (port=port+1 , host=host_ip , timeout=timeout) is False

        assert port_is_not_open(host=host   , port=port  , timeout=timeout  ) is False
        assert port_is_not_open(host=host_ip, port=port  , timeout=timeout  ) is False
        assert port_is_not_open(host=host   , port=port+1, timeout=timeout  ) is True
        assert port_is_not_open(host=host_ip, port=port+1, timeout=timeout  ) is True

    def test_DELETE_json(self):
        url      = self.local_url                                                   # now it is 2 ms
        response = DELETE_json(url, headers=self.headers, data=self.data)
        assert response == {'data_received': 'aaa=42&bbb=123', 'status': 'success'}
        self.add_expected_log('DELETE')
        # url = self.url_template.format(method="delete")                           # this used to take 600ms on average
        # response = DELETE_json(url, headers=self.headers, data=self.data)
        # assert response["form"] ==  { "aaa": "42",  "bbb": "123" }

    def test_GET_bytes(self):
        bytes = GET_bytes(self.url_png)
        assert bytes == Custom_Handler_For_Http_Tests.HTTP_GET_IMAGE_BYTES
        try:
            GET(self.url_png)
            assert False
        except Exception as error:
            assert error.args[4] == 'invalid start byte'
        self.add_expected_log(path='/test.png')
        self.add_expected_log(path='/test.png')
        # bytes = GET_bytes(self.url_png)                                              # this used to take ~220ms
        # assert len(bytes) == 17575
        # assert bytes[:4] == b"\x89PNG"

    def test_GET_json(self):
        #url = self.url_template.format(method="get")                        # took 700ms
        url = self.temp_web_server.url(Custom_Handler_For_Http_Tests.HTTP_GET_DATA_JSON)
        response = GET_json(url, headers=self.headers)

        del response['headers']['X-Amzn-Trace-Id']
        del response['origin']

        assert response == {    'args'   : { 'ddd': '1', 'eee': '2'}                   ,
                                'headers': { 'Accept'         : 'application/json'   ,
                                             'Accept-Encoding': 'identity'           ,
                                             'Host'           : 'httpbin.org'        ,
                                             'User-Agent'     : 'Python-urllib/3.10' } ,
                                'url'    : 'https://httpbin.org/get?ddd=1&eee=2'
                            }
        self.add_expected_log(path='/data.json')

    def test_GET_bytes_to_file(self):
        target = temp_file(extension="png")
        assert file_not_exists(target)
        assert GET_bytes_to_file(self.url_png, target)
        assert file_exists(target)
        assert file_size(target) == 19
        assert file_bytes(target)  == Custom_Handler_For_Http_Tests.HTTP_GET_IMAGE_BYTES
        assert file_delete(target) is True
        self.add_expected_log(path='/test.png')

    def test_OPTIONS(self):
        response_headers = OPTIONS(self.local_url, headers=self.headers)
        assert 'POST' in response_headers['Allow']
        self.add_expected_log('OPTIONS')

    def test_POST_json(self):
        url = self.local_url
        response = POST_json(url, data=self.data, headers=self.headers)
        del response['headers']['X-Amzn-Trace-Id']
        del response['origin']

        assert response == {    'args'   : { 'ddd': '1', 'eee': '2'}                                  ,
                                'data'   : ''                                                         ,
                                'files'  : {}                                                         ,
                                'form'   : { 'aaa': '42', 'bbb': '123'}                               ,
                                'headers': { 'Accept'         : 'application/json'                    ,
                                             'Accept-Encoding': 'identity'                            ,
                                             'Content-Length' : '14'                                  ,
                                             'Content-Type'   : 'application/x-www-form-urlencoded'   ,
                                             'Host'           : f'{self.local_host}:{self.local_port}',
                                             'User-Agent'     : 'Python-urllib/3.10'                } ,
                                'json'   : { 'json':'is here', 'a':42}                                                       ,
                                'url'    : f'{self.local_host}:{self.local_port}/'
                            }
        self.add_expected_log('POST')

    def test_POST_json__with_json_payload(self):
        url = self.local_url
        self.headers['Content-Type'] = "application/json"
        self.data = { 'json':'is here', 'a':42}
        response = POST_json(url, data=self.data, headers=self.headers)

        assert response['headers']['Content-Type'] == self.headers['Content-Type']
        assert response['json'   ]                 == self.data
        self.add_expected_log('POST')

    def test_PUT_json(self):
        url = self.local_url
        response = PUT_json(url, data=self.data, headers=self.headers)

        del response['headers']['X-Amzn-Trace-Id']
        del response['origin']

        assert response['form'] == {'aaa': '42', 'bbb': '123'}
        self.add_expected_log('PUT')

    def test_wait_for_port(self):
        assert wait_for_port(self.local_host , self.local_port                                     ) is True
        assert wait_for_port(self.local_host    , self.local_port+1, max_attempts=2, wait_for=0.001) is False




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
