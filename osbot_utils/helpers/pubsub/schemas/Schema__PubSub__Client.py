from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Schema__PubSub__Clients(Kwargs_To_Self):
    client_id            : str
    status               : str
    timestamp_connect    : int
    timestamp_disconnect : str