from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

class Schema__Table__Requests(Kwargs_To_Self):
    comments      : str
    metadata      : str
    request_type  : str
    request_hash  : str
    request_data  : str
    response_bytes: bytes
    response_hash : str
    response_data : str
    response_type : str
    source        : str
    timestamp     : int
