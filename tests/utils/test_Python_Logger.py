import logging
import sys
from _thread import RLock
from datetime import datetime
from io import TextIOWrapper, StringIO
from logging import Logger, LogRecord
from logging.handlers import MemoryHandler
from unittest import TestCase
from unittest.mock import patch

import pytest

from osbot_utils.utils.Files import file_lines, file_exists, file_contents, file_delete
from osbot_utils.utils.Lists import list_set_dict
from osbot_utils.utils.Objects import obj_dict, obj_items
from osbot_utils.utils.Python_Logger import Python_Logger, Python_Logger_Config, DEFAULT_LOG_LEVEL, \
    MEMORY_LOGGER_CAPACITY, MEMORY_LOGGER_FLUSH_LEVEL
from osbot_utils.utils.Misc import list_set, size


class test_Python_Logger_Config(TestCase):
    def setUp(self):
        self.config = Python_Logger_Config()

    def test__init__(self):
        assert obj_dict(self.config) == {'elastic_host'     : None  ,
                                         'elastic_password' : None  ,
                                         'elastic_port'     : None  ,
                                         'elastic_username' : None  ,
                                         'log_level'        : 10    ,
                                         'log_format'       : '%(asctime)s\t|\t%(name)s\t|\t%(levelname)s\t|\t%(message)s',
                                         'log_to_console'   : False ,
                                         'log_to_file'      : False ,
                                         'log_to_memory'    : False ,
                                         'path_logs'        : None  }


