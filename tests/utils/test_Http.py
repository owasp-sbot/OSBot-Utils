import json
from http.server import BaseHTTPRequestHandler
from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Json import json_dumps, json_dumps_to_bytes

from osbot_utils.testing.Temp_Web_Server import Temp_Web_Server

from osbot_utils.utils import Http

from osbot_utils.utils.Files import temp_file, file_not_exists, file_exists, file_bytes, file_size, file_create_bytes, \
    file_delete
from osbot_utils.utils.Http import DELETE, POST, GET, GET_json, DELETE_json, GET_bytes, GET_bytes_to_file, \
    dns_ip_address, port_is_open, port_is_not_open, current_host_online, POST_json, OPTIONS, PUT_json, \
    is_port_open, wait_for_port


# using httpbin.org because it seems to be the best option
#
# reqbin.com throwns 403 when using the default user-agent ("Python-urllib/3.8") the changes below worked
#        url = "https://reqbin.com/echo/get/json"
#        self.headers["User-Agent"] = "python-requests/2.25.1"
#
# other options:
#
# - https://gorest.co.in/public-api/users
# - https://restful-booker.herokuapp.com/apidoc/index.html

class Custom_Handler_For_Http_Tests(BaseHTTPRequestHandler):

    HTTP_GET_DATA_JSON  = '/data.json'
    HTTP_GET_HTML        = "<html><p>hello world</p></html>"
    HTTP_GET_IMAGE_PATH  = '/test.png'
    HTTP_GET_IMAGE_BYTES = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00'

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
        print(self.path)
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

    def log_message(self, msg_format, *args):
        print("%s - - %s" % (self.address_string(), msg_format % args))


