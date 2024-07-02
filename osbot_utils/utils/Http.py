import json
import socket
import ssl
from time import sleep
from   urllib.request import Request, urlopen

from osbot_utils.utils.Files import save_bytes_as_file, file_size, file_bytes, file_open_bytes, file_create
from osbot_utils.utils.Python_Logger import Python_Logger

URL_CHECK_HOST_ONLINE = 'https://www.google.com'

def current_host_offline(url_to_use=URL_CHECK_HOST_ONLINE):
    return current_host_online(url_to_use=url_to_use) is False

def current_host_online(url_to_use=URL_CHECK_HOST_ONLINE):
    try:
        http_request(url_to_use, method='HEAD')
        return True
    except:
        return False

def dns_ip_address(host):
    return socket.gethostbyname(host)

def is_url_online(target):
    try:
        http_request(target, method='HEAD')
        return True
    except:
        return False

def is_port_open(host, port, timeout=0.5):
    return port_is_open(host=host, port=port, timeout=timeout)

def port_is_open(port : int , host='0.0.0.0', timeout=1.0):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        return result == 0
    except:
        return False


def http_request(url, data=None, headers=None, method='GET', encoding ='utf-8', return_response_object=False):
    ssl_request = url.startswith('https://')
    headers = headers or {}
    if data:
        print()
        if type(data) is not str:                                   # if the data object is not a string
            if headers.get('Content-Type') == "application/json":   # and a json payload is expected
                data = json.dumps(data)                             # convert it to json
        if type(data) is str:                                       # only convert to bytes if current data is a string
            data = data.encode()
    request  = Request(url, data=data, headers=headers)
    request.get_method = lambda: method

    if ssl_request:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        response = urlopen(request, context=gcontext)
    else:
        response = urlopen(request)

    if return_response_object:
        return response
    else:
        result = response.read()
        if encoding:
            return result.decode(encoding)
        return result

def port_is_not_open(port, host='0.0.0.0', timeout=1.0):
    return port_is_open(port, host,timeout) is False

def wait_for_http(url, max_attempts=20, wait_for=0.1):
    for i in range(max_attempts):
        try:
            if GET(url):
                return True
        except:
            pass
        sleep(wait_for)
    return False

def wait_for_ssh(host, max_attempts=120, wait_for=0.5):
    return wait_for_port(host=host, port=22, max_attempts=max_attempts, wait_for=wait_for)

def wait_for_port(host, port, max_attempts=20, wait_for=0.1):
    for i in range(max_attempts):
        if is_port_open(host=host,port=port,timeout=wait_for):
            return True
        sleep(wait_for)
    return False

def wait_for_port_closed(host, port, max_attempts=20, wait_for=0.1):
    for i in range(max_attempts):
        if is_port_open(host=host,port=port,timeout=wait_for) is False:
            return True
        sleep(wait_for)
    return False

def DELETE(url, data=None, headers=None):
    return http_request(url, data, headers, 'DELETE')

def DELETE_json(*args, **kwargs):
    return json.loads(DELETE(*args, **kwargs))

def GET(url,headers = None, encoding='utf-8'):
    return http_request(url, headers=headers, method='GET', encoding=encoding)

def GET_to_file(url,path=None, headers = None, extension=None):
    contents = GET(url, headers)
    return file_create(path=path, contents=contents,extension=extension)

def GET_bytes(url, headers=None):
    return GET(url, headers=headers, encoding=None)

def GET_bytes_to_file(url,path=None, headers = None):
    file_bytes = GET_bytes(url, headers)
    return save_bytes_as_file(file_bytes, path)

def GET_json(*args, **kwargs):
    return json.loads(GET(*args, **kwargs))

def OPTIONS(url,headers = None):
    response = http_request(url, headers=headers, method='OPTIONS', return_response_object=True)
    response_headers  = {}
    for response_header in response.getheaders():
        (name,value) = response_header
        response_headers[name] = value
    return response_headers

def POST(url, data='', headers=None):
    return http_request(url, data, headers, 'POST')

def POST_json(*args, **kwargs):
    return json.loads(POST(*args, **kwargs))

def PUT(url, data='', headers=None):
    return http_request(url, data, headers, 'PUT')

def PUT_json(*args, **kwargs):
    return json.loads(PUT(*args, **kwargs))
