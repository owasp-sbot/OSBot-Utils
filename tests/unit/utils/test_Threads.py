import asyncio
import typing
from unittest import TestCase

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.context_managers.async_invoke import async_invoke
from osbot_utils.utils.Threads import invoke_async_function


class An_Class(Type_Safe):
    value : int = 41

    async def an_async_method(self):
        await asyncio.sleep(0.0001)               # just to confirm it async is working
        self.value += 1
        return self.value

class test_Threads(TestCase):

    def setUp(cls):
        cls.an_class = An_Class()

    def test__setUpClass(self):
        assert isinstance(self.an_class.an_async_method(), typing.Coroutine) is True

    def test_invoke_async_function(self):
        assert invoke_async_function(self.an_class.an_async_method()) == 42

    def test__with_multiple_event_loops(self):
        with async_invoke() as _:
            assert _(self.an_class.an_async_method()) == 42
            assert invoke_async_function(self.an_class.an_async_method()) == 43
            assert _(self.an_class.an_async_method()) == 44
            with async_invoke() as __:
                assert _(self.an_class.an_async_method()) == 45
                assert __(self.an_class.an_async_method()) == 46
                assert invoke_async_function(self.an_class.an_async_method()) == 47
                assert __(self.an_class.an_async_method()) == 48
                assert _(self.an_class.an_async_method()) == 49
            assert _(self.an_class.an_async_method()) == 50