from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

from osbot_utils.utils.Call_Stack import call_stack_current_frame
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Functions import method_line_number

from osbot_utils.utils.Misc import random_string, random_int, wait_for
from osbot_utils.utils.trace.Trace_Call__Handler import DEFAULT_ROOT_NODE_NODE_TITLE

from osbot_utils.utils.trace.Trace_Call__Stack import Trace_Call__Stack
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node


class test_Trace_Call__Stack(TestCase):

    def setUp(self):
        self.stack = Trace_Call__Stack()

    def test_add_stack(self):
        sample_frame  = call_stack_current_frame()
        stack         = self.stack
        stack.add_node(title=DEFAULT_ROOT_NODE_NODE_TITLE)
        root_node     = self.stack.bottom()

        assert stack.size()  == 1
        assert stack         == [root_node]
        assert root_node     == Trace_Call__Stack_Node(call_index=0, name=DEFAULT_ROOT_NODE_NODE_TITLE)

        # case 1: with bad data
        assert stack.add_frame(frame=None) is None
        assert stack == [root_node]                 # confirm no changes made to the default stack

        # case 3: adding valid frame and node
        #node_1 = Trace_Call__Stack_Node(name='node_1')
        assert stack                                        == [root_node]
        assert stack.top()                                  == root_node
        assert stack.top().children                         == []
        assert len(stack)                                   == 1
        assert stack.call_index == 0
        node_1 = stack.add_frame(frame=sample_frame)
        assert type(node_1)                                 is Trace_Call__Stack_Node
        assert node_1.call_index                            == 1
        assert node_1.children                              == []
        assert node_1.name                                  == 'test_Trace_Call__Stack.test_Trace_Call__Stack.test_add_stack'
        assert node_1.source_code                           == ''
        assert len(stack)                                   == 2
        assert stack[-1]                                    == node_1
        assert stack                                        == [root_node, node_1]
        assert stack[-2]                                    == root_node
        assert stack[-3]                                    is None
        assert stack[0]                                     == root_node
        assert stack[1]                                     == node_1
        assert stack[2]                                     is None
        assert root_node.children                           == [node_1]
        assert root_node                                    == Trace_Call__Stack_Node(children=[node_1], name=DEFAULT_ROOT_NODE_NODE_TITLE)

        # case 3: adding another valid node
        #node_2 = Trace_Call__Stack_Node(call_index=2, name='node_2')
        node_2 = stack.add_frame(frame=sample_frame)
        assert len(stack)                                  == 3
        assert stack[-1]                                   == node_2
        assert stack[-2]                                   == node_1
        assert stack[-3]                                   == root_node
        assert stack                                       == [root_node, node_1, node_2]
        assert node_1.children                             == [node_2]
        assert root_node.children                          == [node_1]
        node_1.locals = {}
        node_2.locals = {}
        assert root_node                                   == Trace_Call__Stack_Node(call_index=0, children=[node_1], frame=None        , func_name=''              , name=DEFAULT_ROOT_NODE_NODE_TITLE                                 , module=''                      )
        assert node_1                                      == Trace_Call__Stack_Node(call_index=1, children=[node_2], frame=sample_frame, func_name='test_add_stack',name='test_Trace_Call__Stack.test_Trace_Call__Stack.test_add_stack', module='test_Trace_Call__Stack')
        assert node_2                                      == Trace_Call__Stack_Node(call_index=2, children=[      ], frame=sample_frame, func_name='test_add_stack',name='test_Trace_Call__Stack.test_Trace_Call__Stack.test_add_stack', module='test_Trace_Call__Stack')



    def test_add_node(self):
        title      = random_string()
        with self.stack as _:
            assert _.size() == 0
            assert _.add_node(title) is not None
            assert _.size() == 1
            assert _.bottom() == _.top()
            assert _.top().info() == f'Stack_Node: call_index:0 | name: {title} | children: 0 | source_code: True'
            assert _.top()        == Trace_Call__Stack_Node(name=title)

    def test_create_stack_node(self):
        create_stack_node = self.stack.create_stack_node
        config            = self.stack.config

        # case 1: with bad data
        assert create_stack_node(frame=None, full_name=None, source_code=None, call_index=None) == Trace_Call__Stack_Node(call_index=None, name=None)
        # case 2: with empty data

        source_code = {'source_code': '', 'source_code_caller': '', 'source_code_location': ''}
        assert create_stack_node(frame=None, full_name='', source_code=source_code, call_index=0) == Trace_Call__Stack_Node()

        # case 2: with valid stack
        assert config.capture_locals is True
        sample_frame = call_stack_current_frame()
        assert create_stack_node(frame=sample_frame, full_name='', source_code=source_code, call_index=0) == Trace_Call__Stack_Node(func_name='test_create_stack_node', frame=sample_frame, locals=sample_frame.f_locals, module = 'test_Trace_Call__Stack')

        # case 3: with valid stack and config.capture_locals set to False
        config.capture_locals = False

        assert create_stack_node(frame=sample_frame, full_name='', source_code=source_code, call_index=0) == Trace_Call__Stack_Node(func_name='test_create_stack_node', frame=sample_frame, module = 'test_Trace_Call__Stack')


    def test_map_full_name(self):
        sample_frame  = call_stack_current_frame()
        map_full_name = self.stack.map_full_name

        # case 1: with bad data
        assert map_full_name(frame=None, module=None, func_name=None) is None
        assert map_full_name(frame=None, module='aa', func_name=None) is None
        assert map_full_name(frame=None, module=None, func_name='bb') is None
        assert map_full_name(frame=None, module='',   func_name='')   is None
        assert map_full_name(frame=None, module='aa', func_name='')   is None
        assert map_full_name(frame=None, module='',   func_name='bb') is None

        # case 2: with good frame and empty module and func_name
        assert map_full_name(frame=sample_frame, module= None, func_name=None) is None
        assert map_full_name(frame=sample_frame, module='aaa', func_name=None) is None
        assert map_full_name(frame=sample_frame, module='aaa', func_name=''  ) is None

        # case 3: with good frame and valid module and func_name
        assert map_full_name(frame=sample_frame, module='aaa', func_name='bbb') == 'aaa.test_Trace_Call__Stack.bbb'

        # case 4: with variations of self value

        mock_frame          = MagicMock()
        mock_instance       = MagicMock()
        expected_class_name = 'YourClassName'
        mock_instance.__class__.__name__ = expected_class_name
        mock_frame.f_locals = {'self': mock_instance }

        assert map_full_name(frame=mock_frame, module='aaa', func_name='bbb') == 'aaa.YourClassName.bbb'
        mock_instance.__class__.__name__  = ''
        assert map_full_name(frame=mock_frame, module='aaa', func_name='bbb') == 'aaa.bbb'

        type(mock_instance).class_name = PropertyMock(side_effect=Exception)    # When __class__.__name__ is accessed, raise an exception
        mock_frame.f_locals = {'self': None}                           # Set the 'self' in f_locals to the mock instance
        assert map_full_name(frame=mock_frame, module='aaa', func_name='bbb') == 'aaa.bbb'

    def test_map_source_code(self):
        sample_frame    = call_stack_current_frame()
        map_source_code = self.stack.map_source_code
        config          = self.stack.config

        # case 1: with trace_capture_source_code set to False
        assert config.trace_capture_source_code is False
        assert map_source_code(sample_frame) == {'source_code': '', 'source_code_caller': '', 'source_code_location': ''}

        # case 2: with trace_capture_source_code set to True
        config.trace_capture_source_code = True
        method_in_frame         = test_Trace_Call__Stack.test_map_source_code
        source_code_file        = __file__
        source_code_line_number = method_line_number(method_in_frame) + 15
        source_code_location    = f'{source_code_file}:{source_code_line_number}'
        source_code             = map_source_code(sample_frame)
        assert  source_code == { 'source_code': 'source_code             = map_source_code(sample_frame)'  ,
                                 'source_code_caller': 'method()'                                       ,
                                 'source_code_location': source_code_location                           }


    def test_push_and_pop(self):
        self.stack.config.capture_duration = True
        test_data = Frames_Test_Data()
        frame_1   = test_data.frame_1
        frame_2   = test_data.frame_2
        frame_3   = test_data.frame_3
        stack = self.stack
        assert stack == []

        node_1 = stack.push(frame_1)       ; assert stack == [node_1]
        node_2 = stack.push(frame_2)       ; assert stack == [node_1,node_2]
        node_3 = stack.push(frame_3)       ; assert stack == [node_1, node_2, node_3]
        node_4 = stack.push(frame_1)       ; assert stack == [node_1, node_2, node_3, node_4]

        assert stack.root_node == node_1
        assert stack.pop(node_1 ) is False ; assert stack == [node_1, node_2, node_3, node_4]
        assert stack.pop(node_2 ) is False ; assert stack == [node_1, node_2, node_3, node_4]
        assert stack.pop(node_3 ) is False ; assert stack == [node_1, node_2, node_3, node_4]
        assert stack.pop(node_4 ) is True  ; assert stack == [node_1, node_2, node_3        ]

        node_5 = stack.push(frame_3)       ; assert stack == [node_1, node_2, node_3, node_5]
        assert stack.pop(node_1 ) is False ; assert stack == [node_1, node_2, node_3, node_5]
        assert stack.pop(node_2 ) is False ; assert stack == [node_1, node_2, node_3, node_5]
        assert stack.pop(node_3 ) is False ; assert stack == [node_1, node_2, node_3, node_5]
        assert stack.pop(node_5 ) is True  ; assert stack == [node_1, node_2, node_3]

        assert stack.pop(frame_1) is False ; assert stack == [node_1, node_2, node_3        ]
        assert stack.pop(frame_2) is False ; assert stack == [node_1, node_2, node_3        ]
        assert stack.pop(frame_3) is True  ; assert stack == [node_1, node_2,               ]

        node_6 = stack.push(frame_1)       ; assert stack == [node_1, node_2, node_6        ]
        assert stack.pop(frame_3) is False ; assert stack == [node_1, node_2, node_6        ]
        assert stack.pop(frame_2) is False ; assert stack == [node_1, node_2, node_6        ]
        assert stack.pop(frame_1) is True  ; assert stack == [node_1, node_2                ]
        assert stack.pop(frame_2) is True  ; assert stack == [node_1                        ]
        assert stack.pop(frame_1) is True  ; assert stack == [                            ]

        assert stack.pop(frame_1) is False
        assert stack.pop(frame_2) is False
        assert stack.pop(frame_3) is False

        assert stack           == []
        assert stack.root_node == node_1

        assert node_1.children == [node_2        ]
        assert node_2.children == [node_3, node_6]
        assert node_3.children == [node_4, node_5]
        assert node_4.children == [              ]
        assert node_5.children == [              ]
        assert node_6.children == [              ]

        assert node_1.frame == frame_1
        assert node_2.frame == frame_2
        assert node_3.frame == frame_3
        assert node_4.frame == frame_1
        assert node_5.frame == frame_3
        assert node_6.frame == frame_1

        assert node_1.call_start < node_1.call_end
        assert node_1.call_duration < 0.001                # these values should be very quick

    def test_stack_top(self):
        test_data = Frames_Test_Data()
        stack     = self.stack
        #stack_top = stack.top()
        assert len(stack) == 0

        root_node = stack.add_node(title='test')
        assert type(root_node) is Trace_Call__Stack_Node
        assert len(stack) == 1
        assert stack == [root_node]

        new_node = stack.add_frame(test_data.frame_1)
        assert len(stack) == 2
        assert stack == [root_node, new_node]

    def test_regression__pop_doesnt_remove_node(self):
        sample_frame = call_stack_current_frame()
        stack        = self.stack
        node_1       = stack.push(sample_frame)             # add frame to the stack
        assert stack == [node_1]
        assert stack.pop(sample_frame) is True              # pop frame from stack              | bug was here
        assert stack == []                                  # check that stack is empyty        | bug was here

class Frames_Test_Data(Kwargs_To_Self):
    frame_1 = None
    frame_2 = None
    frame_3 = None

    def __init__(self):
        super().__init__()
        self.frame_1 = self.get_frame_1()
        self.frame_2 = self.get_frame_2()
        self.frame_3 = self.get_frame_3()

    def get_frame_1(self):
        frame_1 = call_stack_current_frame()
        return frame_1

    def get_frame_2(self):
        frame_2 = call_stack_current_frame()
        return frame_2

    def get_frame_3(self):
        frame_3 =call_stack_current_frame()
        return frame_3