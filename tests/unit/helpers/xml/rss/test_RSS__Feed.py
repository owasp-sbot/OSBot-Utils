from unittest                                        import TestCase
from osbot_utils.helpers.xml.rss.RSS__Feed           import RSS__Feed, DEFAULT__RSS_FEED__VERSION
from osbot_utils.helpers.xml.rss.RSS__Channel        import RSS__Channel
from tests.unit.helpers.xml.rss.Test_Data__RSS__Feed import TEST_DATA__RSS_FEED__MULTIPLE_ITEMS


class test_RSS__Feed(TestCase):

    def test_default_values(self):
        feed = RSS__Feed()
        assert feed.version    == "2.0"
        assert feed.channel    is None
        assert feed.namespaces == {}
        assert feed.extensions == {}

    def test_init_with_values(self):
        channel    = RSS__Channel(title="Test Title", link="http://test", description="description", language="en")
        namespaces = {'media': 'http://search.yahoo.com/mrss/'}
        extensions = {'custom_element': 'value'}

        feed = RSS__Feed(version   = DEFAULT__RSS_FEED__VERSION ,
                        channel    = channel                    ,
                        namespaces = namespaces                 ,
                        extensions = extensions                 )

        assert feed.version    == DEFAULT__RSS_FEED__VERSION
        assert feed.channel    == channel
        assert feed.namespaces == namespaces
        assert feed.extensions == extensions

        assert RSS__Feed(version    = None).version    == DEFAULT__RSS_FEED__VERSION
        assert RSS__Feed(namespaces = None).namespaces == {}

    def test_init_with_minimal_required_values(self):
        channel = RSS__Channel(title="Test Title", link="http://test", description="description", language="en")
        feed    = RSS__Feed(channel=channel)

        assert feed.version    == "2.0"
        assert feed.channel    == channel
        assert feed.namespaces == {}
        assert feed.extensions == {}

    def test__from_json___multiple_items(self):
        json_data = TEST_DATA__RSS_FEED__MULTIPLE_ITEMS
        rss_feed = RSS__Feed.from_json(json_data)
        assert rss_feed.json() == json_data
