from osbot_utils.base_classes.Type_Safe import Type_Safe


class Cache__Requests__Config(Type_Safe):
    add_timestamp       : bool   = True
    add_source_location  :bool    = True
    enabled             : bool   = True
    update_mode         : bool   = False
    cache_only_mode     : bool   = False
    pickle_response     : bool   = False
    capture_exceptions  : bool   = False                # once this is working, it might be more useful to have this set to true
    exception_classes   : list

    def disable(self):
        self.enabled = False
        return self

    def enable(self):
        self.enabled = True
        return self

    def only_from_cache(self, value=True):
        self.cache_only_mode = value
        return self

    def set__add_timestamp(self, value):
        self.add_timestamp = value
        return self

    def update(self, value=True):
        self.update_mode = value
        return self
