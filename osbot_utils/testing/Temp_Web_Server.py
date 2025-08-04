from contextlib                 import contextmanager
from functools                  import partial
from http.server                import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading                  import Thread
from urllib.parse               import urljoin
from osbot_utils.utils.Files    import file_create, path_combine, temp_filename, file_create_all_parent_folders
from osbot_utils.utils.Misc     import random_port, random_string
from osbot_utils.utils.Http     import port_is_open, GET


class Temp_Web_Server:
    server        : ThreadingHTTPServer
    server_thread : Thread

    def __init__(self, host: str = None, port: int = None, root_folder: str = None, server_name = None, http_handler = None, wait_for_stop=False):
        self.host          = host         or "127.0.0.1"
        self.port          = port         or random_port()
        self.root_folder   = root_folder  or "."
        self.server_name   = server_name  or "Temp_Web_Server"
        self.http_handler  = http_handler or SimpleHTTPRequestHandler
        self.wait_for_stop = wait_for_stop

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def add_file(self, relative_file_path=None, file_contents=None):
        if relative_file_path is None:
            relative_file_path = temp_filename()
        if file_contents is None:
            file_contents = random_string()
        full_path = path_combine(self.root_folder, relative_file_path)      # todo: fix the path transversal vulnerability that exists in this function #security
        file_create_all_parent_folders(full_path)
        file_create(path=full_path, contents=file_contents)
        return full_path

    def GET(self, path=''):
        url = self.url(path)
        try:
            return GET(url)
        except Exception as error:
            print(error)                    # todo: add support for using logging
            return None

    def GET_contains(self, content, path=''):
        page_html = self.GET(path=path)
        if type(content) is list:
            for item in content:
                if item not in page_html:
                    return False
            return True
        return content in page_html

    def server_port_open(self):
        return port_is_open(host=self.host, port=self.port)

    def stop(self):
        self.server.server_close()
        if self.wait_for_stop:
            self.server.shutdown()
            self.server_thread.join()
        else:
            self.server._BaseServer__shutdown_request = True  # simulate what happens inside self.server.shutdown()
        return self

    def start(self):
        if self.http_handler is  SimpleHTTPRequestHandler:
            handler_config = partial(self.http_handler, directory=self.root_folder)
        else:
            handler_config = partial(self.http_handler)
        self.server        = ThreadingHTTPServer((self.host, self.port), handler_config)
        self.server_thread = Thread(target=self.server.serve_forever, name=self.server_name)
        self.server_thread.start()
        return self

    def url(self,path=''):
        base_url = f"http://{self.host}:{self.port}"
        url      = urljoin(base_url, path)
        return url