# todo refactor into Status class
import traceback

from osbot_utils.utils.Python_Logger import Python_Logger

class Status:
    def __init__(self):
        self.logger               = Python_Logger().setup()
        self.call_logger_method   = False
        self.root_logger_handlers = None
        #self.logger.add_memory_logger()

    def root_logger(self):
        return self.logger.logger.parent

    def clear_root_logger_handlers(self):
        self.root_logger_handlers = self.root_logger().handlers
        self.root_logger().handlers = []

    def restore_root_logger_handlers(self):
        if self.root_logger_handlers:
            self.root_logger().handlers = self.root_logger_handlers
    def status_message(self, status, message:str=None, data=None, error=None):
        return  {  'data'   : data    ,
                   'error'  : error   ,
                   'message': message ,
                   'status' : status
                }

    def last_message(self):
        return self.logger.memory_handler_last_log_entry()

    def log_message(self, status, message:str='', data=None, error=None, stacklevel=3):          # stacklevel is usually 3 because we want to get the caller of the method that called this on
        logger_message = f'[osbot] [{status}] ' + str(message)
        logger_method  = self.logger.__getattribute__(status)
        status_message = self.status_message(status=status, message=message, data=data, error=error)
        if self.call_logger_method:
            kwargs = {}                                                 # todo: add option to capture stack trace and other helpful debug data
            if status =='exception':
                kwargs = dict(exc_info=True, stacklevel=stacklevel)
            logger_method(logger_message, **kwargs)
        return status_message




osbot_status = Status()                 # todo map out the performatin implications of doing this
osbot_logger = osbot_status.logger

def status_critical (message:str='', data=None,error=None): return osbot_status.log_message(status='critical' , message=message, data=data, error=error)
def status_debug    (message:str='', data=None,error=None): return osbot_status.log_message(status='debug'    , message=message, data=data, error=error)
def status_error    (message:str='', data=None,error=None): return osbot_status.log_message(status='error'    , message=message, data=data, error=error)
def status_exception(message:str='', data=None,error=None): return osbot_status.log_message(status='exception', message=message, data=data, error=error)
def status_info     (message:str='', data=None,error=None): return osbot_status.log_message(status='info'     , message=message, data=data, error=error)
def status_ok       (message:str='', data=None,error=None): return osbot_status.log_message(status='ok'       , message=message, data=data, error=error)
def status_warning  (message:str='', data=None,error=None): return osbot_status.log_message(status='warning'  , message=message, data=data, error=error)

log_critical  = status_critical   # level 50
log_error     = status_error      # level 40
log_exception = status_exception  # level 40
log_warning   = status_warning    # level 30
log_info      = status_info       # level 20
log_ok        = status_ok         # level 20
log_debug     = status_debug      # level 10


def send_status_to_logger(value: bool = True):
    osbot_status.call_logger_method = value

#def log_error   (message):#logger().error   (message) # level 40
#def log_info    (message): logger().info    (message) # level 20
#def log_warning (message): logger().warning (message) # level 30


# def status_info   (message:str='', data=None,error=None): osbot_logger.info   ('[osbot] [info]  ' + str(message)); return status_message('info', message=message, data=data, error=error)
# def status_ok     (message:str='', data=None,error=None): osbot_logger.info   ('[osbot] [ok]    ' + str(message)); return status_message('ok', message=message, data=data, error=error)
# def status_warning(message:str='', data=None,error=None): osbot_logger.warning('[osbot] [warning] ' + str(message)); return status_message('warning', message=message, data=data, error=error)

#todo: add status_exception that automatically picks up the exception from the stack trace
