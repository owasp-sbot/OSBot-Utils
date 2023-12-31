from unittest import TestCase
import requests

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
            assert requests.head('https://www.google.com') == return_value

        assert self.wrap_method.calls == [{ 'args'        : ('head', 'https://www.google.com'),
                                            'duration'    : 0 ,
                                            'index'       : 0 ,
                                            'kwargs'      : {'allow_redirects': False},
                                            'return_value': 'an result'}]


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
