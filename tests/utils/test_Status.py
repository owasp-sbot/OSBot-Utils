import sys
import traceback
from io import StringIO
from unittest import TestCase

import pytest

from osbot_utils.utils.Files import file_name
from osbot_utils.utils.Functions import type_file
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_data
from osbot_utils.utils.Python_Logger import Python_Logger, Python_Logger_Config
from osbot_utils.utils.Status import osbot_logger, status_error, status_info, status_debug, status_critical, \
    status_warning, status_ok, log_critical, log_debug, log_error, log_info, log_ok, log_warning, osbot_status, Status, \
    log_exception, status_exception, send_status_to_logger


class test_Status(TestCase):
    osbot_status : Status

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info < (3, 8):
            pytest.skip("Skipping tests that don't work on 3.7 or lower")

        send_status_to_logger(True)
        assert osbot_logger.config.log_to_memory is False
        assert osbot_logger.add_memory_logger  () is True
        assert osbot_logger.config.log_to_memory is True
        assert type(osbot_status) is Status
        cls.osbot_status = osbot_status

    def tearDown(self) -> None:
        assert osbot_logger.memory_handler_clear() is True

    @classmethod
    def tearDownClass(cls) -> None:
        assert osbot_logger.memory_handler_logs() == []
        assert osbot_logger.remove_memory_logger() is True
        send_status_to_logger(False)

    def test__osbot_logger(self):
        assert type(osbot_logger        ) is Python_Logger
        assert type(osbot_logger.config ) is Python_Logger_Config
        assert osbot_logger.logger_name.startswith('Python_Logger__') is True
        assert obj_data(osbot_logger.config) == dict(elastic_host     = None  ,
                                                     elastic_password = None  ,
                                                     elastic_port     = None  ,
                                                     elastic_username = None  ,
                                                     log_format       = '%(asctime)s\\\\t|\\\\t%(name)s\\\\t|\\\\t%(levelname)s\\\\t|\\\\t%(message)s',
                                                     log_level        = 10    ,
                                                     log_to_console   = False ,
                                                     log_to_file      = False ,
                                                     log_to_memory    = True  ,
                                                     path_logs        = None  )

    def test__sending_different_types_of_status_messages(self):

        def send_status_message(message_type, target_method, expected_level= 10, expected_status=None):
            kwargs           = dict(message = f'an {message_type} message'    ,
                                    data    = {'an': message_type}            ,
                                    error   = Exception(f'an {message_type}'))
            result           = kwargs.copy()
            result['status'] = message_type

            assert osbot_logger.memory_handler_messages() == []
            assert target_method(**kwargs)                == result
            assert osbot_logger.memory_handler_messages() == [f'[osbot] [{message_type}] an {message_type} message']
            last_message = osbot_logger.memory_handler_logs().pop()
            assert osbot_logger.memory_handler_clear()    is True
            assert last_message.get('levelname')          == (expected_status or message_type.upper())
            #assert last_message.get('filename')           =='test_Status.py'
            #assert last_message.get('funcName')           =='send_status_message'
            assert last_message.get('levelno')            == expected_level


        # test status_* methods
        send_status_message(message_type='critical' , target_method=status_critical , expected_level=50)
        send_status_message(message_type='debug'    , target_method=status_debug    , expected_level=10)
        send_status_message(message_type='error'    , target_method=status_error    , expected_level=40)
        send_status_message(message_type='exception', target_method=status_exception, expected_level=40, expected_status='ERROR')
        send_status_message(message_type='info'     , target_method=status_info     , expected_level=20)
        send_status_message(message_type='ok'       , target_method=status_ok       , expected_level=20, expected_status='INFO')
        send_status_message(message_type='warning'  , target_method=status_warning  , expected_level=30)

        # test log_* methods

        send_status_message(message_type='critical', target_method=log_critical, expected_level=50)
        send_status_message(message_type='debug'   , target_method=log_debug   , expected_level=10)
        send_status_message(message_type='error'   , target_method=log_error   , expected_level=40)
        send_status_message(message_type='info'    , target_method=log_info    , expected_level=20)
        send_status_message(message_type='ok'      , target_method=log_ok      , expected_level=20, expected_status='INFO')
        send_status_message(message_type='warning' , target_method=log_warning , expected_level=30)


    def test__logging_exceptions(self):
        try:
            1 / 0
        except ZeroDivisionError:
            # This will log the exception message 'Division by zero' with the traceback
            log_exception()

        assert 'exc_text' in list_set(self.osbot_status.last_message())

                # == ['args', 'created', 'exc_info', 'exc_text',
                #                                               'filename', 'funcName', 'levelname', 'levelno', 'lineno',
                #                                               'message', 'module', 'msecs', 'msg', 'name', 'pathname',
                #                                               'process', 'processName', 'relativeCreated', 'stack_info',
                #                                               'taskName', 'thread', 'threadName'])

    def test_status_exception(self):

        kwargs          = dict(message = 'an exception message',
                               data    = {'an': 'exception'}       ,
                               error   = Exception('an exception'  ))
        result          = kwargs.copy()
        result['status'] = 'exception'
        assert osbot_logger.memory_handler_messages()   == []
        assert status_exception(**kwargs)               == result
        assert osbot_logger.memory_handler_messages()   == ['[osbot] [exception] an exception message']
        last_log_entry = osbot_logger.memory_handler_logs().pop()

        # note: asctime below is only showing when pytest_configure is set and configures config.option.log_format
        # assert list_set(last_log_entry) == ['args', 'created', 'exc_info', 'exc_text', 'filename', 'funcName',
        #                                     'levelname', 'levelno', 'lineno', 'message', 'module', 'msecs',
        #                                     'msg', 'name', 'pathname', 'process', 'processName', 'relativeCreated',
        #                                     'stack_info', 'taskName', 'thread', 'threadName']
        assert last_log_entry.get('args'         ) == ()
        assert last_log_entry.get('exc_info'     ) == (None, None, None)
        assert last_log_entry.get('exc_text'     ) == 'NoneType: None'
        if sys.version_info > (3, 11):
            assert last_log_entry.get('filename') == 'test_Status.py'
            assert last_log_entry.get('funcName') == 'test_status_exception'
            assert last_log_entry.get('module'  ) == 'test_Status'
        else:
            assert last_log_entry.get('filename') == 'Status.py'
            assert last_log_entry.get('funcName') == 'status_exception'
            assert last_log_entry.get('module'  ) == 'Status'
        assert last_log_entry.get('levelname'    ) == 'ERROR'
        assert last_log_entry.get('levelno'      ) == 40
        assert last_log_entry.get('lineno'       )  > 0
        assert last_log_entry.get('message'      ) == '[osbot] [exception] an exception message'

        assert last_log_entry.get('msg'          ) == '[osbot] [exception] an exception message'
        assert last_log_entry.get('name'         ) == osbot_logger.logger_name
        assert last_log_entry.get('processName'  ) == 'MainProcess'
        assert last_log_entry.get('stack_info'   ) is None
        assert last_log_entry.get('threadName'   ) == 'MainThread'
        #assert file_name(last_log_entry.get('pathname')) == file_name(type_file(test_Status))


    def test_stack_trace(self):
        def method_a():
            method_b()

        def method_b():
            print_stack_trace(depth=5)

        def print_stack_trace(depth=None):
            for entry in traceback.extract_stack(limit=depth):
                assert type(entry) == traceback.FrameSummary

        method_a()