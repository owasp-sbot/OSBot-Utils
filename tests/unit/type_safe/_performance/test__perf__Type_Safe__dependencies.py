from unittest                                                        import TestCase
from typing                                                          import get_args, get_origin, List, Dict, Any, Union, Optional
import inspect

import pytest

from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.performance.Performance_Measure__Session    import Performance_Measure__Session
from osbot_utils.utils.Objects                                       import (obj_data, default_value, all_annotations,
                                                                             raise_exception_on_obj_type_annotation_mismatch,
                                                                             obj_is_type_union_compatible,
                                                                             obj_is_attribute_annotation_of_type,
                                                                             value_type_matches_obj_annotation_for_attr,
                                                                             value_type_matches_obj_annotation_for_union_and_annotated)
from osbot_utils.utils.Json                                          import json_dumps, json_parse

class An_Class:                                                                            # Simple test class with annotations
    an_str   : str
    an_int   : int
    an_list  : List[str]
    an_dict  : Dict[str, Any]
    an_union : Union[str, int]

class test__perf__Type_Safe__dependencies(TestCase):                                      # Performance tests for Type_Safe dependencies

    @classmethod
    def setUpClass(cls):                                                                  # Set up time thresholds
        pytest.skip("skipping until refactoring of Type_Safe is complete")

        cls.time_0_ns    =      0
        cls.time_100_ns  =    100
        cls.time_200_ns  =    200
        cls.time_300_ns  =    300
        cls.time_400_ns  =    400
        cls.time_500_ns  =    500
        cls.time_600_ns  =    600
        cls.time_700_ns  =    700
        cls.time_800_ns  =    800
        cls.time_900_ns  =    900
        cls.time_1_kns   =  1_000
        cls.time_2_kns   =  2_000
        cls.time_3_kns   =  3_000
        cls.time_4_kns   =  4_000
        cls.time_5_kns   =  5_000
        cls.time_8_kns   =  8_000
        cls.time_9_kns   =  9_000
        cls.time_10_kns  = 10_000
        cls.time_20_kns  = 20_000
        cls.time_30_kns  = 30_000
        cls.time_50_kns  = 50_000

    def test_python_native__type_checks(self):                                           # Test Python native type checking methods
        class Child(An_Class): pass
        obj = An_Class()

        def check_isinstance():                                                           # Performance of isinstance()
            return isinstance(obj, An_Class)

        def check_issubclass():                                                          # Performance of issubclass()
            return issubclass(Child, An_Class)

        def check_type():                                                                # Performance of type()
            return type(obj)

        with Performance_Measure__Session() as session:
            session.measure(check_isinstance ).assert_time(self.time_0_ns, self.time_100_ns)
            session.measure(check_issubclass ).assert_time(self.time_0_ns, self.time_100_ns)
            session.measure(check_type       ).assert_time(self.time_0_ns)

    def test_python_native__attribute_access(self):                                      # Test Python native attribute access
        obj = An_Class()
        obj.an_str = 'abc'

        def do_getattr():                                                                # Performance of getattr()
            return getattr(obj, 'an_str')

        def do_hasattr():                                                                # Performance of hasattr()
            return hasattr(obj, 'an_str')

        def do_setattr():                                                                # Performance of setattr()
            setattr(obj, 'an_str', 'xyz')

        with Performance_Measure__Session() as session:
            session.measure(do_getattr).assert_time(self.time_0_ns  , self.time_100_ns)
            session.measure(do_hasattr).assert_time(self.time_0_ns  , self.time_100_ns)
            session.measure(do_setattr).assert_time(self.time_100_ns)

    def test_python_native__reflection(self):                                           # Test Python native reflection
        obj = An_Class()

        def get_vars():                                                                 # Performance of vars()
            return vars(obj)

        def get_annotations():                                                          # Performance of annotations access
            return An_Class.__annotations__

        def get_mro():                                                                 # Performance of MRO traversal
            return inspect.getmro(An_Class)

        with Performance_Measure__Session() as session:
            session.measure(get_vars       ).assert_time(self.time_0_ns, self.time_100_ns)
            session.measure(get_annotations).assert_time(self.time_0_ns, self.time_100_ns)
            session.measure(get_mro        ).assert_time(self.time_100_ns)

    def test_python_native__typing(self):                                              # Test typing module operations
        def get_origin_list():                                                         # Performance of get_origin()
            return get_origin(List[str])

        def get_origin_dict():
            return get_origin(Dict[str, int])

        def get_origin_union():
            return get_origin(Union[str, int])

        def get_args_list():                                                           # Performance of get_args()
            return get_args(List[str])

        def get_args_dict():
            return get_args(Dict[str, int])

        def get_args_union():
            return get_args(Union[str, int])

        with Performance_Measure__Session() as session:
            session.measure(get_origin_list ).assert_time(self.time_200_ns, self.time_300_ns)
            session.measure(get_origin_dict ).assert_time(self.time_200_ns, self.time_300_ns)
            session.measure(get_origin_union).assert_time(self.time_300_ns)
            session.measure(get_args_list   ).assert_time(self.time_300_ns)
            session.measure(get_args_dict   ).assert_time(self.time_300_ns)
            session.measure(get_args_union  ).assert_time(self.time_300_ns)

    def test_python_native__dict_operations(self):                                     # Test dict operations
        d = {'a': 1, 'b': 2}
        updates = {'c': 3, 'd': 4}

        def dict_get():                                                                # Performance of dict.get()
            return d.get('a')

        def dict_get_default():                                                        # Performance of dict.get() with default
            return d.get('missing', 42)

        def dict_update():                                                             # Performance of dict.update()
            d.update(updates)

        with Performance_Measure__Session() as session:
            session.measure(dict_get        ).assert_time(self.time_0_ns  , self.time_100_ns)
            session.measure(dict_get_default).assert_time(self.time_0_ns  , self.time_100_ns)
            session.measure(dict_update     ).assert_time(self.time_100_ns)

    def test_osbot_utils__core_methods(self):                                         # Test OSBot_Utils core methods
        obj = An_Class()

        def do_obj_data():                                                            # Performance of obj_data()
            return obj_data(obj)

        def do_default_value():                                                       # Performance of default_value()
            return default_value(str)

        def do_all_annotations():                                                     # Performance of all_annotations()
            return all_annotations(obj)

        with Performance_Measure__Session() as session:
            session.measure(do_obj_data       ).assert_time(self.time_8_kns, self.time_9_kns )
            session.measure(do_default_value  ).assert_time(self.time_100_ns)
            session.measure(do_all_annotations).assert_time(self.time_300_ns, self.time_400_ns, self.time_500_ns)

    def test_osbot_utils__type_checks(self):                                         # Test OSBot_Utils type checking
        obj = An_Class()

        def check_type_union():                                                      # Performance of obj_is_type_union_compatible()
            return obj_is_type_union_compatible(str, (str, int))

        def check_annotation_type():                                                 # Performance of obj_is_attribute_annotation_of_type()
            return obj_is_attribute_annotation_of_type(obj, 'an_str', str)

        def check_value_matches():                                                   # Performance of value_type_matches_obj_annotation_for_attr()
            return value_type_matches_obj_annotation_for_attr(obj, 'an_str', 'test')

        def check_value_matches_union():                                             # Performance of value_type_matches_obj_annotation_for_union_and_annotated()
            return value_type_matches_obj_annotation_for_union_and_annotated(obj, 'an_union', 'test')

        with Performance_Measure__Session() as session:
            session.measure(check_type_union         ).assert_time(self.time_300_ns, self.time_400_ns)
            session.measure(check_annotation_type    ).assert_time(self.time_200_ns)
            session.measure(check_value_matches      ).assert_time(self.time_800_ns, self.time_900_ns)
            session.measure(check_value_matches_union).assert_time(self.time_700_ns)

    def test_osbot_utils__serialization(self):                                       # Test OSBot_Utils serialization methods
        data = {'str': 'abc', 'int': 42, 'list': [1,2,3]}

        def do_json_dumps():                                                         # Performance of json_dumps()
            return json_dumps(data)

        def do_json_parse():                                                         # Performance of json_parse()
            return json_parse('{"a":1,"b":2}')

        with Performance_Measure__Session() as session:
            session.measure(do_json_dumps).assert_time(self.time_4_kns )
            session.measure(do_json_parse).assert_time(self.time_700_ns, self.time_800_ns)

    def test_osbot_utils__exception_handling(self):                                  # Test OSBot_Utils exception handling
        obj = An_Class()
        obj.an_str = 'abc'

        def do_type_mismatch():                                                      # Performance of raise_exception_on_obj_type_annotation_mismatch()
            try:
                raise_exception_on_obj_type_annotation_mismatch(obj, 'an_str', 42)
            except TypeError:
                pass

        with Performance_Measure__Session() as session:
            session.measure(do_type_mismatch).assert_time(self.time_2_kns)


    def test_python_native__reflection__class(self):                                    # Test class-level reflection methods
        def get_class_dict():                                                          # Performance of class __dict__ access
            return An_Class.__dict__

        def get_class_bases():                                                         # Performance of class __bases__ access
            return An_Class.__bases__

        def get_class_name():                                                          # Performance of class __name__ access
            return An_Class.__name__

        with Performance_Measure__Session() as session:
            session.measure(get_class_dict ).assert_time(self.time_0_ns, self.time_100_ns)
            session.measure(get_class_bases).assert_time(self.time_0_ns, self.time_100_ns)
            session.measure(get_class_name ).assert_time(self.time_0_ns, self.time_100_ns)

    def test_python_native__dict_special_methods(self):                                # Test dict special methods
        d = {'a': 1, 'b': 2}

        def dict_contains():                                                           # Performance of __contains__
            return 'a' in d

        def dict_len():                                                                # Performance of __len__
            return len(d)

        def dict_iter():                                                               # Performance of __iter__
            return list(d)

        def dict_items():                                                              # Performance of .items()
            return list(d.items())

        with Performance_Measure__Session() as session:
            session.measure(dict_contains).assert_time(self.time_0_ns  , self.time_100_ns)
            session.measure(dict_len     ).assert_time(self.time_0_ns  , self.time_100_ns)
            session.measure(dict_iter    ).assert_time(self.time_100_ns)
            session.measure(dict_items   ).assert_time(self.time_200_ns)

    def test_python_native__typing__complex(self):                                     # Test complex typing operations
        def get_origin_optional():                                                     # Performance of Optional type
            return get_origin(Optional[str])

        def get_origin_nested():                                                       # Performance of nested types
            return get_origin(List[Dict[str, Any]])

        def get_args_optional():                                                       # Performance of Optional args
            return get_args(Optional[str])

        def get_args_nested():                                                         # Performance of nested args
            return get_args(List[Dict[str, Any]])

        with Performance_Measure__Session() as session:
            session.measure(get_origin_optional).assert_time(self.time_200_ns, self.time_300_ns)
            session.measure(get_origin_nested  ).assert_time(self.time_500_ns)
            session.measure(get_args_optional  ).assert_time(self.time_300_ns)
            session.measure(get_args_nested    ).assert_time(self.time_500_ns, self.time_600_ns)

    def test_osbot_utils__type_matches__special(self):                                # Test special type matching cases
        obj = An_Class()

        def check_none_value():                                                       # Test handling of None values
            return value_type_matches_obj_annotation_for_attr(obj, 'an_str', None)

        def check_missing_annotation():                                               # Test handling missing annotations
            return value_type_matches_obj_annotation_for_attr(obj, 'missing', 'test')

        def check_complex_union():                                                    # Test complex union types
            return value_type_matches_obj_annotation_for_union_and_annotated(
                    obj, 'an_union', [1,2,3])

        with Performance_Measure__Session() as session:
            session.measure(check_none_value         ).assert_time(self.time_1_kns)
            session.measure(check_missing_annotation ).assert_time(self.time_500_ns)
            session.measure(check_complex_union      ).assert_time(self.time_700_ns, self.time_800_ns)

    def test_python_native__class_access(self):                                         # Test performance of class access
        obj = An_Class()

        def get_class():                                                                # Performance of __class__ access
            return obj.__class__

        def get_class_module():                                                         # Performance of __module__ access
            return obj.__class__.__module__

        with Performance_Measure__Session() as session:
            session.measure(get_class       ).assert_time(self.time_0_ns, self.time_100_ns)
            session.measure(get_class_module).assert_time(self.time_0_ns, self.time_100_ns)

    def test_python_native__attribute_access_edge_cases(self):                          # Test attribute access edge cases
        obj = An_Class()

        def dir_obj():                                                                  # Performance of dir()
            return dir(obj)

        def getattr_with_default():                                                     # Performance of getattr with default
            return getattr(obj, 'missing', None)

        def getattr_missing():                                                          # Performance of getattr exception
            try:
                return getattr(obj, 'missing')                                          # This should raise AttributeError
            except AttributeError:
                pass

        with Performance_Measure__Session() as session:
            session.measure(dir_obj             ).assert_time(self.time_2_kns)
            session.measure(getattr_with_default).assert_time(self.time_100_ns)
            session.measure(getattr_missing     ).assert_time(self.time_300_ns)

    def test_python_native__hasattr_edge_cases(self):                                   # Test hasattr edge cases
        obj = An_Class()

        def hasattr_missing():                                                          # Performance of hasattr on missing
            return hasattr(obj, 'missing')

        def hasattr_property():                                                         # Performance of hasattr on property
            return hasattr(obj, '__dict__')

        def hasattr_method():                                                           # Performance of hasattr on method
            return hasattr(obj, '__str__')

        with Performance_Measure__Session() as session:
            session.measure(hasattr_missing ).assert_time(self.time_0_ns , self.time_100_ns)
            session.measure(hasattr_property).assert_time(self.time_0_ns , self.time_100_ns)
            session.measure(hasattr_method  ).assert_time(self.time_100_ns)

    # -----

    def test__get_class_info(self):

        import types
        from osbot_utils.type_safe.Type_Safe import Type_Safe

        def get_class_info(cls):

            annotations = {}
            defaults    = {}
            origins     = {}

            for base in inspect.getmro(cls):                                            # Process MRO once
                if base is object:
                    continue

                if hasattr(base, '__annotations__'):                                    # Get annotations
                    annotations.update(base.__annotations__)

                for k, v in vars(base).items():                                         # Get class variables
                    if not k.startswith('__'):
                        if not isinstance(v, (types.FunctionType, classmethod)):
                            defaults[k] = v

            for name, annot in annotations.items():                                     # Process type origins once
                origins[name] = get_origin(annot)

            return {
                    'annotations': annotations,
                    'defaults': defaults,
                    'origins': origins
                }

        class Python__pure_class:                                                                # Simple test class with annotations
            pass

        class Python__one_attr:
            an_str:str

        class Python__multiple_attrs:
            an_str   : str
            an_int   : int
            an_list  : List[str]
            an_dict  : Dict[str, Any]
            an_union : Union[str, int]

        class Type_Safe__one_attr(Type_Safe):
            an_str   : str

        class Type_Safe__multiple_attrs(Type_Safe):
            an_str   : str
            an_int   : int
            an_list  : List[str]
            an_dict  : Dict[str, Any]
            an_union : Union[str, int]

        def get_class_info__Python__pure_class():
            get_class_info(Python__pure_class)

        def get_class_info__Python__one_attr():
            get_class_info(Python__one_attr)

        def get_class_info__Python__multiple_attrs():
            get_class_info(Python__multiple_attrs)

        def call_ctor__Type_Safe__one_attr():
            Type_Safe__one_attr()

        def call_ctor__Type_Safe__multiple_attrs():
            Type_Safe__multiple_attrs()

        assert get_class_info(Python__pure_class     ) == { 'annotations': {}, 'defaults': {}, 'origins': {}}
        assert get_class_info(Python__one_attr       ) == { 'annotations': {'an_str': str },
                                                            'defaults'   : {}              ,
                                                            'origins'    : {'an_str': None }}
        assert get_class_info(Python__multiple_attrs) == { 'annotations': {'an_dict': Dict[str, Any],
                                                                            'an_int': int,
                                                                            'an_list': List[str],
                                                                            'an_str': str,
                                                                            'an_union': Union[str, int]},
                                                            'defaults' : {},
                                                            'origins'  : {'an_dict': dict,
                                                                          'an_int': None,
                                                                          'an_list': list,
                                                                          'an_str': None,
                                                                          'an_union': Union}}


        with Performance_Measure__Session() as session:
            print()
            session.measure(get_class_info__Python__pure_class    ).print(40).assert_time(self.time_700_ns, self.time_800_ns, self.time_1_kns  )
            session.measure(get_class_info__Python__one_attr      ).print(40).assert_time(self.time_900_ns , self.time_1_kns, self.time_2_kns  )
            session.measure(get_class_info__Python__multiple_attrs).print(40).assert_time(self.time_900_ns , self.time_1_kns, self.time_2_kns, self.time_3_kns)
            session.measure(call_ctor__Type_Safe__one_attr        ).print(40).assert_time(self.time_9_kns  , self.time_10_kns, self.time_20_kns                  )
            session.measure(call_ctor__Type_Safe__multiple_attrs  ).print(40).assert_time(self.time_30_kns , self.time_50_kns                                    )
