from typing import Optional, Union
from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.base_classes.Type_Safe__List import Type_Safe__List
from osbot_utils.graphs.mermaid.Mermaid         import Mermaid
from osbot_utils.graphs.mermaid.Mermaid__Graph  import Mermaid__Graph
from osbot_utils.graphs.mermaid.Mermaid__Node   import Mermaid__Node
from osbot_utils.graphs.mgraph.MGraph__Node     import MGraph__Node
from osbot_utils.utils.Misc                     import list_set
from osbot_utils.utils.Objects                  import obj_attribute_annotation


class test_Kwargs_To_Self__bugs(TestCase):

    def test__bug__check_type_safety_assignments__on_ctor(self):
        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class__With_Correct_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int = an_int_value
            an_str  : str = an_str_value

        class An_Class__With_Bad_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int  = an_bool_value                      # BUG: should have thrown exception here
            an_str  : str  = an_bool_value                      # will throw exception here


        an_class =  An_Class__With_Correct_Values()             # should create ok and values should match the type
        assert an_class.__locals__() == {'an_bool': an_bool_value, 'an_int': an_int_value, 'an_str': an_str_value}

        expected_message = "variable 'an_str' is defined as type '<class 'str'>' but has value 'True' of type '<class 'bool'>'"
        with self.assertRaises(Exception) as context:
            An_Class__With_Bad_Values()
        assert context.exception.args[0] == expected_message

    def test__bug__check_type_safety_assignments____on_ctor__union(self):
        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class__With_Correct_Values(Kwargs_To_Self):
            an_bool     : Optional[bool            ] = an_bool_value
            an_int      : Optional[int             ] = an_int_value
            an_str      : Optional[str             ] = an_str_value
            an_bool_none: Optional[bool            ] = None
            an_int_none : Optional[int             ] = None
            an_str_none : Optional[str             ] = None
            an_bool_int : Optional[Union[bool, int]] = an_bool_value
            an_str_int  : Optional[Union[str , int]] = an_str_value
            an_int_bool : Optional[Union[bool, int]] = an_int_value
            an_int_str  : Optional[Union[str , int]] = an_int_value

        an_class = An_Class__With_Correct_Values()
        assert an_class.__locals__() == { 'an_bool': an_bool_value, 'an_bool_int': True        , 'an_bool_none': None ,
                                          'an_int': an_int_value  , 'an_int_bool': an_int_value,'an_int_none' : None , 'an_int_str': an_int_value,
                                          'an_str': an_str_value  , 'an_str_int': an_str_value, 'an_str_none' : None }

        class An_Class__With_Bad_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int  = an_bool_value                      # BUG: should have thrown exception here (bool should be allowed on int)
            an_str  : str  = an_bool_value                      # will throw exception here

        expected_message = "variable 'an_str' is defined as type '<class 'str'>' but has value 'True' of type '<class 'bool'>'"
        with self.assertRaises(Exception) as context:
            An_Class__With_Bad_Values()
        assert context.exception.args[0] == expected_message

    def test__bug__check_type_safety_assignments__on_obj(self):
        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class(Kwargs_To_Self):
            an_bool : bool
            an_int  : int
            an_str  : str

        an_class = An_Class()
        assert an_class.__locals__() == {'an_bool': False, 'an_int': 0, 'an_str': ''}       # confirm default values assignment

        an_class.an_bool = an_bool_value                                                    # these should all work
        an_class.an_int  = an_int_value                                                     # since we are doing the correct type assigment
        an_class.an_str  = an_str_value

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            expected_message = f"Invalid type for attribute '{var_name}'. Expected '<class '{expected_type}'>' but got '<class '{got_type}'>'"
            assert context.exception.args[0] == expected_message

        asserts_exception('an_bool',an_str_value , 'bool', 'str' )
        asserts_exception('an_bool',an_int_value , 'bool', 'int' )
        asserts_exception('an_str' ,an_bool_value, 'str' , 'bool')
        asserts_exception('an_str' ,an_int_value , 'str' , 'int' )
        asserts_exception('an_int' ,an_str_value , 'int' , 'str' )
        #asserts_exception('an_int' ,an_bool_value , 'int' , 'bool' )                     # BUG: should have raised exception
        an_class.an_int = an_bool_value                                                   # BUG  should have raised exception

    def test__bug__check_type_safety_assignments__allows_bool_to_int(self):
        an_bool_value = True                                        # this is a bool

        class Should_Raise_Exception(Kwargs_To_Self):               # a class that uses Kwargs_To_Self as a base class
            an_int: int = an_bool_value                             # BUG : the an_int variable is defined as an int, but it is assigned a bool

        should_raise_exception = Should_Raise_Exception()                                   # BUG an exception should have been raised
        assert should_raise_exception.__locals__()    == {'an_int': an_bool_value}          # BUG confirming that an_int is a bool
        assert should_raise_exception.an_int          is True                               # BUG in this case the value True
        assert type(an_bool_value                )    is bool                               # confirm an_bool_value is a bool
        assert type(should_raise_exception.an_int)    is bool                               # BUG:  confirming that an_int is a bool
        assert should_raise_exception.__annotations__ == {'an_int': int }                   # confirm that the an_int annotation is int

    def test__regression__check_type_safety_assignments__on_list(self):

        class An_Class(Kwargs_To_Self):
            an_str     : str
            an_str_list: list[str]
            an_int_list: list[int]

        an_class = An_Class()

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            expected_message = (f"Invalid type for attribute '{var_name}'. Expected '<class '{expected_type}'>' "
                                f"but got '<class '{got_type}'>'")
            assert context.exception.args[0] == expected_message

        asserts_exception('an_str', 42, 'str','int')

        an_class.an_str_list.append('should work')
        an_class.an_int_list.append(42            )

        with self.assertRaises(Exception) as context:
            an_class.an_str_list.append(42)                                 # FIXED was: BUG should have not worked
        assert context.exception.args[0] == "In Type_Safe__List: Invalid type for item: Expected 'str', but got 'int'"

        with self.assertRaises(Exception) as context:
            an_class.an_int_list.append('should not work')                  # FIXED was: BUG should have not worked
        assert context.exception.args[0] == "In Type_Safe__List: Invalid type for item: Expected 'int', but got 'str'"


    def test__regression__mermaid__list_allows_wrong_type(self):
        mermaid_graph = Mermaid__Graph()
        mermaid_node  = Mermaid__Node()
        graph_nodes   = mermaid_graph.nodes
        bad_node      = 'an str'

        assert obj_attribute_annotation(mermaid_graph, 'nodes') == list[Mermaid__Node]       # confirm nodes is list[Mermaid__Node]
        #assert type(graph_nodes) is list                                                              # FIXED was BUG: confirm that we lose type in graph_nodes
        assert type(graph_nodes) is Type_Safe__List                                                    # FIXED now graph_nodes is a typed list
        assert repr(graph_nodes) == 'list[Mermaid__Node]'                                              # FIXED confirm graph_nodes is list[Mermaid__Node]

        mermaid_graph.nodes.append(mermaid_node)                                        # adding Mermaid__Node directly
        graph_nodes        .append(mermaid_node)                                        # which should be appended ok
        assert graph_nodes == mermaid_graph.nodes == [mermaid_node, mermaid_node]       # and should be in list[Mermaid__Node] nodes var

        with self.assertRaises(Exception) as context_1:
            mermaid_graph.nodes.append(bad_node)                                        # FIXED was BUG: type issue
        with self.assertRaises(Exception) as context_2:
            mermaid_graph.nodes.append(1)                                               # FIXED was BUG: str and ints
        with self.assertRaises(Exception) as context_3:
            graph_nodes        .append(bad_node)                                        # FIXED was BUG: are not of type Mermaid__Node
        with self.assertRaises(Exception) as context_4:
            graph_nodes        .append(2)                                               # FIXED was BUG: and break nodes type safety list[Mermaid__Node]

        #assert graph_nodes == [mermaid_node, mermaid_node, bad_node, 1, bad_node, 2]   # FIXED was BUG: graph_nodes should not have the bad values
        assert graph_nodes == mermaid_graph.nodes == [mermaid_node, mermaid_node]       # FIXED bad values have not been added to graph_nodes

        exception_template = "In Type_Safe__List: Invalid type for item: Expected 'Mermaid__Node', but got '{type_name}'"
        assert context_1.exception.args[0] == exception_template.format(type_name='str')
        assert context_2.exception.args[0] == exception_template.format(type_name='int')
        assert context_3.exception.args[0] == exception_template.format(type_name='str')
        assert context_4.exception.args[0] == exception_template.format(type_name='int')


    def test__bug__mermaid__cast_issue_with_base_class__with_new_vars(self):

        new_node_1 = Mermaid().add_node(key='id')
        assert list_set(new_node_1.__kwargs__()) == ['attributes', 'config', 'key', 'label']
        assert type(new_node_1).__name__ == 'Mermaid__Node'

        new_node_2 = Mermaid().add_node(key='id')
        assert type(new_node_2).__name__ == 'Mermaid__Node'

        assert list_set(new_node_2.__dict__         ) == ['attributes', 'config', 'key', 'label']


        mermaid_node = Mermaid__Graph().add_node(key='id')
        assert type(mermaid_node).__name__ == 'Mermaid__Node'
        assert list_set(mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']   # BUG, should be ['attributes', 'key', 'label']

        mgraph_node = MGraph__Node(key='id')
        assert type(mgraph_node).__name__ == 'MGraph__Node'
        new_mermaid_node = Mermaid__Node()
        assert list_set(mgraph_node.__dict__     ) == ['attributes', 'key'   , 'label'       ]
        assert list_set(new_mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']

        new_mermaid_node.merge_with(mgraph_node)
        assert list_set(new_mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label'          ]