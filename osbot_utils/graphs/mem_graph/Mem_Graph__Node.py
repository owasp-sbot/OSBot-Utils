from osbot_utils.utils.Misc import random_id

from osbot_utils.base_classes.Kwargs_To_Self      import Kwargs_To_Self


class Mem_Graph__Node(Kwargs_To_Self):

    key   : str
    label : str
    data : dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.label:
            self.label = random_id()
        if not self.key:
            self.key = self.label

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'[Graph Node] {self.key}'