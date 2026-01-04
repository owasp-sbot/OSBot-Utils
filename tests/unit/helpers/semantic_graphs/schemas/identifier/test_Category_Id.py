from unittest                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id import Category_Id
from osbot_utils.testing.Graph__Deterministic__Ids                      import deterministic_ids
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id        import Obj_Id


class test_Category_Id(TestCase):                                                    # Test category identifier

    def test__init__(self):                                                          # Test initialization
        with deterministic_ids():
            with Category_Id(Obj_Id()) as _:
                assert str(_) == 'f0000001'
