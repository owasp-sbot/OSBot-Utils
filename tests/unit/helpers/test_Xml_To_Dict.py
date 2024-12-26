from unittest                        import TestCase
from xml.etree.ElementTree           import Element
from osbot_utils.helpers.Xml_To_Dict import Xml_To_Dict


class test_Xml_To_Dict(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_xml_data    = TEST_DATA__XML_1
        cls.xml_to_dict = Xml_To_Dict(xml_data=cls.test_xml_data).setup().parse()

    def test_setup(self):
        with self.xml_to_dict as _:
            assert _.xml_data    == self.test_xml_data
            assert type(_.root)  == Element
            assert _.root.attrib == {'version': '2.0'}
            assert _.namespaces  == {'sy': 'http://purl.org/rss/1.0/modules/syndication/'}


    def test_parse(self):
        with self.xml_to_dict as _:
            expected_dict = {'channel': {'description'    : 'Test Description Feed'                                             ,
                                         'item'           : { 'author'      : 'info@test-feed.com (Test Author)'                ,
                                                              'description' : 'Test Description'                                ,
                                                              'enclosure'   : { 'length': '12216320'                            ,
                                                                                'type'  : 'image/jpeg'                          ,
                                                                                'url'   : 'https://example.com/image.jpg'       },
                                                              'guid'        : 'https://test-feed.com/2024/12/test-article.html' ,
                                                              'link'        : 'https://test-feed.com/2024/12/test-article.html' ,
                                                              'pubDate'     : 'Wed, 04 Dec 2024 22:53:00 +0530'                 ,
                                                              'title'       : 'Test Article'                                    },
                                         'language'       : 'en-us'                                                         ,
                                         'lastBuildDate'  : 'Thu, 05 Dec 2024 01:33:01 +0530'                               ,
                                         'link'           : 'https://test-feed.com'                                         ,
                                         'title'          : 'Test Feed'                                                     ,
                                         'updateFrequency': '1'                                                             ,
                                         'updatePeriod'   : 'hourly'                                                        },
                             'version': '2.0'                                                                               }
            assert _.xml_dict == expected_dict        # BUG data is missing

    def test_load_namespaces(self):
        xml_string = """<?xml version="1.0" encoding="UTF-8"?>
                        <rss version="2.0"
                            xmlns:content="http://purl.org/rss/1.0/modules/content/"
                            xmlns:wfw="http://wellformedweb.org/CommentAPI/"
                            xmlns:dc="http://purl.org/dc/elements/1.1/"
                            xmlns:atom="http://www.w3.org/2005/Atom"
                            xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
                            xmlns:slash="http://purl.org/rss/1.0/modules/slash/">
                            <channel>
                                <title>Sample Security News</title>
                            </channel>
                        </rss>"""

        # Parse the XML
        with Xml_To_Dict(xml_data=xml_string).setup().parse() as _:
            assert _.root.attrib == {'version': '2.0'}
            assert _.namespaces == { 'atom'   : 'http://www.w3.org/2005/Atom'                 ,
                                     'content': 'http://purl.org/rss/1.0/modules/content/'    ,
                                     'dc'     : 'http://purl.org/dc/elements/1.1/'            ,
                                     'slash'  : 'http://purl.org/rss/1.0/modules/slash/'      ,
                                     'sy'     : 'http://purl.org/rss/1.0/modules/syndication/',
                                     'wfw'    : 'http://wellformedweb.org/CommentAPI/'        }

    def test_basic_parsing(self):
        with Xml_To_Dict(xml_data=TEST_DATA__XML_BASIC).setup().parse() as _:
            assert _.xml_dict == {'child': 'Simple Text'}

    def test_attributes(self):
        with Xml_To_Dict(xml_data=TEST_DATA__XML_ATTRIBUTES).setup().parse() as _:
            expected = {
                'attr1': 'value1',
                'attr2': 'value2',
                'child': {'prop': 'test', '_text': 'Child Text'}
            }
            assert _.xml_dict == expected

    def test_multiple_items(self):
        with Xml_To_Dict(xml_data=TEST_DATA__XML_MULTI_ITEMS).setup().parse() as _:
            expected = {
                'item': ['First', 'Second', 'Third']
            }
            assert _.xml_dict == expected

    def test_namespaces(self):
        with Xml_To_Dict(xml_data=TEST_DATA__XML_NAMESPACES).setup().parse() as _:
            assert _.namespaces == {
                'ns1': 'http://example.com/ns1',
                'ns2': 'http://example.com/ns2'
            }
            assert _.xml_dict == {
                'element': ['NS1 Content', 'NS2 Content']
            }

    def test_mixed_content(self):
        with Xml_To_Dict(xml_data=TEST_DATA__XML_MIXED_CONTENT).setup().parse() as _:
            expected = {
                '_text': 'Text Content', #'Text Content More Text',
                'child': 'Child Text'
            }
            assert _.xml_dict == expected

    def test_cdata(self):
        with Xml_To_Dict(xml_data=TEST_DATA__XML_CDATA).setup().parse() as _:
            expected = {
                'description': 'Special <characters> & content'
            }
            assert _.xml_dict == expected

    def test_empty_elements(self):
        with Xml_To_Dict(xml_data=TEST_DATA__XML_EMPTY).setup().parse() as _:
            expected = {
                'empty': '',
                'self-closing': ''
            }
            assert _.xml_dict == expected

    def test_invalid_xml(self):
        with self.assertRaises(ValueError) as context:
            Xml_To_Dict(xml_data=TEST_DATA__XML_INVALID).setup()
        assert "Invalid XML:" in str(context.exception)

    def test_edge_cases(self):
        # Test None XML data
        with self.assertRaises(ValueError):        # Type_Safe will raise this
            Xml_To_Dict().setup()

        # Test empty XML string
        with self.assertRaises(ValueError):
            Xml_To_Dict(xml_data='').setup()

        # Test XML with only whitespace
        with self.assertRaises(ValueError):
            Xml_To_Dict(xml_data='   \n   ').setup()

    def test_type_checks(self):
        xml_to_dict = Xml_To_Dict(xml_data=TEST_DATA__XML_BASIC).setup().parse()
        assert isinstance(xml_to_dict.xml_data, str)
        assert isinstance(xml_to_dict.root, Element)
        assert isinstance(xml_to_dict.namespaces, dict)
        assert isinstance(xml_to_dict.xml_dict, dict)

TEST_DATA__XML_1 = '''<?xml version="1.0" encoding="UTF-8"?>
                      <rss version="2.0" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/">
                          <channel>
                              <title>Test Feed</title>
                              <link>https://test-feed.com</link>
                              <description>Test Description Feed</description>
                              <language>en-us</language>
                              <lastBuildDate>Thu, 05 Dec 2024 01:33:01 +0530</lastBuildDate>
                              <sy:updatePeriod>hourly</sy:updatePeriod>
                              <sy:updateFrequency>1</sy:updateFrequency>
                              <item>
                                  <title>Test Article</title>
                                  <description><![CDATA[Test Description]]></description>
                                  <link>https://test-feed.com/2024/12/test-article.html</link>
                                  <guid>https://test-feed.com/2024/12/test-article.html</guid>
                                  <pubDate>Wed, 04 Dec 2024 22:53:00 +0530</pubDate>
                                  <author>info@test-feed.com (Test Author)</author>
                                  <enclosure url="https://example.com/image.jpg" type="image/jpeg" length="12216320"/>
                              </item>
                          </channel>
                      </rss>'''

TEST_DATA__XML_BASIC = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <child>Simple Text</child>
</root>'''

TEST_DATA__XML_ATTRIBUTES = '''<?xml version="1.0" encoding="UTF-8"?>
<root attr1="value1" attr2="value2">
    <child prop="test">Child Text</child>
</root>'''

TEST_DATA__XML_MULTI_ITEMS = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item>First</item>
    <item>Second</item>
    <item>Third</item>
</root>'''

TEST_DATA__XML_NAMESPACES = '''<?xml version="1.0" encoding="UTF-8"?>
<root xmlns:ns1="http://example.com/ns1"
      xmlns:ns2="http://example.com/ns2">
    <ns1:element>NS1 Content</ns1:element>
    <ns2:element>NS2 Content</ns2:element>
</root>'''

TEST_DATA__XML_MIXED_CONTENT = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
    Text Content
    <child>Child Text</child>
    More Text
</root>'''

TEST_DATA__XML_CDATA = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <description><![CDATA[Special <characters> & content]]></description>
</root>'''

TEST_DATA__XML_EMPTY = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <empty></empty>
    <self-closing/>
</root>'''

TEST_DATA__XML_INVALID = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
    <unclosed>
</root>'''