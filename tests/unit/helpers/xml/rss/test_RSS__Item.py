from unittest                                       import TestCase
from osbot_utils.helpers.xml.rss.RSS__Feed__Parser  import RSS__Feed__Parser
from osbot_utils.helpers.xml.rss.RSS__Item          import RSS__Item
from osbot_utils.helpers.xml.rss.RSS__Enclosure     import RSS__Enclosure


class test_RSS__Item(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feed_parser = RSS__Feed__Parser()

    def setUp(self):
        self.item = RSS__Item(title       = "Test Item",
                              link        = "https://test.com/item",
                              description = "Test Description",
                              guid        = self.feed_parser.extract_guid({'#text': 'https://test.com/item', 'isPermaLink': 'false'}),
                              pubDate     = "Thu, 26 Dec 2024 15:03:13 GMT",
                              creator     = "Test Author")

    def test_base_attributes(self):
        assert self.item.title       == "Test Item"
        assert self.item.link        == "https://test.com/item"
        assert self.item.description == "Test Description"
        assert self.item.guid        == self.feed_parser.extract_guid({'#text': 'https://test.com/item', 'isPermaLink': 'false'})
        assert self.item.pubDate     == "Thu, 26 Dec 2024 15:03:13 GMT"
        assert self.item.creator     == "Test Author"
        assert self.item.categories  == []
        assert self.item.content     == {}
        assert self.item.thumbnail   == {}
        assert self.item.extensions  == {}

    def test_with_enclosure(self):
        enclosure = RSS__Enclosure( url="https://test.com/image.jpg", type="image/jpeg", length=12345 )
        self.item.enclosure = enclosure
        assert self.item.enclosure == enclosure
        assert self.item.enclosure.type == "image/jpeg"
        assert self.item.enclosure.length == 12345

    def test_with_categories(self):
        categories = ["Technology", "News"]
        item = RSS__Item(title       = "Test Item"                      ,
                         link        = "https://test.com/item"          ,
                         description = "Test Description"               ,
                         guid        = self.feed_parser.extract_guid({'#text': 'https://test.com/item'}),
                         pubDate     = "Thu, 26 Dec 2024 15:03:13 GMT"  ,
                         creator     = "Test Author"                    ,
                         categories  = categories                       )
        assert item.categories == categories

    def test_with_media_content(self):
        content = {
            'url': 'https://test.com/image.jpg',
            'medium': 'image',
            'title': {'#text': 'Test Image', 'type': 'html'}
        }
        self.item.content = content
        assert self.item.content == content
        assert self.item.content['medium'] == 'image'

    def test_with_thumbnail(self):
        thumbnail = {'url': 'https://test.com/thumb.jpg'}
        self.item.thumbnail = thumbnail
        assert self.item.thumbnail == thumbnail