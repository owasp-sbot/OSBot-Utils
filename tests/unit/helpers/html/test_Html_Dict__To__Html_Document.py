from unittest                                               import TestCase
from osbot_utils.helpers.duration.decorators.print_duration import print_duration
from osbot_utils.helpers.html.Html_Dict__To__Html_Document  import Html_Dict__To__Html_Document
from osbot_utils.helpers.html.Html__To__Html_Dict import Html__To__Html_Dict, STRING__SCHEMA_NODES
from osbot_utils.helpers.html.schemas.Schema__HTML_Document import Schema__HTML_Document
from tests._test_data.Sample_Test_Files                     import Sample_Test_Files


class test_Html_Dict__To__Html_Document(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html         = Sample_Test_Files().html_bootstrap_example()            # Load HTML sample
        cls.html_dict    = Html__To__Html_Dict(html=cls.html).convert()
        cls.html_to_json = Html_Dict__To__Html_Document(html__dict=cls.html_dict)

    def test_convert(self):
        with self.html_to_json as _:
            assert type(_.convert()) is Schema__HTML_Document
            assert _.html__document.root_node.json()                      == _.html__dict
            assert _.html__document.root_node.attrs                       == {'lang': 'en'}
            assert _.html__document.root_node.tag                         == 'html'
            assert _.html__dict.get('attrs'                             ) == {'lang': 'en'}
            assert _.html__dict.get(STRING__SCHEMA_NODES)[0].get('attrs') == {}


