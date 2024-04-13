from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

class Schema__Table__Requests(Kwargs_To_Self):
    request_hash  : str
    request_data  : str
    response_hash : str
    response_data : str
    response_bytes: bytes
    cache_hits    : int                         # todo: to implement
    timestamp     : int
    latest        : bool                        # todo: add native bool support to sqlite
    comments      : str