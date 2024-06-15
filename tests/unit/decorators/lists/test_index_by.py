from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.testing.Unit_Test import Unit_Test

class test_index_by(Unit_Test):

    @group_by
    @index_by
    def get_data(self):
        return [{'key': 'key_1', 'value': 'value_1', "answer": "42"    },
                {'key': 'key_1', 'value': 'value_2', "answer": "not 42"},
                {'key': 'key_2', 'value': 'value_1', "answer": "42"     },
                {'key': 'key_2', 'value': 'value_1', "answer": "42 not"}]

    def test_index_by(self):
        assert self.get_data(index_by='key'   ) == { 'key_1'  : {'answer': 'not 42', 'key': 'key_1', 'value': 'value_2'},
                                                     'key_2'  : {'answer': '42 not', 'key': 'key_2', 'value': 'value_1'}}
        assert self.get_data(index_by='value' ) == { 'value_1': {'answer': '42 not', 'key': 'key_2', 'value': 'value_1'},
                                                     'value_2': {'answer': 'not 42', 'key': 'key_1', 'value': 'value_2'}}

        assert self.get_data(index_by='answer') == { '42'     : {'answer': '42', 'key': 'key_2', 'value': 'value_1'},
                                                     '42 not' : {'answer': '42 not', 'key': 'key_2', 'value': 'value_1'},
                                                     'not 42' : {'answer': 'not 42', 'key': 'key_1', 'value': 'value_2'}}