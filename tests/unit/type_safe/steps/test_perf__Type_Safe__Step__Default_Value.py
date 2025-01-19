from unittest                                                     import TestCase
from typing                                                       import List, Dict, Any, Union, Optional
from typing                                                       import Set, Type, ForwardRef
from osbot_utils.testing.performance.Performance_Measure__Session import Performance_Measure__Session
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Value   import type_safe_step_default_value

class test_perf__Type_Safe__Step__Default_Value(TestCase):

    @classmethod
    def setUpClass(cls):                                                             # Define timing thresholds
        cls.time_100_ns  =    100
        cls.time_200_ns  =    200
        cls.time_300_ns  =    300
        cls.time_400_ns  =    400
        cls.time_500_ns  =    500
        cls.time_600_ns  =    600
        cls.time_700_ns  =    700
        cls.time_800_ns  =    800
        cls.time_1_kns   =  1_000
        cls.time_2_kns   =  2_000
        cls.time_3_kns   =  3_000
        cls.time_5_kns   =  5_000
        cls.time_6_kns   =  6_000
        cls.time_7_kns   =  7_000
        cls.time_8_kns   =  8_000

    def test_primitive_types(self):                                                  # Test primitive type defaults
        class SimpleClass: pass                                                      # Dummy class for context

        def get_str_default():                                                      # Test str default
            return type_safe_step_default_value.default_value(SimpleClass, str)

        def get_int_default():                                                      # Test int default
            return type_safe_step_default_value.default_value(SimpleClass, int)

        def get_float_default():                                                    # Test float default
            return type_safe_step_default_value.default_value(SimpleClass, float)

        def get_bool_default():                                                     # Test bool default
            return type_safe_step_default_value.default_value(SimpleClass, bool)

        with Performance_Measure__Session() as session:
            session.measure(get_str_default  ).assert_time(self.time_1_kns)
            session.measure(get_int_default  ).assert_time(self.time_1_kns)
            session.measure(get_float_default).assert_time(self.time_1_kns)
            session.measure(get_bool_default ).assert_time(self.time_1_kns)

    def test_collection_types(self):                                                # Test collection type defaults
        class CollectionClass: pass

        def get_list_default():                                                     # Test basic List
            return type_safe_step_default_value.default_value(CollectionClass, List)

        def get_dict_default():                                                     # Test basic Dict
            return type_safe_step_default_value.default_value(CollectionClass, Dict)

        def get_set_default():                                                      # Test basic Set
            return type_safe_step_default_value.default_value(CollectionClass, Set)

        with Performance_Measure__Session() as session:
            session.measure(get_list_default).assert_time(self.time_800_ns)
            session.measure(get_dict_default).assert_time(self.time_600_ns)
            session.measure(get_set_default ).assert_time(self.time_400_ns)

    def test_parametrized_collections(self):                                        # Test parametrized collections
        class ParamClass: pass

        def get_list_str_default():                                                # Test List[str]
            return type_safe_step_default_value.default_value(ParamClass, List[str])

        def get_dict_str_int_default():                                            # Test Dict[str, int]
            return type_safe_step_default_value.default_value(ParamClass, Dict[str, int])

        def get_set_int_default():                                                 # Test Set[int]
            return type_safe_step_default_value.default_value(ParamClass, Set[int])

        with Performance_Measure__Session() as session:
            session.measure(get_list_str_default     ).assert_time(self.time_2_kns)
            session.measure(get_dict_str_int_default ).assert_time(self.time_2_kns)
            session.measure(get_set_int_default      ).assert_time(self.time_700_ns)

    def test_forward_references(self):                                              # Test forward references
        class ForwardClass:
            self_list : List['ForwardClass']                                       # Self-referential list
            self_dict : Dict[str, 'ForwardClass']                                  # Self-referential dict

        def get_forward_list_default():                                            # Test List with forward ref
            return type_safe_step_default_value.default_value(
                ForwardClass,
                List[ForwardRef('ForwardClass')])

        def get_forward_dict_default():                                            # Test Dict with forward ref
            return type_safe_step_default_value.default_value(
                ForwardClass,
                Dict[str, ForwardRef('ForwardClass')])

        with Performance_Measure__Session() as session:
            session.measure(get_forward_list_default).assert_time(self.time_7_kns)
            session.measure(get_forward_dict_default).assert_time(self.time_7_kns)

    def test_type_annotations(self):                                               # Test Type annotations
        class TypeClass: pass

        def get_type_default():                                                    # Test basic Type
            return type_safe_step_default_value.default_value(TypeClass, Type)

        def get_type_str_default():                                               # Test Type[str]
            return type_safe_step_default_value.default_value(TypeClass, Type[str])

        def get_type_forward_default():                                           # Test Type with forward ref
            return type_safe_step_default_value.default_value(
                TypeClass,
                Type[ForwardRef('TypeClass')])

        with Performance_Measure__Session() as session:
            session.measure(get_type_default        ).assert_time(self.time_2_kns                   )
            session.measure(get_type_str_default    ).assert_time(self.time_700_ns, self.time_800_ns)
            session.measure(get_type_forward_default).assert_time(self.time_6_kns                   )

    def test_nested_collections(self):                                             # Test nested collections
        class NestedClass: pass

        def get_nested_list_default():                                            # Test List[List[str]]
            return type_safe_step_default_value.default_value(
                NestedClass,
                List[List[str]])

        def get_nested_dict_default():                                            # Test Dict[str, Dict[str, int]]
            return type_safe_step_default_value.default_value(
                NestedClass,
                Dict[str, Dict[str, int]])

        def get_mixed_nested_default():                                           # Test Dict[str, List[int]]
            return type_safe_step_default_value.default_value(
                NestedClass,
                Dict[str, List[int]])

        with Performance_Measure__Session() as session:
            session.measure(get_nested_list_default ).assert_time(self.time_2_kns)
            session.measure(get_nested_dict_default ).assert_time(self.time_2_kns)
            session.measure(get_mixed_nested_default).assert_time(self.time_2_kns)

    def test_complex_types(self):                                                  # Test complex type combinations
        class ComplexClass: pass

        def get_optional_list_default():                                          # Test Optional[List[str]]
            return type_safe_step_default_value.default_value(
                ComplexClass,
                Optional[List[str]])

        def get_union_types_default():                                           # Test Union[str, int, List[float]]
            return type_safe_step_default_value.default_value(
                ComplexClass,
                Union[str, int, List[float]])

        def get_complex_dict_default():                                          # Test Dict[str, Union[int, List[str]]]
            return type_safe_step_default_value.default_value(
                ComplexClass,
                Dict[str, Union[int, List[str]]])

        with Performance_Measure__Session() as session:
            session.measure(get_optional_list_default).assert_time(self.time_2_kns)
            session.measure(get_union_types_default  ).assert_time(self.time_2_kns)
            session.measure(get_complex_dict_default ).assert_time(self.time_3_kns)

    def test_inheritance_types(self):                                              # Test with inheritance
        class BaseClass: pass
        class ChildClass(BaseClass): pass
        class GrandChild(ChildClass): pass

        def get_base_type_default():                                              # Test Type[BaseClass]
            return type_safe_step_default_value.default_value(
                GrandChild,
                Type[BaseClass])

        def get_child_list_default():                                            # Test List[ChildClass]
            return type_safe_step_default_value.default_value(
                GrandChild,
                List[ChildClass])

        def get_grandchild_dict_default():                                       # Test Dict[str, GrandChild]
            return type_safe_step_default_value.default_value(
                GrandChild,
                Dict[str, GrandChild])

        with Performance_Measure__Session() as session:
            session.measure(get_base_type_default      ).assert_time(self.time_700_ns, self.time_800_ns)
            session.measure(get_child_list_default     ).assert_time(self.time_2_kns )
            session.measure(get_grandchild_dict_default).assert_time(self.time_2_kns )

    def test_edge_cases(self):                                                     # Test edge cases
        class EdgeClass: pass

        def get_any_default():                                                    # Test Any type
            return type_safe_step_default_value.default_value(EdgeClass, Any)

        def get_empty_union_default():                                           # Test empty Union
            return type_safe_step_default_value.default_value(EdgeClass, Union)

        def get_none_default():                                                  # Test None type
            return type_safe_step_default_value.default_value(EdgeClass, type(None))

        with Performance_Measure__Session() as session:
            session.measure(get_any_default        ).assert_time(self.time_2_kns)
            session.measure(get_empty_union_default).assert_time(self.time_2_kns)
            session.measure(get_none_default       ).assert_time(self.time_1_kns)