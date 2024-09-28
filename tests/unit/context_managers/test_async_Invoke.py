import asyncio
import logging
import typing
from unittest                                   import TestCase
from osbot_utils.context_managers.async_invoke  import async_invoke


class An_Class:

    async def an_async_method(self):
        await asyncio.sleep(0.001)               # just to confirm it async is working
        return 42

class test_async_invoke(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.an_class = An_Class()

    def test__setUpClass(self):
        assert isinstance(self.an_class.an_async_method(),  typing.Coroutine) is True

    def test_async_invoke(self):
        with async_invoke() as _:
            assert _(self.an_class.an_async_method()) == 42





