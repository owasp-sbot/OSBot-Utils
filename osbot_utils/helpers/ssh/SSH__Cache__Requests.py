from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Patch    import Sqlite__Cache__Requests__Patch
from osbot_utils.helpers.ssh.SSH                                        import SSH
from osbot_utils.utils.Json                                             import json_to_str, json_loads
from osbot_utils.utils.Toml                                             import dict_to_toml, toml_to_dict

SQLITE_DB_NAME__SSH_REQUESTS_CACHE = 'ssh_requests_cache.sqlite'
SQLITE_TABLE_NAME__SSH_REQUESTS    = 'ssh_requests'



class SSH__Cache__Requests(Sqlite__Cache__Requests__Patch):
    db_path    : str
    db_name    : str =  SQLITE_DB_NAME__SSH_REQUESTS_CACHE
    table_name : str =  SQLITE_TABLE_NAME__SSH_REQUESTS

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_class           = SSH
        self.target_function        = SSH.execute_command
        self.target_function_name   = "execute_command"
        self.print_requests         = False


    def invoke_target(self, target, target_args, target_kwargs):
        if self.print_requests:
            print(f'[invoke_target]: {target_args}')
        return super().invoke_target(target, target_args, target_kwargs)

    # todo: finish this implementation
    def request_data(self, *args, **kwargs):
        ssh      = args[0]
        ssh_host = ssh.ssh_host
        args_with_out_self = args[1:]
        request_data = dict(args   = args_with_out_self,
                            kwargs = kwargs            ,
                            ssh_host = ssh_host        )

        return dict_to_toml(request_data)
        # pprint('>>>>>> request_data <<<<<<< ')
        # pprint(request_data)
        #
        # pprint('------ request_data ------- ')
        # target_self, operation_name, api_params = args
        # request_data =  {'operation_name': operation_name,
        #                 'api_params'    : api_params    }
        # #if self.print_requests:
            #print(f'[request_data]: {request_data}')
        #request_data = json_to_str(request_data)            # todo: this used to use yaml, change to a better mode

        #return super().request_data(*args, **kwargs)

    def requests_data__all(self):
        requests_data__all = super().requests_data__all()
        for item in requests_data__all:
            request_data_raw      = item.get('request_data')
            request_data_original = toml_to_dict(json_loads(request_data_raw))
            item['request_data']  = request_data_original
        return requests_data__all