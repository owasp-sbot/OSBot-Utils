import inspect
import logging
import sys
import types
from logging                                                import Logger, StreamHandler, FileHandler
from logging.handlers                                       import MemoryHandler
from osbot_utils.decorators.lists.group_by                  import group_by
from osbot_utils.decorators.lists.index_by                  import index_by
from osbot_utils.decorators.methods.cache_on_function       import cache_on_function
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.utils.Misc                                 import random_string
from osbot_utils.utils.Files                                import temp_file
from osbot_utils.utils.Objects                              import obj_dict

#DEFAULT_LOG_FORMAT  = '%(asctime)s.%(msecs)03d %(levelname)s - %(message)s'

DEFAULT_LOG_LEVEL         = logging.DEBUG
DEFAULT_LOG_FORMAT        = '%(asctime)s\t|\t%(name)s\t|\t%(levelname)s\t|\t%(message)s'
DEFAULT_LOG_DATE_FORMAT   = '%M:%S'
MEMORY_LOGGER_CAPACITY    = 1024*10
MEMORY_LOGGER_FLUSH_LEVEL = logging.ERROR

# for reference here are the log levels
# CRITICAL    50
# ERROR       40
# WARNING     30
# INFO        20
# DEBUG       10
# NOTSET      0

class Python_Logger_Config:

    def __init__(self):
        # self.elastic_host           = None                     # this needs to be implemented in OSBot_Elastic
        # self.elastic_password       = None
        # self.elastic_port           = None
        # self.elastic_username       = None
        #self.log_to_aws_s3          = False                     # todo
        #self.log_to_aws_cloud_trail = False                     # todo
        #self.log_to_aws_firehose    = False                     # todo
        self.log_to_console         = False                     # todo
        self.log_to_file            = False                     # todo
        #self.log_to_elastic         = False                     # todo
        self.log_to_memory          = False
        self.path_logs              = None
        self.log_format             = DEFAULT_LOG_FORMAT
        self.log_date_format        = DEFAULT_LOG_DATE_FORMAT
        self.log_level              = DEFAULT_LOG_LEVEL


