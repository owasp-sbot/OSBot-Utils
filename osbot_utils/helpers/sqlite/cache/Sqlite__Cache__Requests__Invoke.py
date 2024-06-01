import types

from osbot_utils.base_classes.Type_Safe                               import Type_Safe
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Actions import Sqlite__Cache__Requests__Actions
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Config import Sqlite__Cache__Requests__Config
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Data import Sqlite__Cache__Requests__Data
from osbot_utils.utils.Json import json_loads
from osbot_utils.utils.Objects import pickle_load_from_bytes, pickle_save_to_bytes


class Sqlite__Cache__Requests__Invoke(Type_Safe):
    cache_actions    : Sqlite__Cache__Requests__Actions
    cache_data       : Sqlite__Cache__Requests__Data
    config           : Sqlite__Cache__Requests__Config
    on_invoke_target : types.FunctionType

    def invoke(self, target, target_args, target_kwargs):
        return self.invoke_with_cache(target, target_args, target_kwargs)

    def invoke_target(self, target, target_args, target_kwargs):
        if self.on_invoke_target:
            raw_response = self.on_invoke_target(target, target_args, target_kwargs)
        else:
            raw_response = target(*target_args, **target_kwargs)
        return self.transform_raw_response(raw_response)

    def invoke_with_cache(self, target, target_args, target_kwargs, request_data=None):
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
            self.cache_actions.cache_add(request_data=request_data, response_data=response_data)
            return response_data_obj
        except Exception as exception:
            if self.config.capture_exceptions:
                response_data     = self.cache_data.response_data_serialize(exception)
                self.cache_actions.cache_add(request_data=request_data, response_data=response_data)
            raise exception

    def transform_raw_response(self, raw_response):
        return raw_response
