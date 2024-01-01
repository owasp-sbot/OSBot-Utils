# todo refactor into Status class
from osbot_utils.utils.Python_Logger import Python_Logger

class Status:
    def __init__(self):
        self.logger = Python_Logger().setup()
        #self.logger.add_memory_logger()

    def status_message(self, status, message:str=None, data=None, error=None):
        return  {  'data'   : data    ,
                   'error'  : error   ,
                   'message': message ,
                   'status' : status
                }

    # def debug  (self, message:str='', data=None, error=None, stacklevel=3):                                 # stacklevel is usually 3 because we want to get the caller of the method that called this one
    #     self.logger.debug('[osbot] [debug] ' + str(message), exc_info=True, stacklevel=stacklevel)
    #     return self.status_message('debug', message=message, data=data, error=error)
    #
    # def error  (self, message:str='', data=None, error=None):
    #     self.logger.error('[osbot] [error] ' + str(message), exc_info=True)
    #     return self.status_message('error', message=message, data=data, error=error)
    #
    # def critical (self, message:str='', data=None, error=None):
    #     #self.logger.critical('[osbot] [critical] ' + str(message), exc_info=True)
    #     logger_method = self.logger.__getattribute__('critical')
    #     logger_method('[osbot] [critical] ' + str(message), exc_info=True)
    #     return self.status_message('critical', message=message, data=data, error=error)

    def log_message(self, status, message:str='', data=None, error=None, stacklevel=3):          # stacklevel is usually 3 because we want to get the caller of the method that called this on
        logger_message = f'[osbot] [{status}] ' + str(message)
        logger_method  = self.logger.__getattribute__(status)
        status_message = self.status_message(status=status, message=message, data=data, error=error)
        logger_method(logger_message, exc_info=True, stacklevel=stacklevel)
        return status_message



osbot_status = Status()
osbot_logger = osbot_status.logger

def status_critical(message:str='', data=None,error=None): return osbot_status.log_message(status='critical', message=message, data=data, error=error)
def status_debug   (message:str='', data=None,error=None): return osbot_status.log_message(status='debug'   , message=message, data=data, error=error)
def status_error   (message:str='', data=None,error=None): return osbot_status.log_message(status='error'   , message=message, data=data, error=error)
def status_info    (message:str='', data=None,error=None): return osbot_status.log_message(status='info'    , message=message, data=data, error=error)
def status_ok      (message:str='', data=None,error=None): return osbot_status.log_message(status='ok'      , message=message, data=data, error=error)
def status_warning (message:str='', data=None,error=None): return osbot_status.log_message(status='warning' , message=message, data=data, error=error)


# def status_info   (message:str='', data=None,error=None): osbot_logger.info   ('[osbot] [info]  ' + str(message)); return status_message('info', message=message, data=data, error=error)
# def status_ok     (message:str='', data=None,error=None): osbot_logger.info   ('[osbot] [ok]    ' + str(message)); return status_message('ok', message=message, data=data, error=error)
# def status_warning(message:str='', data=None,error=None): osbot_logger.warning('[osbot] [warning] ' + str(message)); return status_message('warning', message=message, data=data, error=error)

#todo: add status_exception that automatically picks up the exception from the stack trace
