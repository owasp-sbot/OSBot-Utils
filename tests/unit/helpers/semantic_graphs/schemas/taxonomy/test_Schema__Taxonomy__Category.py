from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category


class test_Schema__Taxonomy__Category(TestCase):                                     # Test category schema

    def test__init__(self):                                                          # Test initialization with defaults
        with Schema__Taxonomy__Category() as _:
            assert type(_.category_id)  is Category_Id
            assert str(_.category_id)   == ''
            assert str(_.name)          == ''
            assert str(_.description)   == ''
            assert str(_.parent_ref)    == ''
            assert _.child_refs         == []

    def test__with_values(self):                                                     # Test with explicit values
        with Schema__Taxonomy__Category(category_id = Category_Id('code_unit')         ,
                                        name        = 'code_unit'                      ,
                                        description = 'Executable code units'          ,
                                        parent_ref  = Category_Id('code_element')      ,
                                        child_refs  = [Category_Id('class_unit')]      ) as _:
            assert str(_.category_id)  == 'code_unit'
            assert str(_.name)         == 'code_unit'
            assert str(_.description)  == 'Executable code units'
            assert str(_.parent_ref)   == 'code_element'
            assert len(_.child_refs)   == 1
