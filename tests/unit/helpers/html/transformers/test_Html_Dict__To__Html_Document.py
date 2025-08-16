from unittest                                                            import TestCase
from osbot_utils.helpers.html.transformers.Html_Dict__To__Html_Document  import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.transformers.Html_Document__To__Html_Dict  import Html_Document__To__Html_Dict
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict           import Html__To__Html_Dict, STRING__SCHEMA_NODES
from osbot_utils.helpers.html.schemas.Schema__Html_Document              import Schema__Html_Document
from tests._test_data.Sample_Test_Files                                  import Sample_Test_Files

class test_Html_Dict__To__Html_Document(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html         = Sample_Test_Files().html_bootstrap_example()            # Load Html sample
        cls.html_dict    = Html__To__Html_Dict(html=cls.html).convert()
        cls.html_to_json = Html_Dict__To__Html_Document(html__dict=cls.html_dict)

    def test_convert(self):
        with self.html_to_json as _:
            assert type(_.convert()) is Schema__Html_Document

            assert _.html__document.root_node.attrs == {'lang': 'en'}                           #  verify the conversion worked
            assert _.html__document.root_node.tag == 'html'

            converter = Html_Document__To__Html_Dict(html__document=_.html__document)           # To compare dictionaries, convert back
            converted_back = converter.convert()
            assert converted_back == _.html__dict



