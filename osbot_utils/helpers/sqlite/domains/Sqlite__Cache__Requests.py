from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Sqlite__Cache__Requests(Kwargs_To_Self):
    add_timestamp  : bool            = True
    enabled        : bool            = True
    update_mode    : bool            = False
    cache_only_mode: bool            = False