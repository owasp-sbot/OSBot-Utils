from unittest                                                     import TestCase
from osbot_utils.testing.performance.Performance_Measure__Session import Performance_Measure__Session
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id  import Obj_Id, is_obj_id, new_obj_id


class test_Obj_Id(TestCase):

    def test__new__(self):
        obj_id = Obj_Id()
        assert type(obj_id           ) is Obj_Id
        assert isinstance(obj_id, str) is True
        assert is_obj_id(obj_id      ) is True

    def test_new_obj_id(self):
        obj_id = new_obj_id()
        assert is_obj_id(obj_id)

    def test__perf__new__(self):
        with Performance_Measure__Session() as _:
            _.measure(lambda: Obj_Id()    ).assert_time__less_than(1000)

    def test__perf__new_obj_id(self):
        with Performance_Measure__Session() as _:
            _.measure(lambda: new_obj_id()    ).assert_time__less_than(500)
            _.measure(lambda: is_obj_id('abc')).assert_time__less_than(500)