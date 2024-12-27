from unittest                                   import TestCase
from osbot_utils.helpers.xml.Xml__File__Load    import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Xml  import Xml__File__To_Xml

class test_Xml__File__To_Xml(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml_file_load   = Xml__File__Load()
        cls.xml_file_to_xml = Xml__File__To_Xml()

    def setUp(self):                                                         # Core test data setup
        self.basic_xml = '<root><child>test</child></root>'
        self.basic_file = self.xml_file_load.load_from_string(self.basic_xml)

    def test_convert_basic_xml(self):                                       # Test basic XML conversion
        result = self.xml_file_to_xml.convert_to_xml(self.basic_file, pretty_print=False)
        assert '<root><child>test</child></root>' in result

    def test_convert_with_attributes(self):                                 # Test attribute handling
        xml = '<root id="1"><child attr="value">test</child></root>'
        xml_file = self.xml_file_load.load_from_string(xml)
        result = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)
        assert 'id="1"' in result
        assert 'attr="value"' in result

    def test_convert_with_namespaces(self):                                # Test namespace handling
        xml = ( '<?xml version="1.0" ?>\n'
                '<root xmlns:test="http://test.com">\n'
                '  <test:child>Namespaced</test:child>\n'
                '</root>')
        xml_file = self.xml_file_load.load_from_string(xml)
        result   = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=True)
        assert xml_file.json() == {'namespaces': {'test': 'http://test.com'},
                                   'root_element': { 'attributes': {},
                                                     'children': [ { 'attributes': {},
                                                                     'children': ['Namespaced'],
                                                                     'namespace': 'http://test.com',
                                                                     'namespace_prefix': 'test',
                                                                     'tag': 'child'}],
                                                     'namespace': '',
                                                     'namespace_prefix': '',
                                                     'tag': 'root'},
                                   'xml_data': '<?xml version="1.0" ?>\n'
                                               '<root xmlns:test="http://test.com">\n'
                                               '  <test:child>Namespaced</test:child>\n'
                                               '</root>'}
        assert result          == xml

    def test_convert_with_nested_elements(self):                           # Test nested element handling
        xml = '''<root>
                    <level1>
                        <level2>Deep</level2>
                    </level1>
                 </root>'''
        xml_file = self.xml_file_load.load_from_string(xml)
        result = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)
        assert '<level1><level2>Deep</level2></level1>' in result

    def test_convert_with_text_variations(self):                           # Test text content variations
        xml = '''<root>
                    Plain text
                    <a>Element text</a>
                    Mixed <b>content</b> here
                    <c>  Whitespace  </c>
                 </root>'''
        xml_file = self.xml_file_load.load_from_string(xml)
        result = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)
        assert 'Plain text' in result
        assert '<a>Element text</a>' in result
        assert 'Mixed' in result
        assert '<b>content</b>' in result
        assert 'here' in result
        assert '<c>Whitespace</c>' in result

    def test_convert_special_characters(self):                             # Test special character handling
        xml = '''<root>
                    <a>&lt;escaped&gt;</a>
                    <b>&#65;</b>
                    <c>Text &amp; more</c>
                    <d>Üñîçødé</d>
                 </root>'''
        xml_file = self.xml_file_load.load_from_string(xml)
        result = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)
        assert '&lt;escaped&gt;' in result
        assert 'A' in result
        assert 'Text &amp; more' in result
        assert 'Üñîçødé' in result

    def test_convert_empty_elements(self):                                 # Test empty element handling
        xml = '<root><empty/><blank></blank></root>'
        xml_file = self.xml_file_load.load_from_string(xml)
        result = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)
        assert '<empty />' in result or '<empty/>' in result
        assert '<blank />' in result or '<blank></blank>' in result

    def test_convert_namespace_variations(self):                           # Test namespace variations
        xml      = '<root xmlns="http://default.com"><child>text</child></root>'
        xml_file = self.xml_file_load.load_from_string(xml)
        result   = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)


        original_loaded = self.xml_file_load.load_from_string(xml)
        result_loaded   = self.xml_file_load.load_from_string(result)

        assert result                     == xml                                # Verify XML content roundtrip
        assert original_loaded.namespaces == result_loaded.namespaces           # Verify correct handling of default namespace
        assert original_loaded.json()     == result_loaded.json()               # Verify overall structure remains identical

    def test_empty_or_invalid_input(self):                                      # Test error handling
        with self.assertRaises(ValueError):
            xml_file = self.xml_file_load.load_from_string('<root/>')
            xml_file.root_element = None
            self.xml_file_to_xml.convert_to_xml(xml_file)

    def test_convert_large_document(self):                                # Test large document handling
        size = 10 # 1000
        xml = '<?xml version="1.0"?><root>' + '<item>text</item>' * size + '</root>'
        xml_file = self.xml_file_load.load_from_string(xml)
        result = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)
        assert result.count('<item>text</item>') == size

    def test_convert_with_deep_nesting(self):                            # Test deep nesting
        size = 10  # 100
        xml = '<a>' + '<b>' * size + 'text' + '</b>' * size + '</a>'
        xml_file = self.xml_file_load.load_from_string(xml)
        result = self.xml_file_to_xml.convert_to_xml(xml_file, pretty_print=False)
        assert result.count('<b>') == size
        assert result.count('</b>') == size
        assert 'text' in result