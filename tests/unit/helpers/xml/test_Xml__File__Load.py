from unittest                                import TestCase
from xml.etree.ElementTree                   import ParseError
from osbot_utils.helpers.xml.Xml__Element    import XML__Element
from osbot_utils.helpers.xml.Xml__File       import Xml__File
from osbot_utils.helpers.xml.Xml__File__Load import Xml__File__Load

class test_Xml__File__Load(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml_loader = Xml__File__Load()

    def setUp(self):                                                  # Core test data setup
        self.test_xml = '''<?xml version="1.0" encoding="UTF-8"?>
                          <root xmlns:test="http://test.com">
                              <child attr="value">Text</child>
                              <test:element>Namespaced</test:element>
                          </root>'''

    def test_load_from_string(self):                                 # Basic loading test
        xml_file = self.xml_loader.load_from_string(self.test_xml)
        assert isinstance(xml_file, Xml__File)
        assert isinstance(xml_file.root_element, XML__Element)
        assert xml_file.namespaces == {'test': 'http://test.com'}

    def test_load_invalid_xml(self):                                # Invalid XML handling
        invalid_xmls = ['<root><unclosed></root>',                  # Mismatched tags
                        '<root></>'              ,                  # Empty tag
                        '<<root>>'               ,                  # Double brackets
                        '<root xmlns:="invalid">',                  # Invalid namespace
                        '<1root></1root>'        ]                  # Invalid tag name
        for xml in invalid_xmls:
            with self.assertRaises(ParseError):
                self.xml_loader.load_from_string(xml)


    def test_load_empty_or_none(self):                             # Empty or None input handling
        empty_inputs__ParseError = ['   ' ,                        # Whitespace only
                                    '\n\t']                        # Newlines and tabs

        empty_inputs__ValueError = [''  ,                          # Empty string
                                    None]                          # None value
        for xml in empty_inputs__ParseError:
            with self.assertRaises(ParseError):
                self.xml_loader.load_from_string(xml)

        for xml in empty_inputs__ValueError:
            with self.assertRaises(ValueError):
                self.xml_loader.load_from_string(xml)

    def test_namespace_variations(self):                           # Namespace handling variations
        namespace_xmls = {
            # Default namespace
            '<root xmlns="http://default.com"><child>text</child></root>':
                {'': 'http://default.com'},

            # Multiple namespaces
            '''<root xmlns:ns1="http://ns1.com" xmlns:ns2="http://ns2.com">
                   <ns1:child>text</ns1:child>
               </root>''':
                {'ns1': 'http://ns1.com', 'ns2': 'http://ns2.com'},

            # Nested namespaces
            '''<root xmlns:outer="http://outer.com">
                   <child xmlns:inner="http://inner.com">
                       <inner:elem>text</inner:elem>
                   </child>
               </root>''':
                {'outer': 'http://outer.com', 'inner': 'http://inner.com'}
        }

        for xml, expected_namespaces in namespace_xmls.items():
            #with self.subTest(xml=xml):
                xml_file = self.xml_loader.load_from_string(xml)
                assert all(ns in xml_file.namespaces for ns in expected_namespaces)

    def test_attribute_variations(self):                          # Attribute variations
        xml = '''<root id="1" empty="" space="a b">
                    <child ns:attr="value" xmlns:ns="http://ns.com"/>
                    <mix attr1="one" attr2="two"/>
                 </root>'''
        xml_file = self.xml_loader.load_from_string(xml)
        root = xml_file.root_element

        assert root.attributes['id'].value == '1'                    # Normal attribute
        assert root.attributes['empty'].value == ''                  # Empty attribute
        assert root.attributes['space'].value == 'a b'              # Space in value

        child = root.children[0]
        ns_key = '{http://ns.com}attr'
        assert ns_key in child.attributes                           # Namespaced attribute with full URI
        assert child.attributes[ns_key].namespace == 'http://ns.com'
        assert child.attributes[ns_key].name == 'attr'
        assert child.attributes[ns_key].value == 'value'

        mix = root.children[1]
        assert len(mix.attributes) == 2                             # Multiple attributes

    def test_text_content_variations(self):                      # Text content variations
        xml = '''<root>
                     Plain text
                     <a>Element text</a>
                     Mixed <b>content</b> here
                     <c>  Whitespace  </c>
                     <d></d>
                     <e/>
                 </root>'''
        xml_file = self.xml_loader.load_from_string(xml)
        root = xml_file.root_element

        assert 'Plain text' in root.children                     # Direct text content
        assert root.children[1].children[0] == 'Element text'    # Element text
        assert root.children[2] == 'Mixed'                       # Mixed content start
        assert root.children[4] == 'here'                        # Mixed content end
        assert root.children[5].children[0] == 'Whitespace'      # Whitespace handling

    def test_special_characters(self):                          # Special character handling
        xml = '''<root>
                     <a>&lt;escaped&gt;</a>
                     <b>&#65;</b>
                     <c>Text &amp; more</c>
                     <d>Üñîçødé</d>
                 </root>'''
        xml_file = self.xml_loader.load_from_string(xml)
        root = xml_file.root_element

        assert root.children[0].children[0] == '<escaped>'      # XML escapes
        assert root.children[1].children[0] == 'A'              # Numeric character reference
        assert root.children[2].children[0] == 'Text & more'    # Ampersand handling
        assert root.children[3].children[0] == 'Üñîçødé'        # Unicode characters

    def test_deep_nesting(self):                               # Deep nesting handling
        size = 10  # 100
        xml = '<a>' + '<b>' * size + 'text' + '</b>' * size + '</a>'
        xml_file = self.xml_loader.load_from_string(xml)

        current = xml_file.root_element
        depth = 0
        while current.children and isinstance(current.children[0], XML__Element):
            current = current.children[0]
            depth += 1
            assert current.tag == 'b'

        assert depth == size                                     # Verify nesting depth
        assert current.children[0] == 'text'                    # Verify deepest content

    def test_large_document(self):                             # Large document handling
        size = 10 # 1000
        large_xml = '<?xml version="1.0"?><root>' + \
                   '<item>text</item>' * size + \
                   '</root>'
        xml_file = self.xml_loader.load_from_string(large_xml)
        root = xml_file.root_element

        assert len(root.children) == size                      # Verify number of children
        assert all(child.tag == 'item' for child in root.children if isinstance(child, XML__Element))
        assert all(child.children[0] == 'text' for child in root.children if isinstance(child, XML__Element))

    def test_namespace_attribute_handling(self):                 # Comprehensive namespace attribute testing
        xml = '''<root xmlns:a="http://a.com" xmlns:b="http://b.com">
                    <a:elem1 b:attr1="value1" a:attr2="value2">
                        <b:elem2 a:attr3="value3" attr4="value4"/>
                    </a:elem1>
                    <elem3 xmlns:c="http://c.com" c:attr5="value5"/>
                </root>'''
        xml_file = self.xml_loader.load_from_string(xml)
        root = xml_file.root_element

        # First level element attributes
        elem1 = root.children[0]
        assert elem1.tag == 'elem1'                                # Namespace stripped from tag

        b_attr1 = '{http://b.com}attr1'
        assert b_attr1 in elem1.attributes                        # b namespace attribute
        assert elem1.attributes[b_attr1].namespace == 'http://b.com'
        assert elem1.attributes[b_attr1].name == 'attr1'
        assert elem1.attributes[b_attr1].value == 'value1'

        a_attr2 = '{http://a.com}attr2'
        assert a_attr2 in elem1.attributes                        # a namespace attribute
        assert elem1.attributes[a_attr2].namespace == 'http://a.com'
        assert elem1.attributes[a_attr2].name == 'attr2'
        assert elem1.attributes[a_attr2].value == 'value2'

        # Nested element attributes
        elem2 = elem1.children[0]
        assert elem2.tag == 'elem2'

        a_attr3 = '{http://a.com}attr3'
        assert a_attr3 in elem2.attributes                        # a namespace in nested element
        assert elem2.attributes[a_attr3].namespace == 'http://a.com'
        assert elem2.attributes[a_attr3].name == 'attr3'

        assert 'attr4' in elem2.attributes                        # non-namespaced attribute
        assert elem2.attributes['attr4'].namespace == ''

        # Locally declared namespace
        elem3 = root.children[1]
        c_attr5 = '{http://c.com}attr5'
        assert c_attr5 in elem3.attributes                        # local namespace attribute
        assert elem3.attributes[c_attr5].namespace == 'http://c.com'
        assert elem3.attributes[c_attr5].name == 'attr5'
        assert elem3.attributes[c_attr5].value == 'value5'