class test_Http(TestCase):
    temp_web_server : Temp_Web_Server
    local_url       : str
    local_host      : str
    local_port      : int
    url_png         : str

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_web_server = Temp_Web_Server(http_handler=Custom_Handler_For_Http_Tests)
        cls.temp_web_server.start()
        cls.local_url      = cls.temp_web_server.url()
        cls.local_host     = cls.temp_web_server.host
        cls.local_port     = cls.temp_web_server.port
        cls.url_png        = cls.temp_web_server.url(Custom_Handler_For_Http_Tests.HTTP_GET_IMAGE_PATH)
        assert cls.temp_web_server.GET() == Custom_Handler_For_Http_Tests.HTTP_GET_HTML

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_web_server.stop()

    def setUp(self) -> None:
        self.headers      = {"Accept": "application/json"}
        self.data         = "aaa=42&bbb=123"
        self.data_json    = { "aaa":42 , "bbb":"123"}
        #self.url_png      = 'https://avatars.githubusercontent.com/u/52993993?s=200&v=4'
        self.url_template = "https://httpbin.org/{method}?ddd=1&eee=2"

    def test_current_host_online(self):
        url_to_use = self.local_url
        assert current_host_online(url_to_use=url_to_use                    ) is True
        assert current_host_online(url_to_use='http://111-2222-3333-abc.com') is False


    def test_DELETE_json(self):
        # url = self.url_template.format(method="delete")                           # this used to take 600ms on average
        # response = DELETE_json(url, headers=self.headers, data=self.data)
        # assert response["form"] ==  { "aaa": "42",  "bbb": "123" }
        url      = self.local_url                                                   # now it is 2 ms
        response = DELETE_json(url, headers=self.headers, data=self.data)
        assert response == {'data_received': 'aaa=42&bbb=123', 'status': 'success'}

    def test_GET_bytes(self):
        bytes = GET_bytes(self.url_png)
        assert bytes == Custom_Handler_For_Http_Tests.HTTP_GET_IMAGE_BYTES
        try:
            GET(self.url_png)
            assert False
        except Exception as error:
            assert error.args[4] == 'invalid start byte'
        # bytes = GET_bytes(self.url_png)                                              # this used to take ~220ms
        # assert len(bytes) == 17575
        # assert bytes[:4] == b"\x89PNG"

    def test_GET_json(self):
        #url = self.url_template.format(method="get")                        # took 700ms

        url = self.temp_web_server.url(Custom_Handler_For_Http_Tests.HTTP_GET_DATA_JSON)
        response = GET_json(url, headers=self.headers)
        pprint(response)

        del response['headers']['X-Amzn-Trace-Id']
        del response['origin']

        assert response == {    'args'   : { 'ddd': '1', 'eee': '2'}                   ,
                                'headers': { 'Accept'         : 'application/json'   ,
                                             'Accept-Encoding': 'identity'           ,
                                             'Host'           : 'httpbin.org'        ,
                                             'User-Agent'     : 'Python-urllib/3.10' } ,
                                'url'    : 'https://httpbin.org/get?ddd=1&eee=2'
                            }

    def test_GET_bytes_to_file(self):
        target = temp_file(extension="png")
        assert file_not_exists(target)
        assert GET_bytes_to_file(self.url_png, target)
        assert file_exists(target)
        assert file_size(target) == 19
        assert file_bytes(target)  == Custom_Handler_For_Http_Tests.HTTP_GET_IMAGE_BYTES
        assert file_delete(target) is True

    def test_wait_for_port(self):
        assert wait_for_port(self.local_host , self.local_port                                     ) is True
        assert wait_for_port(self.local_host    , self.local_port+1, max_attempts=2, wait_for=0.001) is False


    def test_OPTIONS(self):
        url = self.url_template.format(method="post")
        response_headers = OPTIONS(url, headers=self.headers)
        assert 'POST' in response_headers['Allow']

    def test_POST_json(self):
        url      = self.url_template.format(method="post")
        response = POST_json(url, data=self.data, headers=self.headers)

        del response['headers']['X-Amzn-Trace-Id']
        del response['origin']

        assert response == {    'args'   : { 'ddd': '1', 'eee': '2'}                                  ,
                                'data'   : ''                                                         ,
                                'files'  : {}                                                         ,
                                'form'   : { 'aaa': '42', 'bbb': '123'}                               ,
                                'headers': { 'Accept'         : 'application/json'                  ,
                                             'Accept-Encoding': 'identity'                          ,
                                             'Content-Length' : '14'                                ,
                                             'Content-Type'   : 'application/x-www-form-urlencoded' ,
                                             'Host'           : 'httpbin.org'                       ,
                                             'User-Agent'     : 'Python-urllib/3.10'                } ,
                                'json'   : None                                                       ,
                                'url'    : 'https://httpbin.org/post?ddd=1&eee=2'
                            }

    def test_POST_json__with_json_payload(self):
        url = self.url_template.format(method="post")
        self.headers['Content-Type'] = "application/json"
        self.data = { 'json':'is here', 'a':42}
        response = POST_json(url, data=self.data, headers=self.headers)

        assert response['headers']['Content-Type'] == self.headers['Content-Type']
        assert response['json'   ]                 == self.data
        #print()
        #pprint(response)

    def test_PUT_json(self):
        url      = self.url_template.format(method="put")
        response = PUT_json(url, data=self.data, headers=self.headers)

        del response['headers']['X-Amzn-Trace-Id']
        del response['origin']

        assert response['form'] == {'aaa': '42', 'bbb': '123'}

    # todo|: replace this test with a local web server, it fails quite a number of times locally and they can take a while
    def test_is_port_open__port_is_open__port_is_not_open(self):
        host    = "www.google.com"
        port    = 443
        host_ip = dns_ip_address(host)
        timeout = 0.10

        assert is_port_open(host=host   , port=port  , timeout=timeout) is True
        assert is_port_open(host=host_ip, port=port  , timeout=timeout) is True
        assert is_port_open(host=host   , port=port+1, timeout=timeout) is False
        assert is_port_open(host=host_ip, port=port+1, timeout=timeout) is False

        assert port_is_open(host=host   , port=port  , timeout=timeout) is True
        assert port_is_open(host=host_ip, port=port  , timeout=timeout) is True
        assert port_is_open(host=host   , port=port+1, timeout=timeout) is False
        assert port_is_open(host=host_ip, port=port+1, timeout=timeout) is False

        assert port_is_not_open(host=host   , port=port  , timeout=timeout) is False
        assert port_is_not_open(host=host_ip, port=port  , timeout=timeout) is False
        assert port_is_not_open(host=host   , port=port+1, timeout=timeout) is True
        assert port_is_not_open(host=host_ip, port=port+1, timeout=timeout) is True