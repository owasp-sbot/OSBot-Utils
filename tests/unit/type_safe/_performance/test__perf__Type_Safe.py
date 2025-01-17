import time
from typing import Any, Dict, List
from unittest import TestCase

from osbot_utils.context_managers.capture_duration import capture_duration
from osbot_utils.type_safe.Type_Safe import Type_Safe

from osbot_utils.utils.Dev import pprint

from osbot_utils.context_managers.print_duration import print_duration


class test__perf__Type_Safe(TestCase):

    def test__python__class_creation(self):             # 50,000 pure Python classes take ~5ms

        size         = 50000
        max_duration = 7            # ms

        class An_Class:
            pass

        with capture_duration() as duration:
            for i in range(size):
                An_Class()
        assert duration.duration < max_duration

    def test__Type_Safe__class_creation(self):      # 10,000 simple Type_Safe classes take ~57ms

        size         = 1
        max_duration = 60            # ms

        class An_Class(Type_Safe):
            pass

        with capture_duration() as duration:
            for i in range(size):
                An_Class()


        #pprint(duration.duration)
        assert duration.duration < max_duration



    # def test__per_counter(self):
    #     class An_Class(Type_Safe):
    #         a: str
    #         b: int
    #     start = time.perf_counter()
    #     An_Class()
    #     end = time.perf_counter()
    #     pprint((end - start))

