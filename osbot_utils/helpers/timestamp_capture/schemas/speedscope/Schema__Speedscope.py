from typing                                                                      import List
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Shared     import Schema__Speedscope_Shared
from osbot_utils.helpers.timestamp_capture.schemas.speedscope.Schema__Speedscope_Profile    import Schema__Speedscope_Profile


class Schema__Speedscope(Type_Safe):                                             # Complete speedscope.app format
    schema             : str = 'https://www.speedscope.app/file-format-schema.json'
    shared             : Schema__Speedscope_Shared
    profiles           : List[Schema__Speedscope_Profile]
    name               : str = ''
    activeProfileIndex : int = 0