class Python_Logger(Type_Safe):
    config      : Python_Logger_Config
    logger      : Logger
    logger_name : str

    critical    : types.MethodType        # these will be replaced by Python_Logger_Config.setup_log_methods
    debug       : types.MethodType
    error       : types.MethodType
    exception   : types.MethodType
    info        : types.MethodType
    ok          : types.MethodType
    warning     : types.MethodType

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_logger_name(self.logger_name)
        self.set_config     (self.config     )
        self.setup()                            # todo: understand side effect of setting up logger on __init__

    def disable(self):
        self.logger.disabled = True
        return self

    def set_logger_name(self, logger_name):
        if logger_name:                                     # if the value is provided, use it
            self.logger_name = logger_name
            return self
        for frame_info in inspect.stack():                  # Look for the first frame that is outside this Python_Logger class
            if 'self' in frame_info.frame.f_locals:
                caller_self = frame_info.frame.f_locals['self']
                caller_module = caller_self.__class__.__name__
                if caller_module != 'Python_Logger':
                    self.logger_name = 'Python_Logger__' + caller_module
                    return self

        self.logger_name = random_string(prefix="Python_Logger_")
        return self

    def manager_get_loggers(self):
        return Logger.manager.loggerDict

    def manager_remove_logger(self):
        logger_dict = Logger.manager.loggerDict
        if self.logger_name in logger_dict:                 # need to do it manually here since Logger.manager doesn't seem to have a way to remove loggers
            del logger_dict[self.logger_name]
            return True
        return False

    def setup(self, logger_name=None, log_level=None,add_console_logger=False, add_memory_logger=True):
        if logger_name:
            self.logger_name = logger_name
        if self.logger is None:
            self.logger =  logging.getLogger(self.logger_name)
        self.setup_log_methods()
        self.set_log_level(log_level)
        if add_console_logger:
            self.add_console_logger()
        if add_memory_logger:
            self.add_handler_memory()
        return self

    def setup_log_methods(self):
        # adds these helper methods like this so that the filename and function values are accurate
        setattr(self, "critical"  , self.logger.critical  )
        setattr(self, "debug"     , self.logger.debug     )
        setattr(self, "error"     , self.logger.error     )
        setattr(self, "exception" , self.logger.exception )
        setattr(self, "info"      , self.logger.info      )
        setattr(self, "ok"        , self.logger.info      )
        setattr(self, "warning"   , self.logger.warning   )





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

    def set_log_format(self, log_format=None, date_format=None):
        if log_format:
            self.config.log_format = log_format
        if date_format:
            self.config.log_date_format = date_format

    def set_log_level(self, level=None):
        level = level or self.config.log_level
        if self.logger:
            self.logger.setLevel(level)
            return True
        return False

    # Getters

    def log_handler(self, handler_type):
        for handler in self.log_handlers():
            if type(handler) is handler_type:
                return handler
        return None

    def log_handler_console(self):
        return self.log_handler(StreamHandler)

    def log_handler_file(self):
        return self.log_handler(logging.FileHandler)

    def log_handler_memory(self):                                                   # todo: change how this memory logger works (see notes in the other memory logger methods in Python_Logger
        return self.log_handler(MemoryHandler)

    def log_handlers(self):
        if self.logger:
            return self.logger.handlers
        return []

    def log_handlers_remove(self, handler):
        if handler and handler in self.log_handlers():
            self.logger.removeHandler(handler)
            return True
        return False

    def log_handlers_remove_type(self, handler_type):
        handler = self.log_handler(handler_type)
        return self.log_handlers_remove(handler)

    def log_formatter(self):
        return logging.Formatter(fmt=self.config.log_format, datefmt=self.config.log_date_format)

    def log_level(self):
        return self.config.log_level

    # Actions

    def add_console_logger(self):
        self.config.log_to_console = True
        return self.add_handler_console()

    def add_memory_logger(self):                                        # todo: figure out the exact workflow of this, since this memory logger is not tied to the current instance of Python_Logger (it's a global logger)
        self.config.log_to_memory = True
        return self.add_handler_memory()

    def add_file_logger(self,path_log_file=None):
        self.config.log_to_file = True
        return self.add_handler_file(path_log_file=path_log_file)

    def remove_memory_logger(self):                                     # todo: improve this workflow since this operating at the global loggers level, which means that this will get the first one, not the one from this python_Logger
        memory_logger = self.log_handler_memory()
        if self.log_handlers_remove(memory_logger):
            self.config.log_to_file = False
            return True
        return False


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

    def add_handler_memory(self, memory_capacity=None):
        if self.log_handler_memory() is None:
            if self.logger and self.config.log_to_memory:
                capacity       = memory_capacity or MEMORY_LOGGER_CAPACITY
                flush_level    = MEMORY_LOGGER_FLUSH_LEVEL
                target         = None                       # we want the messages to only be kept in memory
                memory_handler = MemoryHandler(capacity=capacity, flushLevel=flush_level, target=target,flushOnClose=True)
                memory_handler.setLevel(self.log_level())
                self.logger.addHandler(memory_handler)
                return memory_handler

    # Utils

    def memory_handler(self) -> MemoryHandler:
        return self.log_handler_memory()

    def memory_handler_buffer(self):
        if self.config.log_to_memory:
            memory_handler = self.memory_handler()
            if memory_handler:
                return memory_handler.buffer
        return []

    def memory_handler_clear(self):
        if self.config.log_to_memory:
            memory_handler = self.memory_handler()
            memory_handler.buffer = []
            return True
        return False

    def memory_handler_exceptions(self):
        return self.memory_handler_logs(index_by='levelname').get('EXCEPTIONS', {})

    @index_by
    @group_by
    def memory_handler_logs(self):
        logs = []
        for log_record in self.memory_handler_buffer():
            logs.append(obj_dict(log_record))
        return logs

    def memory_handler_last_log_entry(self):
        memory_buffer = self.memory_handler_buffer()
        if memory_buffer:                               # Check if the buffer is not empty
            last_log_record = memory_buffer[-1]         # get the last record
            return obj_dict(last_log_record)            # convert record into a nice json object
        return {}

    def memory_handler_messages(self):
        messages = []
        for log_entry in self.memory_handler_logs():
            message = log_entry.get('message')  or log_entry.get('msg') or '(log message not found in log entry)' # todo: figure out the scenarios that lead to a value in 'msg' or in 'message'
            messages.append(message)
        return messages

    # Root logger
    def root_logger__clear_handlers(self):              # useful in some debugging sessinon
        logging.root.handlers.clear()
        return self
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