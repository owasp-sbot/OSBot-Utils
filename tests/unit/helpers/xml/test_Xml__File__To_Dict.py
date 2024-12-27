from unittest                                   import TestCase
from osbot_utils.helpers.xml.Xml__File__Load    import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Dict import Xml__File__To_Dict


class test_Xml__File__To_Dict(TestCase):
    def setUp(self):
        self.loader    = Xml__File__Load()
        self.converter = Xml__File__To_Dict()

    def test_basic_conversion(self):                                          # Test basic conversion
        xml = '<root attr="value"><child>Text</child></root>'
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result == {
            'attr': 'value',
            'child': 'Text'
        }

    def test_nested_conversion(self):                                         # Test nested structures
        xml = '''<root>
                    <level1>
                        <level2>Deep</level2>
                    </level1>
                </root>'''
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result['level1']['level2'] == 'Deep'

    def test_multiple_elements(self):                                         # Test multiple elements
        xml = '''<root>
                    <item>First</item>
                    <item>Second</item>
                </root>'''
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result['item'] == ['First', 'Second']

    def test_mixed_content(self):                                            # Test mixed content
        xml = '<root>Text <em>Important</em> More Text</root>'
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert 'Text' in result['_text']
        assert 'More Text' in result['_text']
        assert result['em'] == 'Important'

    def test_empty_elements(self):                                           # Test empty elements
        xml      = '<root><empty/><blank></blank></root>'
        xml_file = self.loader.load_from_string(xml)
        result   = self.converter.to_dict(xml_file)
        assert result == {'blank': {}, 'empty': {}}

