import ssl

from unittest                               import TestCase
from unittest.mock                          import patch, call

from osbot_utils.testing.Custom_Handler_For_Http_Tests import Custom_Handler_For_Http_Tests
from osbot_utils.utils.Objects              import class_full_name, obj_data
from osbot_utils.testing.Temp_Web_Server    import Temp_Web_Server
from osbot_utils.utils.Files                import temp_file, file_not_exists, file_exists, file_bytes, file_size, file_create_bytes, file_delete, file_contents
from osbot_utils.utils.Http import DELETE, POST, GET, GET_json, DELETE_json, GET_bytes, GET_bytes_to_file, \
    dns_ip_address, port_is_open, port_is_not_open, current_host_online, POST_json, OPTIONS, PUT_json, \
    is_port_open, wait_for_port, current_host_offline, http_request, wait_for_http, wait_for_ssh, \
    wait_for_port_closed, GET_to_file, url_join_safe, parse_cookies


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

    def test_http_request(self):
        with patch('osbot_utils.utils.Http.urlopen') as mock_urlopen:
            url_https = 'https://aaaaa.bbbbb'
            response = http_request(url=url_https,return_response_object=True)
            assert type(response).__name__ == 'MagicMock'
            mock_urlopen.assert_called()
            request = mock_urlopen.call_args[0][0]                      # *args
            context = mock_urlopen.call_args[1].get('context')          # **kwargs
            assert class_full_name(request) == 'urllib.request.Request'
            assert class_full_name(context) == 'ssl.SSLContext'

            assert obj_data(request) == {'data'             : None                   ,
                                         'fragment'         : None                   ,
                                         'full_url'         : 'https://aaaaa.bbbbb'  ,
                                         'get_method'       : f'{request.get_method}',
                                         'headers'          : '{}'                   ,
                                         'host'             : 'aaaaa.bbbbb'          ,
                                         'origin_req_host'  : 'aaaaa.bbbbb'          ,
                                         'selector'         : ''                     ,
                                         'type'             : 'https'                ,
                                         'unredirected_hdrs': '{}'                   ,
                                         'unverifiable'     : False                  }
            assert context.protocol == ssl.PROTOCOL_TLSv1_2
            #mock_urlopen.assert_called_with('http://www.google.com')

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

        assert port_is_open    (port=port                                   ) is True
        assert port_is_open    (port=port   , host=host    , timeout=timeout) is True
        assert port_is_open    (port=port   , host=host_ip , timeout=timeout) is True
        assert port_is_open    (port=port+1 ,                               ) is False
        assert port_is_open    (port=port+1 , host=host    , timeout=timeout) is False
        assert port_is_open    (port=port+1 , host=host_ip , timeout=timeout) is False
        assert port_is_open    (port=None   , host=host_ip, timeout=timeout ) is False
        assert port_is_open    (port=port   , host=None    , timeout=timeout) is False


        assert port_is_not_open(host=host   , port=port  , timeout=timeout  ) is False
        assert port_is_not_open(host=host_ip, port=port  , timeout=timeout  ) is False
        assert port_is_not_open(host=host   , port=port+1, timeout=timeout  ) is True
        assert port_is_not_open(host=host_ip, port=port+1, timeout=timeout  ) is True

    def test_parse_cookies(self):
        cookie_header   = ('SESSION_ID__USER="user123"; expires=Tue, 29 Oct 2024 22:00:56 GMT; Max-Age=0; '     # Main test with multiple cookies
                           'Path=/; SameSite=lax, SESSION_ID__PERSONA="persona456"; '
                           'expires=Tue, 29 Oct 2024 22:00:56 GMT; Max-Age=0; Path=/; SameSite=lax')
        parsed_cookies  = parse_cookies(cookie_header)

        assert len(parsed_cookies)     == 2
        assert "SESSION_ID__USER"      in parsed_cookies
        assert "SESSION_ID__PERSONA"   in parsed_cookies

        assert parsed_cookies["SESSION_ID__USER"   ]["value"   ] == "user123"
        assert parsed_cookies["SESSION_ID__PERSONA"]["value"   ] == "persona456"

        expected_expiry = "Tue, 29 Oct 2024 22:00:56 GMT"
        assert parsed_cookies["SESSION_ID__USER"   ]["expires" ] == expected_expiry
        assert parsed_cookies["SESSION_ID__PERSONA"]["expires" ] == expected_expiry

        assert parsed_cookies["SESSION_ID__USER"   ]["path"    ] == "/"
        assert parsed_cookies["SESSION_ID__PERSONA"]["path"    ] == "/"

        assert parsed_cookies["SESSION_ID__USER"   ]["samesite"] == "lax"
        assert parsed_cookies["SESSION_ID__PERSONA"]["samesite"] == "lax"

        assert parsed_cookies["SESSION_ID__USER"   ]["max-age" ] == "0"
        assert parsed_cookies["SESSION_ID__PERSONA"]["max-age" ] == "0"

        # Test cookies with secure and httponly flags
        cookie_header = (
            'SESSION_ID__USER="user123"; Secure; HttpOnly; Path=/; SameSite=strict, '
            'SESSION_ID__PERSONA="persona456"; Secure; Path=/; SameSite=none'
        )
        parsed_cookies = parse_cookies(cookie_header)

        assert parsed_cookies["SESSION_ID__USER"]["value"] == "user123"
        assert parsed_cookies["SESSION_ID__USER"]["secure"] is True
        assert parsed_cookies["SESSION_ID__USER"]["httponly"] is True
        assert parsed_cookies["SESSION_ID__USER"]["path"] == "/"
        assert parsed_cookies["SESSION_ID__USER"]["samesite"] == "strict"

        assert parsed_cookies["SESSION_ID__PERSONA"]["value"] == "persona456"
        assert parsed_cookies["SESSION_ID__PERSONA"]["secure"] is True
        assert parsed_cookies["SESSION_ID__PERSONA"]["httponly"] is False
        assert parsed_cookies["SESSION_ID__PERSONA"]["path"] == "/"
        assert parsed_cookies["SESSION_ID__PERSONA"]["samesite"] == "none"


        # Test empty cookie header
        cookie_header = ""
        parsed_cookies = parse_cookies(cookie_header)
        assert parsed_cookies == {}


        # Test with minimal attributes (no expires, max-age, path, samesite, secure, httponly)
        cookie_header = 'TEST_COOKIE="test_value"'
        parsed_cookies = parse_cookies(cookie_header)

        assert len(parsed_cookies) == 1
        assert parsed_cookies["TEST_COOKIE"]["value"] == "test_value"
        assert parsed_cookies["TEST_COOKIE"] == {'comment' : ''          ,
                                                 'domain'  : ''          ,
                                                 'expires' : ''          ,
                                                 'httponly': False       ,
                                                 'max-age' : ''          ,
                                                 'path'    : ''          ,
                                                 'samesite': ''          ,
                                                 'secure'  : False       ,
                                                 'value'   : 'test_value',
                                                 'version' : ''          }

    def test_parse_cookies__bug__parse_multiple_cookies_from_fastapi_client(self):
        cookie_header = "SESSION_ID__USER=1dca22d5-aaaa-bbbb-cccc-ca58f06cdfdf; Path=/abc;, SESSION_ID__ACTIVE=1dca22d5-bbbb-cccc-dddd-ca58f06cdfdf; Path=/;"
        cookie_header = cookie_header.replace(';,', ';')                        #kinda a hack, but works
        parsed_cookies = parse_cookies(cookie_header, include_empty=False)
        #assert parsed_cookies == {} # FIXED, was: BUG , should be 2 cookies
        assert parsed_cookies == {'SESSION_ID__ACTIVE': {'httponly': False,
                                                         'path': '/',
                                                         'secure': False,
                                                         'value': '1dca22d5-bbbb-cccc-dddd-ca58f06cdfdf'},
                                  'SESSION_ID__USER': {'httponly': False,
                                                       'path': '/abc',
                                                       'secure': False,
                                                       'value': '1dca22d5-aaaa-bbbb-cccc-ca58f06cdfdf'}} != {}


    def test_wait_for_http(self):
        url = self.local_url
        assert wait_for_http(url) is True
        self.add_expected_log()
        assert wait_for_http('127.0.0.2', max_attempts=1, wait_for=0.001) is False
        assert wait_for_http('aa'       , max_attempts=1, wait_for=0.001) is False
        assert wait_for_http(None       , max_attempts=1, wait_for=0.001) is False

    def test_wait_for_ssh(self):
        with patch('osbot_utils.utils.Http.wait_for_port') as mock_wait_for_port:
            response = wait_for_ssh('127.0.0.1')
            assert response.__class__.__name__ == 'MagicMock'
            mock_wait_for_port.assert_called()
            assert mock_wait_for_port.call_args == call(host='127.0.0.1', port=22, max_attempts=120, wait_for=0.5)

    def test_wait_for_port_closed(self):
        assert wait_for_port_closed(self.local_host, self.local_port  , max_attempts=1, wait_for=0.001) is False
        assert wait_for_port_closed(self.local_host, self.local_port+1, max_attempts=1, wait_for=0.001) is True

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

    def test_GET_to_file(self):
        url          = self.local_url
        file_via_get = GET_to_file(url)
        assert file_exists  (file_via_get)
        assert file_contents(file_via_get) == Custom_Handler_For_Http_Tests.HTTP_GET_HTML
        assert file_delete  (file_via_get) is True
        self.add_expected_log()

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
                                'headers': response.get('headers')                                    ,
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

    def test_url_join_safe(self):
        #when no path is provided
        assert url_join_safe(None          ) is None
        assert url_join_safe('a'           ) == 'a'
        assert url_join_safe('a/b'         ) == 'a/b'
        assert url_join_safe('http://a'    ) == 'http://a'
        assert url_join_safe('http://a/'   ) == 'http://a'
        assert url_join_safe('http://a/b'  ) == 'http://a/b'
        assert url_join_safe('http://a.b/b') == 'http://a.b/b'
        assert url_join_safe('https://ab/b') == 'https://ab/b'

        # normal cases
        assert url_join_safe('https://a.b/c', 'd'      ) == 'https://a.b/c/d'
        assert url_join_safe('https://a.b/c', 'd/e'    ) == 'https://a.b/c/d/e'
        assert url_join_safe('https://a.b/c', 'd.json' ) == 'https://a.b/c/d.json'
        assert url_join_safe('https://a.b/c', 'd/j.on' ) == 'https://a.b/c/d/j.on'
        assert url_join_safe('https://a.b/c', 'd/j.o.n') == 'https://a.b/c/d/j.o.n'
        assert url_join_safe('https://a.b/c', 'd.j.s.' ) == 'https://a.b/c/d.j.s.'
        assert url_join_safe('https://a.b/c', 'd/./e'  ) == 'https://a.b/c/d/e'

        # with params (confirming that the params are correctly encoded in the query string (i.e. query strings params will need to be submitted separately)
        assert url_join_safe('https://a.b/c', 'd.json#'   ) == 'https://a.b/c/d.json-'
        assert url_join_safe('https://a.b/c', 'd.json?'   ) == 'https://a.b/c/d.json-'
        assert url_join_safe('https://a.b/c', 'd.json?a=b') == 'https://a.b/c/d.json-a-b'

        # abuse cases (with / and \ )
        assert url_join_safe('https://a.b/c', None) is None
        assert url_join_safe('https://a.b/c', r'd/../e'     ) == 'https://a.b/c/d/-/e'
        assert url_join_safe('https://a.b/c', r'/d/../e'    ) == 'https://a.b/c/d/-/e'
        assert url_join_safe('https://a.b/c', r'//d/../e'   ) == 'https://a.b/c/d/-/e'
        assert url_join_safe('https://a.b/c', r'\d/../e'    ) == 'https://a.b/c/-d/-/e'
        assert url_join_safe('https://a.b/c', r'\\d/../e'   ) == 'https://a.b/c/-d/-/e'
        assert url_join_safe('https://a.b/c', r'\\\d/../e'  ) == 'https://a.b/c/-d/-/e'
        assert url_join_safe('https://a.b/c', r'\\/d/../e'  ) == 'https://a.b/c/-/d/-/e'
        assert url_join_safe('https://a.b/c', r'\\//d/../e' ) == 'https://a.b/c/-/d/-/e'
        assert url_join_safe('https://a.b/c', r'\\//\\d//e' ) == 'https://a.b/c/-/-d/e'
        assert url_join_safe('https://a.b/c', r'\\///d/../e') == 'https://a.b/c/-/d/-/e'
        assert url_join_safe('https://a.b/c', r'\\\///d/./e') == 'https://a.b/c/-/d/e'
        assert url_join_safe('https://a.b/c', r'\\\\\\d//e' ) == 'https://a.b/c/-d/e'
        assert url_join_safe('https://a.b/c', r'/////\d//e' ) == 'https://a.b/c/-d/e'
        assert url_join_safe('https://a.b/c', r'....//\d//e') == 'https://a.b/c/--/-d/e'

        # abuse cases (with ..)
        assert url_join_safe('https://a.b/c', 'd/.../e'    ) == 'https://a.b/c/d/-./e'
        assert url_join_safe('https://a.b/c', 'd/..../e'   ) == 'https://a.b/c/d/--/e'
        assert url_join_safe('https://a.b/c', 'd/././../e' ) == 'https://a.b/c/d/-/e'
        assert url_join_safe('https://a.b/c', 'd/../e..'   ) == 'https://a.b/c/d/-/e-'
        assert url_join_safe('https://a.b/c', 'd/../e../f' ) == 'https://a.b/c/d/-/e-/f'
        assert url_join_safe('https://a.b/c', 'd/../e.../f') == 'https://a.b/c/d/-/e-./f'
        assert url_join_safe('https://a.b/c', 'd/../e....f') == 'https://a.b/c/d/-/e--f'
        assert url_join_safe('https://a.b/c', 'd/../e...f' ) == 'https://a.b/c/d/-/e-.f'
        assert url_join_safe('https://a.b/c', 'd/./e..json') == 'https://a.b/c/d/e-json'
        assert url_join_safe('https://a.b/c', 'd/./e.json' ) == 'https://a.b/c/d/e.json'

        # abuse cases (with encodings)
        assert url_join_safe('https://a.b/c', '%2e%2ee.json'            ) == 'https://a.b/c/-e.json'
        assert url_join_safe('https://a.b/c', 'etc/passwd'              ) == 'https://a.b/c/etc/passwd'
        assert url_join_safe('https://a.b/c', '%2e%2e/%2e%2e/etc/passwd') == 'https://a.b/c/-/-/etc/passwd'
        assert url_join_safe('https://a.b/c', '<h1>/xss'                ) == 'https://a.b/c/-h1-/xss'
        assert url_join_safe('https://a.b/c', '<h1\'>/xss'              ) == 'https://a.b/c/-h1-/xss'
        assert url_join_safe('https://a.b/c', '<h1`>/xss'               ) == 'https://a.b/c/-h1-/xss'
        assert url_join_safe('https://a.b/c', '<h1">/xss'               ) == 'https://a.b/c/-h1-/xss'
        assert url_join_safe('https://a.b/c', '/\\\'"`d'                ) == 'https://a.b/c/-d'
        assert url_join_safe('https://a.b/c', '\x00\x0a'                ) == 'https://a.b/c/-'


        # abuse case (other variations)
        assert url_join_safe('https://a.b/c', "http://abc/b") == 'https://a.b/c/http-/abc/b'








