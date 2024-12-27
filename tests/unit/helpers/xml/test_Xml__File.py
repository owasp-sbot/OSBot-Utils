from unittest                                   import TestCase
from osbot_utils.base_classes.Type_Safe__Dict   import Type_Safe__Dict
from osbot_utils.helpers.xml.Xml__Element       import XML__Element
from osbot_utils.helpers.xml.Xml__File          import Xml__File

class test_Xml__File(TestCase):
    def setUp(self):
        self.xml_data = '<root><child>test</child></root>'
        self.xml_file = Xml__File(xml_data=self.xml_data)

    def test_create_file(self):                                                # Test file creation
        assert self.xml_file.xml_data           == self.xml_data
        assert type(self.xml_file.root_element) is XML__Element
        assert type(self.xml_file.namespaces)   is Type_Safe__Dict

    def test_file_with_namespaces(self):                                      # Test namespace initialization
        xml_file = Xml__File(xml_data=self.xml_data,
                             namespaces={'ns': 'http://example.com'} )
        assert xml_file.namespaces['ns'] == 'http://example.com'