from unittest                                        import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.helpers.Guid                        import Guid
from osbot_utils.helpers.xml.Xml__File__Load         import Xml__File__Load
from osbot_utils.helpers.xml.Xml__File__To_Dict      import Xml__File__To_Dict
from osbot_utils.helpers.xml.rss.RSS__Feed__Parser   import RSS__Feed__Parser
from tests.unit.helpers.xml.rss.Test_Data__RSS__Feed import TEST_DATA__BASIC_FEED, TEST_DATA__FEED_WITH_ITEMS, \
    TEST_DATA__TECH_NEWS__FEED_XML, TEST_DATA__CYBER_NEWS__FEED_XML, TEST_DATA__SECURITY_ALERTS__FEED_XML, \
    TEST_DATA__FEED_WITH_MEDIA, TEST_DATA__TECH_NEWS__FEED_XML_JSON, TEST_DATA__CYBER_NEWS__FEED_XML__JSON, \
    TEST_DATA__SECURITY_ALERTS__FEED_XML__JSON


class test_RSS__Feed__Parser(TestCase):
    def setUp(self):
        self.parser = RSS__Feed__Parser()
        self.loader = Xml__File__Load()
        self.converter = Xml__File__To_Dict()

    def test_empty_feed(self):
        with self.assertRaises(ValueError) as context:
            self.parser.from_dict({})
        assert str(context.exception) == "Invalid RSS feed: no channel element found"

    def test_basic_feed_parsing(self):
        xml_file = self.loader.load_from_string(TEST_DATA__BASIC_FEED)
        data = self.converter.to_dict(xml_file)
        feed = self.parser.from_dict(data)

        assert feed.version == "2.0"
        assert feed.channel.title == "Test Feed"
        assert feed.channel.link == "https://test.com"
        assert feed.channel.description == "Test Description"
        assert feed.channel.language == "en"
        assert feed.channel.last_build_date == "Thu, 26 Dec 2024 15:03:13 GMT"
        assert len(feed.channel.items) == 0

    def test_feed_with_items(self):
        xml_file = self.loader.load_from_string(TEST_DATA__FEED_WITH_ITEMS)
        data = self.converter.to_dict(xml_file)
        feed = self.parser.from_dict(data)

        assert len(feed.channel.items) == 2

        item = feed.channel.items[0]
        assert item.title       == "Test Item 1"
        assert item.link        == "https://test.com/item1"
        assert item.description == "Description 1"
        assert item.guid        == Guid('https://test.com/item1')
        assert item.pubDate     == "Thu, 26 Dec 2024 15:03:13 GMT"
        assert item.creator     == "Author 1"

    def test_feed_with_media(self):
        xml_file = self.loader.load_from_string(TEST_DATA__FEED_WITH_MEDIA)
        data = self.converter.to_dict(xml_file)
        feed = self.parser.from_dict(data)

        item = feed.channel.items[0]
        assert item.thumbnail == {'url': 'https://test.com/thumb.jpg'}
        assert item.content == {
            'url': 'https://test.com/image.jpg',
            'medium': 'image',
            'title': {
                '#text': 'Test Image',
                'type': 'html'
            }
        }

    def test_with_provided_test_data(self):
        # Test each of the provided test data examples
        test_feeds = { TEST_DATA__TECH_NEWS__FEED_XML      : TEST_DATA__TECH_NEWS__FEED_XML_JSON        ,
                       TEST_DATA__CYBER_NEWS__FEED_XML     : TEST_DATA__CYBER_NEWS__FEED_XML__JSON      ,
                       TEST_DATA__SECURITY_ALERTS__FEED_XML: TEST_DATA__SECURITY_ALERTS__FEED_XML__JSON }

        for source_xml, expected_json in test_feeds.items():
            xml_file = self.loader.load_from_string(source_xml)
            data     = self.converter.to_dict(xml_file)
            feed     = self.parser.from_dict(data)

            assert feed.json() == expected_json
            assert feed.version             == "2.0"
            assert feed.channel             is not None
            assert feed.channel.title       != ""
            assert feed.channel.link        != ""
            assert feed.channel.description != ""
            assert feed.channel.language    is not None

