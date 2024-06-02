from osbot_utils.helpers.Print_Table import Print_Table
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Patch    import Sqlite__Cache__Requests__Patch
from osbot_utils.helpers.ssh.SSH                                        import SSH
from osbot_utils.utils.Call_Stack import call_stack_frames_data
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_name
from osbot_utils.utils.Json                                             import json_to_str, json_loads
from osbot_utils.utils.Toml                                             import dict_to_toml, toml_to_dict

SQLITE_DB_NAME__SSH_REQUESTS_CACHE = 'ssh_requests_cache.sqlite'
SQLITE_TABLE_NAME__SSH_REQUESTS    = 'ssh_requests'



class SSH__Cache__Requests(Sqlite__Cache__Requests__Patch):
    db_path                           : str
    db_name                           : str  = SQLITE_DB_NAME__SSH_REQUESTS_CACHE
    table_name                        : str  = SQLITE_TABLE_NAME__SSH_REQUESTS
    add_caller_signature_to_cache_key : bool = True

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

    def request_data(self, *args, **kwargs):
        ssh                 = args[0]
        ssh_host            = ssh.ssh_host
        args_with_out_self  = args[1:]
        request_data = dict(args             = args_with_out_self,
                            kwargs           = kwargs            ,
                            ssh_host         = ssh_host          )
        if self.add_caller_signature_to_cache_key:
            frames              = call_stack_frames_data(8)                 # todo: refactor this to separate method
            caller_signature = (f"{frames[0].get('name')}:{frames[0].get('lineno')}  | "
                                f"{frames[1].get('name')}:{frames[1].get('lineno')}  | "
                                f"{frames[2].get('name')}:{frames[2].get('lineno')}'")
            request_data['caller_signature'] = caller_signature            # this adds support for different caches to the same method call (main limitation is that it is directly tied with the line numbers)

        return dict_to_toml(request_data)

    def requests_data__all(self):
        requests_data__all = super().requests_data__all()
        for item in requests_data__all:
            request_data_raw      = item.get('request_data')
            request_data_original = toml_to_dict(json_loads(request_data_raw))
            item['request_data']  = request_data_original
        return requests_data__all