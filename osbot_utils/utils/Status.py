import logging

# todo refactor into Status class
from osbot_utils.utils.Python_Logger import Python_Logger

osbot_logger = Python_Logger().setup() # logging.getLogger()

def status_message(status, message:str=None, data=None, error=None):
    return  {  'data'   : data    ,
               'error'  : error   ,
               'message': message ,
               'status' : status
            }

def status_error  (message:str='', data=None,error=None): osbot_logger.error  ('[osbot] [error] ' + str(message)); return status_message('error', message=message, data=data, error=error)
def status_debug  (message:str='', data=None,error=None): osbot_logger.debug  ('[osbot] [debug] ' + str(message)); return status_message('debug', message=message, data=data, error=error)
def status_fatal  (message:str='', data=None,error=None): osbot_logger.fatal  ('[osbot] [fatal] ' + str(message)); return status_message('fatal', message=message, data=data, error=error)
def status_info   (message:str='', data=None,error=None): osbot_logger.info   ('[osbot] [info]  ' + str(message)); return status_message('info', message=message, data=data, error=error)
def status_ok     (message:str='', data=None,error=None): osbot_logger.info   ('[osbot] [ok]    ' + str(message)); return status_message('ok', message=message, data=data, error=error)
def status_warning(message:str='', data=None,error=None): osbot_logger.warning('[osbot] [warning] ' + str(message)); return status_message('warning', message=message, data=data, error=error)

#todo: add logging hook that automatically picks up the caller (class and method) from the stack trace
#todo: add status_exception that automatically picks up the exception from the stack trace
