from enum import Enum

class Enum__Http__Method(str, Enum):
    GET     = "GET"
    POST    = "POST"
    PUT     = "PUT"
    DELETE  = "DELETE"
    PATCH   = "PATCH"
    HEAD    = "HEAD"
    OPTIONS = "OPTIONS"