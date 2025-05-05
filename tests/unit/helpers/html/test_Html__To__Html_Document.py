from unittest                                           import TestCase
from osbot_utils.helpers.html.Html__To__Html_Document   import Html__To__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Document import Schema__Html_Document
from tests._test_data.Sample_Test_Files                 import Sample_Test_Files


class test_Html__To__Html_Document(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html             = Sample_Test_Files().html_bootstrap_example()            # Load Html sample
        cls.html_to_document = Html__To__Html_Document(html=cls.html)

    def test_convert(self):
        with self.html_to_document as _:
            assert type(_.convert()) is Schema__Html_Document
            assert _.html__document.root_node.attrs == {'lang': 'en'}