from pprint import pprint
from unittest import TestCase

from osbot_utils.utils import Http

from osbot_utils.utils.Files import temp_file, file_not_exists, file_exists, file_bytes, file_size, file_create_bytes
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

class test_Http(TestCase):

    def setUp(self) -> None:
        self.headers      = {"Accept": "application/json"}
        self.data         = "aaa=42&bbb=123"
        self.data_json    = { "aaa":42 , "bbb":"123"}
        self.url_png      = 'https://avatars.githubusercontent.com/u/52993993?s=200&v=4'
        self.url_template = "https://httpbin.org/{method}?ddd=1&eee=2"

    def test_current_host_online(self):
        assert current_host_online() is True
        assert current_host_online(url_to_use='http://111-2222-3333-abc.com') is False

    def test_wait_for_port(self):
        assert wait_for_port('www.google.com', 443                ) is True
        assert wait_for_port('bad-ip'        , 443, max_attempts=2) is False

    def test_DELETE_json(self):
        url = self.url_template.format(method="delete")
        response = DELETE_json(url, headers=self.headers, data=self.data)
        assert response["form"] ==  { "aaa": "42",  "bbb": "123" }

    def test_GET_bytes(self):
        bytes = GET_bytes(self.url_png)
        assert len(bytes) == 17575
        assert bytes[:4] == b"\x89PNG"

    def test_GET_bytes_to_file(self):
        target = temp_file(extension="png")
        assert file_not_exists(target)
        assert GET_bytes_to_file(self.url_png, target)
        assert file_exists(target)
        assert file_size(target) == 17575
        assert file_bytes(target)[:4] == b"\x89PNG"

    def test_GET_json(self):
        url = self.url_template.format(method="get")
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