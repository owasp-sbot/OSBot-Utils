from unittest                                   import TestCase
from osbot_utils.helpers.Random_Guid            import Random_Guid
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive
from osbot_utils.utils.Json                     import json_to_str, json_round_trip
from osbot_utils.utils.Misc                     import is_guid
from osbot_utils.utils.Objects                  import base_types


class test_Random_Guid(TestCase):

    def test__init__(self):
        random_guid = Random_Guid()
        assert len(random_guid)         == 36
        assert type(random_guid)        is Random_Guid
        assert type(str(random_guid))   is  str                       # FIXED: not it is a string | BUG a bit weird why this is not a str
        assert base_types(random_guid)  == [Type_Safe__Primitive, str, object, object]
        assert str(random_guid)         == random_guid

        assert is_guid    (random_guid)
        assert isinstance (random_guid, str)

        assert Random_Guid()      != Random_Guid()
        assert str(Random_Guid()) != str(Random_Guid())


        assert json_to_str(random_guid)           == f'"{random_guid}"'
        assert json_round_trip(random_guid)       == str(random_guid)
        assert type(json_round_trip(random_guid)) is str
