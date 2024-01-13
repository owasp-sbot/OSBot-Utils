from io import StringIO
from pprint import PrettyPrinter
from unittest import TestCase
from unittest.mock import call, patch

import requests
from osbot_utils.utils.Objects import obj_info

from osbot_utils.testing.Patch_Print import Patch_Print
from osbot_utils.utils.Files import pickle_save_to_file

from osbot_utils.utils.trace.Trace_Call import Trace_Call

from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.Hook_Method import Hook_Method


class test_Hook_Method(TestCase):

    def setUp(self) -> None:
        self.target        = requests.api.request
        self.target_module = requests.api
        self.target_method = 'request'
        self.wrap_method = Hook_Method(target_module=self.target_module, target_method=self.target_method)

    def test__init__(self):
        assert self.wrap_method.target        == self.target
        assert self.wrap_method.target_module == self.target_module
        assert self.wrap_method.target_method == self.target_method

    def test___enter__exit__(self):
        assert requests.api.request == self.target
        with self.wrap_method:
            assert requests.api.request == self.wrap_method.wrapper_method
            requests.head('https://www.google.com')
            assert self.wrap_method.calls_count() == 1
        assert requests.api.request == self.target

    def test_after_call(self):
        def on_after_call(return_value,  *args, **kwargs):
            if type(return_value) is str:
                return f'status code: {return_value} {args[0]} {args[1]} {kwargs}'
            else:
                return f'{return_value.status_code}'

        self.wrap_method.add_on_after_call(on_after_call)
        self.wrap_method.add_on_after_call(on_after_call)

        with self.wrap_method:
            requests.head('https://www.google.com')

        assert self.wrap_method.calls_last_one()['return_value'] == "status code: 200 ('head', 'https://www.google.com') {'allow_redirects': False} {}"

    def test_before_call(self):
        assert self.wrap_method.calls_last_one() == None
        def on_before_call(*args, **kwargs):
            args = (args[0], args[1] + '/404')
            return (args, kwargs)

        self.wrap_method.add_on_before_call(on_before_call)

        with self.wrap_method:
            requests.head('https://www.google.com')

        assert self.wrap_method.calls_last_one()['return_value'].status_code == 404

    def test_mock_call(self):
        return_value = 'an result'
        def mock_call (*args, **kwargs):
            assert args   == ('head', 'https://www.google.com')
            assert kwargs == {'allow_redirects': False}
            return return_value

        self.wrap_method.set_mock_call(mock_call)

        with self.wrap_method:
            def an_method():
                assert requests.head('https://www.google.com') == return_value
            an_method()

        call_stack = self.wrap_method.calls[0]['call_stack']                            # we need to remove this from the call since assert with __repr__ wasn't working
        del self.wrap_method.calls[0]['call_stack']
        assert call_stack.stack_lines__calls() == [ '\x1b[34m┌ requests.api.head\x1b[0m'              ,
                                                    '\x1b[0m│ test_Hook_Method.an_method\x1b[0m'      ,
                                                    '\x1b[32m└ test_Hook_Method.test_mock_call\x1b[0m']

        assert self.wrap_method.calls == [{ 'args'        : ('head', 'https://www.google.com'),
                                            'duration'    : 0                                 ,
                                            'exception'   : None                              ,
                                            'index'       : 0                                 ,
                                            'kwargs'      : {'allow_redirects': False         },
                                            'return_value': 'an result'                       }]


    def test_wrap__unwrap(self):                    # todo: refactor this to use a class that doesn't take so long
        assert requests.api.request == self.target

        self.wrapped_method = self.wrap_method.wrap()

        assert requests.api.request != self.target
        assert requests.api.request == self.wrap_method.wrapper_method

        kwargs = { 'method': 'HEAD', 'url':'https://www.google.com'}

        requests.api.request(method='HEAD', url='https://www.google.com')
        requests.api.request(**kwargs)
        requests.head       ('https://www.google.com')
        requests.get        ('https://www.google.com/404')

        assert self.wrap_method.calls_count()            == 4
        assert self.wrap_method.calls[0]['args'        ] == ()
        assert self.wrap_method.calls[0]['kwargs'      ] == {'method': 'HEAD', 'url': 'https://www.google.com'}
        assert self.wrap_method.calls[0]['return_value'].status_code == 200
        assert self.wrap_method.calls[1]['args'        ] == ()
        assert self.wrap_method.calls[1]['kwargs'      ] == {'method': 'HEAD', 'url': 'https://www.google.com'}
        assert self.wrap_method.calls[1]['return_value'].status_code == 200
        assert self.wrap_method.calls[2]['args'        ] == ('head', 'https://www.google.com')
        assert self.wrap_method.calls[2]['kwargs'      ] == {'allow_redirects': False}
        assert self.wrap_method.calls[2]['return_value'].status_code == 200
        assert self.wrap_method.calls[3]['args'        ] == ('get', 'https://www.google.com/404')
        assert self.wrap_method.calls[3]['kwargs'      ] == {'params': None}
        assert self.wrap_method.calls[3]['return_value'].status_code == 404

        self.wrap_method.unwrap()

        assert requests.api.request == self.target


    def test_wrap__unwrap___check_original(self):
        assert requests.api.request == self.target


    # todo: add use of Mem_Graph to calculate all paths, namely the ones from _safe_repr
    def test__hook_and_check_call_stack(self):
        # this is a really cool examle which shows both Trace_Call and Hook_Method in action

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with Trace_Call() as _:
                _.config.all()#.trace_enabled = False
            #_.config.trace_show_internals = True
            #_.config.trace_capture_lines = True
                def an_method():
                    pprint('in trace')
                an_method()

        assert fake_out.getvalue() ==("\n'in trace'\n"
                                      '\n--------- CALL TRACER ----------'
                                      '\nHere are the 6 traces captured\n'
                                      '\n\x1b[1m📦  \x1b[38;2;138;148;138m\x1b[0m.\x1b[1mTrace Session\x1b[0m\x1b[0m\n'
                                      '\x1b[1m│   └── 🔗️ \x1b[38;2;138;148;138mtest_Hook_Method\x1b[0m.\x1b[1man_method\x1b[0m\x1b[0m\n'
                                      '\x1b[1m│       └── 🔗️ \x1b[38;2;138;148;138mDev\x1b[0m.\x1b[1mpprint\x1b[0m\x1b[0m\n'
                                      '\x1b[1m│           └── 🔗️ \x1b[38;2;138;148;138mpprint\x1b[0m.\x1b[1mpprint\x1b[0m\x1b[0m\n'
                                      '\x1b[1m│               └── 🔗️ \x1b[38;2;138;148;138mPrettyPrinter\x1b[0m.\x1b[1mpprint\x1b[0m\x1b[0m\n'
                                      '\x1b[1m└────────────────────── 🧩️ \x1b[38;2;138;148;138mPrettyPrinter\x1b[0m.\x1b[1mformat\x1b[0m\x1b[0m\n') != "\n'in trace'\n"

        #_.print_lines()
        #pprint(_.stats_data())
        #pprint(_.view_data())


        with Hook_Method(target_module=PrettyPrinter, target_method='_safe_repr') as _:
            pprint('in hook')

        call_stack = _.calls[0].get('call_stack')
        assert _.calls[0].get('return_value') == ("'in hook'", True, False)

        #call_stack.max_depth = 20
        #call_stack.print_table()

        with Patch_Print() as _:
            call_stack.print__source_code()
            assert _.call_args_list() == [call('\x1b[34m┌ return self._safe_repr(object, context, maxlevels, level)\x1b[0m'),
                                          call('\x1b[0m│ repr, readable, recursive = self.format(object, context.copy(),\x1b[0m'),
                                          call('\x1b[0m│ rep = self._repr(object, context, level)\x1b[0m'),
                                          call('\x1b[0m│ self._format(object, self._stream, 0, 0, {}, 0)\x1b[0m'),
                                          call('\x1b[0m│ printer.pprint(object)\x1b[0m'),
                                          call('\x1b[0m│ original_pprint.pprint(arg, indent=2)       # use a pprint to format\x1b[0m'),
                                          call("\x1b[32m└ pprint('in hook')\x1b[0m")]

        with Patch_Print() as _:
            call_stack.print()
            assert _.call_args_list() == [call('\x1b[34m┌ pprint.format\x1b[0m'),
                                      call('\x1b[0m│ pprint._repr\x1b[0m'),
                                      call('\x1b[0m│ pprint._format\x1b[0m'),
                                      call('\x1b[0m│ pprint.pprint\x1b[0m'),
                                      call('\x1b[0m│ pprint.pprint\x1b[0m'),
                                      call('\x1b[0m│ osbot_utils.utils.Dev.pprint\x1b[0m'),
                                      call('\x1b[32m└ test_Hook_Method.test__hook_and_check_call_stack\x1b[0m')]