class test_Python_Logger(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info < (3, 11):
            pytest.skip("Skipping test that does't work on 3.11 or lower")

    def setUp(self):
        self.logger = Python_Logger().setup()
        self.logger.set_log_level(logging.DEBUG)

    def tearDown(self) -> None:
        self.logger.manager_remove_logger()

    def test__init__(self):
        assert obj_items(self.logger.config) == obj_items(Python_Logger_Config())
        assert self.logger.logger            is not None

    def test_set_logger_name(self):
        assert self.logger.logger_name                             == 'Python_Logger__test_Python_Logger'
        assert self.logger.set_logger_name('new_name').logger_name == 'new_name'

    # Helpers and Setup methods

    def test_manager_get_loggers(self):
        loggers = list_set(self.logger.manager_get_loggers())
        assert len(loggers) > 4
        assert self.logger.logger_name  in loggers
        assert 'Python_Logger__Status'  in loggers
        #assert 'Python_Logger__Mermaid' in loggers

    def test_setup(self):                           # setup is called as part of the Unit Tests setUp() with default values
        config = self.logger.config
        logger = self.logger.logger

        assert type(logger)         == Logger
        assert logger.disabled      == False
        assert logger.filters       == []
        assert logger.level         == config.log_level
        assert logger.propagate     == True
        assert logger.handlers      == []
        assert logger.name.startswith("Python_Logger") is True

    # Logging methods



    @patch('sys.stdout', new_callable=StringIO)
    def test_add_console_logger(self, sys_stdout):
        assert self.logger.add_console_logger() is True
        console_handler = self.logger.log_handler_console()
        obj_data = obj_dict(console_handler)
        assert obj_data == {  '_closed'     : False                     ,
                              '_name'       : None                      ,
                              'filters'     : []                        ,
                              'formatter'   : obj_data.get('formatter') ,
                              'level'       : DEFAULT_LOG_LEVEL         ,
                              'lock'        : obj_data.get('lock')      ,
                              'stream'      : obj_data.get('stream')    }

        debug_message = 'an debug message'
        self.logger.debug(debug_message)
        log_entry = sys_stdout.getvalue().split('\t|\t')
        assert len(log_entry) == 4
        assert str(datetime.now().minute) in log_entry[0]
        assert self.logger.logger_name    == log_entry[1]
        assert 'DEBUG'                    == log_entry[2]
        assert f'{debug_message}\n'       == log_entry[3]

    def test_add_file_logger(self):
        if sys.version_info > (3, 12):
            pytest.skip("Skipping test that doesn't work on 3.13 or higher")

        assert self.logger.add_file_logger() is True
        file_handler = self.logger.log_handler_file()
        log_file     = file_handler.baseFilename
        obj_data     = obj_dict(file_handler)
        del obj_data['_builtin_open']
        assert obj_data== { '_closed'       : False                       ,
                            '_name'         : None                        ,
                            'baseFilename'  : obj_data.get('baseFilename'),
                            'delay'         : False                       ,
                            'encoding'      : 'locale'                    ,
                            'errors'        : None                        ,
                            'filters'       : []                          ,
                            'formatter'     : obj_data.get('formatter')   ,
                            'level'         : DEFAULT_LOG_LEVEL           ,
                            'lock'          : obj_data.get('lock')        ,
                            'mode'          : 'a'                         ,
                            'stream'        : obj_data.get('stream')      }

        assert file_exists(log_file)   is True
        assert file_contents(log_file) == ''
        assert type(obj_data.get('stream')) == TextIOWrapper


        info_message = 'an info  message'
        self.logger.info(info_message)

        log_message_items = file_contents(log_file).split('\t|\t')
        assert len(log_message_items) == 4
        assert datetime.now().strftime('%Y-%m-%d %H:%M:%S') in log_message_items[0]
        assert self.logger.logger_name                      == log_message_items[1]
        assert 'INFO'                                       == log_message_items[2]
        assert f'{info_message}\n'                          == log_message_items[3]

        self.logger.info('an debug  message')
        log_lines = list(file_lines(log_file))
        assert len(log_lines) == 2
        assert 'an debug  message\n' in log_lines.pop()
        assert file_delete(log_file)


    def test_add_memory_logger(self):
        mem_handler : MemoryHandler
        assert self.logger.config.log_to_memory is False
        assert self.logger.add_handler_memory() is False
        assert self.logger.add_memory_logger     () is True

        mem_handler = self.logger.log_handler(MemoryHandler)

        assert size(self.logger.log_handlers()) == 1
        assert mem_handler                      is not None
        obj_data = obj_dict(mem_handler)
        assert type(obj_data['lock'])   is RLock

        assert obj_data == {  '_closed'     : False                     ,
                              '_name'       : None                      ,
                              'buffer'      : []                        ,
                              'capacity'    : MEMORY_LOGGER_CAPACITY    ,
                              'filters'     : []                        ,
                              'flushLevel'  : MEMORY_LOGGER_FLUSH_LEVEL ,
                              'flushOnClose': True                      ,
                              'formatter'   : None                      ,
                              'level'       : DEFAULT_LOG_LEVEL         ,
                              'lock'        : obj_data['lock'  ]        ,
                              'target'      : None       }

        assert mem_handler.buffer == []
        self.logger.info('an info message')
        assert size(mem_handler.buffer ) == 1
        log_record = mem_handler.buffer.pop()
        assert type(log_record) is LogRecord

        # note: asctime below is only showing when pytest_configure is set and configures config.option.log_format
        assert 'args' in list_set_dict(log_record)
                # == [ 'args', 'created', 'exc_info', 'exc_text', 'filename',
                #                               'funcName', 'levelname', 'levelno', 'lineno', 'message',
                #                               'module', 'msecs', 'msg', 'name', 'pathname', 'process',
                #                               'processName', 'relativeCreated', 'stack_info', 'taskName', 'thread', 'threadName'])

        assert log_record.message == 'an info message'

    def test_memory_handler_messages(self):
        test_message = 'an debug message'
        from http import cookiejar
        http_cookiejar_logger = Python_Logger(logger_name='http.cookiejar').setup()
        http_cookiejar_logger.add_memory_logger()
        cookiejar.debug = True
        cookiejar._debug(test_message)
        assert http_cookiejar_logger.memory_handler_messages() == [test_message]

        # test below is a good example of grabing the logger from urllib3, but it takes took long (since it makes a full http request and requests requests api)
        # import requests
        # urllib3_logger = Python_Logger(logger_name='urllib3').setup()           # get urllib3 logger
        # urllib3_logger.add_memory_logger()                                      # add a memory logger
        # requests.get('https://www.google.com/aaa')                              # make a request to Google which uses urllib3
        # assert urllib3_logger.memory_handler_messages() == ['Starting new HTTPS connection (1): www.google.com:443',
        #                                                     'https://www.google.com:443 "GET /aaa HTTP/1.1" 404 1564']

    def test_debug__info__warning__error__critical(self):

        self.logger.add_memory_logger()
        assert self.logger.debug     == self.logger.logger.debug
        assert self.logger.info      == self.logger.logger.info
        assert self.logger.warning   == self.logger.logger.warning
        assert self.logger.error     == self.logger.logger.error
        assert self.logger.critical  == self.logger.logger.critical
        assert self.logger.exception == self.logger.logger.exception
        
        assert self.logger.debug   ('debug message'    ) is None
        assert self.logger.info    ('info message'     ) is None
        assert self.logger.warning ('warning message'  ) is None
        assert self.logger.error   ('error message'    ) is None
        assert self.logger.critical('critical message' ) is None

        assert self.logger.memory_handler_messages() == [ 'debug message' , 'info message'    , 'warning message' , 'error message'   , 'critical message']
        log_messages = self.logger.memory_handler_logs(group_by='levelname')

        assert list_set(log_messages) == ['CRITICAL', 'DEBUG', 'ERROR', 'INFO', 'WARNING']
        critical_logs = log_messages.get('CRITICAL')
        debug_logs    = log_messages.get('DEBUG')
        error_logs    = log_messages.get('ERROR')
        info_logs     = log_messages.get('INFO')
        warning_logs  = log_messages.get('WARNING')

        def assert_log(log_entries, levelname, levelno, message):
            assert size(log_entries) == 1
            log_entry = log_entries.pop()
            assert log_entry.get('levelname') == levelname
            assert log_entry.get('levelno'  ) == levelno
            assert log_entry.get('message'  ) == message
            # note: asctime below is only showing when pytest_configure is set and configures config.option.log_format
            assert 'args' in list_set(log_entry)
            #assert list_set(log_entry) == [ 'args', 'created',  'exc_info',  'exc_text',  'filename',  'funcName',  'levelname',  'levelno',  'lineno',  'message',  'module',  'msecs',  'msg',  'name',  'pathname',  'process',  'processName',  'relativeCreated',  'stack_info',  'taskName', 'thread',  'threadName' ]

        assert_log(critical_logs, 'CRITICAL', 50, 'critical message')
        assert_log(debug_logs   , 'DEBUG'   , 10, 'debug message'   )
        assert_log(error_logs   , 'ERROR'   , 40, 'error message'   )
        assert_log(info_logs    , 'INFO'    , 20, 'info message'    )
        assert_log(warning_logs , 'WARNING' , 30, 'warning message' )

    def test_exception(self):
        self.logger.add_memory_logger()
        assert self.logger.memory_handler_exceptions() == {}
        self.logger.exception('')                                     # log with no params outside an exception
        log_exception = self.logger.memory_handler_logs().pop()
        assert log_exception.get('exc_info' ) == (None, None, None)
        assert log_exception.get('exc_text' ) == 'NoneType: None'
        assert log_exception.get('levelname') =='ERROR'
        assert log_exception.get('message'  ) == ''
        try:
            40 / 0
        except Exception as error:
            self.logger.logger.exception(error)

        log_exception = self.logger.memory_handler_logs().pop()

        assert str(log_exception.get('exc_info')[0]) == "<class 'ZeroDivisionError'>"
        assert 'ZeroDivisionError: division by zero' in log_exception.get('exc_text')
        assert log_exception.get('message') == 'division by zero'