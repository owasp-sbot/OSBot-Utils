from unittest import TestCase

from osbot_utils.helpers.ast.builder.Ast__Code__Templates import Ast__Code__Templates
from osbot_utils.utils.Dev import pprint


class test_Ast__Code__Templates(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ast_code_templates = Ast__Code__Templates

    def test_flask_app_template(self):
        with self.ast_code_templates as _:
            builder = _.flask_app_template()
            pprint(builder)