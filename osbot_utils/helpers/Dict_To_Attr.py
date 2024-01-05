from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Dict_To_Attr:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)