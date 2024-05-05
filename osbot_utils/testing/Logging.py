import inspect
import logging
from io import StringIO

import sys

from osbot_utils.decorators.methods.cache_on_self import cache_on_self

DEFAULT_LOG_FORMAT = '%(levelname)s - %(message)s'
DEFAULT_LOG_LEVEL  = logging.DEBUG

class Logging:

    def __init__(self, target=None, log_level: int = None, log_format=None, log_to_console=False):
        self.target     = target
        self.log_level  = log_level  or DEFAULT_LOG_LEVEL
        self.log_format = log_format or DEFAULT_LOG_FORMAT
        if log_to_console:
            self.log_to_sys_stdout()

    def __enter__(self): return self
    def __exit__ (self, exc_type, exc_val, exc_tb): pass

    def add_stream_handler(self, stream):
        stream_handler = logging.StreamHandler(stream=stream)
        self.logger().addHandler(stream_handler)
        self.set_logger_level()
        self.set_format(stream_handler)

        return stream_handler

    @cache_on_self
    def logger(self):
        if self.target is not None:
            if inspect.isclass(self.target) or inspect.ismodule(self.target):
                self.target = self.target.__name__
        return logging.getLogger(self.target)

    def enable_pycharm_logging(self):
        if self.is_pycharm_running():
            self.log_to_sys_stdout()
        return self

    def is_pycharm_running(self) -> bool:
        first_arg = sys.argv[0]
        return ('docrunner.py' in first_arg) or ('pytest_runner.py' in first_arg)

    def log_to_sys_stdout(self):
        return self.add_stream_handler(sys.stdout)

    def log_to_string_io(self):
        log_stream = StringIO()
        return self.add_stream_handler(log_stream)


    def set_format(self, stream_handler):
        formatter = logging.Formatter(self.log_format)
        stream_handler.setFormatter(formatter)
        return formatter

    def set_logger_level(self):
        self.logger().setLevel(self.log_level)


    def info    (self,message, *args, **kwargs): self.logger().info     (message, *args, **kwargs)
    def warning (self,message, *args, **kwargs): self.logger().warning  (message, *args, **kwargs)
    def debug   (self,message, *args, **kwargs): self.logger().debug    (message, *args, **kwargs)
    def error   (self,message, *args, **kwargs): self.logger().error    (message, *args, **kwargs)
    def critical(self,message, *args, **kwargs): self.logger().critical (message, *args, **kwargs)