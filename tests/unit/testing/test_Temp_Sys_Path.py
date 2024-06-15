import sys
from unittest import TestCase

from osbot_utils.testing.Temp_Sys_Path import Temp_Sys_Path


class test_Temp_Sys_Path(TestCase):

    def test_temp_sys_path(self):
        test_path = "/test/path/to/add"

        # Ensure the test_path is not already in sys.path
        self.assertNotIn(test_path, sys.path)

        with Temp_Sys_Path(test_path):
            self.assertIn(test_path, sys.path)

        # Check that the path is removed after exiting the context
        self.assertNotIn(test_path, sys.path)
