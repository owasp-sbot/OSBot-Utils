from enum import Enum, auto

from osbot_utils.utils.Objects import obj_info

from osbot_utils.utils.Dev import pprint

from osbot_utils.helpers.Local_Cache import Local_Cache

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mem_graph.Mem_Graph import Mem_Graph


class Serialization_Mode(Enum):
    JSON    = auto()
    PICKLE  = auto()
    YAML    = auto()

class Mem_Graph__Serializer(Kwargs_To_Self):

    local_cache : Local_Cache                                       # todo, refactor this into an MGraph__Storage__Disk class
    mgraph      : Mem_Graph
    mode        : Serialization_Mode = Serialization_Mode.PICKLE
    key         : str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key         = f'serialiser_for {self.mgraph.key}'
        self.local_cache = Local_Cache('a')


    def save(self):
        if self.mode == Serialization_Mode.JSON:
            return self.save_to_json()
        if self.mode == Serialization_Mode.PICKLE:
            return self.save_to_pickle()
        if self.mode == Serialization_Mode.YAML:
            return self.save_to_yaml()
        return False

    def save_to_json(self):
        return '...json save - to be implemented...'

    def save_to_pickle(self):
        obj_info(self.local_cache)
        return '...pickle save - to be implemented...'

    def save_to_yaml(self):
        return '...yaml save - to be implemented...'