import json
import re
import socket
import ssl
import unicodedata
from http.cookies            import SimpleCookie
from time                    import sleep
from urllib.parse            import quote, urljoin, urlparse
from   urllib.request        import Request, urlopen
from osbot_utils.utils.Str   import html_decode
from osbot_utils.utils.Misc  import url_decode
from osbot_utils.utils.Files import save_bytes_as_file, file_create

URL_CHECK_HOST_ONLINE         = 'https://www.google.com'
URL_JOIN_SAFE__MAX_ITERATIONS = 5

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


def parse_cookies(cookie_header, include_empty=True):
    cookie = SimpleCookie()
    cookie.load(cookie_header)
    parsed_cookies = {}
    for key, morsel in cookie.items():
        cookie_attrs = {"value": morsel.value}
        for attr, value in morsel.items():
            if attr.lower() in ["secure", "httponly"]:
                cookie_attrs[attr] = (value == True)
            else:
                if value or include_empty:
                    cookie_attrs[attr] = value.strip(', ')      # we need to strip for the cases when there are multiple cookies split by , (as seen in FastAPI Test Client)
        parsed_cookies[key] = cookie_attrs

    return parsed_cookies


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

def POST_json_get_bytes(url=None, data=None):
    headers          = {'Content-Type': "application/json"}     # todo add support for providing custom headers
    kwargs = dict(url     = url   ,
                  data    = data,
                  headers = headers      ,
                  method  = 'POST'       ,
                  encoding = None
                  )
    response = http_request(**kwargs)
    return response

def PUT(url, data='', headers=None):
    return http_request(url, data, headers, 'PUT')

def PUT_json(*args, **kwargs):
    return json.loads(PUT(*args, **kwargs))

def url_join_safe(base_path, path=''):
    if not isinstance(base_path, str) or not isinstance(path, str):
        return None

    max_iterations   = URL_JOIN_SAFE__MAX_ITERATIONS

    path = unicodedata.normalize('NFC', path)
    path_normalised = path
    for _ in range(max_iterations):
        fixed_segments = []
        for segment in path_normalised.split('/'):
            segment_decoded = html_decode(url_decode(segment))
            fixed_segment = re.sub(r'[^a-zA-Z0-9\-_.]+', '-', segment_decoded)
            fixed_segment = fixed_segment.replace("..", "-")
            if fixed_segment:
                fixed_segments.append(fixed_segment)
        path_cleaned = '/'.join(fixed_segments)

        if path_cleaned == path_normalised:
            break
        path_normalised = path_cleaned
    else:
        return None                                                         # If we exit the loop without breaking, return None

    if not base_path.endswith('/'):                                          # Ensure that the base path ends with '/'
        base_path += '/'

    if path_normalised.startswith('/'):                                      # Remove leading '/' from path
        path_normalised = path_normalised[1:]

    path_quoted     = quote(path_normalised,  safe='/')                      # Quote the path to encode special characters
    joined_path     = urljoin(base_path, path_quoted)                        # Join the base path and normalized path
    parsed_base     = urlparse(base_path)                                    # Parse and verify the result
    parsed_joined   = urlparse(joined_path)

    if (parsed_joined.scheme == parsed_base.scheme and                       # Ensure the joined URL starts with the base URL to prevent open redirect vulnerabilities
            parsed_joined.netloc == parsed_base.netloc and
            joined_path.startswith(base_path)):
        if joined_path.endswith('/'):                                        # Remove trailing slash
            joined_path = joined_path[:-1]
        return joined_path

    return None