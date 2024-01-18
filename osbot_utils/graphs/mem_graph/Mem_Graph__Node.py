from osbot_utils.utils.Misc import random_id

from osbot_utils.base_classes.Kwargs_To_Self      import Kwargs_To_Self


class Mem_Graph__Node(Kwargs_To_Self):
    attributes : dict
    key        : str
    label      : str


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

    def data(self):
        return self.__locals__()             # todo: see if there is a better way to do this (specialy as the node objects gets more features and attributes)