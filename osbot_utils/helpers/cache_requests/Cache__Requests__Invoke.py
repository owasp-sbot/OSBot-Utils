import threading
import types

from osbot_utils.type_safe.Type_Safe                                 import Type_Safe
from osbot_utils.helpers.cache_requests.Cache__Requests__Actions        import Cache__Requests__Actions
from osbot_utils.helpers.cache_requests.Cache__Requests__Config         import Cache__Requests__Config
from osbot_utils.helpers.cache_requests.Cache__Requests__Data           import Cache__Requests__Data


class Cache__Requests__Invoke(Type_Safe):
    cache_actions    : Cache__Requests__Actions
    cache_data       : Cache__Requests__Data
    config           : Cache__Requests__Config
    on_invoke_target : types.FunctionType
    cursor_thread_id : int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor_thread_id =  threading.get_ident()          # we need to capture this to make sure we are operating on the same thread

    def can_operate_in_this_thread(self):
        return self.cursor_thread_id == threading.get_ident()

    def invoke(self, target, target_args, target_kwargs):
        return self.invoke_with_cache(target, target_args, target_kwargs)

    def invoke_target(self, target, target_args, target_kwargs):
        if self.on_invoke_target:
            raw_response = self.on_invoke_target(target, target_args, target_kwargs)
        else:
            raw_response = target(*target_args, **target_kwargs)
        return self.transform_raw_response(raw_response)



    def invoke_with_cache(self, target, target_args, target_kwargs, request_data=None):
        if self.can_operate_in_this_thread() is False:                                  # make sure we are in the correct thread
            return self.invoke_target(target, target_args, target_kwargs)
        if self.config.enabled is False:
            if self.config.cache_only_mode:
                return None
            return self.invoke_target(target, target_args, target_kwargs)
        if request_data is None:
            request_data  = self.cache_data.cache_request_data(*target_args, **target_kwargs)
        cache_entry   = self.cache_data.cache_entry(request_data)
        if cache_entry:
            if self.config.update_mode is True:
                self.cache_actions.cache_delete(request_data)
            else:
                return self.cache_data.response_data_deserialize(cache_entry)
        if self.config.cache_only_mode is False:
            return self.invoke_target__and_add_to_cache(request_data, target, target_args, target_kwargs)


    def invoke_target__and_add_to_cache(self,request_data, target, target_args, target_kwargs):
        try:
            response_data_obj = self.invoke_target(target, target_args, target_kwargs)
            response_data     = self.cache_data.response_data_serialize(response_data_obj)
            if response_data:
                self.cache_actions.cache_add(request_data=request_data, response_data=response_data)
            return response_data_obj
        except Exception as exception:
            if self.config.capture_exceptions:
                response_data     = self.cache_data.response_data_serialize(exception)
                self.cache_actions.cache_add(request_data=request_data, response_data=response_data)
            raise exception

    def transform_raw_response(self, raw_response):
        return raw_response
