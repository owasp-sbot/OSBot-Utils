from unittest                                   import TestCase
from osbot_utils.helpers.xml.Xml__Element       import XML__Element
from osbot_utils.helpers.xml.Xml__File__Load    import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Xml  import Xml__File__To_Xml

class test_Xml__Large_Files(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.xml_loader = Xml__File__Load()
        cls.xml_to_xml = Xml__File__To_Xml()

    def test_large_soap_message(self):
        # Test handling of large SOAP message with deep nesting and namespaces
        soap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope                 
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <soapenv:Header>
                    <ns1:RequestHeader
                        soapenv:actor="http://schemas.xmlsoap.org/soap/actor/next"
                        soapenv:mustUnderstand="0"
                        xmlns:ns1="https://www.google.com/apis/ads/publisher/v202308">
                        <ns1:networkCode>123456</ns1:networkCode>
                        <ns1:applicationName>large_soap_test</ns1:applicationName>
                    </ns1:RequestHeader>
                </soapenv:Header>
                <soapenv:Body>
                    <ns2:payload xmlns:ns2="http://example.com/payload">
                        {"<ns2:item>test data</ns2:item>" * 10}
                    </ns2:payload>
                </soapenv:Body>
            </soapenv:Envelope>'''

        xml_file = self.xml_loader.load_from_string(soap_xml)

        # Verify structure
        root = xml_file.root_element
        assert root.tag == 'Envelope'
        assert root.namespace == 'http://schemas.xmlsoap.org/soap/envelope/'

        # Verify namespaces
        assert len(xml_file.namespaces) >= 4
        assert xml_file.namespaces['soapenv'] == 'http://schemas.xmlsoap.org/soap/envelope/'
        assert xml_file.namespaces['xsd'] == 'http://www.w3.org/2001/XMLSchema'

        # Test roundtrip
        result      = self.xml_to_xml.convert_to_xml(xml_file, pretty_print=True)
        result_file = self.xml_loader.load_from_string(result)
        assert dict(result_file.namespaces) == {'ns0': 'http://schemas.xmlsoap.org/soap/envelope/',
                                                **xml_file.namespaces}

    def test_large_rss_feed(self):
        # Test handling of large RSS feed with multiple entries
        size      = 3 # 500
        rss_items = []
        for i in range(size):  # Create 10 RSS items
            rss_items.append(f'''
                <item>
                    <title>Article {i}</title>
                    <link>http://example.com/article/{i}</link>
                    <description>This is a long description for article {i} with some special characters: &amp; &lt; &gt;</description>
                    <pubDate>Mon, 12 Feb 2024 10:{i:02d}:00 GMT</pubDate>
                    <guid>http://example.com/article/{i}</guid>
                    <category>Test Category {i % 10}</category>
                    <content:encoded><![CDATA[
                        <div>
                            <h1>Article {i}</h1>
                            <p>Detailed content with <b>formatting</b> and special characters: & < ></p>
                            {"<div>Nested content level 1</div>" * 5}
                        </div>
                    ]]></content:encoded>
                </item>''')

        rss_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0" 
                 xmlns:content="http://purl.org/rss/1.0/modules/content/"
                 xmlns:dc="http://purl.org/dc/elements/1.1/"
                 xmlns:media="http://search.yahoo.com/mrss/">
                <channel>
                    <title>Large RSS Feed Test</title>
                    <link>http://example.com</link>
                    <description>Testing large RSS feed handling</description>
                    <language>en-us</language>
                    <lastBuildDate>Mon, 12 Feb 2024 12:00:00 GMT</lastBuildDate>
                    {"".join(rss_items)}
                </channel>
            </rss>'''

        xml_file = self.xml_loader.load_from_string(rss_xml)

        # Verify basic structure
        assert xml_file.root_element.tag == 'rss'
        channel = xml_file.root_element.children[0]
        assert channel.tag == 'channel'

        # Count items
        items = [child for child in channel.children if isinstance(child, XML__Element) and child.tag == 'item']
        assert len(items) == size

        # Test roundtrip
        result = self.xml_to_xml.convert_to_xml(xml_file, pretty_print=False)
        result_file = self.xml_loader.load_from_string(result)
        assert len([child for child in result_file.root_element.children[0].children
                   if isinstance(child, XML__Element) and child.tag == 'item']) == size


    # todo: fix these tests
    # def test_deeply_nested_large_xml(self):
    #     # Create a deeply nested structure with lots of attributes and mixed content
    #     def create_nested_element(depth, width):
    #         if depth == 0:
    #             return f'<leaf attr{width}="value{width}">Content {width}</leaf>'
    #
    #         children = []
    #         for i in range(width):
    #             children.append(create_nested_element(depth - 1, width))
    #
    #         return f'''<level{depth}
    #                     attr{depth}="value{depth}"
    #                     ns{depth}:attr="ns_value{depth}"
    #                     xmlns:ns{depth}="http://example.com/ns{depth}">
    #                     Text at level {depth}
    #                     {"".join(children)}
    #                     More text at level {depth}
    #                 </level{depth}>'''
    #
    #     large_nested_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    #         <root xmlns="http://example.com/default">
    #             {create_nested_element(5, 5)}
    #         </root>'''
    #
    #     xml_file = self.xml_loader.load_from_string(large_nested_xml)
    #
    #     # Verify namespaces
    #     assert '' in xml_file.namespaces  # Default namespace
    #     assert all(f'ns{i}' in xml_file.namespaces for i in range(1, 6))
    #
    #     # Test structure
    #     def verify_element(element, expected_depth):
    #         if expected_depth == 0:
    #             assert element.tag == 'leaf'
    #             return
    #
    #         assert element.tag == f'level{expected_depth}'
    #         children = [child for child in element.children if isinstance(child, XML__Element)]
    #         assert len(children) == 5
    #
    #         for child in children:
    #             verify_element(child, expected_depth - 1)
    #
    #     verify_element(xml_file.root_element.children[0], 5)
    #
    #     # Test roundtrip
    #     result = self.xml_to_xml.convert_to_xml(xml_file, pretty_print=False)
    #     result_file = self.xml_loader.load_from_string(result)
    #     assert xml_file.namespaces == result_file.namespaces
    #
    # def test_xml_with_large_attributes(self):
    #     # Test handling of elements with many attributes
    #     attributes = []
    #     values = []
    #     for i in range(100):  # Create 100 attributes per element
    #         attributes.append(f'attr{i}="value{i}"')
    #         values.append(f'value{i}')
    #
    #     xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    #         <root>
    #             <element {"".join(f'ns{i}:attr{i}="ns_value{i}" xmlns:ns{i}="http://example.com/ns{i}" ' for i in range(50))}>
    #                 {"".join(f'<child{i} {" ".join(attributes)}>{i}</child{i}>' for i in range(50))}
    #             </element>
    #         </root>'''
    #
    #     xml_file = self.xml_loader.load_from_string(xml)
    #
    #     # Verify structure
    #     element = xml_file.root_element.children[0]
    #     assert len(element.attributes) >= 50  # Including namespace declarations
    #
    #     # Verify attribute values
    #     for i in range(50):
    #         ns_attr = f'{{http://example.com/ns{i}}}attr{i}'
    #         assert ns_attr in element.attributes
    #         assert element.attributes[ns_attr].value == f'ns_value{i}'
    #
    #     # Test roundtrip
    #     result = self.xml_to_xml.convert_to_xml(xml_file, pretty_print=False)
    #     result_file = self.xml_loader.load_from_string(result)
    #     assert xml_file.namespaces == result_file.namespaces
    #
    # def test_mixed_content_large_xml(self):
    #     # Test handling of mixed content with various text nodes and elements
    #     def create_mixed_content(depth, width):
    #         if depth == 0:
    #             return f'Text{width}'
    #
    #         parts = []
    #         for i in range(width):
    #             parts.extend([
    #                 f'Text before {depth}-{i} ',
    #                 f'<elem{depth}-{i}>',
    #                 create_mixed_content(depth - 1, width),
    #                 f'</elem{depth}-{i}>',
    #                 f' Text after {depth}-{i}'
    #             ])
    #         return ''.join(parts)
    #
    #     xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    #         <root>
    #             {create_mixed_content(4, 4)}
    #         </root>'''
    #
    #     xml_file = self.xml_loader.load_from_string(xml)
    #
    #     # Verify mixed content structure
    #     def count_text_nodes(element):
    #         text_count = sum(1 for child in element.children if isinstance(child, str))
    #         element_count = 0
    #         for child in element.children:
    #             if isinstance(child, XML__Element):
    #                 text_count += count_text_nodes(child)
    #                 element_count += 1
    #         return text_count
    #
    #     total_text_nodes = count_text_nodes(xml_file.root_element)
    #     assert total_text_nodes > 100  # Should have many text nodes
    #
    #     # Test roundtrip
    #     result = self.xml_to_xml.convert_to_xml(xml_file, pretty_print=False)
    #     result_file = self.xml_loader.load_from_string(result)
    #     assert count_text_nodes(result_file.root_element) == total_text_nodes