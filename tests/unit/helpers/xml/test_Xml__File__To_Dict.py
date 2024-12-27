from unittest                                   import TestCase
from osbot_utils.helpers.xml.Xml__File__Load    import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Dict import Xml__File__To_Dict


class test_Xml__File__To_Dict(TestCase):
    def setUp(self):
        self.loader    = Xml__File__Load()
        self.converter = Xml__File__To_Dict()

    def test_basic_conversion(self):
        xml = '<root attr="value"><child>Text</child></root>'
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result == {
            'attr': 'value',
            'child': 'Text'
        }

    def test_attributes_with_text(self):                                      # Test elements with both attributes and text
        xml = '<root><title type="html">Some text</title></root>'
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result['title'] == {
            'type': 'html',
            '#text': 'Some text'
        }

    def test_nested_with_attributes(self):                                    # Test nested elements with attributes
        xml = '''
            <content url="https://example.com" type="article">
                <title format="plain">Article Title</title>
                <body format="html">Content here</body>
            </content>
        '''
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result == {
            'url': 'https://example.com',
            'type': 'article',
            'title': {
                'format': 'plain',
                '#text': 'Article Title'
            },
            'body': {
                'format': 'html',
                '#text': 'Content here'
            }
        }

    def test_multiple_elements(self):                                         # Test multiple elements
        xml = '''
            <root>
                <item type="first">One</item>
                <item type="second">Two</item>
            </root>
        '''
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result['item'] == [
            {'type': 'first', '#text': 'One'},
            {'type': 'second', '#text': 'Two'}
        ]

    def test_mixed_content(self):                                            # Test mixed content
        xml = '<root status="active">Text <em>Important</em> More Text</root>'
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result['status'] == 'active'
        assert 'Text' in result['#text']
        assert 'More Text' in result['#text']
        assert result['em'] == 'Important'

    def test_empty_elements(self):                                           # Test empty elements
        xml = '<root><empty attr="val"/><blank></blank></root>'
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result == {
            'empty': {'attr': 'val'},
            'blank': {}
        }

    def test_complex_media_content(self):                                    # Test real-world media content example
        xml = '''
            <content url="https://example.com/image.jpg" medium="image">
                <title type="html">image.jpg</title>
                <description type="plain">An image description</description>
            </content>
        '''
        xml_file = self.loader.load_from_string(xml)
        result = self.converter.to_dict(xml_file)

        assert result == {
            'url': 'https://example.com/image.jpg',
            'medium': 'image',
            'title': {
                'type': 'html',
                '#text': 'image.jpg'
            },
            'description': {
                'type': 'plain',
                '#text': 'An image description'
            }
        }