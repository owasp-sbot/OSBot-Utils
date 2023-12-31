import logging
import sys
from logging          import Logger, StreamHandler, FileHandler
from logging.handlers import MemoryHandler

from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_function import cache_on_function
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Misc import random_string
from osbot_utils.utils.Files import temp_file
from osbot_utils.utils.Objects import obj_dict

DEFAULT_LOG_LEVEL         = logging.DEBUG
DEFAULT_LOG_FORMAT        = '%(asctime)s\t|\t%(name)s\t|\t%(levelname)s\t|\t%(message)s'
MEMORY_LOGGER_CAPACITY    = 1024*10
MEMORY_LOGGER_FLUSH_LEVEL = logging.ERROR

class Python_Logger_Config:
    def __init__(self):
        self.elastic_host           = None
        self.elastic_password       = None
        self.elastic_port           = None
        self.elastic_username       = None
        #self.log_to_aws_s3          = False                     # todo
        #self.log_to_aws_cloud_trail = False                     # todo
        #self.log_to_aws_firehose    = False                     # todo
        self.log_to_console         = False                     # todo
        self.log_to_file            = False                     # todo
        #self.log_to_elastic         = False                     # todo
        self.log_to_memory          = False
        self.path_logs              = None
        self.log_format             = DEFAULT_LOG_FORMAT
        self.log_level              = DEFAULT_LOG_LEVEL


class Python_Logger:
    config : Python_Logger_Config
    logger : Logger
    def __init__(self, logger_name= None, logger_config : Python_Logger_Config = None):
        self.logger_name = logger_name or random_string(prefix="Python_Logger_")
        self.set_config(logger_config)

    def manager_get_loggers(self):
        return Logger.manager.loggerDict

    def manager_remove_logger(self):
        logger_dict = Logger.manager.loggerDict
        if self.logger_name in logger_dict:                 # need to do it manually here since Logger.manager doesn't seem to have a way to remove loggers
            del logger_dict[self.logger_name]
            return True
        return False

    def setup(self):
        self.logger =  logging.getLogger(self.logger_name)
        self.setup_log_methods(self)
        self.set_log_level()
        self.add_handler_memory()
        return self

    def setup_log_methods(self, target):
        # adds these helper methods like this so that the filename and function values are accurate
        setattr(target, "debug"     , self.logger.debug     )
        setattr(target, "info"      , self.logger.info      )
        setattr(target, "warning"   , self.logger.warning   )
        setattr(target, "error"     , self.logger.error     )
        setattr(target, "exception" , self.logger.exception )
        setattr(target, "critical"  , self.logger.critical  )

        # self.info       = self.logger.info
        # self.warning    = self.logger.warning
        # self.error      = self.logger.error
        # self.exception  = self.logger.exception
        # self.critical   = self.logger.critical


    # Setters
    def set_config(self, config):
        if type(config) is Python_Logger_Config:
            self.config = config
        else:
            self.config = Python_Logger_Config()
        return self.config

    def set_log_format(self, format):
        if format:
            self.config.log_format = format

    def set_log_level(self, level=None):
        level = level or self.config.log_level
        if self.logger:
            self.logger.setLevel(level)
            return True
        return False

    # Getters
    def log_handlers(self):
        if self.logger:
            return self.logger.handlers
        return []

    def log_handler(self, handler_type):
        for handler in self.log_handlers():
            if type(handler) is handler_type:
                return handler
        return None

    def log_handler_console(self):
        return self.log_handler(StreamHandler)

    def log_handler_file(self):
        return self.log_handler(logging.FileHandler)

    def log_handler_memory(self):
        return self.log_handler(MemoryHandler)

    def log_formatter(self):
        return logging.Formatter(self.config.log_format)

    def log_level(self):
        return self.config.log_level

    # Actions

    def add_console_logger(self):
        self.config.log_to_console = True
        return self.add_handler_console()

    def add_memory_logger(self):
        self.config.log_to_memory = True
        return self.add_handler_memory()

    def add_file_logger(self,path_log_file=None):
        self.config.log_to_file = True
        return self.add_handler_file(path_log_file=path_log_file)

    # Handlers
    def add_handler_console(self):
        if self.logger and self.config.log_to_console:
            handler = StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(self.log_formatter())
            self.logger.addHandler(handler)
            return True
        return False

    def add_handler_file(self, path_log_file=None):
        if self.logger and self.config.log_to_file:
            if path_log_file is None:
                path_log_file = temp_file(extension='.log')
            handler = FileHandler(path_log_file)
            handler.setLevel(self.log_level())
            handler.setFormatter(self.log_formatter())
            self.logger.addHandler(handler)
            return True
        return False

    def add_handler_memory(self):
        if self.logger and self.config.log_to_memory:
            capacity       = MEMORY_LOGGER_CAPACITY
            flush_level    = MEMORY_LOGGER_FLUSH_LEVEL
            target         = None                       # we want the messages to only be kept in memory
            memory_handler = MemoryHandler(capacity=capacity, flushLevel=flush_level, target=target,flushOnClose=True)
            memory_handler.setLevel(self.log_level())
            self.logger.addHandler(memory_handler)
            return True
        return False

    # Utils
    def memory_handler_exceptions(self):
        return self.memory_handler_logs(index_by='levelname').get('EXCEPTIONS', {})

    @index_by
    @group_by
    def memory_handler_logs(self):
        logs           = []
        memory_handler = self.log_handler_memory()
        if memory_handler:
            for log_record in memory_handler.buffer:
                logs.append(obj_dict(log_record))
        return logs

    def memory_handler_messages(self):
        return [log_entry.get('message') for log_entry in self.memory_handler_logs()]

    # Logging methods

    # def debug    (self, msg='', *args, **kwargs): return self._log('debug'     , msg, *args, **kwargs)
    # #def info     (self, msg='', *args, **kwargs): return self.__log__('info'      , msg, *args, **kwargs)
    # def warning  (self, msg='', *args, **kwargs): return self._log('warning'   , msg, *args, **kwargs)
    # def error    (self, msg='', *args, **kwargs): return self._log('error'     , msg, *args, **kwargs)
    # def exception(self, msg='', *args, **kwargs): return self._log('exception' , msg, *args, **kwargs)
    # def critical (self, msg='', *args, **kwargs): return self._log('critical'  , msg, *args, **kwargs)
    #
    # def __log__(self, level, msg, *args, **kwargs):
    #     if self.logger:
    #         log_method = getattr(self.logger, level)
    #         log_method(msg, *args, **kwargs)
    #         return True
    #     return False

@cache_on_function
def logger_info():
    python_logger = Python_Logger().setup()
    return python_logger.logger.info

@cache_on_function
def logger_error():
    python_logger = Python_Logger().setup()
    return python_logger.logger.error