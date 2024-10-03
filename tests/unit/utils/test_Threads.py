import asyncio
import typing
from unittest import TestCase

import pytest

from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.context_managers.async_invoke import async_invoke
from osbot_utils.utils.Threads import invoke_async_function, invoke_in_new_event_loop


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

    def test_invoke_in_new_event_loop(self):
        async def an_method():
            return 42
        assert invoke_in_new_event_loop(an_method()) == 42

        async def inception_level_1(value_1):
            async def inception_level_3(value_3):
                return value_3
            def inception_level_2(value_2):
                return invoke_in_new_event_loop(inception_level_3(value_2+1))
            return inception_level_2(value_1+1)

        assert invoke_in_new_event_loop(inception_level_1(1)) == 3

    def test_invoke_in_new_event_loop__exception(self):            # Test handling of exceptions within the coroutine
        async def failing_coro():
            raise ValueError("Test exception")

        with pytest.raises(ValueError, match="Test exception") as context:
            invoke_in_new_event_loop(failing_coro())
        assert context.value.args[0] == "Test exception"            # Assert exception raised


    def test_invoke_in_new_event_loop__non_coroutine(self):         # Test handling of non-coroutine inputs
        with pytest.raises(TypeError) as context:
            invoke_in_new_event_loop(42)
        assert context.value.args[0] == "An asyncio.Future, a coroutine or an awaitable is required"


    def test_invoke_in_new_event_loop__asyncio_sleep(self):         # Test with an async I/O operation
        async def sleep_coro():
            await asyncio.sleep(0.1)
            return 'slept'

        result = invoke_in_new_event_loop(sleep_coro())             # Assert that the coroutine returns the expected result after sleep
        assert result == 'slept'

    def test_invoke_in_new_event_loop__concurrent(self):            # Test concurrent invocations of the helper function
        async def coro(n):
            await asyncio.sleep(0.1)
            return n

        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(invoke_in_new_event_loop, coro(i)) for i in range(5)]
            results = [future.result() for future in futures]
            assert results == [0, 1, 2, 3, 4]                       # Assert that all concurrent invocations return correct results

    def test_invoke_in_new_event_loop__nested_calls(self):          # Test nested calls to the helper function
        async def coro(n):
            if n <= 0:
                return n
            else:
                return invoke_in_new_event_loop(coro(n - 1)) + 1

        result = invoke_in_new_event_loop(coro(5))
        assert result == 5                                         # Assert that nested invocations return the correct cumulative result


    def test_invoke_in_new_event_loop__multiple_invocations(self):  # Test multiple successive invocations
        async def coro():
            return 42

        for _ in range(10):
            assert invoke_in_new_event_loop(coro()) == 42


