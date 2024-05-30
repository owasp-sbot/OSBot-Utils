from osbot_utils.helpers.sqlite.domains.Sqlite__Cache__Requests__Patch import Sqlite__Cache__Requests__Patch
from osbot_utils.helpers.ssh.SSH import SSH
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json_to_str

SQLITE_DB_NAME__SSH_REQUESTS_CACHE = 'ssh_requests_cache.sqlite'
SQLITE_TABLE_NAME__SSH_REQUESTS    = 'ssh_requests'



class SSH__Cache__Requests(Sqlite__Cache__Requests__Patch):

    def __init__(self, db_path=None):
        self.target_class           = SSH
        self.target_function        = SSH.execute_command
        self.target_function_name   = "execute_command"
        self.db_name                = SQLITE_DB_NAME__SSH_REQUESTS_CACHE
        self.table_name             = SQLITE_TABLE_NAME__SSH_REQUESTS
        #self.capture_exceptions     = True
        #self.exception_classes      = [ClientError]
        self.print_requests         = False
        super().__init__(db_path=db_path)

    def invoke_target(self, target, target_args, target_kwargs):
        if self.print_requests:
            print(f'[invoke_target]: {target_args}')
        return super().invoke_target(target, target_args, target_kwargs)

    # todo: finish this implementation
    def request_data(self, *args, **kwargs):

        # pprint('>>>>>> request_data <<<<<<< ')
        # pprint(args)
        # pprint(kwargs)
        # pprint('------ request_data ------- ')
        # target_self, operation_name, api_params = args
        # request_data =  {'operation_name': operation_name,
        #                 'api_params'    : api_params    }
        # #if self.print_requests:
            #print(f'[request_data]: {request_data}')
        #request_data = json_to_str(request_data)            # todo: this used to use yaml, change to a better mode

        return super().request_data(*args, **kwargs)