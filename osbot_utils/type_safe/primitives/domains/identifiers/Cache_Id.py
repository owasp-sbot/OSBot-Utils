from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid import Random_Guid


class Cache_Id(Random_Guid):            # helper class so that we don't use Random_Guid to represent the cache_id class
    def __new__(cls, value=None):
        if value is None or value == '':
            return str.__new__(cls, '')
        else:
            return super().__new__(cls, value)

    @staticmethod
    def new() -> 'Cache_Id':
        return Cache_Id(Random_Guid())
